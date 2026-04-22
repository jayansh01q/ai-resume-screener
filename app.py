import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(file):
    """Reads an uploaded PDF file and extracts text."""
    try:
        text = ""
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text: {e}"

def calculate_match_score(resume_text, job_description):
    """Calculates TF-IDF cosine similarity."""
    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    match_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(match_score * 100, 2)

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Resume Screener", page_icon="📄")

st.title("📄 AI Resume Screener")
st.write("Upload a candidate's resume and paste the job description to calculate their mathematical match score.")

# 1. Job Description Input
st.subheader("1. Job Requirements")
job_desc = st.text_area("Paste the Job Description here:", height=150)

# 2. Resume Uploader
st.subheader("2. Candidate Resume")
uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")

# 3. Execution Button
if st.button("Calculate Match Score"):
    if not job_desc.strip():
        st.warning("Please paste a job description first.")
    elif uploaded_file is None:
        st.warning("Please upload a PDF resume.")
    else:
        with st.spinner("Analyzing document vectors..."):
            # Extract text
            resume_content = extract_text_from_pdf(uploaded_file)
            
            if resume_content.startswith("Error"):
                st.error(resume_content)
            else:
                # Calculate Score
                score = calculate_match_score(resume_content, job_desc)
                
                # Display Results
                st.markdown("---")
                st.subheader("Analysis Complete")
                
                # Dynamic visual feedback based on realistic ATS thresholds
                if score >= 15:
                    st.success(f"**Match Score: {score}%** - Highly relevant candidate. Move to interview stage.")
                elif score >= 5:
                    st.info(f"**Match Score: {score}%** - Potential match. Requires manual review.")
                else:
                    st.error(f"**Match Score: {score}%** - Low match. Likely not a fit for this role.")