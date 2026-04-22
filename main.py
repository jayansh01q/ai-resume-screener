from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def extract_text_from_pdf(file_path):
    """Reads a PDF file and extracts all text from it."""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except FileNotFoundError:
        return "Error: File not found. Please check the file path."
    except Exception as e:
        return f"An error occurred: {e}"

def calculate_match_score(resume_text, job_description):
    """
    Uses TF-IDF to vectorize the text and calculates the cosine similarity
    to find the percentage match between the resume and the job description.
    """
    # Put both texts into a list
    documents = [resume_text, job_description]
    
    # Initialize the Vectorizer. 
    # stop_words='english' automatically removes common words like "the", "and", "is"
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Convert texts into a matrix of TF-IDF features
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calculate the cosine similarity between the two vectors
    match_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Convert to percentage and round to 2 decimal places
    return round(match_score * 100, 2)

if __name__ == "__main__":
    print("--- AI Resume Screener Initialized ---\n")
    
    # 1. Define your mock job description here
    job_desc = """
    We are looking for a software engineer with strong programming skills in Python and SQL. 
    The ideal candidate should have experience with machine learning, database management, 
    and building scalable applications. Familiarity with GitHub and version control is required.
    """
    
    # 2. Point this to the PDF you want to test
    pdf_path = "sample_resume.pdf"
    
    if os.path.exists(pdf_path):
        print(f"Extracting text from: {pdf_path}...")
        resume_content = extract_text_from_pdf(pdf_path)
        
        if not resume_content.startswith("Error"):
            print("Calculating match score...")
            score = calculate_match_score(resume_content, job_desc)
            
            print("\n" + "="*30)
            print(f"Match Score: {score}%")
            print("="*30 + "\n")
            
            if score >= 15:
                print("Result: Highly relevant candidate. Move to interview stage.")
            elif score >= 5:
                print("Result: Potential match. Requires manual review.")
            else:
                print("Result: Low match. Likely not a fit for this role.")
        else:
            print(resume_content)
    else:
        print(f"Please place a file named '{pdf_path}' in the same directory to test the script.")