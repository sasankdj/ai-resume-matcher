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
    Use Gemini 2.5 Flash to generate JSON-based resume improvements
    directly aligned to the provided job description.
    """
    prompt = f"""
    You are a professional resume optimization assistant.

    Compare the following resume and job description.

    --- Job Description ---
    {jd_text}

    --- Resume ---
    {resume_text[:4000]}

    The goal is to tailor the resume to better match the JD.
    Identify specific phrases, sentences, or bullet points from the resume
    that should be **rewritten or replaced** to align more closely with the JD.

    Focus on:
    - Adding missing JD keywords or responsibilities
    - Replacing weak phrases with JD-aligned, measurable achievements
    - Enhancing technical relevance and phrasing for the JD
    - Avoid generic advice; give specific replacements

    Output *only valid JSON* in this structure:
    {{
      "summary": "Brief overview of how aligned the resume is and general advice.",
      "replacements": [
        {{
          "section": "Profile",
          "original_phrase": "original text snippet from resume",
          "suggested_phrase": "AI-improved rewrite aligned to JD"
        }},
        {{
          "section": "Experience",
          "original_phrase": "...",
          "suggested_phrase": "..."
        }}
      ]
    }}

    No markdown, no commentary, only valid JSON.
    """

    try:
        response = genai.GenerativeModel(MODEL_ID).generate_content(prompt)
        text = response.text.strip()

        # Parse the JSON safely
        try:
            parsed = json.loads(text)
            return parsed
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end != -1:
                cleaned = text[start:end]
                return json.loads(cleaned)
            else:
                return {
                    "summary": "AI response not structured correctly.",
                    "replacements": []
                }
    except Exception as e:
        return {
            "summary": f"Error generating AI suggestion: {e}",
            "replacements": []
        }
