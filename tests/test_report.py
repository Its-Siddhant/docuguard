
import unittest

from docuguard.report import generate_report


class TestReport(unittest.TestCase):

    def test_report_contains_filename(self):
        report = generate_report("README.md", [])

        self.assertIn("README.md", report)

    def test_empty_findings(self):
        report = generate_report("README.md", [])

        self.assertIn("No documentation issues detected.", report)

    def test_report_counts_findings(self):
        findings = [
            {
                "severity": "error",
                "category": "Links",
                "line": 5,
                "message": "Broken link detected.",
                "suggestion": "Verify the link."
            },
            {
                "severity": "warning",
                "category": "Structure",
                "line": None,
                "message": "Missing section.",
                "suggestion": "Add the section."
            }
        ]

        report = generate_report("README.md", findings)

        self.assertIn("Total findings: 2", report)
        self.assertIn("Errors: 1", report)
        self.assertIn("Warnings: 1", report)


if __name__ == "__main__":
    unittest.main()
