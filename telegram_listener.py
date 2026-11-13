import os
import time
import json
import urllib.request
import urllib.parse
from database import get_job_stats, get_assessments, get_connection
from telegram_notifier import send_telegram_message

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8967390841:AAG-H6uDlZFu5ZPG0GD0cz2c0O4HfpDVwws")
AUTHORIZED_CHAT_ID = str(os.environ.get("TELEGRAM_CHAT_ID", "6482856507"))

def handle_command(text: str, chat_id: str):
    cmd = text.strip().lower()

    if cmd.startswith("/start") or cmd.startswith("/help"):
        msg = (
            "🤖 <b>JOB & ASSESSMENT BOT COMMANDS</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "• <b>/status</b> - Current system stats & application counts\n"
            "• <b>/tests</b> - Show pending online tests & interview links\n"
            "• <b>/prep qa</b> - Software Testing & QA master review\n"
            "• <b>/prep python</b> - Solved coding assessment problems\n"
            "• <b>/prep ai</b> - AI & Machine Learning key topics\n"
            "• <b>/resume</b> - Direct link to your live ATS resume\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "<i>Candidate: VARUN M S (BCA 2025)</i>"
        )
        send_telegram_message(msg, chat_id=chat_id)

    elif cmd.startswith("/status"):
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

    elif cmd.startswith("/tests"):
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

    elif cmd.startswith("/resume"):
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
