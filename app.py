"""
=============================================================================
TITLE: AI Resume Screener Pro
=============================================================================
This application is an AI-powered resume screening tool that helps recruiters
and hiring managers quickly evaluate candidates. It extracts text from PDF
resumes, compares it against a provided job description using natural
language processing (TF-IDF and Cosine Similarity), and calculates a match
score. It also features a MySQL database integration to save candidate scores
and an interactive analytics dashboard to visualize the results.
"""

# --- CORE IMPORTS ---
# 'streamlit' is used to build the interactive web user interface.
# 'mysql.connector' allows the app to connect, read, and write to a local MySQL database.
# 'pypdf' is used to read and extract text content from uploaded PDF resumes.
# 'sklearn' (scikit-learn) provides the machine learning tools:
#   - TfidfVectorizer: converts text into numerical vectors based on word importance.
#   - cosine_similarity: calculates how similar two text vectors are (giving us the match score).
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

# --- ANALYTICS DASHBOARD ---
# The following imports and function power the analytics dashboard below.
# 'pandas' is used to load data from our MySQL database into a structured DataFrame,
# which makes it easy to manipulate and pass to visualization libraries.
# 'plotly.express' is used to generate interactive, visually appealing charts 
# based on that DataFrame (like the score distribution histogram).
import pandas as pd
import plotly.express as px

def show_analytics():
    st.markdown("---")
    st.header("📊 Recruitment Analytics Dashboard")
    
    try:
        # 1. Fetch data from MySQL
        conn = mysql.connector.connect(**db_config)
        query = "SELECT candidate_name, match_score, analysis_date FROM candidate_scores"
        df = pd.read_sql(query, conn)
        conn.close()

        if not df.empty:
            # 2. Create the Plotly Chart
            fig = px.bar(
                df, 
                x="candidate_name", 
                y="match_score",
                title="Candidate Comparison",
                labels={'match_score': 'Match Score (%)', 'candidate_name': 'Candidate'},
                color="match_score",
                color_continuous_scale="Viridis" # This adds a cool color gradient!
            )
            
            # 3. Display stats and chart
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Resumes Scanned", len(df))
            with col2:
                st.metric("Average Match Score", f"{round(df['match_score'].mean(), 2)}%")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 4. Show raw data table (optional but pro)
            with st.expander("View Raw Database Records"):
                st.dataframe(df.sort_values(by="analysis_date", ascending=False))
        else:
            st.info("No data found in the database yet. Run an analysis to see the dashboard!")
            
    except Exception as e:
        st.error(f"Could not load dashboard: {e}")

# Call the function at the very end of your script
show_analytics()
