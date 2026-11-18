# DocuGuard
### AI-Assisted Documentation Quality Auditor

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://docuguard-web.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)](https://streamlit.io/)
[![GenAI](https://img.shields.io/badge/AI-Groq%20LLM-orange)](https://groq.com/)

**DocuGuard** is a Python-based documentation quality auditing tool that helps technical writers and developers improve the clarity, consistency, structure and reliability of Markdown documentation.

It combines deterministic rule-based validation with Generative AI-powered writing suggestions, while keeping technical accuracy and final editorial decisions under human control.

**Live Application:** https://docuguard-web.streamlit.app/

---

## The Problem

Technical documentation is essential to software products, but maintaining its quality can be challenging.

Common documentation problems include:

- Inconsistent terminology and technical naming conventions.
- Incorrect heading hierarchy and poorly structured sections.
- Broken internal Markdown links.
- Overly long, ambiguous or difficult-to-understand sentences.
- Missing or incomplete documentation sections.
- Unsupported technical claims and potentially misleading instructions.

Manually reviewing these issues across multiple documents can be time-consuming.

DocuGuard addresses this problem by automating repeatable documentation checks and using AI to assist with more contextual writing improvements.

## Key Features

### 1. Deterministic Documentation Validation
- Required section detection.
- Markdown heading hierarchy validation.
- Long sentence identification.
- Broken relative Markdown link detection.
- Terminology consistency checking.

### 2. AI-Assisted Documentation Analysis
- Clarity and readability suggestions.
- Identification of ambiguous or wordy statements.
- Missing contextual information detection.
- Identification of potentially unsupported technical claims.
- Structured suggestions with severity and technical-risk classifications.

### 3. Interactive Web Application
- Upload Markdown documents through a Streamlit interface.
- Enable or disable AI-assisted analysis.
- View findings and suggestions independently.
- Monitor errors, warnings and AI suggestions through separate metrics.
- Download generated Markdown audit reports.

### 4. Command-Line Interface
Run documentation audits directly from the terminal and generate Markdown reports.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Core application and validation logic |
| Streamlit | Interactive web interface |
| Groq API | AI-assisted documentation analysis |
| LLM (GPT-OSS 120B) | Contextual writing suggestions |
| Regular Expressions | Terminology and text validation |
| Markdown | Input documentation and audit reports |
| Pytest / unittest | Automated testing |
| Git & GitHub | Version control and project management |

## System Architecture

```text
                 Markdown Document
                         |
                         v
                  Input Processing
                         |
              +----------+----------+
              |                     |
              v                     v
       Deterministic Engine     AI Analysis Engine
              |                     |
       +------+------+        Groq LLM API
       |      |      |              |
    Structure Links Terminology     |
       |      |      |              |
       +------+------+--------------+
                         |
                         v
                  Findings & Suggestions
                         |
                         v
                    Human Review
                         |
                         v
                  Markdown Report
                         |
                         v
                  Streamlit Interface
```

## Project Structure

```text
docuguard/
│
├── docuguard/
│   ├── __init__.py
│   ├── markdown_checker.py
│   ├── terminology.py
│   ├── report.py
│   └── ai_analyzer.py
│
├── samples/
│   └── sample_README.md
│
├── reports/
│
├── tests/
│   ├── test_markdown_checker.py
│   ├── test_terminology.py
│   ├── test_report.py
│   └── test_ai_analyzer.py
│
├── app.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.13
- Git
- A Groq API key (optional for deterministic checks; required for AI-assisted analysis)

### 1. Clone the Repository

```bash
git clone https://github.com/Its-Siddhant/docuguard.git
cd docuguard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Never commit your actual API key to GitHub.

### 4. Launch the Web Application

```bash
streamlit run app.py
```

Open the local URL provided by Streamlit.

## Command-Line Usage

DocuGuard also supports command-line auditing.

Run a deterministic audit:

```bash
py main.py samples/sample_README.md
```

Enable AI-assisted analysis:

```bash
py main.py samples/sample_README.md --ai
```

Generated reports are saved in the `reports/` directory.

## Running Tests

Execute the automated test suite:

```bash
py -m unittest discover -s tests -v
```

## Responsible AI and Accuracy Policy

DocuGuard is designed around a human-in-the-loop approach.

AI-generated suggestions are advisory rather than authoritative.

The AI analysis workflow incorporates safeguards to:

- Treat uploaded document content as untrusted input.
- Avoid following instructions embedded inside uploaded documents.
- Discourage fabricated commands, URLs, APIs and technical specifications.
- Require human verification of AI-generated suggestions.
- Flag technical claims that require independent verification.
- Keep deterministic validation separate from AI-generated recommendations.

The application does not automatically rewrite or approve technical documentation.

## Current Limitations

- The application currently accepts Markdown files rather than complete documentation repositories.
- Relative links are checked against the uploaded document's temporary working directory; associated assets and files are not uploaded automatically.
- AI suggestions depend on the availability and behaviour of the configured language model.
- AI-generated findings may require additional human investigation.
- The application should not be used to process confidential documentation without appropriate data-handling approval.

## Future Scope

- Documentation quality scoring with transparent evaluation criteria.
- Support for HTML and additional documentation formats.
- Repository-level documentation auditing.
- Semantic search and retrieval-augmented generation (RAG).
- Custom terminology dictionaries.
- CI/CD integration for automated documentation checks.
- Documentation version comparison and change analysis.

## Author

**Siddhant Jain**

Computer Science & Engineering | Technical Writing | Python | Generative AI

[LinkedIn](https://www.linkedin.com/in/the-siddhant-jain/)

---

*DocuGuard: Better documentation through automation, intelligent assistance and human judgment.*
