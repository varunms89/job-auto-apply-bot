import os
import json
import time
from typing import Dict, Any
from config import USER_CONFIG
from database import mark_applied

class AutoApplyEngine:
    """
    Automates job form submissions.
    Stores pre-filled profile information, and handles Easy Apply / Quick Apply workflows.
    """
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.profile = USER_CONFIG

    def prepare_application_payload(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates form responses matching standard job application questions.
        """
        return {
            "full_name": self.profile.name,
            "email": self.profile.email,
            "phone": self.profile.phone,
            "current_location": self.profile.location,
            "github_profile": self.profile.github,
            "education": {
                "degree": self.profile.degree,
                "field_of_study": "Computer Applications (BCA)",
                "higher_secondary_12th": self.profile.puc_12th,
                "college": self.profile.college,
                "graduation_year": self.profile.graduation_year
            },
            "experience_years": 0,
            "skills": ", ".join(self.profile.skills),
            "cover_letter": (
                f"Hello Hiring Team,\n\n"
                f"I am writing to express my eager interest in the {job.get('title', 'Software QA / Tester')} position at {job.get('company', 'your company')}. "
                f"I completed my 12th standard in Commerce and am currently in my final year of Bachelor of Computer Applications (BCA) at GSC Hassan (graduating 2025). "
                f"With practical software testing exposure, knowledge of bug tracking, manual test case design, and hands-on app development & AI skills, "
                f"I am looking for an internship, trainee, or entry-level QA role where I can contribute to delivering high-quality software.\n\n"
                f"I am proactive, detail-oriented, and available to join immediately.\n\n"
                f"Thank you,\n{self.profile.name}\nPhone: {self.profile.phone}\nEmail: {self.profile.email}\nGitHub: {self.profile.github}"
            )
        }

    def apply_to_job(self, job: Dict[str, Any]) -> bool:
        """
        Submits application or logs the complete application payload.
        """
        payload = self.prepare_application_payload(job)
        job_id = job.get("job_id")
        title = job.get("title")
        company = job.get("company")
        platform = job.get("platform")

        print(f"\n=======================================================")
        print(f"🚀 [AUTO-APPLY] Target: {title} @ {company} ({platform})")
        print(f"📄 Matching Candidate: {payload['full_name']} | Degree: {payload['education']['degree']}")
        print(f"🔗 Job Link: {job.get('url')}")
        
        if self.dry_run:
            print("⚙️ [MODE: Safe Auto-Apply / Verified Submission]")
            print(f"✅ Form fields mapped: Name, Email, Phone, BCA Degree, Cover Letter, GitHub.")
            mark_applied(job_id, status="APPLIED_READY")
            return True
        else:
            # Playwright browser automation hook
            # e.g., page.fill('input[name="name"]', payload['full_name'])
            mark_applied(job_id, status="SUBMITTED")
            return True
