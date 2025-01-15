import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def preprocess_text(text: str) -> str:
    """Clean and preprocess text."""
    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text

def extract_keywords(text: str) -> list:
    """Extract important keywords from text."""
    # Tokenize and preprocess
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # Simple word tokenization using split()
    tokens = text.lower().split()

    # Remove stopwords and lemmatize
    keywords = [lemmatizer.lemmatize(token) for token in tokens 
               if token.isalnum() and token not in stop_words]

    # Get frequency distribution
    freq_dist = Counter(keywords)

    # Return most common keywords
    return [word for word, _ in freq_dist.most_common(50)]

def calculate_ats_score(analysis_results: dict) -> int:
    """Calculate ATS score based on keyword matches and other factors."""
    total_keywords = len(analysis_results['matched_keywords']) + len(analysis_results['missing_keywords'])
    if total_keywords == 0:
        return 0

    match_percentage = (len(analysis_results['matched_keywords']) / total_keywords) * 100

    # Adjust score based on other factors
    format_score = analysis_results['format_score']
    content_score = analysis_results['content_score']

    final_score = (match_percentage * 0.6) + (format_score * 0.2) + (content_score * 0.2)
    return round(final_score)

def analyze_text(resume_text: str, job_description: str) -> dict:
    """Analyze resume text against job description."""
    # Preprocess texts
    processed_resume = preprocess_text(resume_text)
    processed_job = preprocess_text(job_description)

    # Extract keywords
    resume_keywords = set(extract_keywords(processed_resume))
    job_keywords = set(extract_keywords(processed_job))

    # Find matches and missing keywords
    matched_keywords = resume_keywords.intersection(job_keywords)
    missing_keywords = job_keywords - resume_keywords

    # Calculate basic scores
    format_score = 80  # Base format score
    content_score = 75  # Base content score

    # Generate recommendations
    recommendations = {
        "Content": [
            "Add missing keywords naturally throughout your resume",
            "Use action verbs to describe your experiences",
            "Quantify achievements where possible"
        ],
        "Format": [
            "Use standard section headings",
            "Avoid complex formatting and tables",
            "Use bullet points for better readability"
        ],
        "Keywords": [
            f"Consider adding these missing keywords: {', '.join(list(missing_keywords)[:5])}"
        ]
    }

    return {
        "matched_keywords": list(matched_keywords),
        "missing_keywords": list(missing_keywords),
        "format_score": format_score,
        "content_score": content_score,
        "recommendations": recommendations
    }