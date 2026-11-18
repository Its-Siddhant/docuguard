
import json
import os
import unittest
from unittest.mock import MagicMock, patch

from docuguard.ai_analyzer import analyze_documentation


class TestAIAnalyzer(unittest.TestCase):

    def setUp(self):
        self.valid_response = {
            "summary": "Documentation needs minor improvements.",
            "suggestions": [
                {
                    "category": "Clarity",
                    "severity": "info",
                    "original_text": "Install the software.",
                    "issue": "The installation instructions lack context.",
                    "suggestion": "Explain the installation prerequisites.",
                    "technical_risk": "low",
                    "requires_human_review": True
                }
            ]
        }

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self):
        with self.assertRaisesRegex(ValueError, "GROQ_API_KEY is missing"):
            analyze_documentation("# Test documentation")

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}, clear=True)
    def test_empty_document(self):
        with self.assertRaisesRegex(ValueError, "document is empty"):
            analyze_documentation("   ")

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}, clear=True)
    @patch("docuguard.ai_analyzer.Groq")
    def test_successful_analysis(self, mock_groq):
        mock_client = MagicMock()
        mock_groq.return_value = mock_client

        mock_client.chat.completions.create.return_value.choices[0].message.content = (
            json.dumps(self.valid_response)
        )

        result = analyze_documentation("# Test documentation")

        self.assertEqual(result["summary"], self.valid_response["summary"])
        self.assertEqual(len(result["suggestions"]), 1)
        mock_client.chat.completions.create.assert_called_once()

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}, clear=True)
    @patch("docuguard.ai_analyzer.Groq")
    def test_invalid_json_response(self, mock_groq):
        mock_client = MagicMock()
        mock_groq.return_value = mock_client

        mock_client.chat.completions.create.return_value.choices[0].message.content = (
            "This is not valid JSON"
        )

        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            analyze_documentation("# Test documentation")

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}, clear=True)
    @patch("docuguard.ai_analyzer.Groq")
    def test_invalid_severity(self, mock_groq):
        mock_client = MagicMock()
        mock_groq.return_value = mock_client

        invalid_response = self.valid_response.copy()
        invalid_response["suggestions"] = [
            self.valid_response["suggestions"][0].copy()
        ]
        invalid_response["suggestions"][0]["severity"] = "critical"

        mock_client.chat.completions.create.return_value.choices[0].message.content = (
            json.dumps(invalid_response)
        )

        with self.assertRaisesRegex(ValueError, "Invalid AI suggestion severity"):
            analyze_documentation("# Test documentation")

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}, clear=True)
    @patch("docuguard.ai_analyzer.Groq")
    def test_human_review_is_mandatory(self, mock_groq):
        mock_client = MagicMock()
        mock_groq.return_value = mock_client

        invalid_response = self.valid_response.copy()
        invalid_response["suggestions"] = [
            self.valid_response["suggestions"][0].copy()
        ]
        invalid_response["suggestions"][0]["requires_human_review"] = False

        mock_client.chat.completions.create.return_value.choices[0].message.content = (
            json.dumps(invalid_response)
        )

        with self.assertRaisesRegex(ValueError, "must always require human review"):
            analyze_documentation("# Test documentation")


if __name__ == "__main__":
    unittest.main()
