# AI Resume Screener 📄🤖

An automated Natural Language Processing (NLP) tool that screens PDF resumes against job descriptions to calculate a compatibility match score. 

***

## Features

* **AI-Powered Analysis**: Utilizes **TF-IDF** (Term Frequency-Inverse Document Frequency) and **Cosine Similarity** to generate precise percentage match scores between candidate skills and job requirements.
* **Automated PDF Parsing**: Extracts and processes raw text data from PDF documents using `pypdf`.
* **Interactive Web Interface**: A sleek, user-friendly frontend built with **Streamlit** for real-time resume uploading and job description analysis.
* **Persistent Backend Storage**: Integrated **MySQL database** to log and track candidate match history, allowing for long-term data retention.
* **Data Visualization Dashboard**: Interactive charts and trend analysis using **Plotly** to visualize recruitment metrics.
* **Secure Access**: (Coming Soon) Role-based authentication to protect sensitive candidate data.

***

## Tech Stack

* **Languages**: Python, SQL
* **Frontend Framework**: Streamlit
* **Database**: MySQL Server
* **Key Libraries**:
    * `pypdf` (v6.10.2): Robust PDF document parsing.
    * `scikit-learn` (v1.8.0): Machine Learning and Natural Language Processing (NLP).
    * `mysql-connector-python`: Official driver for Python to MySQL communication.
    * `fpdf2`: Automated generation of mock PDF resumes for system testing.
    * `plotly`: Dynamic data visualization and charting.

***

## Database Setup (MySQL)
This project uses MySQL to persist analysis results.
1. Install MySQL Server and Workbench.
2. Create a database named `resume_db`.
3. Run the SQL script located in `database/schema.sql` to create the required tables.
4. Update the `db_config` dictionary in `app.py` with your local MySQL `root` password.

## Expected Demo Output

By running this project against our mock resumes, you can expect the following match scores:
* **Software Engineer Resume:** `18.33%` (Highly relevant candidate)
* **Head Chef Resume:** `3.35%` (Low match)

> **Note on TF-IDF Scoring:** In the context of Document Term Frequency-Inverse Document Frequency, a `15–20%` cosine similarity overlap is actually an exceptionally strong contextual match. Resumes are sparse texts while job descriptions are highly concentrated, so pure vector overlap naturally yields lower relative numbers compared to generic keyword counting algorithms.

## How to Run Locally

1. Clone the repository:
   ~~~bash
   git clone https://github.com/jayansh01q/ai-resume-screener.git
   ~~~

2. Navigate into the directory:
   ~~~bash
   cd ai-resume-screener
   ~~~

3. Install the required dependencies:
   ~~~bash
   pip install -r requirements.txt
   ~~~

4. Generate the mock PDF resumes for testing:
   ~~~bash
   python make_pdfs.py
   ~~~

* **Option A: Run the Web Interface (Recommended)**
  Launch the interactive Streamlit web application:
  ~~~bash
  streamlit run app.py
  ~~~

* **Option B: Run the Command Line Version**
  If you prefer the terminal, you can run the core script directly:
  ~~~bash
  python main.py
  ~~~

## Development Methodology: AI-Assisted Architecture
This project was built using an AI-assisted development workflow. I acted as the lead system architect, utilizing Large Language Models (like Claude 3.5 Sonnet and GPT-4o) to accelerate the prototyping and coding phase. My primary focus was on system design, library integration (`scikit-learn`, `pypdf`, `streamlit`), and tuning the mathematical thresholds to accurately reflect real-world ATS strictness.
I utilized an AI-assisted architecture to bridge the gap between the NLP logic and data persistence. While the AI helped generate the `mysql-connector` boilerplates, I focused on designing the relational schema and ensuring the Python backend correctly sanitized inputs before committing to the MySQL instance.
