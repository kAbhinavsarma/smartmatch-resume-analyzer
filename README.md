# SmartMatch: Resume and Job Description Analyzer

[Live Demo](https://smartmatch-analyzer.streamlit.app/)

SmartMatch is a professional resume and job description analyzer that compares candidate qualifications against job requirements, providing skill matching, gap identification, and structured reports for recruiters and job seekers.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Technical Overview](#technical-overview)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Contact](#contact)

---

## About

SmartMatch analyzes resumes and job descriptions to extract skills, identify gaps, and generate comparison reports. It uses semantic matching and NLP techniques to assist users in understanding alignment between candidate profiles and job requirements.

---

## Features

- **Skill Extraction**: Extracts skills from resumes and job descriptions using NLP and AI models.
- **Gap Analysis**: Identifies missing or recommended skills.
- **Semantic Matching**: Uses sentence transformers for deep similarity comparison.
- **Report Generation**: Exports PDF and CSV reports.
- **Cost Tracking**: Tracks OpenAI API usage.

---

## Technical Overview

### Frontend

- Streamlit for interactive UI and workflow management.
- Responsive design for cross-device compatibility.

### Backend

- Python with OpenAI GPT-4 integration.
- spaCy and sentence transformers for NLP.
- pandas and NumPy for data processing.
- PyMuPDF and Tesseract OCR for document handling.

---

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd smartmatch-resume-analyzer
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_md
   ```
4. Configure environment variables by copying the template:
   ```bash
   cp .env.example .env
   ```
   Add your OpenAI API key in the `.env` file.

5. Launch the application:
   ```bash
   streamlit run src/main.py
   ```

The application will open in your browser at `http://localhost:8501`.

---

## Deployment

The application can be deployed on Streamlit Cloud, Heroku, AWS, or Docker.

### Environment Variables

- `OPENAI_API_KEY`: Required for AI functionality.
- `APP_ENVIRONMENT`: Optional (`development` or `production`).
- `TESSERACT_PATH`: Optional path for OCR support.

---

## Project Structure

- `config/`: Configuration files.
- `data/`: Skill categories and data models.
- `src/`: Main application logic, core modules, AI handlers, UI components, utilities.
- `docs/`: Documentation and assets.
- `requirements.txt`: Dependencies.

---

## Contributing

Contributions to improve features, UI, documentation, or bug fixes are welcome. Please open issues or submit pull requests with clear descriptions.

---

## Contact

**Developers:**

- Sukhbodh Tripathi – sukhbodhtripathi210@gmail.com
- K Abhinav Sarma – kabhinavsarma@gmail.com

For questions, suggestions, or collaboration, please reach out via email or open an issue in the repository.

---

[Live Demo](https://smartmatch-analyzer.streamlit.app/)
