#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("split_ebook.py")
SPEC = importlib.util.spec_from_file_location("split_ebook", SCRIPT_PATH)
split_ebook = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(split_ebook)


class GaijiExtractionTests(unittest.TestCase):
    def test_preserves_alt_text_in_ruby_base(self):
        xhtml = (
            '<body><p><ruby><img class="gaiji" src="gaiji.png" alt="葛"/>'
            '<rt>かつ</rt>飾<rt>しか</rt></ruby>区</p></body>'
        )

        self.assertEqual(split_ebook.xhtml_to_markdown(xhtml), "葛飾[かつしか]区")

    def test_preserves_voiced_katakana_alt_text_in_ruby_reading(self):
        xhtml = (
            '<body><p><ruby><rb>撃て</rb><rt><img class="gaiji" '
            'src="gaiji.png" alt="ア濁点"/>ー</rt></ruby></p></body>'
        )

        self.assertEqual(split_ebook.xhtml_to_markdown(xhtml), "撃て[ア゙ー]")

    def test_replaces_inline_gaiji_alt_without_splitting_paragraph(self):
        xhtml = (
            '<body><p>「なにが<img class="gaiji" src="gaiji.png" '
            'alt="!!?"/>」</p></body>'
        )

        self.assertEqual(split_ebook.xhtml_to_markdown(xhtml), "「なにが!!?」")

    def test_keeps_unknown_gaiji_as_inline_marker(self):
        xhtml = (
            '<body><p>白<img class="gaiji" src="gaiji.png" alt=""/>です</p></body>'
        )

        self.assertEqual(
            split_ebook.xhtml_to_markdown(xhtml),
            "白![gaiji.png](images/gaiji.png)です",
        )

    def test_keeps_illustrations_as_block_markers(self):
        xhtml = '<body><p>前</p><p><img src="illustration.jpg" alt=""/></p><p>後</p></body>'

        self.assertEqual(
            split_ebook.xhtml_to_markdown(xhtml),
            "前\n\n![illustration.jpg](images/illustration.jpg)\n\n後",
        )


if __name__ == "__main__":
    unittest.main()
