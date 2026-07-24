import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_epub


def test_inline_md_preserves_valid_ruby():
    rendered = build_epub.inline_md(
        "Cast <ruby>Vaa-ra<rt>Freeze</rt></ruby>.", "../image/"
    )
    assert rendered == "Cast <ruby>Vaa-ra<rt>Freeze</rt></ruby>."


def test_inline_md_escapes_unapproved_raw_html():
    rendered = build_epub.inline_md("<script>bad()</script>")
    assert rendered == "&lt;script&gt;bad()&lt;/script&gt;"


def test_inline_gaiji_inside_ruby_becomes_xhtml_image():
    rendered = build_epub.inline_md(
        "<ruby>Da-u![glyph](images/gaiji.png)-<rt>Smash</rt></ruby>",
        "../image/",
    )
    assert rendered == (
        '<ruby>Da-u<img class="gaiji" src="../image/gaiji.png" alt="glyph"/>'
        '-<rt>Smash</rt></ruby>'
    )


if __name__ == "__main__":
    for func in [v for k, v in list(globals().items()) if k.startswith("test_")]:
        func()
    print("ok")
