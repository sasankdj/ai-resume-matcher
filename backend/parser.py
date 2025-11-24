import PyPDF2
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    "python", "java", "flask", "django", "machine learning", "tensorflow",
    "react", "sql", "javascript", "data analysis", "nlp", "deep learning",
    "aws", "docker", "kubernetes", "git", "html", "css", "api", "rest", "cloud"
]

def extract_text_from_pdf(file):
    """Extract text from PDF file."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_skills(text):
    """Extract skills based on predefined list."""
    text_lower = text.lower()
    found = [skill for skill in SKILLS_DB if skill in text_lower]
    return list(set(found))
