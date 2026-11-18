
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

    parser.add_argument(
        "--ai",
        action="store_true",
        help="Enable AI-assisted documentation analysis"
    )

    args = parser.parse_args()

    file_path = Path(args.file)

    if not file_path.exists() or not file_path.is_file():
        print(f"Error: File not found: {file_path}")
        return

    if file_path.suffix.lower() != ".md":
        print("Error: Please provide a Markdown (.md) file.")
        return

    content = file_path.read_text(encoding="utf-8")

    print("\nStarting DocuGuard audit...\n")

    findings = audit_markdown(content, file_path)
    findings.extend(check_terminology(content))

    ai_analysis = None

    if args.ai:
        print("Running AI-assisted analysis...\n")

        try:
            from docuguard.ai_analyzer import analyze_documentation

            ai_analysis = analyze_documentation(content)

            print(
                f"AI suggestions: "
                f"{len(ai_analysis['suggestions'])}"
            )

        except Exception as error:
            print(f"AI analysis failed: {error}")
            print("Continuing with deterministic findings only.")

    report = generate_report(
        file_path.name,
        findings,
        ai_analysis
    )

    reports_directory = Path("reports")
    reports_directory.mkdir(exist_ok=True)

    report_path = reports_directory / "audit_report.md"
    report_path.write_text(report, encoding="utf-8")

    print("\nAudit completed.")
    print(f"Deterministic findings: {len(findings)}")
    print(f"Report generated: {report_path.resolve()}")


if __name__ == "__main__":
    main()
