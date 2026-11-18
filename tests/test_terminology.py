
import unittest

from docuguard.terminology import check_terminology


class TestTerminology(unittest.TestCase):

    def test_inconsistent_github(self):
        findings = check_terminology("We use Github for version control.")

        self.assertGreater(len(findings), 0)
        self.assertTrue(
            any("GitHub" in item["suggestion"] for item in findings)
        )

    def test_correct_terminology(self):
        findings = check_terminology(
            "We use GitHub and JavaScript with Markdown."
        )

        self.assertEqual(len(findings), 0)

    def test_multiple_inconsistencies(self):
        content = "We use Github and Javascript."
        findings = check_terminology(content)

        self.assertGreaterEqual(len(findings), 2)


if __name__ == "__main__":
    unittest.main()
