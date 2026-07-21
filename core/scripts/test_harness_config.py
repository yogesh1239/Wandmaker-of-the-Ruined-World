import os
import tempfile
import textwrap

import harness_config


LEGACY_CONFIG = textwrap.dedent("""\
    # Novel Config

    ## Chapter-title map

    | Vol | N | JP title | EN title |
    |-|-|-|-|
    | 1 | 1 | 一 | First |
    | 1 | 2 | 二 | Reunion: A New Dawn |
""")


UNIT_CONFIG = textwrap.dedent("""\
    # Novel Config

    ## Unit paths

    | Unit | Source path | English path | Editing path |
    |-|-|-|-|
    | main | Source/main | English/main | Editing/main |
    | arc-2 | Source/Arc 2 | English/Arc 2 | Editing/Arc 2 |

    ## Chapter-title map

    | Unit | N | JP title | EN title |
    |-|-|-|-|
    | main | 37 | 第37話 | The Visitor |
    | arc-2 | 37 | 第37話 | The Visitor Returns |
""")


def write_project(config_text, files):
    root = tempfile.mkdtemp()
    with open(os.path.join(root, "novel.config.md"), "w", encoding="utf-8") as f:
        f.write(config_text)
    for relpath, text in files.items():
        path = os.path.join(root, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    return root


def load(root):
    return harness_config.load_project_config(os.path.join(root, "novel.config.md"))


def test_legacy_volume_row_resolves_as_unit_1():
    root = write_project(
        LEGACY_CONFIG,
        {"English/Volume 1/Chapter 1 - First.md": "clean prose\n"},
    )
    cfg = load(root)
    row = cfg.resolve_chapter(unit="1", chapter="1")
    assert row.unit == "1"
    assert row.chapter == "1"
    assert row.title == "First"
    assert row.english_dir == os.path.join(root, "English", "Volume 1")
    assert row.final_path == os.path.join(root, "English", "Volume 1", "Chapter 1 - First.md")


def test_single_unit_can_be_inferred_for_webnovel():
    config = UNIT_CONFIG.replace(
        "| arc-2 | 37 | 第37話 | The Visitor Returns |\n",
        "",
    ).replace(
        "| arc-2 | Source/Arc 2 | English/Arc 2 | Editing/Arc 2 |\n",
        "",
    )
    root = write_project(
        config,
        {"English/main/Chapter 37 - The Visitor.md": "clean prose\n"},
    )
    cfg = load(root)
    row = cfg.resolve_chapter(unit=None, chapter="37")
    assert row.unit == "main"
    assert row.final_path == os.path.join(root, "English", "main", "Chapter 37 - The Visitor.md")


def test_ambiguous_unit_requires_unit_argument():
    root = write_project(
        UNIT_CONFIG,
        {
            "English/main/Chapter 37 - The Visitor.md": "clean prose\n",
            "English/Arc 2/Chapter 37 - The Visitor Returns.md": "clean prose\n",
        },
    )
    cfg = load(root)
    try:
        cfg.resolve_chapter(unit=None, chapter="37")
    except harness_config.ConfigError as exc:
        assert "multiple units" in str(exc)
    else:
        raise AssertionError("expected ambiguous unit failure")


def test_sanitized_filename_falls_back_to_chapter_glob():
    root = write_project(
        LEGACY_CONFIG,
        {"English/Volume 1/Chapter 2 - Reunion A New Dawn.md": "clean prose\n"},
    )
    cfg = load(root)
    row = cfg.resolve_chapter(unit="1", chapter="2")
    assert row.title == "Reunion: A New Dawn"
    assert row.final_path.endswith("Chapter 2 - Reunion A New Dawn.md")


def test_ambiguous_sanitized_glob_is_fatal():
    root = write_project(
        LEGACY_CONFIG,
        {
            "English/Volume 1/Chapter 2 - Reunion A New Dawn.md": "clean prose\n",
            "English/Volume 1/Chapter 2 - Reunion, A New Dawn.md": "clean prose\n",
        },
    )
    cfg = load(root)
    try:
        cfg.resolve_chapter(unit="1", chapter="2")
    except harness_config.ConfigError as exc:
        assert "multiple files" in str(exc)
    else:
        raise AssertionError("expected ambiguous file failure")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("ok")
