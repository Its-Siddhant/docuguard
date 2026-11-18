
import streamlit as st
import tempfile
from pathlib import Path

from docuguard.markdown_checker import audit_markdown
from docuguard.terminology import check_terminology
from docuguard.report import generate_report


# Page configuration
st.set_page_config(
    page_title="DocuGuard | Documentation Auditor",
    page_icon="D",
    layout="wide"
)

# Application header
st.title("DocuGuard")
st.subheader("Documentation Quality Auditor")

st.write(
    "Audit your Markdown documentation for structural issues, "
    "broken links, terminology inconsistencies and clarity."
)

st.info(
    "Deterministic checks identify rule-based issues. "
    "AI suggestions are advisory and require human verification."
)

# File upload and AI settings
uploaded_file = st.file_uploader(
    "Upload your Markdown documentation",
    type=["md"]
)

use_ai = st.toggle(
    "Enable AI-assisted analysis",
    value=False
)


# Run audit
if uploaded_file is not None:

    try:
        content = uploaded_file.getvalue().decode("utf-8-sig")
    except UnicodeDecodeError:
        st.error("Unable to read this file. Please upload a UTF-8 encoded Markdown file.")
        st.stop()

    st.write(f"**File:** {uploaded_file.name}")
    st.write(f"**Document size:** {len(content)} characters")

    if st.button("Run DocuGuard Audit", type="primary"):

        if not content.strip():
            st.error("The uploaded Markdown document is empty.")

        else:
            with st.spinner("Auditing documentation..."):

                # Deterministic analysis
                with tempfile.TemporaryDirectory() as temp_dir:
                    file_path = Path(temp_dir) / uploaded_file.name
                    file_path.write_text(content, encoding="utf-8")

                    findings = audit_markdown(content, file_path)

                findings.extend(check_terminology(content))

                # AI-assisted analysis
                ai_analysis = None

                if use_ai:
                    try:
                        from docuguard.ai_analyzer import analyze_documentation

                        ai_analysis = analyze_documentation(content)

                    except Exception as error:
                        st.warning(
                            f"AI analysis could not be completed: {error}"
                        )

                # Generate report
                report = generate_report(
                    uploaded_file.name,
                    findings,
                    ai_analysis
                )

            # Store results
            st.session_state["audit_report"] = report
            st.session_state["findings"] = findings
            st.session_state["ai_analysis"] = ai_analysis

            st.success("Documentation audit completed.")


# Display audit results
if "audit_report" in st.session_state:

    findings = st.session_state["findings"]
    ai_analysis = st.session_state["ai_analysis"]

    st.divider()
    st.header("Audit Results")

    # Calculate metrics
    errors = sum(
        1 for item in findings
        if item.get("severity") == "error"
    )

    warnings = sum(
        1 for item in findings
        if item.get("severity") == "warning"
    )

    ai_suggestions_count = (
        len(ai_analysis.get("suggestions", []))
        if ai_analysis else 0
    )

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rule-Based Findings", len(findings))
    col2.metric("Errors", errors)
    col3.metric("Warnings", warnings)
    col4.metric("AI Suggestions", ai_suggestions_count)

    # Deterministic findings
    st.subheader("Deterministic Findings")

    if findings:
        for index, finding in enumerate(findings, 1):
            with st.expander(f"Finding {index}"):
                st.json(finding)
    else:
        st.success("No deterministic documentation issues detected.")

    # AI analysis
    st.subheader("AI-Assisted Analysis")

    if ai_analysis:
        st.write(ai_analysis["summary"])

        for index, suggestion in enumerate(
            ai_analysis["suggestions"], 1
        ):
            with st.expander(f"AI Suggestion {index}"):
                st.json(suggestion)
                st.warning("Human verification is required.")
    else:
        st.caption(
            "AI analysis was not performed or was unavailable."
        )

    # Download report
    st.divider()

    st.download_button(
        label="Download Audit Report",
        data=st.session_state["audit_report"],
        file_name="docuguard_audit_report.md",
        mime="text/markdown"
    )
