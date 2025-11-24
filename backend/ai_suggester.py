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
    Rewrite each section of the resume aligned to JD.
    Inject missing skills and key terms naturally into the rewritten version.
    """
    prompt = f"""
    You are a professional resume optimization engine.

    --- JOB DESCRIPTION ---
    {jd_text}

    --- CANDIDATE RESUME ---
    {resume_text[:4000]}

    --- MISSING SKILLS / KEYWORDS ---
    {', '.join(missing_skills) if missing_skills else 'None'}

    --- TASK ---
    1. Rewrite the resume sections (Profile, Experience, Projects) so they align with the JD.
    2. Naturally incorporate the missing skills and keywords into the rewritten sections.
    3. Keep it concise, formal, and achievement-focused.
    4. Output must be valid JSON, strictly following this structure:

    {{
      "summary": "Brief note about how the resume was tailored to the JD.",
      "sections": [
        {{
          "section_name": "Profile",
          "original_text": "Original section from resume",
          "rewritten_text": "JD-aligned rewritten section with missing skills added"
        }},
        {{
          "section_name": "Experience",
          "original_text": "...",
          "rewritten_text": "..."
        }},
        {{
          "section_name": "Projects",
          "original_text": "...",
          "rewritten_text": "..."
        }}
      ]
    }}

    Respond with only valid JSON.
    """

    try:
        response = genai.GenerativeModel(MODEL_ID).generate_content(prompt)
        text = response.text.strip()

        # Clean JSON
        start = text.find("{")
        end = text.rfind("}") + 1
        cleaned = text[start:end]
        return json.loads(cleaned)

    except Exception as e:
        return {
            "summary": f"Error generating AI suggestion: {e}",
            "sections": []
        }
