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

    cycle_number = 1
    while True:
        try:
            print(f"\n🔄 [Cycle #{cycle_number}] Executing live job scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
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
