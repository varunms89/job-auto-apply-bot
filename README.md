# 🤖 Autonomous Job Auto-Apply Bot & Quality Engineering Suite

**Author:** VARUN M S (Final Year BCA 2025 | QA & Python Automation Engineer)  
**Live Cloud Dashboard:** [job-auto-apply-bot.onrender.com](https://job-auto-apply-bot.onrender.com)  
**Developer Portfolio:** [varunms89.github.io](https://varunms89.github.io)  
**GitHub Profile:** [github.com/varunms89](https://github.com/varunms89)  

---

## 🌿 Repository Branches & Portfolio Architecture

This repository serves as the central hub for Varun M S's software testing, AI screening, and automation engineering portfolio. Each key project is organized into its own dedicated branch:

| Branch Name | GitHub Branch Link | Focus Area & Deliverables |
| :--- | :---: | :--- |
| **`main`** *(Default)* | [View `main`](https://github.com/varunms89/job-auto-apply-bot/tree/main) | **Autonomous Job Auto-Apply Bot & Render Cloud Dashboard** (Python, Postgres/SQLite, 24/7 Crawler, Live Web Terminal, Mock API, Telegram Notifier) |
| **`qa-ecommerce-test-suite`** | [View `qa-ecommerce-test-suite`](https://github.com/varunms89/job-auto-apply-bot/tree/qa-ecommerce-test-suite) | **Comprehensive QA Testing Suite** (50+ Test Cases, Playwright E2E UI Tests, GitHub Actions CI/CD Badges, Postman API Test Collection) |
| **`ai-resume-screener`** | [View `ai-resume-screener`](https://github.com/varunms89/job-auto-apply-bot/tree/ai-resume-screener) | **AI Resume Screener & Job Match Platform** (Google Gemini Semantic ATS Matching, FastAPI REST Microservice, Swagger UI `/docs`) |
| **`portfolio`** | [View `portfolio`](https://github.com/varunms89/job-auto-apply-bot/tree/portfolio) | **Developer Portfolio Website** (HTML5, Tailwind/Clean CSS, Interactive Playwright Terminal Simulator, 1-Click ATS Resume Print) |

### Switching Between Branches Locally:
```bash
# Clone the repository
git clone https://github.com/varunms89/job-auto-apply-bot.git
cd job-auto-apply-bot

# Switch to the QA Test Suite branch
git checkout qa-ecommerce-test-suite

# Switch to the AI Resume Screener branch
git checkout ai-resume-screener

# Switch to the Portfolio branch
git checkout portfolio

# Switch back to the Main Job Bot branch
git checkout main
```

---

## 📁 `main` Branch: Core Engine Structure

- [`server.py`](server.py): Unified HTTP web server hosting the live dashboard, real-time log terminal (`/api/logs`), and mock REST API (`/api/v1/...`).
- [`config.py`](config.py): Candidate profile configuration and 100% strict Online / Remote matching policy.
- [`matcher.py`](matcher.py): Autonomous scoring engine evaluating role alignment, seniority filters (rejecting 5+ years), and work-from-home verification.
- [`apply_engine.py`](apply_engine.py): Form autofiller generating customized cover letters and applicant payloads.
- [`scrapers.py`](scrapers.py): Real-time scrapers across tech platforms (RemoteOK, ArbeitNow, Remotive, Jobicy, LinkedIn, Internshala, Wellfound).
- [`telegram_notifier.py`](telegram_notifier.py): Telegram notification engine delivering morning briefings, assessment alerts, and daily wrap-ups.
- [`telegram_listener.py`](telegram_listener.py): Interactive command listener (`/status`, `/tests`, `/prep`, `/interview`).
- [`database.py`](database.py): Relational database manager supporting Cloud PostgreSQL with local SQLite auto-fallback.
- [`test_bot.py`](test_bot.py): Verification suite covering matchers, assessment parsers, IEEE test case generation, and mock API endpoints.

---

## 🚀 How to Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run verification unit tests
python3 -m unittest test_bot.py

# 3. Start the bot and web dashboard
./start_bot.sh
```

Live dashboard will be available at: `http://localhost:8080` (or `https://job-auto-apply-bot.onrender.com`).
