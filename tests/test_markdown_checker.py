
import unittest
import tempfile
from pathlib import Path

from docuguard.markdown_checker import (
    check_required_sections,
    check_heading_hierarchy,
    check_long_sentences,
    check_broken_links,
    audit_markdown
)


class TestMarkdownChecker(unittest.TestCase):

    def test_missing_required_sections(self):
        content = "# Project\n\nSome description."
        findings = check_required_sections(content)

        self.assertEqual(len(findings), 4)
        self.assertTrue(
            all(item["category"] == "Structure" for item in findings)
        )

    def test_heading_hierarchy_jump(self):
        content = "# Main\n\n### Subsection"
        findings = check_heading_hierarchy(content)

        self.assertEqual(len(findings), 1)
        self.assertIn("H1", findings[0]["message"])
        self.assertIn("H3", findings[0]["message"])

    def test_long_sentence(self):
        content = " ".join(["documentation"] * 35) + "."
        findings = check_long_sentences(content)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["category"], "Readability")

    def test_short_sentence(self):
        content = "This is a short sentence."
        findings = check_long_sentences(content)

        self.assertEqual(len(findings), 0)

    def test_broken_relative_link(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "README.md"
            source.write_text("# Test", encoding="utf-8")

            content = "[Missing file](missing.md)"
            findings = check_broken_links(content, source)

            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0]["severity"], "error")

    def test_valid_relative_link(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "README.md"
            target = Path(directory) / "guide.md"

            source.write_text("# Test", encoding="utf-8")
            target.write_text("# Guide", encoding="utf-8")

            content = "[Guide](guide.md)"
            findings = check_broken_links(content, source)

            self.assertEqual(len(findings), 0)

    def test_external_link_is_ignored(self):
        content = "[GitHub](https://github.com)"
        findings = check_broken_links(content, Path("README.md"))

        self.assertEqual(len(findings), 0)

    def test_audit_returns_findings(self):
        content = "# Project\n\n### Installation"
        findings = audit_markdown(content)

        self.assertIsInstance(findings, list)
        self.assertGreater(len(findings), 0)


if __name__ == "__main__":
    unittest.main()
