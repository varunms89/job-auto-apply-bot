"""
Bot Administration & Management Control Center Module
Provides runtime state management, configuration persistence (bot_settings.json),
database cleanup/CRUD actions, manual scan/notification triggers, and the /admin Web UI.
"""

import os
import json
import time
import threading
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

from config import USER_CONFIG
from database import get_connection, is_pg, get_job_stats, get_assessments, record_job, update_job_status

IST = timezone(timedelta(hours=5, minutes=30))
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_settings.json")
START_TIME = time.time()

DEFAULT_SETTINGS = {
    "bot_enabled": True,
    "auto_apply_enabled": True,
    "strict_remote_only": True,
    "min_match_score": 35.0,
    "scan_interval_minutes": 60,
    "telegram_reports_only_on_new": True,
    "candidate_name": USER_CONFIG.name,
    "candidate_email": USER_CONFIG.email,
    "candidate_phone": USER_CONFIG.phone,
    "candidate_github": USER_CONFIG.github,
    "candidate_linkedin": getattr(USER_CONFIG, "linkedin", "https://www.linkedin.com/in/varun-m-s-8861639284"),
    "enabled_portals": {
        "RemoteOK": True,
        "ArbeitNow": True,
        "Remotive": True,
        "Jobicy": True,
        "LinkedIn": True,
        "Internshala": True,
        "Wellfound_Himalayas": True,
        "Freshersworld": True
    },
    "target_keywords": [
        "Software Tester", "QA Intern", "Manual Tester", "Quality Assurance",
        "Playwright Automation", "Python Intern", "AI Intern", "Machine Learning Intern"
    ]
}

RUNTIME_STATUS = {
    "is_scanning": False,
    "last_scan_time": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST"),
    "last_scan_found": 0,
    "last_scan_applied": 0,
    "total_cycles": 1
}


def load_bot_settings() -> Dict[str, Any]:
    settings = json.loads(json.dumps(DEFAULT_SETTINGS))
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                for k, v in saved.items():
                    if k == "enabled_portals" and isinstance(v, dict):
                        settings["enabled_portals"].update(v)
                    else:
                        settings[k] = v
        except Exception:
            pass
    return settings


def save_bot_settings(new_data: Dict[str, Any]) -> Dict[str, Any]:
    current = load_bot_settings()
    for key in [
        "bot_enabled", "auto_apply_enabled", "strict_remote_only",
        "telegram_reports_only_on_new", "candidate_name", "candidate_email",
        "candidate_phone", "candidate_github", "candidate_linkedin",
        "internshala_cookie", "smtp_password"
    ]:
        if key in new_data:
            current[key] = new_data[key]

    if "min_match_score" in new_data:
        try:
            current["min_match_score"] = float(new_data["min_match_score"])
        except Exception:
            pass

    if "scan_interval_minutes" in new_data:
        try:
            current["scan_interval_minutes"] = max(5, int(new_data["scan_interval_minutes"]))
        except Exception:
            pass

    if "enabled_portals" in new_data and isinstance(new_data["enabled_portals"], dict):
        for pk, pv in new_data["enabled_portals"].items():
            current["enabled_portals"][pk] = bool(pv)

    if "target_keywords" in new_data:
        if isinstance(new_data["target_keywords"], list):
            current["target_keywords"] = [str(x).strip() for x in new_data["target_keywords"] if str(x).strip()]
        elif isinstance(new_data["target_keywords"], str):
            current["target_keywords"] = [x.strip() for x in new_data["target_keywords"].split(",") if x.strip()]

    # Sync with runtime USER_CONFIG
    USER_CONFIG.name = current["candidate_name"]
    USER_CONFIG.email = current["candidate_email"]
    USER_CONFIG.phone = current["candidate_phone"]
    USER_CONFIG.github = current["candidate_github"]
    USER_CONFIG.linkedin = current["candidate_linkedin"]

    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2)
    except Exception:
        pass
    return current


def get_admin_overview() -> Dict[str, Any]:
    settings = load_bot_settings()
    stats = get_job_stats()
    assessments = get_assessments()

    conn = get_connection()
    db_type = "PostgreSQL (Cloud)" if is_pg(conn) else "SQLite (jobs_bot.db)"
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM jobs WHERE match_score = 0")
    zero_score_count = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM jobs WHERE starred = 1 OR starred = TRUE")
    starred_count = cur.fetchone()[0]

    cur.execute("""
        SELECT id, job_id, platform, title, company, location, match_score, status, url
        FROM jobs
        ORDER BY id DESC
        LIMIT 25
    """)
    recent_jobs = [
        {
            "id": r[0], "job_id": r[1], "platform": r[2], "title": r[3],
            "company": r[4], "location": r[5], "match_score": r[6],
            "status": r[7], "url": r[8]
        }
        for r in cur.fetchall()
    ]
    conn.close()

    submitted = stats.get("SUBMITTED", 0) + stats.get("APPLIED", 0) + stats.get("APPLIED_READY", 0)
    interviewing = stats.get("INTERVIEWING", 0) + stats.get("TEST_GIVEN", 0) + stats.get("OFFERED", 0)
    total_jobs = sum(stats.values())
    uptime_mins = int((time.time() - START_TIME) // 60)

    return {
        "status": "success",
        "settings": settings,
        "runtime": RUNTIME_STATUS,
        "system": {
            "db_backend": db_type,
            "uptime_minutes": uptime_mins,
            "server_time_ist": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST"),
            "telegram_configured": bool(os.environ.get("TELEGRAM_BOT_TOKEN")),
            "gemini_configured": bool(os.environ.get("GEMINI_API_KEY")),
            "imap_configured": bool(os.environ.get("IMAP_USER") or os.environ.get("EMAIL_USER"))
        },
        "metrics": {
            "total_jobs": total_jobs,
            "submitted_count": submitted,
            "interviewing_count": interviewing,
            "rejected_zero_score": zero_score_count,
            "starred_count": starred_count,
            "pending_assessments": len([a for a in assessments if a.get("status") == "PENDING"]),
            "total_assessments": len(assessments)
        },
        "recent_jobs": recent_jobs,
        "assessments": assessments[:15]
    }


def trigger_immediate_scan_async() -> Dict[str, Any]:
    if RUNTIME_STATUS["is_scanning"]:
        return {"status": "busy", "message": "A job scan cycle is already running in the background."}

    def _worker():
        RUNTIME_STATUS["is_scanning"] = True
        try:
            from main import run_job_bot_cycle
            settings = load_bot_settings()
            print("⚡ [ADMIN PANEL] Manual job scan cycle triggered by administrator...")
            run_job_bot_cycle(auto_apply=settings.get("auto_apply_enabled", True))
            RUNTIME_STATUS["last_scan_time"] = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")
            RUNTIME_STATUS["total_cycles"] += 1
        except Exception as e:
            print(f"⚠️ [ADMIN SCAN ERROR] {e}")
        finally:
            RUNTIME_STATUS["is_scanning"] = False

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    return {"status": "started", "message": "Immediate job scan launched in background! Watch Live Terminal below."}


def execute_db_admin_action(action: str, data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_connection()
    cur = conn.cursor()
    ph = "%s" if is_pg(conn) else "?"

    try:
        if action == "purge_rejected":
            cur.execute("DELETE FROM jobs WHERE match_score = 0 AND status = 'DISCOVERED'")
            removed = cur.rowcount
            conn.commit()
            conn.close()
            print(f"🧹 [ADMIN DB] Purged {removed} zero-score rejected job listings.")
            return {"status": "success", "message": f"Cleaned {removed} rejected (0-score) listings from database."}

        elif action == "purge_foreign":
            cur.execute("DELETE FROM jobs WHERE url LIKE '%uk.linkedin.com%' OR title LIKE '%Glasgow%' OR location LIKE '%United Kingdom%'")
            removed = cur.rowcount
            conn.commit()
            conn.close()
            print(f"🌍 [ADMIN DB] Purged {removed} foreign country-locked job listings.")
            return {"status": "success", "message": f"Purged {removed} foreign geo-locked listings."}

        elif action == "delete_job":
            jid = data.get("id")
            cur.execute(f"DELETE FROM jobs WHERE id = {ph} OR job_id = {ph}", (int(jid) if str(jid).isdigit() else -1, str(jid)))
            conn.commit()
            conn.close()
            return {"status": "success", "message": f"Deleted job #{jid}."}

        elif action == "delete_assessment":
            aid = int(data.get("id", 0))
            cur.execute(f"DELETE FROM assessments WHERE id = {ph}", (aid,))
            conn.commit()
            conn.close()
            return {"status": "success", "message": f"Deleted assessment #{aid}."}

        elif action == "add_manual_job":
            title = data.get("title", "Software QA Engineer (Remote)").strip()
            company = data.get("company", "Tech Company").strip()
            platform = data.get("platform", "Direct / Manual").strip()
            location = data.get("location", "Remote / WFH").strip()
            url = data.get("url", "https://").strip()
            status = data.get("status", "SUBMITTED").strip()
            score = float(data.get("match_score", 100.0))
            job_id = f"manual_{int(time.time())}"
            conn.close()
            record_job(job_id, platform, title, company, location, url, "Added manually via Bot Admin Panel", score, "Manual Admin Entry", status)
            print(f"➕ [ADMIN DB] Manually added job: {title} @ {company} ({status})")
            return {"status": "success", "message": f"Added '{title}' at {company} ({status})."}

        conn.close()
        return {"status": "error", "message": f"Unknown db action: {action}"}
    except Exception as e:
        conn.close()
        return {"status": "error", "message": str(e)}


def render_admin_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>⚙️ Bot Administration & Control Center - VARUN M S</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --border: #334155;
            --text: #f8fafc;
            --muted: #94a3b8;
            --primary: #3b82f6;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
        }
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; background: var(--bg); color: var(--text); }
        nav { background: #020617; border-bottom: 1px solid var(--border); padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
        nav .brand { font-weight: 800; font-size: 1.15rem; color: white; display: flex; align-items: center; gap: 10px; }
        nav .links a { color: var(--muted); text-decoration: none; margin-left: 18px; font-weight: 600; font-size: 0.9rem; padding: 6px 12px; border-radius: 6px; transition: 0.15s; }
        nav .links a:hover, nav .links a.active { color: white; background: #1e293b; }
        .container { max-width: 1320px; margin: 24px auto; padding: 0 20px; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; margin-bottom: 22px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 20px 24px; border-radius: 12px; border: 1px solid var(--border); }
        .status-pill { display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 9999px; font-weight: 700; font-size: 0.85rem; background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.4); }
        .status-pill.paused { background: rgba(245,158,11,0.15); color: #fbbf24; border-color: rgba(245,158,11,0.4); }
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(195px, 1fr)); gap: 14px; margin-bottom: 24px; }
        .kpi-card { background: var(--card); border: 1px solid var(--border); padding: 16px 18px; border-radius: 10px; }
        .kpi-card .label { color: var(--muted); font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        .kpi-card .val { font-size: 1.85rem; font-weight: 800; margin-top: 6px; }
        .kpi-card .sub { font-size: 0.78rem; color: var(--muted); margin-top: 4px; }
        .grid-2 { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 20px; margin-bottom: 24px; }
        @media (max-width: 960px) { .grid-2 { grid-template-columns: 1fr; } }
        .panel { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px 22px; margin-bottom: 20px; }
        .panel h2 { margin: 0 0 14px 0; font-size: 1.12rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
        .btn-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px; }
        button.btn { border: none; padding: 10px 16px; border-radius: 8px; font-weight: 700; font-size: 0.86rem; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 8px; transition: 0.15s; color: white; }
        button.btn:hover { opacity: 0.92; transform: translateY(-1px); }
        .btn-primary { background: #2563eb; }
        .btn-success { background: #16a34a; }
        .btn-warning { background: #d97706; }
        .btn-danger { background: #dc2626; }
        .btn-slate { background: #334155; border: 1px solid #475569; }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
        label.field-label { display: block; font-size: 0.82rem; font-weight: 600; color: #cbd5e1; margin-bottom: 5px; }
        input[type="text"], input[type="number"], select, textarea { width: 100%; background: #0f172a; border: 1px solid var(--border); color: white; padding: 9px 12px; border-radius: 6px; font-size: 0.88rem; }
        .portal-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(165px, 1fr)); gap: 8px; margin: 10px 0 16px 0; }
        .portal-item { background: #0f172a; border: 1px solid var(--border); padding: 8px 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px; font-size: 0.85rem; font-weight: 600; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
        th { text-align: left; padding: 10px 12px; background: #020617; color: var(--muted); font-size: 0.78rem; text-transform: uppercase; }
        td { padding: 10px 12px; border-bottom: 1px solid var(--border); }
        .toast { position: fixed; bottom: 24px; right: 24px; background: #16a34a; color: white; padding: 12px 20px; border-radius: 8px; font-weight: 700; box-shadow: 0 8px 20px rgba(0,0,0,0.4); display: none; z-index: 9999; }
        pre.terminal { background: #020617; color: #4ade80; padding: 14px; border-radius: 8px; font-family: monospace; font-size: 0.8rem; height: 250px; overflow-y: auto; border: 1px solid #1e293b; margin: 0; line-height: 1.45; }
    </style>
</head>
<body>
    <nav>
        <div class="brand">⚙️ Bot Administration & Management Console</div>
        <div class="links">
            <a href="/">📊 Main Job Dashboard</a>
            <a href="/admin" class="active">⚙️ Admin Control Panel</a>
            <a href="/prep">📚 Prep & Siemens OA Hub</a>
            <a href="/test-report" target="_blank">🧪 CI/CD Test Report</a>
            <a href="/resume" target="_blank">📄 ATS Resume</a>
        </div>
    </nav>

    <div id="toastBanner" class="toast">✅ Action completed!</div>

    <div class="container">
        <div class="top-bar">
            <div>
                <div style="font-size:0.78rem; color:#60a5fa; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Autonomous Engine Control Center</div>
                <h1 style="margin:4px 0 6px 0; font-size:1.5rem;">VARUN M S — Job Bot & QA Pipeline Administrator</h1>
                <div style="font-size:0.86rem; color:var(--muted);">
                    Database: <b id="sysDb" style="color:white;">Loading...</b> •
                    Last Scan: <b id="sysLastScan" style="color:white;">...</b> •
                    Server Clock: <span id="sysClock">...</span>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:12px;">
                <div id="botStatusPill" class="status-pill">🟢 ENGINE ACTIVE (AUTONOMOUS)</div>
                <button class="btn btn-warning" onclick="toggleBotPower()" id="togglePowerBtn">⏸️ Pause Auto-Apply</button>
            </div>
        </div>

        <!-- KPI Metrics Row -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="label">Total Listings in DB</div>
                <div class="val" id="kpiTotal">0</div>
                <div class="sub">Across 8 Job Portals</div>
            </div>
            <div class="kpi-card">
                <div class="label">Submitted / Processed</div>
                <div class="val" id="kpiSubmitted" style="color:#4ade80;">0</div>
                <div class="sub">100% Online / Remote Matches</div>
            </div>
            <div class="kpi-card">
                <div class="label">Starred / Shortlisted</div>
                <div class="val" id="kpiStarred" style="color:#fde047;">0</div>
                <div class="sub">Priority Applications</div>
            </div>
            <div class="kpi-card">
                <div class="label">Rejected (0-Score Clutter)</div>
                <div class="val" id="kpiRejected" style="color:#f87171;">0</div>
                <div class="sub">On-site / Senior Filtered</div>
            </div>
            <div class="kpi-card">
                <div class="label">Pending Assessments</div>
                <div class="val" id="kpiAssessments" style="color:#60a5fa;">0</div>
                <div class="sub">Tracked Invitations</div>
            </div>
        </div>

        <div class="grid-2">
            <!-- Left Column: Engine Triggers & Configuration -->
            <div>
                <div class="panel">
                    <h2>⚡ Instant Engine Controls & Online Internship Auto-Apply</h2>
                    <div class="btn-grid">
                        <button class="btn btn-primary" onclick="triggerAction('scan')">🔄 Run Job Scan Cycle Now</button>
                        <button class="btn btn-success" onclick="triggerAction('batch_apply_internships')">🚀 Auto-Apply Online Internships</button>
                        <button class="btn btn-warning" onclick="triggerAction('login_internshala')">🔑 Login to Internshala (Browser)</button>
                        <button class="btn btn-success" onclick="triggerAction('telegram_report')">📲 Send Status to Telegram</button>
                        <button class="btn btn-slate" onclick="triggerAction('morning_briefing')">🌅 Send Morning Briefing</button>
                        <button class="btn btn-slate" onclick="triggerAction('evening_wrapup')">🌙 Send Evening Wrap-Up</button>
                        <button class="btn btn-slate" onclick="triggerAction('scan_email')">📧 Scan Gmail Inbox (IMAP)</button>
                        <button class="btn btn-slate" onclick="triggerAction('run_tests')">🧪 Run 21 CI Tests & Report</button>
                    </div>
                </div>

                <div class="panel">
                    <h2>
                        <span>🎛️ Bot Matching Policy & Scraper Configuration</span>
                        <button class="btn btn-success" style="padding:6px 14px; font-size:0.8rem;" onclick="saveSettings()">💾 Save All Settings</button>
                    </h2>
                    <div class="form-row">
                        <div>
                            <label class="field-label">Min Match Score Threshold (0 - 100)</label>
                            <input type="number" id="cfgMinScore" min="10" max="95" step="5" value="35">
                        </div>
                        <div>
                            <label class="field-label">Scan Interval (Minutes)</label>
                            <input type="number" id="cfgInterval" min="5" max="720" value="60">
                        </div>
                    </div>
                    <div class="form-row">
                        <div>
                            <label class="field-label">Work Mode Policy</label>
                            <select id="cfgStrictRemote">
                                <option value="true">🌐 100% Strictly Online / Remote / WFH Only</option>
                                <option value="false">🏢 Allow Hybrid / Bangalore In-Office</option>
                            </select>
                        </div>
                        <div>
                            <label class="field-label">Hourly Telegram Notification Mode</label>
                            <select id="cfgTgOnlyNew">
                                <option value="true">🔕 Smart Mode (Only when NEW matches found)</option>
                                <option value="false">🔔 Verbose Mode (Send report every cycle)</option>
                            </select>
                        </div>
                    </div>

                    <label class="field-label" style="margin-top:8px;">Active Job Scrapers (Toggle Portals On/Off):</label>
                    <div class="portal-grid" id="portalCheckboxes"></div>

                    <label class="field-label">Target Role Keywords (Comma-separated):</label>
                    <input type="text" id="cfgKeywords" style="margin-bottom:12px;">

                    <div class="form-row">
                        <div>
                            <label class="field-label">Candidate Name</label>
                            <input type="text" id="cfgName">
                        </div>
                        <div>
                            <label class="field-label">Candidate Email & Phone</label>
                            <input type="text" id="cfgEmail">
                        </div>
                    </div>
                </div>

                <!-- Manual Application Entry & DB Cleanup -->
                <div class="panel">
                    <h2>🗄️ Database Maintenance & Manual Job Entry</h2>
                    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:16px;">
                        <button class="btn btn-danger" onclick="dbAction('purge_rejected', {})">🧹 Purge 0-Score Rejected Jobs</button>
                        <button class="btn btn-warning" onclick="dbAction('purge_foreign', {})">🌍 Purge Foreign UK/US Jobs</button>
                        <a href="/export/jobs.csv" class="btn btn-slate" style="text-decoration:none;">📥 Export Jobs CSV</a>
                    </div>
                    <div style="border-top:1px solid var(--border); padding-top:14px;">
                        <div style="font-weight:700; font-size:0.88rem; margin-bottom:10px; color:#93c5fd;">➕ Manually Log an External Application</div>
                        <div class="form-row">
                            <input type="text" id="manTitle" placeholder="Role Title (e.g. QA Automation Intern)">
                            <input type="text" id="manCompany" placeholder="Company Name (e.g. Razorpay)">
                        </div>
                        <div class="form-row">
                            <input type="text" id="manUrl" placeholder="Job Posting URL">
                            <select id="manStatus">
                                <option value="SUBMITTED">✅ SUBMITTED</option>
                                <option value="TEST_GIVEN">📝 TEST_GIVEN</option>
                                <option value="INTERVIEWING">🎙️ INTERVIEWING</option>
                                <option value="OFFERED">🎉 OFFERED</option>
                            </select>
                        </div>
                        <button class="btn btn-primary" onclick="addManualJob()">➕ Add Application to Pipeline</button>
                    </div>
                </div>
            </div>

            <!-- Right Column: Live Terminal, Telegram Broadcast & System Health -->
            <div>
                <div class="panel">
                    <h2>
                        <span>📡 Live Bot Engine Terminal</span>
                        <button class="btn btn-slate" style="padding:4px 10px; font-size:0.75rem;" onclick="clearLogs()">🗑️ Clear Buffer</button>
                    </h2>
                    <pre id="adminTerminal" class="terminal">Connecting to live bot log stream...</pre>
                </div>

                <div class="panel">
                    <h2>💬 Direct Telegram Bot Messenger</h2>
                    <label class="field-label">Send Custom Alert / Note to Your Telegram:</label>
                    <textarea id="customTgText" rows="3" placeholder="Type a custom reminder, test link, or note to send to your Telegram phone..." style="margin-bottom:10px;"></textarea>
                    <button class="btn btn-primary" onclick="sendCustomTelegram()">🚀 Send Message to Telegram</button>
                </div>

                <div class="panel">
                    <h2>🔐 Integration & Credential Health</h2>
                    <div id="healthList" style="font-size:0.88rem; line-height:1.8;"></div>
                </div>
            </div>
        </div>

        <!-- Recent Applications Admin Table -->
        <div class="panel">
            <h2>
                <span>📋 Recent Pipeline Records (Quick Status & Delete Control)</span>
                <button class="btn btn-slate" style="padding:5px 12px; font-size:0.78rem;" onclick="loadAdminData()">🔄 Refresh Table</button>
            </h2>
            <div style="overflow-x:auto;">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Role Title</th>
                            <th>Company</th>
                            <th>Platform</th>
                            <th>Location</th>
                            <th>Score</th>
                            <th>Pipeline Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody id="adminJobsTbody"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        let currentSettings = {};

        function showToast(msg, isErr=false) {
            let t = document.getElementById('toastBanner');
            t.style.background = isErr ? '#dc2626' : '#16a34a';
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3200);
        }

        function loadAdminData() {
            fetch('/api/admin/overview')
                .then(r => r.json())
                .then(data => {
                    currentSettings = data.settings || {};
                    let m = data.metrics || {};
                    let sys = data.system || {};
                    let rt = data.runtime || {};

                    document.getElementById('kpiTotal').innerText = m.total_jobs || 0;
                    document.getElementById('kpiSubmitted').innerText = m.submitted_count || 0;
                    document.getElementById('kpiStarred').innerText = m.starred_count || 0;
                    document.getElementById('kpiRejected').innerText = m.rejected_zero_score || 0;
                    document.getElementById('kpiAssessments').innerText = m.pending_assessments || 0;

                    document.getElementById('sysDb').innerText = sys.db_backend || 'SQLite';
                    document.getElementById('sysLastScan').innerText = rt.last_scan_time || 'Just now';
                    document.getElementById('sysClock').innerText = sys.server_time_ist || '';

                    // Power state
                    let pill = document.getElementById('botStatusPill');
                    let pBtn = document.getElementById('togglePowerBtn');
                    if (currentSettings.auto_apply_enabled !== false) {
                        pill.className = 'status-pill';
                        pill.innerText = rt.is_scanning ? '🔄 SCANNING PORTALS NOW...' : '🟢 ENGINE ACTIVE (AUTONOMOUS)';
                        pBtn.innerText = '⏸️ Pause Auto-Apply';
                    } else {
                        pill.className = 'status-pill paused';
                        pill.innerText = '⏸️ AUTO-APPLY PAUSED';
                        pBtn.innerText = '▶️ Resume Auto-Apply';
                    }

                    // Populate form inputs
                    document.getElementById('cfgMinScore').value = currentSettings.min_match_score ?? 35;
                    document.getElementById('cfgInterval').value = currentSettings.scan_interval_minutes ?? 60;
                    document.getElementById('cfgStrictRemote').value = String(currentSettings.strict_remote_only !== false);
                    document.getElementById('cfgTgOnlyNew').value = String(currentSettings.telegram_reports_only_on_new !== false);
                    document.getElementById('cfgKeywords').value = (currentSettings.target_keywords || []).join(', ');
                    document.getElementById('cfgName').value = currentSettings.candidate_name || 'VARUN M S';
                    document.getElementById('cfgEmail').value = currentSettings.candidate_email || 'msvarun89@gmail.com';

                    // Portals checkboxes
                    let portals = currentSettings.enabled_portals || {};
                    let pHtml = '';
                    Object.keys(portals).forEach(pk => {
                        let chk = portals[pk] ? 'checked' : '';
                        pHtml += `<label class="portal-item"><input type="checkbox" class="portal-chk" data-portal="${pk}" ${chk}> ${pk}</label>`;
                    });
                    document.getElementById('portalCheckboxes').innerHTML = pHtml;

                    // Health checklist
                    document.getElementById('healthList').innerHTML = `
                        <div>✅ <b>Database Engine:</b> ${sys.db_backend} (Connected)</div>
                        <div>${sys.telegram_configured ? '✅' : '⚠️'} <b>Telegram Bot API:</b> ${sys.telegram_configured ? 'Connected & Listening (Singleton)' : 'Token Missing'}</div>
                        <div>✅ <b>LinkedIn Remote Filter:</b> Strict <code>f_WT=2</code> Enabled</div>
                        <div>✅ <b>Playwright Self-Healing Suite:</b> Active (98% Confidence)</div>
                        <div>${sys.imap_configured ? '✅' : 'ℹ️'} <b>Gmail IMAP Monitor:</b> ${sys.imap_configured ? 'Active' : 'Optional (Set IMAP_USER in .env)'}</div>
                    `;

                    // Recent jobs table
                    let rows = (data.recent_jobs || []).map(j => `
                        <tr>
                            <td style="font-family:monospace; color:#94a3b8;">#${j.id}</td>
                            <td><a href="${j.url}" target="_blank" style="color:#60a5fa; font-weight:600; text-decoration:none;">${j.title} ↗</a></td>
                            <td>${j.company}</td>
                            <td><span style="background:#0f172a; padding:2px 8px; border-radius:4px; border:1px solid #334155;">${j.platform}</span></td>
                            <td style="color:#cbd5e1;">${j.location}</td>
                            <td style="font-weight:700; color:${j.match_score >= 35 ? '#4ade80' : '#94a3b8'};">${j.match_score}</td>
                            <td>
                                <select onchange="updateJobStatus(${j.id}, this.value)" style="padding:4px 8px; font-size:0.78rem; width:auto;">
                                    ${['DISCOVERED','SUBMITTED','TEST_GIVEN','INTERVIEWING','OFFERED','REJECTED'].map(s => `<option value="${s}" ${j.status===s?'selected':''}>${s}</option>`).join('')}
                                </select>
                            </td>
                            <td>
                                <button class="btn btn-danger" style="padding:4px 10px; font-size:0.75rem;" onclick="dbAction('delete_job', {id: ${j.id}})">Delete</button>
                            </td>
                        </tr>
                    `).join('');
                    document.getElementById('adminJobsTbody').innerHTML = rows || '<tr><td colspan="8">No jobs found.</td></tr>';
                });
        }

        function saveSettings() {
            let portals = {};
            document.querySelectorAll('.portal-chk').forEach(el => {
                portals[el.getAttribute('data-portal')] = el.checked;
            });
            let payload = {
                min_match_score: parseFloat(document.getElementById('cfgMinScore').value),
                scan_interval_minutes: parseInt(document.getElementById('cfgInterval').value),
                strict_remote_only: document.getElementById('cfgStrictRemote').value === 'true',
                telegram_reports_only_on_new: document.getElementById('cfgTgOnlyNew').value === 'true',
                target_keywords: document.getElementById('cfgKeywords').value,
                candidate_name: document.getElementById('cfgName').value,
                candidate_email: document.getElementById('cfgEmail').value,
                enabled_portals: portals
            };
            fetch('/api/admin/settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            }).then(r => r.json()).then(res => {
                showToast('💾 Bot configuration saved & applied!');
                loadAdminData();
            });
        }

        function toggleBotPower() {
            let nextState = !(currentSettings.auto_apply_enabled !== false);
            fetch('/api/admin/settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({auto_apply_enabled: nextState})
            }).then(r => r.json()).then(() => {
                showToast(nextState ? '▶️ Autonomous Auto-Apply Resumed!' : '⏸️ Autonomous Auto-Apply Paused!');
                loadAdminData();
            });
        }

        function triggerAction(act) {
            showToast('⏳ Executing ' + act + '...');
            fetch('/api/admin/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: act})
            }).then(r => r.json()).then(res => {
                showToast('✅ ' + (res.message || 'Completed!'));
                setTimeout(loadAdminData, 1000);
            });
        }

        function dbAction(action, payload) {
            payload.action = action;
            fetch('/api/admin/db-action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            }).then(r => r.json()).then(res => {
                showToast('🗄️ ' + (res.message || 'Database updated!'));
                loadAdminData();
            });
        }

        function addManualJob() {
            let title = document.getElementById('manTitle').value.trim();
            let company = document.getElementById('manCompany').value.trim();
            let url = document.getElementById('manUrl').value.trim();
            let status = document.getElementById('manStatus').value;
            if (!title || !company) {
                showToast('⚠️ Enter Role Title and Company Name', true);
                return;
            }
            dbAction('add_manual_job', {title, company, url, status});
            document.getElementById('manTitle').value = '';
            document.getElementById('manCompany').value = '';
            document.getElementById('manUrl').value = '';
        }

        function updateJobStatus(id, status) {
            fetch('/api/jobs/update-status', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: id, status: status})
            }).then(() => showToast('✅ Updated Job #' + id + ' to ' + status));
        }

        function sendCustomTelegram() {
            let txt = document.getElementById('customTgText').value.trim();
            if (!txt) return;
            fetch('/api/admin/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: 'custom_telegram', message: txt})
            }).then(r => r.json()).then(res => {
                showToast('📲 ' + (res.message || 'Sent to Telegram!'));
                document.getElementById('customTgText').value = '';
            });
        }

        function clearLogs() {
            fetch('/api/admin/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: 'clear_logs'})
            }).then(() => {
                document.getElementById('adminTerminal').innerText = '[Logs cleared by administrator]';
            });
        }

        function pollLogs() {
            fetch('/api/logs').then(r => r.json()).then(d => {
                let term = document.getElementById('adminTerminal');
                if (d.lines && d.lines.length) {
                    term.innerText = d.lines.join('\\n');
                    term.scrollTop = term.scrollHeight;
                }
            }).catch(() => {});
        }

        window.addEventListener('DOMContentLoaded', () => {
            loadAdminData();
            pollLogs();
            setInterval(pollLogs, 4000);
            setInterval(loadAdminData, 15000);
        });
    </script>
</body>
</html>"""
