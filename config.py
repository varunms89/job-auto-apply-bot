import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class UserProfile:
    name: str = "VARUN M S"
    email: str = "msvarun89@gmail.com"
    phone: str = "8861639284"
    location: str = "Hassan, Karnataka, India"
    work_preference: str = "Remote / Work From Home & Bangalore / Karnataka Hybrid / On-site"
    github: str = "https://github.com/varunms89"
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
        "Technical Support Engineer",
        "Application Support Analyst",
        "QA Support Trainee",
        "Junior Python / Web Trainee",
        "Graduate Trainee"
    ])
    skills: List[str] = field(default_factory=lambda: [
        "Software Testing",
        "Manual Testing",
        "QA Testing & Test Execution",
        "Bug Tracking & Reporting",
        "JIRA",
        "Postman (API Testing Basics)",
        "Technical Support / Troubleshooting",
        "Python",
        "SQL Basics",
        "AI / ML Tools"
    ])
    bio: str = "Final Year BCA student actively applying for Software Tester / QA roles and allied entry-level technical roles (Tech Support, Application Support, Trainee) across Remote / WFH and Bangalore / Karnataka."

USER_CONFIG = UserProfile()
