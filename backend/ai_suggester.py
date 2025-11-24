import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY missing. Add it to .env")

genai.configure(api_key=api_key)
MODEL_ID = "gemini-2.5-flash"

def generate_suggestions(resume_text: str, jd_text: str, missing_skills: list) -> dict:
    """
    Generate a JD-tailored rewritten version of the resume using Gemini.
    Output includes section-by-section original and improved text.
    """
    prompt = f"""
    You are an AI resume optimization engine.

    Your goal:
    Rewrite this candidate's resume so it perfectly aligns with the given Job Description (JD).

    --- JOB DESCRIPTION ---
    {jd_text}

    --- CANDIDATE RESUME ---
    {resume_text[:4000]}

    --- INSTRUCTIONS ---
    1. Analyze the job description carefully for keywords, skills, and responsibilities.
    2. Identify relevant sections from the resume such as:
       - Profile / Summary
       - Experience
       - Projects
       - Skills (if any)
    3. For each section, rewrite it to:
       - Include key JD terms and responsibilities naturally.
       - Make language more professional and metrics-driven.
       - Emphasize alignment with the JD (e.g., “AI/ML Engineer” roles).
    4. Do NOT summarize. Provide rewritten text that could replace the original section.

    Output *only valid JSON* with this structure:
    {{
      "summary": "Brief note about overall JD alignment and changes made.",
      "sections": [
        {{
          "section_name": "Profile",
          "original_text": "Original section text from resume",
          "rewritten_text": "Rewritten JD-aligned version"
        }},
        {{
          "section_name": "Experience",
          "original_text": "Original section",
          "rewritten_text": "JD-aligned improved section"
        }}
      ]
    }}

    Do NOT include markdown, commentary, or explanations.
    """

    try:
        response = genai.GenerativeModel(MODEL_ID).generate_content(prompt)
        text = response.text.strip()

        # Try parsing JSON safely
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end != -1:
                return json.loads(text[start:end])
            else:
                return {
                    "summary": "Failed to parse AI output",
                    "sections": []
                }

    except Exception as e:
        return {
            "summary": f"Error generating AI suggestion: {e}",
            "sections": []
        }
