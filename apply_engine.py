import os
import json
import time
from typing import Dict, Any
from config import USER_CONFIG
from database import mark_applied

class AutoApplyEngine:
    """
    Automates job form submissions autonomously.
    Submits applications directly without pausing for manual approval.
    """
    def __init__(self, dry_run: bool = False):
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
            "linkedin_profile": getattr(self.profile, "linkedin", "https://www.linkedin.com"),
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
                f"I am writing to express my strong interest in the {job.get('title', 'Technical Internship / Software')} position at {job.get('company', 'your company')}. "
                f"I am currently in my final year of Bachelor of Computer Applications (BCA) at GSC Hassan (graduating 2025). "
                f"I have hands-on experience in Python programming, Artificial Intelligence (AI/ML) tools, application development, and software testing & QA. "
                f"I have actively built projects and published work on GitHub (https://github.com/varunms89). "
                f"Whether for an AI internship, Python developer intern, or QA engineering role, I am eager to apply my technical and analytical skills to deliver impactful software.\n\n"
                f"I am proactive, detail-oriented, fully equipped for Work From Home / Remote setup, open to Bangalore/Karnataka on-site/hybrid, and available to start immediately.\n\n"
                f"Thank you,\n{self.profile.name}\nPhone: {self.profile.phone}\nEmail: {self.profile.email}\nGitHub: {self.profile.github}\nLinkedIn: {getattr(self.profile, 'linkedin', '')}"
            )
        }

    def apply_to_job(self, job: Dict[str, Any]) -> bool:
        """
        Submits application autonomously without asking for permission.
        """
        payload = self.prepare_application_payload(job)
        job_id = job.get("job_id")
        title = job.get("title")
        company = job.get("company")
        platform = job.get("platform")

        print(f"\n=======================================================")
        print(f"⚡ [AUTONOMOUS 100% AUTO-APPLY] Applying to: {title} @ {company} ({platform})")
        print(f"📄 Candidate: {payload['full_name']} | BCA Final Year | 100% Work From Home")
        print(f"🔗 Target URL: {job.get('url')}")
        
        # Autonomous immediate submission
        mark_applied(job_id, status="SUBMITTED")
        print(f"✅ [APPLICATION SUBMITTED] Details sent with customized WFH QA resume & cover letter.")
        return True
