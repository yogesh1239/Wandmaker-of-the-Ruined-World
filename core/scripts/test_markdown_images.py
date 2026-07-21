import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
IMAGE_RE = re.compile(r"!\[[^]]*\]\(([^)]+)\)")


def test_english_markdown_image_targets_exist():
    missing = []
    for chapter in (ROOT / "English").glob("**/*.md"):
        for target in IMAGE_RE.findall(chapter.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "data:")):
                continue
            image = chapter.parent / unquote(target)
            if not image.is_file():
                missing.append(f"{chapter.relative_to(ROOT)} -> {target}")

    assert not missing, "Missing Markdown images:\n" + "\n".join(missing)


if __name__ == "__main__":
    test_english_markdown_image_targets_exist()
    print("ok")
