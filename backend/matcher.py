from sentence_transformers import SentenceTransformer, util
from parser import extract_skills
from ai_suggester import generate_suggestions

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity(text1, text2):
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    score = util.pytorch_cos_sim(emb1, emb2).item()
    return round(score * 100, 2)

def analyze_resume_vs_jd(resume_text, jd_text):
    similarity = compute_similarity(resume_text, jd_text)
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    missing_skills = [s for s in jd_skills if s not in resume_skills]

    if similarity >= 85:
        match_status = "Excellent Match ✅"
    elif similarity >= 65:
        match_status = "Partial Match ⚠️"
    else:
        match_status = "Low Match ❌"

    ai_feedback = generate_suggestions(resume_text, jd_text, missing_skills)

    return {
        "similarity": similarity,
        "match_status": match_status,
        "summary": ai_feedback.get("summary", "No summary provided."),
        "replacements": ai_feedback.get("replacements", []),
        "missing_skills": missing_skills
    }
