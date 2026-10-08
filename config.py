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
    github: str = "https://github.com/varunms89"
    degree: str = "Bachelor of Computer Applications (BCA) - Final Year"
    puc_12th: str = "12th Standard / Pre-University (Commerce)"
    graduation_year: str = "2025"
    college: str = "Government Science College (GSC), Hassan"
    experience_level: str = "Fresher / Final Year Student / Intern"
    roles_targeted: List[str] = field(default_factory=lambda: [
        "Software Tester",
        "QA Intern",
        "QA Engineer",
        "Quality Assurance Tester",
        "Manual Tester",
        "Automation Tester",
        "Junior QA Analyst",
        "QA Trainee",
        "Graduate Engineer Trainee - QA"
    ])
    skills: List[str] = field(default_factory=lambda: [
        "Software Testing",
        "Manual Testing",
        "Test Cases Design",
        "Bug Reporting",
        "QA Testing",
        "AI / ML Tools",
        "Python",
        "App Development",
        "SDLC / STLC Basics"
    ])
    bio: str = "Computer applications student (BCA) looking for first work experience in QA / Software Testing / Entry-level Software Development. Passionate about AI skills, apps, and bug tracking."

USER_CONFIG = UserProfile()
