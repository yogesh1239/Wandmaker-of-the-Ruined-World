# core/scripts/test_derive_build_config.py
import json
import os
import subprocess
import sys
import tempfile
import textwrap

SCRIPT = os.path.join(os.path.dirname(__file__), "derive_build_config.py")

CONFIG = textwrap.dedent("""\
    # Novel Config — Test Novel

    ## Identity
    - **Title (JP):** テスト
    - **Title (EN):** Test Novel
    - **Type:** Japanese light novel
    - **Genre / setting:** test
    - **Author:** Test Author

    ## Source ebooks → volumes

    | Vol | Source file | Format | Extraction |
    |-|-|-|-|
    | 1 | `source.epub` | epub | split_ebook.py direct |

    ## Paths
    - Source (split chapters + images): `Source/Volume N/`
    - Output (drafts, assembled, EPUBs): `English/Volume N/`
    - Edit logs / reconciliation / image specs: `Editing/Volume N/`

    ## Conventions
    - **Romanization:** no macrons.

    ## Register lock
    **Status:** Locked — Standard — test fixture.

    ## Chapter-title map

    | Vol | N | JP title | EN title |
    |-|-|-|-|
    | 1 | 1 | 一 | First |
    | 1 | 2 | 二 | Second |

    ## EPUB metadata (per volume)
    - **Series:** Test Series
    - **Title pattern:** `Test Novel, Vol. N`
    - **Language:** en
    - **Original:** テスト — (Test Author, set by /setup-novel)
    - **Cover / colophon:** keep Japanese.
""")


def make_project(with_chapters=True):
    d = tempfile.mkdtemp()
    with open(os.path.join(d, "novel.config.md"), "w", encoding="utf-8") as f:
        f.write(CONFIG)
    if with_chapters:
        vol_dir = os.path.join(d, "English", "Volume 1")
        os.makedirs(vol_dir, exist_ok=True)
        # Only chapter 1 exists on disk; chapter 2 ("Second") is missing.
        with open(os.path.join(vol_dir, "Chapter 1 - First.md"), "w", encoding="utf-8") as f:
            f.write("Some translated prose.\n")
    return d


def run(project_dir, extra_args=()):
    out_path = os.path.join(project_dir, "Editing", "Volume 1", "build_config.json")
    p = subprocess.run(
        [sys.executable, SCRIPT, "novel.config.md", "--volume", "1", *extra_args],
        cwd=project_dir, capture_output=True, text=True,
    )
    return p, out_path


def test_derives_config_with_one_missing_chapter():
    d = make_project(with_chapters=True)
    p, out_path = run(d)
    assert p.returncode == 0, p.stderr
    assert "Second" in p.stderr or "2" in p.stderr, p.stderr  # missing chapter warning

    assert os.path.isfile(out_path), p.stdout + p.stderr
    with open(out_path, encoding="utf-8") as f:
        cfg = json.load(f)

    assert len(cfg["chapters"]) == 1
    assert cfg["chapters_dir"].endswith(os.path.join("English", "Volume 1"))
    assert cfg["chapters"][0]["title"] == "First"
    assert cfg["source_epub"].endswith("source.epub")
    assert cfg["metadata"]["language"] == "en"
    assert cfg["metadata"]["title"] == "Test Novel, Vol. 1"
    assert cfg["metadata"]["creators"] == [{"name": "Test Author", "role": "aut"}]


def test_custom_out_path():
    d = make_project(with_chapters=True)
    custom_out = os.path.join(d, "somewhere", "cfg.json")
    p, _ = run(d, extra_args=["--out", custom_out])
    assert p.returncode == 0, p.stderr
    assert os.path.isfile(custom_out)


def test_zero_chapters_found_exits_2():
    d = make_project(with_chapters=False)
    p, out_path = run(d)
    assert p.returncode == 2, p.stdout + p.stderr
    assert not os.path.isfile(out_path)


# Chapter 3's title carries a Windows-illegal ':' — the pipeline files such a
# chapter under a sanitized name, so the exact title-derived filename never
# exists on disk. derive must fall back to a "Chapter <N> - *.md" glob.
CONFIG_COLON = CONFIG.replace(
    "| 1 | 2 | 二 | Second |",
    "| 1 | 3 | 三 | Reunion: A New Dawn |",
)


def make_colon_project(disk_names):
    d = tempfile.mkdtemp()
    with open(os.path.join(d, "novel.config.md"), "w", encoding="utf-8") as f:
        f.write(CONFIG_COLON)
    vol_dir = os.path.join(d, "English", "Volume 1")
    os.makedirs(vol_dir, exist_ok=True)
    for name in disk_names:
        with open(os.path.join(vol_dir, name), "w", encoding="utf-8") as f:
            f.write("Some translated prose.\n")
    return d


def test_sanitized_filename_chapter_included_via_glob():
    # Chapter 1 filed under its exact title; chapter 3 under a sanitized name
    # (the ':' dropped). Both must land in the config.
    d = make_colon_project([
        "Chapter 1 - First.md",
        "Chapter 3 - Reunion A New Dawn.md",
    ])
    p, out_path = run(d)
    assert p.returncode == 0, p.stderr
    with open(out_path, encoding="utf-8") as f:
        cfg = json.load(f)
    by_title = {c["title"]: c["md"] for c in cfg["chapters"]}
    assert len(cfg["chapters"]) == 2, cfg
    # The true title (with ':') is kept; the md points at the sanitized file.
    assert by_title["Reunion: A New Dawn"] == "Chapter 3 - Reunion A New Dawn.md", cfg


def test_ambiguous_glob_errors():
    # Two files match "Chapter 3 - *.md" — derive can't pick one, must fail loud.
    d = make_colon_project([
        "Chapter 1 - First.md",
        "Chapter 3 - Reunion A New Dawn.md",
        "Chapter 3 - Reunion, A New Dawn.md",
    ])
    p, out_path = run(d)
    assert p.returncode == 2, p.stdout + p.stderr
    assert "multiple" in p.stderr.lower(), p.stderr
    assert not os.path.isfile(out_path)


def test_still_missing_chapter_warns_and_excludes():
    # No file for chapter 3 at all (exact name absent AND glob empty) -> excluded
    # with a warning, exactly as the plain missing case behaves.
    d = make_colon_project(["Chapter 1 - First.md"])
    p, out_path = run(d)
    assert p.returncode == 0, p.stderr
    assert "3" in p.stderr, p.stderr
    with open(out_path, encoding="utf-8") as f:
        cfg = json.load(f)
    assert len(cfg["chapters"]) == 1, cfg
    assert cfg["chapters"][0]["title"] == "First"


if __name__ == "__main__":
    for _name, _fn in list(globals().items()):
        if _name.startswith("test_"):
            _fn()
    print("ok")
