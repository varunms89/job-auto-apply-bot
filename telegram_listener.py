import os
import time
import json
import urllib.request
import urllib.parse
from database import get_job_stats, get_assessments, get_connection
from telegram_notifier import send_telegram_message

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8967390841:AAG-H6uDlZFu5ZPG0GD0cz2c0O4HfpDVwws")
AUTHORIZED_CHAT_ID = str(os.environ.get("TELEGRAM_CHAT_ID", "6482856507"))

INTERVIEW_QUESTIONS = [
    {
        "id": 1,
        "question": "Q1 of 3: Can you walk me through the Bug Life Cycle from discovery to closure, and what would you do if a developer rejects your bug as 'Not a Bug'?",
        "keywords": ["reproduce", "steps", "screenshot", "log", "requirement", "srs", "brd", "retest", "close", "reject", "lead", "ba", "priority", "severity"],
        "model_answer": "Log the defect with complete steps to reproduce, expected vs actual result, severity/priority, and screenshots/logs. If rejected, first verify against requirements/SRS documentation. If still reproducible, demonstrate the exact steps to the developer or provide DevTools console/network logs. If disputed, consult the QA Lead or Product Owner.",
        "tip": "Always mention verifying against SRS requirements and providing reproducible Chrome DevTools network logs."
    },
    {
        "id": 2,
        "question": "Q2 of 3: How would you design test cases for an e-commerce coupon code input (valid 10% to 50% discount) using Boundary Value Analysis and Equivalence Partitioning?",
        "keywords": ["boundary", "equivalence", "valid", "invalid", "10", "50", "9", "11", "49", "51", "partition", "test case"],
        "model_answer": "Equivalence Partitioning: Valid partition is [10, 50]. Invalid partitions are <10 (e.g. 5) and >50 (e.g. 60). Boundary Value Analysis tests: 9 (Min-1), 10 (Min), 11 (Min+1), 49 (Max-1), 50 (Max), 51 (Max+1). Also test null/empty input and special characters.",
        "tip": "Explicitly recite the 6 exact BVA values: 9, 10, 11, 49, 50, and 51."
    },
    {
        "id": 3,
        "question": "Q3 of 3: What is the key difference between Smoke Testing and Regression Testing, and when in a sprint cycle do you run each?",
        "keywords": ["smoke", "build", "shallow", "critical", "regression", "side effect", "deep", "fix", "commit", "release", "sprint"],
        "model_answer": "Smoke Testing (Build Verification Testing) is shallow and fast; run immediately upon receiving a new build to check basic critical functionality before proceeding. Regression Testing is comprehensive and deep; run after bug fixes or code changes to ensure existing features were not broken.",
        "tip": "Emphasize that smoke testing is a fast gatekeeper test, while regression ensures zero unintended side-effects."
    }
]

interview_sessions = {}

def handle_command(text: str, chat_id: str):
    cmd = text.strip().lower()

    # Check if this message is part of an active mock interview
    if chat_id in interview_sessions and not cmd.startswith("/") and text not in ["📊 Application Status", "🚨 Upcoming Tests", "💼 HR Screening Script", "📝 QA Practice Quiz", "📄 Live ATS Resume", "🌅 Morning Briefing"]:
        sess = interview_sessions[chat_id]
        step = sess["step"]
        q = INTERVIEW_QUESTIONS[step]

        # Score the answer based on keywords & length
        matched = [k for k in q["keywords"] if k in text.lower()]
        word_count = len(text.split())
        if word_count < 5:
            score = 4.0
        else:
            ratio = len(matched) / len(q["keywords"])
            score = min(10.0, max(5.0, round(5.0 + ratio * 6.5, 1)))

        sess["scores"].append(score)

        feedback = (
            f"🎯 <b>Evaluation for Q{step+1}:</b>\n"
            f"⭐️ <b>Your Score:</b> <code>{score}/10</code>\n\n"
            f"✅ <b>Model Answer:</b>\n<i>\"{q['model_answer']}\"</i>\n\n"
            f"💡 <b>Pro Tip:</b> {q['tip']}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
        )

        if step < len(INTERVIEW_QUESTIONS) - 1:
            sess["step"] += 1
            next_q = INTERVIEW_QUESTIONS[sess["step"]]
            feedback += f"\n<b>{next_q['question']}</b>\n\n<i>Type your response below:</i>"
            send_telegram_message(feedback, chat_id=chat_id)
            return
        else:
            total_score = sum(sess["scores"])
            avg = round(total_score / len(sess["scores"]), 1)
            verdict = "🎉 Outstanding! You are 100% ready for technical QA screening calls!" if avg >= 8.0 else "💡 Good job! Review the model answers above to sharpen your responses!"
            feedback += (
                f"\n🏁 <b>MOCK INTERVIEW COMPLETE!</b>\n"
                f"📊 <b>Total Score:</b> <code>{round(total_score, 1)} / 30</code> (Average: <code>{avg}/10</code>)\n"
                f"{verdict}\n\n"
                f"Tap <b>🎯 Mock Interview</b> anytime to practice again!"
            )
            del interview_sessions[chat_id]
            send_telegram_message(feedback, chat_id=chat_id)
            return

    # Normal Command Handlers
    if cmd.startswith("/interview") or "mock interview" in cmd or "🎯" in text:
        interview_sessions[chat_id] = {"step": 0, "scores": []}
        q1 = INTERVIEW_QUESTIONS[0]
        msg = (
            "🎯 <b>INTERACTIVE TECHNICAL MOCK INTERVIEW STARTED</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "<i>I will ask you 3 real-world interview questions asked by top tech recruiters. Type or voice-dictate your answer to each question:</i>\n\n"
            f"<b>{q1['question']}</b>\n\n"
            "<i>Type your answer below:</i>"
        )
        send_telegram_message(msg, chat_id=chat_id)
        return

    if cmd.startswith("/start") or cmd.startswith("/help"):
        msg = (
            "🤖 <b>JOB & ASSESSMENT BOT COMMANDS</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "• Tap any button below or type a command:\n"
            "• <b>/interview</b> - Start 3-question technical mock interview\n"
            "• <b>/status</b> - Current system stats & application counts\n"
            "• <b>/tests</b> - Show pending online tests & interview links\n"
            "• <b>/hr</b> - HR phone screening scripts & model answers\n"
            "• <b>/quiz</b> - Practice QA screening questions\n"
            "• <b>/prep qa</b> - Software Testing & QA master review\n"
            "• <b>/prep python</b> - Solved coding assessment problems\n"
            "• <b>/prep ai</b> - AI & Machine Learning key topics\n"
            "• <b>/morning</b> - Daily morning briefing & Question of the Day\n"
            "• <b>/resume</b> - Direct link to your live ATS resume\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "<i>Candidate: VARUN M S (BCA 2025)</i>"
        )
        send_telegram_message(msg, chat_id=chat_id)

    elif cmd.startswith("/status") or "status" in cmd or "📊" in text:
        stats = get_job_stats()
        submitted = stats.get("SUBMITTED", 0) + stats.get("APPLIED", 0) + stats.get("APPLIED_READY", 0)
        total = sum(stats.values())
        unsubmitted = total - submitted

        assessments = get_assessments()
        pending_tests = [a for a in assessments if a.get("status") == "PENDING"]

        msg = (
            "📊 <b>LIVE SYSTEM STATUS REPORT</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"✅ <b>Submitted Applications:</b> <code>{submitted}</code>\n"
            f"⏳ <b>Evaluated / Filtered:</b> <code>{unsubmitted}</code>\n"
            f"📈 <b>Total Listings Scanned:</b> <code>{total}</code>\n"
            f"🚨 <b>Pending Tests / Sessions:</b> <code>{len(pending_tests)}</code>\n\n"
            "🌐 <b>Cloud Dashboard:</b> <a href='https://job-auto-apply-bot.onrender.com'>Open Dashboard</a>\n"
            "💻 <b>Mode:</b> 100% Autonomous (Online/Remote Preference)"
        )
        send_telegram_message(msg, chat_id=chat_id)

    elif cmd.startswith("/tests") or "test" in cmd or "🚨" in text:
        assessments = get_assessments()
        pending = [a for a in assessments if a.get("status") == "PENDING"]
        if not pending:
            msg = "✅ <b>No pending assessments or tests right now!</b>\nWhen an employer sends an assessment link, it will appear here immediately."
        else:
            msg = f"🚨 <b>PENDING TESTS & SESSIONS ({len(pending)}):</b>\n━━━━━━━━━━━━━━━━━━━\n"
            for idx, a in enumerate(pending, 1):
                msg += (
                    f"\n<b>{idx}. {a['company']}</b> ({a['platform']})\n"
                    f"💼 Role: {a['role_title']}\n"
                    f"⏳ Deadline: <code>{a['deadline_or_time']}</code>\n"
                    f"📚 Topic: <code>{a['prep_topic']}</code>\n"
                    f"🔗 <a href='{a['test_url']}'>👉 Click to Take Test</a>\n"
                )
        send_telegram_message(msg, chat_id=chat_id)

    elif cmd.startswith("/hr") or "screening" in cmd or "script" in cmd or "💼" in text:
        from prep_assistant import HR_SCREENING_QUESTIONS
        msg = (
            "💼 <b>TOP HR SCREENING TALKING POINTS</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
        )
        for h in HR_SCREENING_QUESTIONS[:3]:
            msg += (
                f"<b>{h['question']}</b>\n"
                f"🗣️ <i>\"{h['script']}\"</i>\n\n"
            )
        msg += "📖 <a href='https://job-auto-apply-bot.onrender.com/prep'>Open Full 5 Questions on Web Hub ↗</a>"
        send_telegram_message(msg, chat_id=chat_id)

    elif cmd.startswith("/quiz") or "quiz" in cmd or "📝" in text:
        msg = (
            "📝 <b>QA SCREENING PRACTICE QUESTIONS</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "<b>Q1: In Boundary Value Analysis for age 18-60, which boundary set is optimal?</b>\n"
            "A) 10, 20, 50, 70\n"
            "B) 17, 18, 19, 59, 60, 61\n"
            "C) 0, 18, 60, 100\n"
            "👉 <i>Correct: B (Min-1, Min, Min+1, Max-1, Max, Max+1)</i>\n\n"
            "<b>Q2: Which HTTP status code indicates a new resource was created?</b>\n"
            "A) 200 OK\n"
            "B) 201 Created\n"
            "C) 204 No Content\n"
            "👉 <i>Correct: B (201 Created)</i>\n\n"
            "🎯 <a href='https://job-auto-apply-bot.onrender.com/prep'>Take the 10-Question Interactive Quiz with Live Scoring ↗</a>"
        )
        send_telegram_message(msg, chat_id=chat_id)

    elif cmd.startswith("/prep qa"):
        msg = (
            "🧪 <b>QA & TESTING INTERVIEW ESSENTIALS</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "<b>1. Severity vs Priority:</b>\n"
            "• <i>Severity:</i> Technical impact (Crash = Critical, Typo = Low).\n"
            "• <i>Priority:</i> Urgency to fix (Logo misspelled on homepage = Low Severity, High Priority).\n\n"
            "<b>2. Black-Box Techniques:</b>\n"
            "• <i>Equivalence Partitioning:</i> 18-60 valid -> test 25 (valid), 10 and 70 (invalid).\n"
            "• <i>Boundary Value Analysis:</i> For 18-60 -> test 17, 18, 19, 59, 60, 61.\n\n"
            "<b>3. HTTP API Status Codes:</b>\n"
            "• <code>200 OK</code> | <code>201 Created</code> | <code>400 Bad Request</code>\n"
            "• <code>401 Unauthorized</code> | <code>404 Not Found</code> | <code>500 Server Error</code>\n\n"
            "📖 <a href='https://job-auto-apply-bot.onrender.com/prep'>Open Full Preparation Hub</a>"
        )
        send_telegram_message(msg, chat_id=chat_id)

    elif cmd.startswith("/prep python"):
        msg = (
            "🐍 <b>PYTHON CODING ASSESSMENT ESSENTIALS</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "<b>1. Two Sum (Target Pair) - O(n):</b>\n"
            "<pre>def two_sum(nums, target):\n"
            "    seen = {}\n"
            "    for i, n in enumerate(nums):\n"
            "        diff = target - n\n"
            "        if diff in seen: return [seen[diff], i]\n"
            "        seen[n] = i\n"
            "    return []</pre>\n\n"
            "<b>2. Binary Search - O(log n):</b>\n"
            "<pre>def binary_search(arr, target):\n"
            "    l, r = 0, len(arr) - 1\n"
            "    while l &lt;= r:\n"
            "        mid = (l + r) // 2\n"
            "        if arr[mid] == target: return mid\n"
            "        elif arr[mid] &lt; target: l = mid + 1\n"
            "        else: r = mid - 1\n"
            "    return -1</pre>\n\n"
            "📖 <a href='https://job-auto-apply-bot.onrender.com/prep'>Open Full Preparation Hub</a>"
        )
        send_telegram_message(msg, chat_id=chat_id)

    elif cmd.startswith("/prep ai") or cmd.startswith("/prep"):
        msg = (
            "🤖 <b>AI & MACHINE LEARNING ESSENTIALS</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "<b>1. ML Fundamentals:</b>\n"
            "• <i>Supervised:</i> Labeled data (Classification & Regression).\n"
            "• <i>Unsupervised:</i> Unlabeled data (Clustering, PCA).\n"
            "• <i>Overfitting:</i> High train accuracy, low test accuracy. Fix: Regularization, Dropout, Cross-validation.\n\n"
            "<b>2. Prompt Engineering & RAG:</b>\n"
            "• <i>Few-Shot:</i> Provide 2-3 input/output examples in prompt.\n"
            "• <i>Chain-of-Thought (CoT):</i> Instruct 'think step-by-step'.\n"
            "• <i>RAG:</i> Chunk docs -> Embed -> Vector DB search -> Context inject into LLM prompt.\n\n"
            "📖 <a href='https://job-auto-apply-bot.onrender.com/prep'>Open Full Preparation Hub</a>"
        )
        send_telegram_message(msg, chat_id=chat_id)

    elif cmd.startswith("/morning") or "morning" in cmd or "🌅" in text:
        from telegram_notifier import send_morning_briefing
        send_morning_briefing()

    elif cmd.startswith("/resume") or "resume" in cmd or "📄" in text:
        msg = (
            "📄 <b>YOUR LIVE ATS RESUME</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🔗 <a href='https://job-auto-apply-bot.onrender.com/resume'>View & Print ATS Resume (A4 PDF)</a>\n\n"
            "• Includes: Final Year BCA (2025), QA Test Case Design, Python, AI/ML, and your GitHub projects!"
        )
        send_telegram_message(msg, chat_id=chat_id)

    else:
        send_telegram_message("❓ Unknown command. Send <b>/help</b> or <b>/status</b> to see available commands.", chat_id=chat_id)

def run_telegram_listener():
    """
    Long-polling loop for incoming Telegram bot messages.
    """
    offset = None
    print("🤖 Telegram Command Listener started (Listening for /status, /tests, /prep)...")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?timeout=20"
            if offset:
                url += f"&offset={offset}"
                
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                if data.get("ok"):
                    for item in data.get("result", []):
                        offset = item["update_id"] + 1
                        msg = item.get("message")
                        if not msg:
                            continue
                        
                        chat_id = str(msg.get("chat", {}).get("id"))
                        text = msg.get("text", "")
                        
                        # Only respond to authorized user
                        if chat_id == AUTHORIZED_CHAT_ID:
                            handle_command(text, chat_id)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    run_telegram_listener()
