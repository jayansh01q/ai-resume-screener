# AI Resume Screener Pro 📄🤖

> An automated Full-Stack Natural Language Processing (NLP) tool that screens PDF resumes against job descriptions, calculates compatibility scores, and logs analytics to a secure Cloud MySQL database.

## 🚀 Live Demo

**Try the application live here:** AI Resume Screener Pro
*(Use access code: **admin123**)*

## ✨ Features

- **Cloud-Connected Architecture:** Upgraded from local storage to a fully managed Aiven Cloud MySQL database for global, persistent data tracking.
- **Secure Authentication:** Built-in login portal with session-state password protection to secure candidate data.
- **AI-Powered Analysis:** Utilizes TF-IDF and Cosine Similarity to generate precise percentage match scores between candidate skills and job requirements.
- **Automated PDF Parsing:** Extracts and processes raw text data from PDF documents using `pypdf`.
- **Data Visualization Dashboard:** Interactive charts and trend analysis using Plotly to visualize recruitment metrics pulled live from the cloud database.
- **Environment Security:** Implements `python-dotenv` for secure credential management, ensuring no hardcoded secrets in the repository.

## 🛠️ Tech Stack

- **Frontend & Hosting:** Streamlit / Streamlit Community Cloud
- **Database & Hosting:** MySQL Server / Aiven Cloud

### Key Libraries:

- **`pypdf`** (v6.10.2): Robust PDF document parsing.
- **`scikit-learn`** (v1.8.0): Machine Learning and Natural Language Processing (NLP).
- **`mysql-connector-python`**: Database communication (configured for pure TCP connections).
- **`plotly`**: Dynamic data visualization and charting.
- **`python-dotenv`**: Environment variable management.

## 📊 Expected Match Scoring

> **Note on TF-IDF Scoring:** In the context of Document Term Frequency-Inverse Document Frequency, a **15–20% cosine similarity overlap is an exceptionally strong contextual match**. Resumes are sparse texts while job descriptions are highly concentrated, so pure vector overlap naturally yields lower relative numbers compared to generic keyword counting algorithms.

## 💻 How to Run Locally

If you wish to run this application on your own machine, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/jayansh01q/ai-resume-screener.git
cd ai-resume-screener
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup (Bring Your Own DB)

This project requires a MySQL database. You can use a local instance or a free cloud provider like Aiven.

- Create a database named `defaultdb`.
- Execute the `CREATE TABLE` script provided in `database/schema.sql`.
- If using a cloud database that requires SSL, download your provider's CA Certificate and save it in the root folder as `ca.pem`.

### 4. Environment Variables

Create a `.env` file in the root directory and add your database credentials:

```plaintext
MYSQL_HOST=your_database_host
MYSQL_USER=your_database_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DB=defaultdb
MYSQL_PORT=your_port_number
```

### 5. Launch the Application

```bash
streamlit run app.py
```

## 🏗️ Development Methodology: AI-Assisted Architecture

This project was built using an AI-assisted development workflow. I acted as the lead system architect, utilizing Large Language Models to accelerate the prototyping and coding phase. My primary focus was on system design, bridging the gap between the NLP logic (`scikit-learn`) and data persistence (`mysql-connector`), securing the environment with `.env` files, and successfully deploying a production-ready cloud application.
