import time
import os
import sys
from datetime import datetime
from main import run_job_bot_cycle

# Interval between auto-apply scans (in seconds)
# e.g., 3600 seconds = 1 hour
SCAN_INTERVAL_SECONDS = int(os.environ.get("SCAN_INTERVAL_SECONDS", 3600))

def run_continuous_live_bot():
    print("==================================================================")
    print("🚀 CONTINUOUS LIVE JOB AUTO-APPLY BOT STARTED")
    print(f"⏰ Scan Frequency: Every {SCAN_INTERVAL_SECONDS // 60} minutes")
    print("🎯 Mode: 100% Autonomous (No approval needed)")
    print("💻 Target: Software Tester (100% Work From Home / Remote)")
    print("==================================================================")

    # Start interactive Telegram command listener thread
    try:
        import threading
        from telegram_listener import run_telegram_listener
        tg_thread = threading.Thread(target=run_telegram_listener, daemon=True)
        tg_thread.start()
    except Exception as e:
        print(f"⚠️ Note on Telegram listener: {e}")

    cycle_number = 1
    last_briefing_date = None
    last_wrapup_date = None
    while True:
        try:
            now = datetime.now()
            # Daily Morning Briefing at 9:00 AM
            if now.hour == 9 and last_briefing_date != now.date():
                try:
                    from telegram_notifier import send_morning_briefing
                    send_morning_briefing()
                    last_briefing_date = now.date()
                    print("🌅 [Morning Briefing] Sent daily 9:00 AM briefing to Telegram!")
                except Exception as br_err:
                    print(f"⚠️ [Briefing Notice] {br_err}")

            # Daily Evening Wrap-Up at 8:00 PM (20:00)
            if now.hour == 20 and last_wrapup_date != now.date():
                try:
                    from telegram_notifier import send_evening_wrapup
                    send_evening_wrapup()
                    last_wrapup_date = now.date()
                    print("🌙 [Evening Wrap-Up] Sent daily 8:00 PM wrap-up to Telegram!")
                except Exception as wr_err:
                    print(f"⚠️ [Wrap-Up Notice] {wr_err}")

            print(f"\n🔄 [Cycle #{cycle_number}] Executing live job scan at {now.strftime('%Y-%m-%d %H:%M:%S')}...")
            run_job_bot_cycle(auto_apply=True)
            
            # Check for incoming assessment / interview invitation emails
            try:
                from email_monitor import check_gmail_inbox
                detected = check_gmail_inbox()
                if detected > 0:
                    print(f"🚨 [Email Monitor] Detected {detected} new assessment/interview invite(s)!")
            except Exception as mail_err:
                print(f"ℹ️ [Email Monitor Note] {mail_err}")

            print(f"\n⏳ Cycle #{cycle_number} complete. Sleeping for {SCAN_INTERVAL_SECONDS // 60} minutes until next cycle...")
            cycle_number += 1
            time.sleep(SCAN_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\n🛑 Live bot terminated by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n⚠️ Error in cycle #{cycle_number}: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    run_continuous_live_bot()
