import React, { useState } from "react";
import axios from "axios";
// if you’re using react-diff-viewer-continued:
// import DiffViewer from "react-diff-viewer-continued";

function TextDiff({ original, suggested }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
      <div className="bg-red-50 border border-red-300 p-3 rounded-md">
        <h4 className="font-semibold text-red-700 mb-2">Original</h4>
        <pre className="whitespace-pre-wrap text-sm text-gray-800">{original}</pre>
      </div>
      <div className="bg-green-50 border border-green-300 p-3 rounded-md">
        <h4 className="font-semibold text-green-700 mb-2">Suggested</h4>
        <pre className="whitespace-pre-wrap text-sm text-gray-800">{suggested}</pre>
      </div>
    </div>
  );
}

function App() {
  const [useTextResume, setUseTextResume] = useState(false);
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if ((!resumeFile && !resumeText.trim()) || !jd.trim()) {
      setError("Please upload a resume file or paste resume text, and enter a job description.");
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const formData = new FormData();
      if (resumeFile) formData.append("resume", resumeFile);
      if (resumeText.trim()) formData.append("resume_text", resumeText);
      formData.append("jd", jd);

      const res = await axios.post("http://localhost:5000/match_jd", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to get results. Check your backend connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10 px-5">
      <div className="max-w-5xl w-full bg-white shadow-lg rounded-2xl p-8">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
          Resume ↔ JD Interactive Matcher
        </h1>

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Toggle */}
          <div className="flex justify-center space-x-4 mb-3">
            <button
              type="button"
              className={`px-4 py-2 rounded-lg font-semibold ${
                !useTextResume ? "bg-blue-600 text-white" : "bg-gray-200"
              }`}
              onClick={() => setUseTextResume(false)}
            >
              Upload Resume
            </button>
            <button
              type="button"
              className={`px-4 py-2 rounded-lg font-semibold ${
                useTextResume ? "bg-blue-600 text-white" : "bg-gray-200"
              }`}
              onClick={() => setUseTextResume(true)}
            >
              Paste Resume
            </button>
          </div>

          {/* Resume Input */}
          {!useTextResume ? (
            <div>
              <label className="block font-semibold mb-2">Upload Resume (PDF)</label>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setResumeFile(e.target.files[0])}
                className="w-full border border-gray-300 p-2 rounded-lg"
              />
            </div>
          ) : (
            <div>
              <label className="block font-semibold mb-2">Paste Resume Text</label>
              <textarea
                rows="10"
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Paste your resume text here..."
                className="w-full border border-gray-300 p-3 rounded-lg"
              ></textarea>
            </div>
          )}

          {/* Job Description */}
          <div>
            <label className="block font-semibold mb-2">Job Description</label>
            <textarea
              rows="5"
              value={jd}
              onChange={(e) => setJd(e.target.value)}
              placeholder="Paste the job description here..."
              className="w-full border border-gray-300 p-3 rounded-lg"
            ></textarea>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            {loading ? "Analyzing..." : "Match Resume"}
          </button>
        </form>

        {/* Error */}
        {error && <div className="mt-4 text-red-600 text-center">{error}</div>}

        {/* Results */}
        {result && (
  <div className="mt-10">
    <h2 className="text-2xl font-bold text-green-600 mb-4">
      Resume Match Analysis
    </h2>

    {/* --- Match Summary Card --- */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-600">
        <p className="text-gray-700 font-semibold">Similarity Score</p>
        <p className="text-3xl font-bold text-blue-700">
          {result.similarity ? `${result.similarity}%` : "—"}
        </p>
      </div>

      <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-600">
        <p className="text-gray-700 font-semibold">Match Status</p>
        <p className="text-xl font-bold text-green-700">
          {result.match_status}
        </p>
      </div>

      <div className="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500">
        <p className="text-gray-700 font-semibold">Missing Skills</p>
        <p className="text-sm text-yellow-700">
          {result.missing_skills && result.missing_skills.length > 0
            ? result.missing_skills.join(", ")
            : "None 🎉"}
        </p>
      </div>
    </div>

    {/* --- AI Summary --- */}
    <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-md mb-8">
      <p className="text-gray-800 whitespace-pre-line">{result.summary}</p>
    </div>

    {/* --- Section Rewrites --- */}
    {result.sections && result.sections.length > 0 ? (
      result.sections.map((section, i) => (
        <div key={i} className="mb-6 bg-gray-50 p-4 rounded-lg shadow-sm">
          <h3 className="text-xl font-semibold text-gray-700 mb-3">
            {section.section_name}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-red-50 border border-red-300 p-3 rounded-md">
              <h4 className="text-red-700 font-semibold mb-1">Original</h4>
              <p className="text-gray-800 text-sm whitespace-pre-wrap">
                {section.original_text}
              </p>
            </div>
            <div className="bg-green-50 border border-green-300 p-3 rounded-md">
              <h4 className="text-green-700 font-semibold mb-1">
                JD-Aligned Rewrite
              </h4>
              <p className="text-gray-800 text-sm whitespace-pre-wrap">
                {section.rewritten_text}
              </p>
            </div>
          </div>
        </div>
      ))
    ) : (
      <p className="text-gray-600">No rewritten sections found.</p>
    )}
  </div>
)}



      </div>

      <footer className="mt-8 text-gray-500 text-sm">
        Built with 💙 by You — Resume Matcher Project
      </footer>
    </div>
  );
}

export default App;
