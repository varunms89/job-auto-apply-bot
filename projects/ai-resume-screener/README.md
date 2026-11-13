# AI Resume & Job Match Intelligence Screener

**Author:** VARUN M S  
**Role:** AI & Python Developer  
**Repository:** [github.com/varunms89/ai-resume-screener](https://github.com/varunms89)

---

## 📌 Project Overview
An automated Artificial Intelligence (AI) tool built in Python that evaluates candidate resumes against technical Job Descriptions (JDs). It leverages Google Gemini Generative AI to perform:
1. **Semantic ATS Keyword Matching:** Identifies matched vs. missing domain keywords (QA, Testing, Python, AI).
2. **Match Score Calculation (0–100%):** Weighted algorithmic scoring combining hard skill coverage, qualification criteria, and relevant project experience.
3. **Actionable Remediation Feedback:** Generates tailored suggestions to improve interview conversion rates.

---

## 🏗️ Architecture & Features
- **Prompt Engineering:** Utilizes Chain-of-Thought (CoT) and Few-Shot system prompting with structured JSON schemas to eliminate hallucinations.
- **Data Preprocessing:** Cleans and tokenizes raw resume and job text.
- **RESTful CLI & Modular Python Structure:** Clean separation of concerns between extraction, prompt generation, and evaluation.

---

## 🚀 Quickstart

### 1. Command-Line Interface (CLI)
```bash
# Clone the repository
git clone https://github.com/varunms89/ai-resume-screener.git
cd ai-resume-screener

# Run the screener
python3 screener.py
```

### 2. FastAPI REST Microservice & Interactive Swagger UI
The project includes a production-ready FastAPI REST backend with automated Swagger OpenAPI documentation.

```bash
# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app:app --reload --port 8000
```

Once running:
- **Interactive Swagger Documentation:** Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.
- **Redoc Alternative:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check:** `GET /health`

#### Example API Request:
```bash
curl -X POST "http://localhost:8000/api/screen" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "VARUN M S",
    "resume_text": "Python, QA Testing, Playwright, Selenium, SQL, API Testing with Postman",
    "job_title": "QA Automation Engineer",
    "job_description": "Looking for a QA Automation Engineer skilled in Python, Playwright, API testing, and CI/CD pipelines."
  }'
```

#### Example JSON Response:
```json
{
  "candidate_name": "VARUN M S",
  "job_title": "QA Automation Engineer",
  "match_score": 92.5,
  "status": "STRONG MATCH",
  "matched_skills": ["Python", "QA Testing", "Playwright", "API Testing with Postman"],
  "missing_skills": ["CI/CD pipelines"],
  "strengths": ["Strong alignment with core automated testing tech stack"],
  "actionable_feedback": "Highlight familiarity with GitHub Actions CI/CD test badges in your project portfolio."
}
```
