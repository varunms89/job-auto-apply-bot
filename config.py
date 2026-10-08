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
    work_preference: str = "Work From Home (WFH) / Remote"
    github: str = "https://github.com/varunms89"
    degree: str = "Bachelor of Computer Applications (BCA) - Final Year"
    puc_12th: str = "12th Standard / Pre-University (Commerce)"
    graduation_year: str = "2025"
    college: str = "Government Science College (GSC), Hassan"
    experience_level: str = "Fresher / Final Year Student / Intern"
    roles_targeted: List[str] = field(default_factory=lambda: [
        "Software Tester (Work From Home)",
        "Remote Software Tester",
        "QA Tester (WFH / Remote)",
        "Manual Tester (Work From Home)",
        "Remote QA Intern",
        "Remote Quality Assurance Tester"
    ])
    skills: List[str] = field(default_factory=lambda: [
        "Software Testing",
        "Manual Testing",
        "Remote QA Testing",
        "Test Cases Design & Execution",
        "Bug Tracking & Reporting",
        "JIRA",
        "Postman (API Testing Basics)",
        "Python",
        "AI / ML Tools"
    ])
    bio: str = "Final Year BCA student dedicated strictly to Software Tester roles working remotely (Work From Home). Strong foundation in manual testing, bug tracking, and test execution."

USER_CONFIG = UserProfile()
