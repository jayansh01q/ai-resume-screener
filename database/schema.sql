CREATE DATABASE IF NOT EXISTS resume_db;
USE resume_db;

CREATE TABLE IF NOT EXISTS candidate_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_name VARCHAR(255),
    job_title TEXT,
    match_score FLOAT,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
