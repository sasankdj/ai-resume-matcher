from flask import Flask, request, jsonify
from flask_cors import CORS
from parser import extract_text_from_pdf
from matcher import analyze_resume_vs_jd

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return {"message": "Resume ↔ JD Matcher API is running!"}

@app.route('/match_jd', methods=['POST'])
def match_resume_with_jd():
    jd_text = request.form.get('jd', '')
    resume_text = ''

    # ✅ If user pasted resume text manually
    if 'resume_text' in request.form and request.form['resume_text'].strip():
        resume_text = request.form['resume_text'].strip()
    
    # ✅ If user uploaded a resume file
    elif 'resume' in request.files:
        resume_file = request.files['resume']
        resume_text = extract_text_from_pdf(resume_file)

    # ❌ If no resume provided
    else:
        return jsonify({"error": "Please upload a resume or paste text."}), 400

    if not jd_text.strip():
        return jsonify({"error": "Please provide a job description."}), 400

    try:
        result = analyze_resume_vs_jd(resume_text, jd_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
