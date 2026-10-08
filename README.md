# 🤖 Job Auto-Apply Bot (Tester / QA / Fresher Edition)

Built specifically for **Varun M S** (BCA Candidate, Fresher).

---

## 📁 Project Structure

- [`config.py`](file:///Users/varunms/Downloads/die-again/Application%20AI/config.py): Your parsed resume profile (Name, Phone, Email, BCA Degree, GitHub, QA & Testing target roles).
- [`matcher.py`](file:///Users/varunms/Downloads/die-again/Application%20AI/matcher.py): Matching algorithm tailored for QA / Tester / Fresher / Trainee positions. Filters out 5+ year senior roles and boosts entry-level/BCA job postings.
- [`apply_engine.py`](file:///Users/varunms/Downloads/die-again/Application%20AI/apply_engine.py): Form autofiller engine that formats tailored cover letters, personal details, education, and answers.
- [`scrapers.py`](file:///Users/varunms/Downloads/die-again/Application%20AI/scrapers.py): Scrapes Indeed, tech job feeds, and remote QA boards.
- [`govt_scraper.py`](file:///Users/varunms/Downloads/die-again/Application%20AI/govt_scraper.py): Tracks Karnataka government recruitment portals (**KPSC** and **KEA**) for recruitment notifications.
- [`database.py`](file:///Users/varunms/Downloads/die-again/Application%20AI/database.py): SQLite database (`jobs_bot.db`) keeping track of discovered jobs, match scores, and application statuses to prevent duplicates.
- [`main.py`](file:///Users/varunms/Downloads/die-again/Application%20AI/main.py): Pipeline execution entrypoint.
- [`test_bot.py`](file:///Users/varunms/Downloads/die-again/Application%20AI/test_bot.py): Verification tests for match criteria and application payload generation.

---

## 🚀 How to Run Locally

```bash
# 1. Run unit tests
python3 test_bot.py

# 2. Run the main job discovery and auto-apply cycle
python3 main.py
```

---

## ☁️ 24/7 Cloud Deployment (Railway / Render / VPS)

To keep this bot scanning and applying 24/7:
1. Push this folder to your GitHub repository: `https://github.com/varunms89`
2. Connect the repo to [Railway.app](https://railway.app) or [Render.com](https://render.com).
3. Set the start command to:
   ```bash
   python3 main.py
   ```
4. Add a cron schedule or loop interval (e.g., every 3 hours) to automatically check and apply to new openings.
