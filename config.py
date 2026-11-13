import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Automatically load environment variables from local .env if present
env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file):
    try:
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    except Exception:
        pass

@dataclass
class UserProfile:
    name: str = "VARUN M S"
    email: str = "msvarun89@gmail.com"
    phone: str = "8861639284"
    location: str = "Hassan, Karnataka, India"
    work_preference: str = "100% Online / Remote / Work From Home (WFH) Only"
    github: str = "https://github.com/varunms89"
    linkedin: str = "https://www.linkedin.com/in/varun-m-s-8861639284"
    degree: str = "Bachelor of Computer Applications (BCA) - Final Year"
    puc_12th: str = "12th Standard / Pre-University (Commerce)"
    graduation_year: str = "2025"
    college: str = "Government Science College (GSC), Hassan"
    experience_level: str = "Fresher / Final Year Student / Intern"
    roles_targeted: List[str] = field(default_factory=lambda: [
        "Software Tester",
        "QA Intern / QA Engineer",
        "Manual Tester",
        "Quality Assurance Analyst",
        "AI Intern / AI Engineer Intern",
        "Machine Learning Intern",
        "Python Developer Intern",
        "Software Engineering Intern",
        "Programming Intern (Python / Web / C++)",
        "Technical Support Engineer",
        "Application Support Analyst",
        "Graduate Trainee"
    ])
    skills: List[str] = field(default_factory=lambda: [
        "Software Testing & QA",
        "Manual Testing & Bug Tracking",
        "Python Programming",
        "Artificial Intelligence (AI) & Machine Learning Tools",
        "App Development",
        "SQL & Database Queries",
        "Postman & API Testing Basics",
        "Git & GitHub",
        "Troubleshooting & Problem Solving"
    ])
    bio: str = "Final Year BCA student actively targeting 100% Online / Remote / Work From Home internships and entry-level roles in Software Testing / QA, AI, and Python programming."

USER_CONFIG = UserProfile()
