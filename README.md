# 🤖 Autonomous Job Auto-Apply Bot & AI Quality Engineering Suite

![CI/CD QA Pipeline](https://github.com/varunms89/job-auto-apply-bot/actions/workflows/qa_tests.yml/badge.svg)
![Test Coverage](https://img.shields.io/badge/Test_Coverage-98%25-brightgreen?style=flat-square&logo=pytest)
![Playwright Self-Healing](https://img.shields.io/badge/Playwright-AI_Self_Healing-2EAD33?style=flat-square&logo=playwright)
![Cloud Dashboard](https://img.shields.io/badge/Render_Cloud_Hub-LIVE_24%2F7-00C7B7?style=flat-square&logo=render)
![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python)
![Target Roles](https://img.shields.io/badge/Preference-100%25_Online_%2F_Remote_QA-blue?style=flat-square)

**Author:** **VARUN M S** (Final Year BCA 2025 | Software QA, SDET & Python Automation Engineer)  
📧 `msvarun89@gmail.com` | 📱 `+91 8861639284`  

🌐 **Live Cloud Dashboard:** [job-auto-apply-bot.onrender.com](https://job-auto-apply-bot.onrender.com)  
🎯 **Siemens HackerRank OA Simulator & Prep Hub:** [job-auto-apply-bot.onrender.com/prep](https://job-auto-apply-bot.onrender.com/prep)  
📊 **Live CI/CD Automated HTML Test Report:** [job-auto-apply-bot.onrender.com/test-report](https://job-auto-apply-bot.onrender.com/test-report)  
💻 **Developer Portfolio:** [varunms89.github.io](https://varunms89.github.io)  

---

## 🏆 Featured Engineering & QA Automation Projects

### 1. 🩹 AI "Self-Healing" Playwright E-Commerce Test Suite
- **Problem Solved:** Eliminates flaky UI tests when frontend developers rename DOM attributes (`#checkout-btn` → `[data-test='login-button']`).
- **How It Works:** Intercepts `TimeoutError`, inspects live DOM candidates, and uses LLM/heuristic semantic scoring to heal broken locators dynamically at runtime (98% confidence).
- **Code:** [`projects/qa-ecommerce-test-suite/tests/test_self_healing_playwright.py`](projects/qa-ecommerce-test-suite/tests/test_self_healing_playwright.py)

### 2. 🔍 AI Root Cause Analyzer (RCA) & IEEE 829 JIRA Bug Drafter
- **Capabilities:** Parses raw stack traces, HTTP 500/401 logs, and assertion failures into plain-English RCA reports, structured **IEEE 829 JIRA Defect Tickets**, and copy-ready developer code patches.
- **Access:** Live on the [Cloud Prep Hub (`/prep`)](https://job-auto-apply-bot.onrender.com/prep) and via Telegram (`/rca <error_log>`).

### 3. 🎯 Siemens / HackerRank 30-Minute Online Assessment Simulator
- **Capabilities:** Interactive 30-minute countdown simulator featuring the **Top 10 Siemens SDET & QA HackerRank challenges** (Python Server Log Aggregation, SQL Defect SLA Joins, Sliding-Window API Rate Limiting, SemVer Firmware Comparison, and BVA Test Generation) with instant test-case verification.
- **Access:** [Launch Simulator on `/prep`](https://job-auto-apply-bot.onrender.com/prep) or send `/siemens` on Telegram.

### 4. 🥒 AI Gherkin BDD `.feature` & `pytest-bdd` Step Generator
- **Capabilities:** Converts plain-English user stories into Cucumber Gherkin `Scenario Outline` tables and executable Python `pytest-bdd` + Playwright step definitions.

### 5. 🎙️ Voice-Note & Text AI Mock Interview Coach (`/interview`)
- **Capabilities:** Conducts adaptive 3-question technical QA/SDET interviews on Telegram. Accepts **spoken voice notes (`.ogg`)** or text, transcribes speech, and grades both **Technical Accuracy (0–10)** and **Spoken STAR Delivery Clarity**.

---

## 🌿 Multi-Branch Repository Architecture

| Branch Name | GitHub Branch Link | Focus Area & Deliverables |
| :--- | :---: | :--- |
| **`main`** *(Default)* | [View `main`](https://github.com/varunms89/job-auto-apply-bot/tree/main) | **Autonomous Job Auto-Apply Bot, AI QA Suite & Render Cloud Hub** (1,100+ jobs analyzed, 98+ applications submitted, 19/19 CI unit tests) |
| **`qa-ecommerce-test-suite`** | [View `qa-ecommerce-test-suite`](https://github.com/varunms89/job-auto-apply-bot/tree/qa-ecommerce-test-suite) | **Comprehensive QA Testing Suite** (50+ IEEE 829 Test Cases, Self-Healing Playwright E2E Tests, Postman Cloud API Regression Suite) |
| **`ai-resume-screener`** | [View `ai-resume-screener`](https://github.com/varunms89/job-auto-apply-bot/tree/ai-resume-screener) | **AI Resume Screener & Job Match Platform** (Google Gemini Semantic ATS Matching, FastAPI REST Microservice, Swagger UI `/docs`) |
| **`portfolio`** | [View `portfolio`](https://github.com/varunms89/job-auto-apply-bot/tree/portfolio) | **Interactive QA Engineer Portfolio Website** (HTML5, CSS3, Live Terminal Simulator, 1-Click ATS Resume PDF) |

---

## 🚀 Quick Start & Local Verification

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the 19-test QA & AI verification suite + generate HTML report
python3 generate_html_report.py

# 3. Start the 24/7 Autonomous Bot & Web Dashboard (Port 8080)
./start_bot.sh
```
