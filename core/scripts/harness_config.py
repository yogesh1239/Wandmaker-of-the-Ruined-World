#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared config helpers for the translation harness scripts.

The harness historically used "Vol" as the release unit. Webnovels often do
not have volumes, so this module exposes a neutral unit resolver while keeping
legacy Vol tables working unchanged.
"""

import glob
import io
import os
import re
from dataclasses import dataclass


BULLET_RE = re.compile(r"^\s*-\s*\*\*(.+?):\*\*\s*(.*)$")


class ConfigError(Exception):
    """Raised when novel.config.md cannot identify one unambiguous artifact."""


@dataclass(frozen=True)
class ChapterResolution:
    unit: str
    chapter: str
    title: str
    source_dir: str
    english_dir: str
    editing_dir: str
    final_path: str


def split_sections(text):
    parts = re.split(r"(?m)^##\s+(.*)$", text)
    sections = {}
    for i in range(1, len(parts), 2):
        heading = parts[i].strip().lower()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections[heading] = body
    return sections


def get_section(sections, *keywords):
    for heading, body in sections.items():
        if all(k in heading for k in keywords):
            return body
    return ""


def clean(value):
    return value.strip().strip("`").strip()


def parse_bullets(body):
    out = {}
    for line in body.splitlines():
        m = BULLET_RE.match(line.strip())
        if m:
            out[m.group(1).strip().lower()] = clean(m.group(2))
    return out


def parse_table(body):
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return []
    header = [h.strip().lower() for h in rows[0]]
    return [
        {header[i]: (row[i] if i < len(row) else "") for i in range(len(header))}
        for row in rows[1:]
    ]


def _abspath(base_dir, relpath):
    relpath = clean(relpath)
    if os.path.isabs(relpath):
        return os.path.normpath(relpath)
    return os.path.normpath(os.path.join(base_dir, relpath))


def _row_unit(row):
    unit = clean(row.get("unit", ""))
    if unit:
        return unit
    vol = clean(row.get("vol", ""))
    if vol:
        return vol
    return ""


def _legacy_paths(base_dir, unit):
    return {
        "source": os.path.join(base_dir, "Source", "Volume %s" % unit),
        "english": os.path.join(base_dir, "English", "Volume %s" % unit),
        "editing": os.path.join(base_dir, "Editing", "Volume %s" % unit),
    }


def _path_rows_by_unit(base_dir, path_rows):
    paths = {}
    for row in path_rows:
        unit = _row_unit(row)
        if not unit:
            continue
        paths[unit] = {
            "source": _abspath(base_dir, row.get("source path", "Source/%s" % unit)),
            "english": _abspath(base_dir, row.get("english path", "English/%s" % unit)),
            "editing": _abspath(base_dir, row.get("editing path", "Editing/%s" % unit)),
        }
    return paths


class ProjectConfig:
    def __init__(self, config_path, text):
        self.config_path = os.path.abspath(config_path)
        self.base_dir = os.path.dirname(self.config_path)
        self.sections = split_sections(text)
        self.identity = parse_bullets(get_section(self.sections, "identity"))
        self.source_table = parse_table(get_section(self.sections, "source ebooks"))
        self.chapter_table = parse_table(get_section(self.sections, "chapter-title map"))
        self.epub_metadata = parse_bullets(get_section(self.sections, "epub metadata"))
        self.unit_paths = _path_rows_by_unit(
            self.base_dir,
            parse_table(get_section(self.sections, "unit paths")),
        )

    def paths_for_unit(self, unit):
        unit = clean(str(unit))
        if unit in self.unit_paths:
            return self.unit_paths[unit]
        return _legacy_paths(self.base_dir, unit)

    def chapter_rows(self, chapter):
        chapter = clean(str(chapter))
        return [
            row for row in self.chapter_table
            if clean(row.get("n", "")) == chapter and _row_unit(row)
        ]

    def resolve_chapter(self, unit, chapter):
        chapter = clean(str(chapter))
        wanted_unit = clean(str(unit)) if unit is not None else ""
        rows = self.chapter_rows(chapter)
        if wanted_unit:
            rows = [row for row in rows if _row_unit(row) == wanted_unit]

        if not rows:
            scope = "unit %r " % wanted_unit if wanted_unit else ""
            raise ConfigError("chapter %s%snot found in chapter-title map" % (scope, chapter))

        units = sorted({_row_unit(row) for row in rows})
        if not wanted_unit and len(units) > 1:
            raise ConfigError(
                "chapter %s appears in multiple units (%s); pass --unit"
                % (chapter, ", ".join(units))
            )
        if len(rows) > 1:
            raise ConfigError("chapter %s has multiple title rows for unit %s" % (chapter, units[0]))

        row = rows[0]
        resolved_unit = _row_unit(row)
        title = clean(row.get("en title", ""))
        if not title:
            raise ConfigError("chapter %s in unit %s has no EN title" % (chapter, resolved_unit))

        paths = self.paths_for_unit(resolved_unit)
        final_path = resolve_chapter_file(paths["english"], chapter, title)
        return ChapterResolution(
            unit=resolved_unit,
            chapter=chapter,
            title=title,
            source_dir=paths["source"],
            english_dir=paths["english"],
            editing_dir=paths["editing"],
            final_path=final_path,
        )


def resolve_chapter_file(english_dir, chapter, title):
    exact = os.path.join(english_dir, "Chapter %s - %s.md" % (chapter, title))
    if os.path.isfile(exact):
        return exact
    matches = sorted(glob.glob(os.path.join(english_dir, "Chapter %s - *.md" % chapter)))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(os.path.basename(m) for m in matches)
        raise ConfigError(
            "chapter %s (%r) matches multiple files on disk: %s; rename so exactly one remains"
            % (chapter, title, names)
        )
    raise ConfigError("chapter file not found: expected %s" % exact)


def load_project_config(config_path):
    with io.open(config_path, "r", encoding="utf-8") as f:
        return ProjectConfig(config_path, f.read())
