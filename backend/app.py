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
    try:
        jd_text = request.form.get('jd', '')
        resume_text = ''

        if 'resume_text' in request.form and request.form['resume_text'].strip():
            resume_text = request.form['resume_text'].strip()
        elif 'resume' in request.files:
            resume_file = request.files['resume']
            resume_text = extract_text_from_pdf(resume_file)
        else:
            return jsonify({"error": "No resume provided"}), 400

        if not jd_text.strip():
            return jsonify({"error": "Job description missing"}), 400

        result = analyze_resume_vs_jd(resume_text, jd_text)
        return jsonify(result)

    except Exception as e:
        import traceback
        print("🔥 Backend Error Trace:\n", traceback.format_exc())  # full log in console
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
