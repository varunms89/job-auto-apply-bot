import urllib.request
import urllib.parse
import json
import sqlite3
import os
from database import get_connection, DB_PATH
from config import USER_CONFIG

# Telegram Bot Credentials
# Set these in your environment or enter directly:
# e.g., export TELEGRAM_BOT_TOKEN="your_token"
#       export TELEGRAM_CHAT_ID="your_chat_id"
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8967390841:AAG-H6uDlZFu5ZPG0GD0cz2c0O4HfpDVwws")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "6482856507")

def send_telegram_message(text: str, token: str = None, chat_id: str = None) -> bool:
    """
    Sends a formatted message to a Telegram chat or channel.
    """
    bot_token = token or TELEGRAM_BOT_TOKEN
    target_chat = chat_id or TELEGRAM_CHAT_ID

    if not bot_token or not target_chat:
        print("\n⚠️ [Telegram Alert] Bot Token or Chat ID not configured yet.")
        print("💡 Please provide your Telegram Bot Token & Chat ID (instructions below).")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": target_chat,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode())
            if res.get("ok"):
                print("✅ Telegram report delivered successfully!")
                return True
            else:
                print(f"❌ Telegram API Error: {res}")
                return False
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")
        return False

def generate_live_report() -> str:
    """
    Pulls recent application records from Postgres/SQLite and formats a clean Telegram report.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM jobs")
    total_scanned = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM jobs WHERE status IN ('APPLIED_READY', 'APPLIED', 'SUBMITTED')")
    total_applied = cur.fetchone()[0]

    cur.execute("""
        SELECT title, company, match_score, url 
        FROM jobs 
        WHERE status IN ('APPLIED_READY', 'APPLIED', 'SUBMITTED')
        ORDER BY match_score DESC, id DESC 
        LIMIT 6
    """)
    top_jobs = cur.fetchall()
    conn.close()

    report = (
        f"🤖 <b>JOB AUTO-APPLY BOT REPORT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Candidate:</b> {USER_CONFIG.name}\n"
        f"🎓 <b>Profile:</b> BCA Final Year (2025)\n"
        f"🎯 <b>Target:</b> Software Tester / QA Roles\n\n"
        f"📊 <b>Summary:</b>\n"
        f"• Total Listings Scanned: <b>{total_scanned}</b>\n"
        f"• Applications Processed: <b>{total_applied}</b>\n\n"
        f"🚀 <b>Recent Top Matches Applied:</b>\n"
    )

    for idx, (title, comp, score, url) in enumerate(top_jobs, 1):
        report += (
            f"\n{idx}. <b>{title}</b>\n"
            f"   🏢 {comp} | ⭐️ Score: <code>{score}/100</code>\n"
            f"   👉 <a href='{url}'><b>TAP TO VIEW & APPLY ↗</b></a>\n"
        )

    report += (
        f"\n━━━━━━━━━━━━━━━━━━━\n"
        f"✅ <i>Bot is actively monitoring for new openings.</i>"
    )
    return report

def send_assessment_alert(company: str, role_title: str, platform: str, test_url: str,
                          deadline_or_time: str, prep_topic: str = "General", instructions: str = "") -> bool:
    """
    Sends an urgent high-priority Telegram alert when a test link or online interview invite is detected.
    """
    alert = (
        f"🚨 <b>TEST / ONLINE INTERVIEW ALERT!</b> 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Candidate:</b> {USER_CONFIG.name}\n"
        f"🏢 <b>Company:</b> <b>{company}</b>\n"
        f"💼 <b>Role:</b> {role_title}\n"
        f"💻 <b>Platform:</b> <code>{platform}</code>\n"
        f"⏳ <b>Deadline / Time:</b> <b>{deadline_or_time}</b>\n"
        f"📚 <b>Recommended Prep:</b> <code>{prep_topic}</code>\n"
    )
    if instructions:
        alert += f"📝 <b>Note:</b> {instructions}\n"

    alert += (
        f"\n🚀 <a href='{test_url}'><b>👉 TAP TO START ASSESSMENT / JOIN ↗</b></a>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"💡 <i>Tip: Check the Preparation Hub on your Dashboard for QA & Python cheat sheets before starting!</i>"
    )

    print(f"\n🚨 [URGENT TELEGRAM ALERT] Dispatched test alert for {company} ({platform})")
    return send_telegram_message(alert)

def send_morning_briefing() -> bool:
    """
    Sends the 9:00 AM daily job hunt briefing + Question of the Day to Telegram.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM jobs")
    total_scanned = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM jobs WHERE status IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED', 'TEST_GIVEN', 'INTERVIEWING', 'OFFERED')")
    total_applied = cur.fetchone()[0]

    try:
        cur.execute("SELECT count(*) FROM assessments WHERE status = 'PENDING'")
        pending_tests = cur.fetchone()[0]
    except Exception:
        pending_tests = 0
    conn.close()

    # Question of the day from QA_PRACTICE_QUESTIONS
    from prep_assistant import QA_PRACTICE_QUESTIONS
    from datetime import datetime
    day_idx = datetime.now().day % len(QA_PRACTICE_QUESTIONS)
    q = QA_PRACTICE_QUESTIONS[day_idx]

    opts = "\n".join([f"  {chr(65+i)}) {opt}" for i, opt in enumerate(q["options"])])

    briefing = (
        f"🌅 <b>GOOD MORNING VARUN! DAILY JOB BRIEFING</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📅 <b>Date:</b> {datetime.now().strftime('%A, %d %B %Y')}\n"
        f"🎓 <b>Candidate:</b> {USER_CONFIG.name} (BCA 2025)\n\n"
        f"📊 <b>Your Pipeline Status:</b>\n"
        f"• Total Applications Submitted: <b>{total_applied}</b>\n"
        f"• Total Opportunities Evaluated: <b>{total_scanned}</b>\n"
        f"• Pending Tests / Invites: <b>{pending_tests}</b>\n\n"
        f"🧠 <b>QUESTION OF THE DAY (QA / Testing):</b>\n"
        f"<b>Q:</b> {q['question']}\n\n"
        f"{opts}\n\n"
        f"💡 <b>Answer & Reason:</b>\n"
        f"<b>{chr(65+q['answer'])}) {q['options'][q['answer']]}</b>\n"
        f"<i>{q['explanation']}</i>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 <a href='https://job-auto-apply-bot.onrender.com'>Open Live Dashboard</a> | <a href='https://job-auto-apply-bot.onrender.com/prep'>Prep Hub</a>"
    )

    return send_telegram_message(briefing)

def dispatch_report():
    report_text = generate_live_report()
    print("\n---------------------------------------------------------")
    print("📝 GENERATED TELEGRAM REPORT PREVIEW:")
    print("---------------------------------------------------------")
    # Clean tags for terminal preview
    print(report_text.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", "").replace("<i>", "").replace("</i>", "").replace("<a href='", "").replace("'>View Job Posting</a>", ""))
    print("---------------------------------------------------------")

    send_telegram_message(report_text)

if __name__ == "__main__":
    dispatch_report()
