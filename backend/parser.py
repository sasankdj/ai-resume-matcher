import PyPDF2
from sentence_transformers import SentenceTransformer, util

# Load once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

# Expandable skill set
SKILLS_DB = [
    "python", "java", "c++", "flask", "django", "machine learning", 
    "deep learning", "nlp", "tensorflow", "pytorch", "data science", 
    "sql", "mysql", "mongodb", "react", "node.js", "express", 
    "html", "css", "javascript", "typescript", "docker", "kubernetes", 
    "aws", "azure", "cloud", "api", "rest", "fastapi", "git", 
    "data analysis", "pandas", "numpy", "matplotlib", "openai", "streamlit",
    "opencv", "transformers", "scikit-learn", "tailwind", "postman"
]

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_skills(text, threshold=0.65):
    """
    Extract skills using both exact matches and semantic similarity.
    """
    text_lower = text.lower()

    # Exact matches
    direct_hits = [skill for skill in SKILLS_DB if skill in text_lower]

    # Semantic matches for context-based terms
    text_embedding = model.encode(text_lower, convert_to_tensor=True)
    skill_embeddings = model.encode(SKILLS_DB, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(text_embedding, skill_embeddings)[0]
    semantic_hits = [SKILLS_DB[i] for i, score in enumerate(similarities) if score > threshold]

    return sorted(list(set(direct_hits + semantic_hits)))
