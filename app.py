import streamlit as st
import mysql.connector
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- DATABASE CONFIGURATION ---
# Replace 'your_password_here' with the actual password you set in MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'resume_db'
}

def save_to_database(name, job, score):
    """Saves the analysis result into the MySQL table."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        query = "INSERT INTO candidate_scores (candidate_name, job_title, match_score) VALUES (%s, %s, %s)"
        values = (name, job, score)
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database Error: {e}")
        return False

# --- CORE LOGIC ---
def extract_text_from_pdf(file):
    try:
        text = ""
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error: {e}"

def calculate_match_score(resume_text, job_description):
    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    match_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(match_score * 100, 2)

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Resume Screener Pro", page_icon="🚀")

st.title("🚀 AI Resume Screener + MySQL")
st.write("This version automatically saves all analysis results to your local database.")

# 1. Inputs
job_desc = st.text_area("1. Paste Job Description:", height=100)
candidate_name = st.text_input("2. Candidate Full Name (for database):")
uploaded_file = st.file_uploader("3. Upload PDF Resume", type="pdf")

# 2. Execution
if st.button("Analyze & Save to DB"):
    if not job_desc or not candidate_name or not uploaded_file:
        st.warning("Please fill out all fields and upload a resume.")
    else:
        with st.spinner("Processing..."):
            resume_content = extract_text_from_pdf(uploaded_file)
            
            if "Error" not in resume_content:
                score = calculate_match_score(resume_content, job_desc)
                
                # Try to save to MySQL
                db_success = save_to_database(candidate_name, job_desc[:100] + "...", score)
                
                # Display Results
                st.markdown("---")
                if db_success:
                    st.success(f"**Analysis Saved!** Candidate: {candidate_name} | Score: {score}%")
                else:
                    st.warning(f"Analysis calculated ({score}%), but failed to save to database.")
                
                if score >= 15:
                    st.balloons()
                    st.info("Status: Highly Recommended")
            else:
                st.error(resume_content)
