import urllib.request
import urllib.parse
import json
import sqlite3
import os
from database import DB_PATH
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
    Pulls recent application records from SQLite and formats a clean Telegram report.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM jobs")
    total_scanned = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM jobs WHERE status = 'APPLIED_READY' OR status = 'APPLIED'")
    total_applied = cur.fetchone()[0]

    cur.execute("""
        SELECT title, company, match_score, url 
        FROM jobs 
        WHERE status = 'APPLIED_READY' OR status = 'APPLIED'
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
            f"   🔗 <a href='{url}'>View Job Posting</a>\n"
        )

    report += (
        f"\n━━━━━━━━━━━━━━━━━━━\n"
        f"✅ <i>Bot is actively monitoring for new openings.</i>"
    )
    return report

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
