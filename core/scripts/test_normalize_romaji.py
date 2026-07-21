#!/usr/bin/env python3
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("normalize_romaji.py")


class NormalizeRomajiTests(unittest.TestCase):
    def run_normalizer(self, convention, text):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "novel.config.md").write_text(
                "## Conventions\n"
                f"- **Romanization:** {convention}\n",
                encoding="utf-8",
            )
            target = root / "chapter.md"
            target.write_text(text, encoding="utf-8")
            subprocess.run(
                ["python3", str(SCRIPT), str(target)],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
            return target.read_text(encoding="utf-8")

    def test_unmarked_long_vowel_lock_strips_macron_without_doubling(self):
        result = self.run_normalizer(
            "no macrons; leave Japanese long vowels unmarked",
            "Ōhinata met Tōhoku's Tarō.\n",
        )
        self.assertEqual(result, "Ohinata met Tohoku's Taro.\n")

    def test_vowel_doubling_lock_preserves_legacy_behavior(self):
        result = self.run_normalizer(
            "no macrons; use vowel-doubling",
            "Ōhinata met Tōhoku's Tarō.\n",
        )
        self.assertEqual(result, "Ouhinata met Touhoku's Tarou.\n")


if __name__ == "__main__":
    unittest.main()
