import sqlite3
import os
import json
from config import USER_CONFIG
from database import DB_PATH

class GovtApplicationHelper:
    """
    Assists in preparing dossiers and autofill packages for Government exams (KEA, KPSC, RRB, SSC).
    Due to OTP, Aadhaar e-KYC, and biometric requirements on Indian government servers,
    this generates a 1-click ready Dossier with exact details needed for registration.
    """
    def __init__(self):
        self.profile = USER_CONFIG

    def get_12th_eligible_notifications(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, portal, notification_title, link FROM govt_notifications")
        rows = cur.fetchall()
        conn.close()

        # Specific 12th standard suitable Karnataka and Central posts
        keywords_12th = ["constable", "village administrative", "vao", "clerk", "sda", "surveyor", "purec", "junior assistant", "ntpc"]
        matched = []
        for r in rows:
            title_lower = r[2].lower()
            if any(k in title_lower for k in keywords_12th):
                matched.append({
                    "id": r[0],
                    "portal": r[1],
                    "title": r[2],
                    "url": r[3]
                })
        return matched

    def generate_candidate_dossier(self, govt_job):
        """
        Creates an exact form-filling profile to copy-paste during application.
        """
        return {
            "Job Title": govt_job["title"],
            "Portal": govt_job["portal"],
            "Application Link": govt_job["url"],
            "Applicant Details": {
                "Full Name (As per 10th/12th Marks Card)": self.profile.name,
                "Mobile Number (For OTP)": self.profile.phone,
                "Email ID": self.profile.email,
                "Native District / Place": "Hassan, Karnataka",
                "Medium of Instruction": "Kannada / English",
                "Educational Qualification 1 (12th / PUC)": {
                    "Stream": "Commerce",
                    "Status": "Passed",
                    "Board": "Department of Pre-University Education, Karnataka"
                },
                "Higher Education (Pursuing)": {
                    "Course": "Bachelor of Computer Applications (BCA)",
                    "Institution": "Government Science College (GSC), Hassan",
                    "Expected Year of Passing": "2025"
                },
                "Computer Literacy": "Yes (BCA Student, Computer Applications & Programming Knowledge)",
                "Languages Known": "Kannada (Read, Write, Speak - 1st Language eligible), English"
            }
        }

def prepare_all_govt_applications():
    helper = GovtApplicationHelper()
    matched = helper.get_12th_eligible_notifications()

    print("==================================================================")
    print("🏛️ GOVERNMENT JOB APPLICATIONS (12th / PUC ELIGIBLE POSTS)")
    print(f"👤 Candidate: {USER_CONFIG.name} | Native: Hassan, Karnataka")
    print(f"🎓 Qualification Basis: 12th Commerce + BCA Pursuing")
    print("==================================================================")

    if not matched:
        print("No immediate 12th matching notifications found.")
        return

    print(f"\n✅ Found {len(matched)} direct 12th Standard / PUC Government Openings:\n")
    dossiers = []
    for idx, item in enumerate(matched, 1):
        print(f"{idx}. [{item['portal']}] {item['title']}")
        print(f"   🔗 Direct Portal Link: {item['url']}")
        dossier = helper.generate_candidate_dossier(item)
        dossiers.append(dossier)

    # Save to JSON dossier file
    out_file = os.path.join(os.path.dirname(__file__), "govt_application_dossier.json")
    with open(out_file, "w") as f:
        json.dump(dossiers, f, indent=2)

    print(f"\n📁 Prepared Application Dossier saved to: govt_application_dossier.json")
    print("==================================================================")

if __name__ == "__main__":
    prepare_all_govt_applications()
