
import re


STANDARD_TERMS = {
    "GitHub": ["Github", "github"],
    "JavaScript": ["Javascript", "javascript"],
    "Markdown": ["markdown"],
    "README": ["Readme", "readme"],
    "Python": ["python"],
    "API": ["Api", "api"],
}


def check_terminology(content):
    """Identify non-standard technical terminology."""
    findings = []

    for standard_term, variations in STANDARD_TERMS.items():
        for variation in variations:
            pattern = re.compile(
                rf"\b{re.escape(variation)}\b",
                re.IGNORECASE
            )

            for match in pattern.finditer(content):
                # Avoid flagging an already correct spelling.
                if match.group(0) == standard_term:
                    continue

                line_number = content.count(
                    "\n", 0, match.start()
                ) + 1

                findings.append({
                    "severity": "info",
                    "category": "Terminology",
                    "line": line_number,
                    "message": (
                        f"Inconsistent terminology: "
                        f"'{match.group(0)}'."
                    ),
                    "suggestion": (
                        f"Use '{standard_term}' consistently."
                    )
                })

    return findings
