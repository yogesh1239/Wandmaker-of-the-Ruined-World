import re

import build_epub


CFG = {
    "img_href_base": "../image/",
    "css_links": ["../style/english.css"],
    "chapters_dir": ".",
}


def render(md, tmp_path):
    p = tmp_path / "ch.md"
    p.write_text(md, encoding="utf-8")
    doc, _ = build_epub.build_chapter({"id": "c1", "title": "T"}, str(p), CFG)
    return doc


def test_headerless_table_renders_as_table(tmp_path):
    doc = render("Before.\n\n| | |\n|-|-|\n| Age | 43 |\n| Weight | 430 kg |\n\nAfter.\n",
                 tmp_path)
    assert "<table><tbody>" in doc
    assert "<thead>" not in doc          # "| | |" spacer row is dropped
    assert "<td>Age</td><td>43</td>" in doc
    assert "<td>Weight</td><td>430 kg</td>" in doc
    assert "|" not in re.sub(r"<[^>]+>", "", doc)   # no raw pipes leak into text


def test_table_with_real_header(tmp_path):
    doc = render("| Date | Event |\n|-|-|\n| 3/3 | Surgery. |\n", tmp_path)
    assert "<thead><tr><th>Date</th><th>Event</th></tr></thead>" in doc
    assert "<td>3/3</td><td>Surgery.</td>" in doc


def test_paragraphs_around_table_are_not_merged(tmp_path):
    doc = render("Before.\n| a | b |\n|-|-|\n| 1 | 2 |\nAfter.\n", tmp_path)
    assert "<p>Before.</p>" in doc
    assert "<p>After.</p>" in doc


if __name__ == "__main__":
    import pathlib
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        t = pathlib.Path(d)
        test_headerless_table_renders_as_table(t)
        test_table_with_real_header(t)
        test_paragraphs_around_table_are_not_merged(t)
    print("ok")
