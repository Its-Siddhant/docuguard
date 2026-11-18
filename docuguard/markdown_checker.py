
import re
from pathlib import Path
from urllib.parse import unquote


REQUIRED_SECTIONS = [
    "installation",
    "usage",
    "features",
    "license",
]

MAX_SENTENCE_WORDS = 30


def check_required_sections(content):
    """Check whether essential README sections exist."""
    findings = []

    headings = re.findall(
        r"^#{1,6}\s+(.+)$",
        content,
        re.MULTILINE
    )

    normalized_headings = {
        re.sub(r"[^\w\s]", "", heading).strip().lower()
        for heading in headings
    }

    for section in REQUIRED_SECTIONS:
        if section not in normalized_headings:
            findings.append({
                "severity": "warning",
                "category": "Structure",
                "line": None,
                "message": f"Missing recommended section: {section.title()}",
                "suggestion": f"Consider adding a '{section.title()}' section."
            })

    return findings


def check_heading_hierarchy(content):
    """Detect heading level jumps."""
    findings = []
    previous_level = 0

    for line_number, line in enumerate(content.splitlines(), start=1):
        match = re.match(r"^(#{1,6})\s+", line)

        if not match:
            continue

        current_level = len(match.group(1))

        if previous_level and current_level > previous_level + 1:
            findings.append({
                "severity": "warning",
                "category": "Structure",
                "line": line_number,
                "message": (
                    f"Heading level jumps from H{previous_level} "
                    f"to H{current_level}."
                ),
                "suggestion": "Use heading levels sequentially."
            })

        previous_level = current_level

    return findings


def check_long_sentences(content, max_words=MAX_SENTENCE_WORDS):
    """Flag sentences exceeding the configured word limit."""
    findings = []

    for line_number, line in enumerate(content.splitlines(), start=1):
        if line.lstrip().startswith("#"):
            continue

        if line.lstrip().startswith(("```", "|", ">", "- ", "* ", "+ ")):
            continue

        sentences = re.split(r"(?<=[.!?])\s+", line.strip())

        for sentence in sentences:
            words = re.findall(r"\b[\w'-]+\b", sentence)

            if len(words) > max_words:
                findings.append({
                    "severity": "info",
                    "category": "Readability",
                    "line": line_number,
                    "message": (
                        f"Long sentence detected ({len(words)} words)."
                    ),
                    "suggestion": (
                        "Consider splitting this sentence into shorter "
                        "sentences for better readability."
                    )
                })

    return findings


def check_broken_links(content, source_path=None):
    """Detect broken local Markdown links."""
    findings = []

    if source_path is None:
        return findings

    source = Path(source_path).resolve()
    base_directory = source.parent

    link_pattern = r"(?<!!)\[[^\]]*\]\(([^)]+)\)"

    for line_number, line in enumerate(content.splitlines(), start=1):
        for match in re.finditer(link_pattern, line):
            target = match.group(1).strip()

            # Ignore external links and email links.
            if re.match(r"^(https?://|mailto:|//)", target, re.I):
                continue

            # Ignore empty links and anchor-only links.
            if not target or target.startswith("#"):
                continue

            target = unquote(target.split("#")[0].split("?")[0])

            if not target:
                continue

            linked_path = (base_directory / target).resolve()

            if not linked_path.exists():
                findings.append({
                    "severity": "error",
                    "category": "Links",
                    "line": line_number,
                    "message": f"Broken relative link: {target}",
                    "suggestion": (
                        "Verify the target path or correct the Markdown link."
                    )
                })

    return findings


def audit_markdown(content, source_path=None):
    """Run all deterministic Markdown quality checks."""
    findings = []

    findings.extend(check_required_sections(content))
    findings.extend(check_heading_hierarchy(content))
    findings.extend(check_long_sentences(content))
    findings.extend(check_broken_links(content, source_path))

    return findings
