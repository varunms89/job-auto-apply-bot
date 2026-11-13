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
    bio: str = "Final Year BCA student passionate about Software Testing / QA, AI internships, and Python/software engineering internships across Remote / WFH and Bangalore / Karnataka."

USER_CONFIG = UserProfile()
