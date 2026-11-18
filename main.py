
import argparse
from pathlib import Path

from docuguard.markdown_checker import audit_markdown
from docuguard.terminology import check_terminology
from docuguard.report import generate_report


def main():
    parser = argparse.ArgumentParser(
        description="DocuGuard - Documentation Quality Auditor"
    )

    parser.add_argument(
        "file",
        help="Path to the Markdown file to audit"
    )

    args = parser.parse_args()

    file_path = Path(args.file)

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return

    if file_path.suffix.lower() != ".md":
        print("Error: Please provide a Markdown (.md) file.")
        return

    content = file_path.read_text(encoding="utf-8")

    print("\nStarting DocuGuard audit...\n")

    findings = audit_markdown(content, file_path)
    findings.extend(check_terminology(content))

    report = generate_report(
        file_path.name,
        findings
    )

    reports_directory = Path("reports")
    reports_directory.mkdir(exist_ok=True)

    report_path = reports_directory / "audit_report.md"
    report_path.write_text(report, encoding="utf-8")

    print("Audit completed successfully.")
    print(f"Total findings: {len(findings)}")
    print(f"Report generated: {report_path.resolve()}")


if __name__ == "__main__":
    main()
