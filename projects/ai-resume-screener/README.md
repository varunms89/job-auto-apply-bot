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
```bash
# Clone the repository
git clone https://github.com/varunms89/ai-resume-screener.git
cd ai-resume-screener

# Run the screener
python3 screener.py
```
