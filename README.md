# AI Resume Screener 📄🤖

An automated Natural Language Processing (NLP) tool that screens PDF resumes against job descriptions to calculate a compatibility match score. 

## Features
* Extracts text from PDF documents.
* Uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to vectorize text data.
* Calculates **Cosine Similarity** to generate a percentage match score between the candidate's skills and the job requirements.
* Filters out common English stop words to ensure accurate keyword matching.

## Tech Stack
* **Language:** Python
* **Libraries:** `pypdf` (v6.10.2, Document Parsing), `scikit-learn` (v1.8.0, Machine Learning / NLP), `fpdf2` (PDF Generation)

## Expected Demo Output

By running this project against our mock resumes, you can expect the following match scores:
* **Software Engineer Resume:** `18.33%` (Highly relevant candidate)
* **Head Chef Resume:** `3.35%` (Low match)

> **Note on TF-IDF Scoring:** In the context of Document Term Frequency-Inverse Document Frequency, a `15–20%` cosine similarity overlap is actually an exceptionally strong contextual match. Resumes are sparse texts while job descriptions are highly concentrated, so pure vector overlap naturally yields lower relative numbers compared to generic keyword counting algorithms.

## How to Run Locally
Clone the repository:
git clone https://github.com/jayansh01q/ai-resume-screener.git

Navigate into the directory:
cd ai-resume-screener

Install the required dependencies:
pip install -r requirements.txt

Generate the mock PDF resumes for testing:
python make_pdfs.py

Option A: Run the Web Interface (Recommended)
Launch the interactive Streamlit web application:
streamlit run app.py

Option B: Run the Command Line Version
If you prefer the terminal, you can run the core script directly:
python main.py

## Development Methodology: AI-Assisted Architecture
This project was built using an AI-assisted development workflow. I acted as the lead system architect, utilizing Large Language Models (like Claude 3.5 Sonnet and GPT-4o) to accelerate the prototyping and coding phase. My primary focus was on system design, library integration (`scikit-learn`, `pypdf`, `streamlit`), and tuning the mathematical thresholds to accurately reflect real-world ATS strictness.