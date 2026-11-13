import os
import json
import threading
from urllib.parse import parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from database import get_connection, get_job_stats, record_assessment, get_assessments, update_assessment_status
from live_bot import run_continuous_live_bot
from prep_assistant import PREP_MODULES, QA_PRACTICE_QUESTIONS, HR_SCREENING_QUESTIONS
from email_monitor import process_email_message
from telegram_notifier import send_assessment_alert

PORT = int(os.environ.get("PORT", 8080))

class HealthCheckAndDashboardHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""

        if parsed_path.path == "/api/assessments":
            # API endpoint to ingest assessment from webhook or form
            try:
                if self.headers.get('Content-Type') == 'application/json':
                    data = json.loads(post_data)
                else:
                    data = {k: v[0] for k, v in parse_qs(post_data).items()}
                
                company = data.get("company", "Tech Company")
                role = data.get("role_title", "Technical Assessment")
                platform = data.get("platform", "Online Portal")
                url = data.get("test_url", "https://mail.google.com")
                deadline = data.get("deadline_or_time", "Within 48 hours")
                topic = data.get("prep_topic", "General")
                notes = data.get("notes", "Submitted via Dashboard / API")

                new_id = record_assessment(company, role, platform, url, deadline, topic, "PENDING", notes)
                
                # Send instant Telegram Alert
                send_assessment_alert(company, role, platform, url, deadline, topic, notes)

                # If from browser form, redirect back to /
                if 'application/json' not in self.headers.get('Content-Type', ''):
                    self.send_response(303)
                    self.send_header('Location', '/')
                    self.end_headers()
                    return

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "id": new_id}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        elif parsed_path.path == "/api/assessments/complete":
            try:
                params = parse_qs(post_data)
                aid = int(params.get("id", [0])[0])
                if aid:
                    update_assessment_status(aid, "COMPLETED")
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
                return
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                return

        elif parsed_path.path == "/api/jobs/update-status":
            try:
                from database import update_job_status
                if self.headers.get('Content-Type') == 'application/json':
                    data = json.loads(post_data)
                else:
                    data = {k: v[0] for k, v in parse_qs(post_data).items()}
                job_id = data.get("id") or data.get("job_id")
                new_status = data.get("status", "SUBMITTED")
                if job_id:
                    update_job_status(job_id, new_status)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "new_status": new_status}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        elif parsed_path.path == "/api/jobs/star":
            try:
                from database import toggle_job_star
                if self.headers.get('Content-Type') == 'application/json':
                    data = json.loads(post_data)
                else:
                    data = {k: v[0] for k, v in parse_qs(post_data).items()}
                job_id = data.get("id") or data.get("job_id")
                new_state = toggle_job_star(job_id) if job_id else False
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "starred": new_state}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path in ["/healthz", "/health"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode("utf-8"))
            return

        if parsed_path.path == "/api/assessments":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            assessments = get_assessments()
            self.wfile.write(json.dumps(assessments).encode("utf-8"))
            return

        if parsed_path.path == "/export/applications.csv":
            import csv
            import io
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, job_id, platform, title, company, location, match_score, status, applied_at, url 
                FROM jobs ORDER BY id DESC;
            """)
            rows = cur.fetchall()
            conn.close()

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["ID", "Job ID", "Platform", "Title", "Company", "Location", "Match Score", "Status", "Applied At", "URL"])
            for r in rows:
                writer.writerow(r)

            csv_data = output.getvalue().encode('utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="varunms_applications_backup.csv"')
            self.end_headers()
            self.wfile.write(csv_data)
            return

        if parsed_path.path == "/resume":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            resume_path = os.path.join(os.path.dirname(__file__), "VARUN_M_S_Resume.html")
            if os.path.exists(resume_path):
                with open(resume_path, "r", encoding="utf-8") as rf:
                    self.wfile.write(rf.read().encode("utf-8"))
            else:
                self.wfile.write(b"<h1>Resume not found.</h1>")
            return

        if parsed_path.path == "/prep":
            # Preparation & Practice Hub
            self.render_prep_hub()
            return

        # Main Dashboard
        self.render_main_dashboard()

    def render_prep_hub(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        qa_sections = "".join([f"<div class='prep-card'><h3>{s['heading']}</h3><div>{s['content']}</div></div>" for s in PREP_MODULES["qa"]["sections"]])
        py_sections = "".join([f"<div class='prep-card'><h3>{s['heading']}</h3><div>{s['content']}</div></div>" for s in PREP_MODULES["python"]["sections"]])
        ai_sections = "".join([f"<div class='prep-card'><h3>{s['heading']}</h3><div>{s['content']}</div></div>" for s in PREP_MODULES["ai"]["sections"]])

        hr_cards = []
        for h in HR_SCREENING_QUESTIONS:
            hr_cards.append(f"""
            <div class='prep-card' style='border-left-color:#0284c7;'>
                <h3 style='color:#0369a1;'>{h['question']}</h3>
                <div style='color:#64748b; font-size:0.85rem; margin-bottom:8px;'><b>Recruiter Intent:</b> {h['intent']}</div>
                <div style='background:#f8fafc; padding:12px; border-radius:6px; border-left:3px solid #0284c7; line-height:1.5;'>
                    <b>🗣️ What You Say:</b><br>
                    \"{h['script']}\"
                </div>
            </div>
            """)
        hr_sections = "".join(hr_cards)

        quiz_cards = []
        for q in QA_PRACTICE_QUESTIONS:
            qid = q["id"]
            opts = "".join([f"<label style='display:block; margin:6px 0; cursor:pointer;'><input type='radio' name='q_{qid}' value='{i}'> {opt}</label>" for i, opt in enumerate(q["options"])])
            quiz_cards.append(f"""
            <div class='prep-card' id='qcard_{qid}' style='border-left-color:#8b5cf6;'>
                <div style='font-weight:600; color:#0f172a; margin-bottom:8px;'>{qid}. {q['question']}</div>
                {opts}
                <div class='explanation' id='expl_{qid}' style='display:none; margin-top:10px; padding:10px; border-radius:6px; font-size:0.88rem; background:#f1f5f9;'>
                    <b>Correct Answer:</b> {q['options'][q['answer']]}<br>
                    <span style='color:#475569;'>💡 {q['explanation']}</span>
                </div>
            </div>
            """)
        quiz_sections = "".join(quiz_cards)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Preparation & Practice Hub - VARUN M S</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; background: #f8fafc; color: #1e293b; }}
                nav {{ background: #0f172a; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }}
                nav a {{ color: #94a3b8; text-decoration: none; margin-left: 20px; font-weight: 500; font-size: 0.95rem; }}
                nav a:hover, nav a.active {{ color: white; text-decoration: underline; }}
                .container {{ max-width: 1100px; margin: 30px auto; padding: 0 20px; }}
                h1 {{ color: #0f172a; margin-bottom: 5px; }}
                .subtitle {{ color: #64748b; margin-bottom: 25px; }}
                .tabs {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
                .tab-btn {{ background: white; border: 1px solid #cbd5e1; padding: 10px 18px; border-radius: 6px; font-weight: 600; cursor: pointer; color: #475569; }}
                .tab-btn.active {{ background: #2563eb; color: white; border-color: #2563eb; }}
                .tab-content {{ display: none; }}
                .tab-content.active {{ display: block; }}
                .prep-card {{ background: white; padding: 20px 25px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin-bottom: 20px; border-left: 4px solid #3b82f6; }}
                .prep-card h3 {{ margin-top: 0; color: #0f172a; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; font-size: 1.15rem; }}
                code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #0f172a; font-family: monospace; }}
                #quiz-score-banner {{ display: none; padding: 15px 20px; border-radius: 8px; font-size: 1.1rem; margin-bottom: 20px; background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; font-weight: 600; text-align: center; }}
            </style>
            <script>
                function switchTab(tabId) {{
                    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                    document.getElementById('tab-' + tabId).classList.add('active');
                    document.getElementById('btn-' + tabId).classList.add('active');
                }}

                const QUIZ_ANSWERS = {{ 1: 1, 2: 2, 3: 2, 4: 1, 5: 1, 6: 2, 7: 1, 8: 2, 9: 1, 10: 2 }};
                function checkQuiz() {{
                    let score = 0;
                    for (let i = 1; i <= 10; i++) {{
                        let selected = document.querySelector('input[name="q_' + i + '"]:checked');
                        let card = document.getElementById('qcard_' + i);
                        let expl = document.getElementById('expl_' + i);
                        expl.style.display = 'block';
                        if (selected && parseInt(selected.value) === QUIZ_ANSWERS[i]) {{
                            score++;
                            card.style.borderLeftColor = '#22c55e';
                            card.style.background = '#f0fdf4';
                        }} else {{
                            card.style.borderLeftColor = '#ef4444';
                            card.style.background = '#fef2f2';
                        }}
                    }}
                    let banner = document.getElementById('quiz-score-banner');
                    banner.style.display = 'block';
                    banner.innerHTML = "🎯 Your Score: <b>" + score + " / 10</b> " + (score >= 8 ? "🎉 Excellent! Ready for QA Screening!" : "💡 Keep reviewing the cheat sheet above!");
                    window.scrollTo({{ top: banner.offsetTop - 50, behavior: 'smooth' }});
                }}
            </script>
        </head>
        <body>
            <nav>
                <div style="font-weight: bold; font-size: 1.1rem;">🤖 Job Bot Hub</div>
                <div>
                    <a href="/">⬅ Back to Job Dashboard</a>
                    <a href="/resume" target="_blank">📄 ATS Resume</a>
                    <a href="/prep" class="active">📚 Preparation & Practice</a>
                    <a href="https://t.me/" target="_blank">📱 Telegram Alerts</a>
                </div>
            </nav>

            <div class="container">
                <h1>📚 Preparation & Practice Assistant</h1>
                <p class="subtitle">Tailored study guides and solved coding questions for <b>VARUN M S</b> (BCA Final Year, 2025)</p>

                <div class="tabs">
                    <button class="tab-btn active" id="btn-qa" onclick="switchTab('qa')">🧪 Software Testing & QA</button>
                    <button class="tab-btn" id="btn-py" onclick="switchTab('py')">🐍 Python & Coding Assessment</button>
                    <button class="tab-btn" id="btn-ai" onclick="switchTab('ai')">🤖 AI & Machine Learning</button>
                    <button class="tab-btn" id="btn-quiz" onclick="switchTab('quiz')">📝 Interactive QA Quiz (10 Qs)</button>
                    <button class="tab-btn" id="btn-hr" onclick="switchTab('hr')">💼 HR Phone Screening Script</button>
                </div>

                <!-- QA Tab -->
                <div class="tab-content active" id="tab-qa">
                    <p style="color: #475569; margin-bottom: 15px;">Focus on test case writing, bug life cycle transitions, severity vs priority, and API status codes.</p>
                    {qa_sections}
                </div>

                <!-- Python Tab -->
                <div class="tab-content" id="tab-py">
                    <p style="color: #475569; margin-bottom: 15px;">Top algorithms and data structures commonly asked in HackerRank, Codility, and technical screening rounds.</p>
                    {py_sections}
                </div>

                <!-- AI Tab -->
                <div class="tab-content" id="tab-ai">
                    <p style="color: #475569; margin-bottom: 15px;">Core ML concepts, data handling in Pandas & NumPy, prompt engineering best practices, and RAG architectures.</p>
                    {ai_sections}
                </div>

                <!-- Quiz Tab -->
                <div class="tab-content" id="tab-quiz">
                    <div id="quiz-score-banner"></div>
                    <p style="color: #475569; margin-bottom: 15px;">Select your answers and click <b>Check Score & Explanations</b> to test your knowledge for recruiter screenings:</p>
                    {quiz_sections}
                    <div style="text-align: center; margin: 30px 0;">
                        <button onclick="checkQuiz()" style="background:#2563eb; color:white; border:none; padding:12px 28px; border-radius:8px; font-size:1rem; font-weight:bold; cursor:pointer;">✅ Check Score & Explanations</button>
                    </div>
                </div>

                <!-- HR Tab -->
                <div class="tab-content" id="tab-hr">
                    <p style="color: #475569; margin-bottom: 15px;">Model answers and recruiter talking points for initial 5-minute phone and video screening calls:</p>
                    {hr_sections}
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def render_main_dashboard(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # 1. Submitted Jobs (including all pipeline stages, starred first)
            cur.execute("""
                SELECT id, title, company, platform, location, match_score, status, url, starred 
                FROM jobs 
                WHERE status IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED', 'TEST_GIVEN', 'INTERVIEWING', 'OFFERED', 'REJECTED') 
                ORDER BY starred DESC, id DESC
            """)
            submitted_jobs = cur.fetchall()

            # 2. Not Submitted (Discovered)
            cur.execute("""
                SELECT id, title, company, platform, location, match_score, match_reasons, url 
                FROM jobs 
                WHERE status NOT IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED', 'TEST_GIVEN', 'INTERVIEWING', 'OFFERED', 'REJECTED') 
                ORDER BY id DESC LIMIT 25
            """)
            not_submitted_jobs = cur.fetchall()

            cur.execute("SELECT count(*) FROM jobs")
            total = cur.fetchone()[0]
            conn.close()
        except Exception:
            submitted_jobs = []
            not_submitted_jobs = []
            total = 0

        # Fetch Assessments
        try:
            assessments = get_assessments()
        except Exception:
            assessments = []

        pending_tests = [a for a in assessments if a["status"] == "PENDING"]
        completed_tests = [a for a in assessments if a["status"] == "COMPLETED"]
        active_interviews = len([r for r in submitted_jobs if r[6] in ('INTERVIEWING', 'OFFERED')])

        # Build Pending Tests Table Rows
        test_rows = []
        for a in pending_tests:
            test_rows.append(f"<tr><td><b>{a['company']}</b></td><td>{a['role_title']}</td><td><span class='badge-platform'>{a['platform']}</span></td><td><b>{a['deadline_or_time']}</b></td><td><code>{a['prep_topic']}</code></td><td><a href='{a['test_url']}' target='_blank' class='btn-take'>Start Test / Join ↗</a></td><td><form method='POST' action='/api/assessments/complete' style='display:inline;'><input type='hidden' name='id' value='{a['id']}'><button type='submit' class='btn-complete'>Mark Done ✓</button></form></td></tr>")
        tests_rows_html = "".join(test_rows) if test_rows else "<tr><td colspan='7' style='text-align:center; color:#64748b; padding:15px;'>No pending test invites right now. Auto-detected email invites or manual additions will appear here instantly!</td></tr>"

        # Build Submitted Jobs Table Rows
        submitted_rows = []
        for idx, r in enumerate(submitted_jobs, 1):
            jid, title, comp, plat, loc, score, status, url, starred = r
            comp_clean = str(comp).replace('"', '').replace("'", "")
            title_clean = str(title).replace('"', '').replace("'", "")
            star_icon = "⭐" if starred else "☆"
            sub_sel = "selected" if status in ('SUBMITTED', 'APPLIED', 'APPLIED_READY') else ""
            tg_sel = "selected" if status == 'TEST_GIVEN' else ""
            int_sel = "selected" if status == 'INTERVIEWING' else ""
            off_sel = "selected" if status == 'OFFERED' else ""
            rej_sel = "selected" if status == 'REJECTED' else ""
            submitted_rows.append(f"""
                <tr>
                    <td style='text-align:center;'><button onclick='toggleStar({jid}, this)' style='background:none; border:none; cursor:pointer; font-size:1.15rem; padding:0;' title='Pin to Top as Dream Company'>{star_icon}</button></td>
                    <td>{idx}</td>
                    <td><b>{title}</b></td>
                    <td>{comp}</td>
                    <td>{plat}</td>
                    <td><b>{score}/100</b></td>
                    <td>
                        <select class='status-select' onchange='changeJobStatus({jid}, this.value)'>
                            <option value='SUBMITTED' {sub_sel}>SUBMITTED</option>
                            <option value='TEST_GIVEN' {tg_sel}>TEST GIVEN</option>
                            <option value='INTERVIEWING' {int_sel}>INTERVIEWING</option>
                            <option value='OFFERED' {off_sel}>OFFERED</option>
                            <option value='REJECTED' {rej_sel}>REJECTED</option>
                        </select>
                    </td>
                    <td><a href='{url}' target='_blank'>View Job ↗</a></td>
                    <td><button class='btn-take' style='background:#0284c7; cursor:pointer; border:none;' onclick='openOutreach("{comp_clean}", "{title_clean}")'>✉️ Outreach</button></td>
                </tr>
            """)
        submitted_rows_html = "".join(submitted_rows) if submitted_rows else "<tr><td colspan='9'>No jobs submitted yet.</td></tr>"

        # Build Not Submitted Jobs Table Rows
        unsub_rows = []
        for idx, r in enumerate(not_submitted_jobs, 1):
            unsub_rows.append(f"<tr><td>{idx}</td><td><b>{r[1]}</b></td><td>{r[2]}</td><td>{r[3]}</td><td><span class='badge-unsub'>{r[6]}</span></td><td><a href='{r[7]}' target='_blank'>View ↗</a></td></tr>")
        unsub_rows_html = "".join(unsub_rows) if unsub_rows else "<tr><td colspan='6'>No unsubmitted jobs.</td></tr>"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Job Auto-Apply Bot - Dashboard</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; background: #f8fafc; color: #1e293b; }}
                nav {{ background: #0f172a; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }}
                nav a {{ color: #94a3b8; text-decoration: none; margin-left: 20px; font-weight: 500; font-size: 0.95rem; }}
                nav a:hover, nav a.active {{ color: white; text-decoration: underline; }}
                .container {{ max-width: 1200px; margin: 30px auto; padding: 0 20px; }}
                h1 {{ color: #0f172a; margin-bottom: 5px; }}
                .subtitle {{ color: #64748b; margin-bottom: 25px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }}
                .stat-card {{ background: white; padding: 15px 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-left: 4px solid #3b82f6; }}
                .stat-card.green {{ border-left-color: #22c55e; }}
                .stat-card.purple {{ border-left-color: #8b5cf6; }}
                .stat-card.red {{ border-left-color: #ef4444; }}
                .stat-card.gray {{ border-left-color: #94a3b8; }}
                .card {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 30px; }}
                .card-alert {{ border: 2px solid #fecaca; background: #fff5f5; }}
                h2 {{ font-size: 1.25rem; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid #f1f5f9; }}
                .tag-alert {{ color: #dc2626; }}
                .tag-submitted {{ color: #15803d; }}
                .tag-unsubmitted {{ color: #b45309; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.92rem; }}
                th, td {{ padding: 12px 14px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
                th {{ background: #f8fafc; color: #475569; font-weight: 600; }}
                tr:hover {{ background: #f8fafc; }}
                .badge-success {{ padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.8rem; background: #dcfce7; color: #166534; }}
                .badge-alert {{ padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.8rem; background: #fee2e2; color: #991b1b; animation: pulse 2s infinite; }}
                .badge-platform {{ padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.75rem; background: #e0e7ff; color: #3730a3; }}
                .badge-unsub {{ padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.8rem; background: #fef3c7; color: #92400e; }}
                .btn-take {{ background: #2563eb; color: white !important; padding: 6px 12px; border-radius: 6px; text-decoration: none !important; font-size: 0.85rem; font-weight: 600; display: inline-block; }}
                .btn-take:hover {{ background: #1d4ed8; }}
                .btn-complete {{ background: #22c55e; color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 0.8rem; font-weight: bold; }}
                .btn-complete:hover {{ background: #16a34a; }}
                .status-select {{ padding: 4px 8px; border-radius: 6px; font-weight: 600; font-size: 0.8rem; border: 1px solid #cbd5e1; cursor: pointer; background: white; }}
                a {{ color: #2563eb; text-decoration: none; font-weight: 500; }}
                a:hover {{ text-decoration: underline; }}
                .quick-add-form {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; background: white; padding: 15px; border-radius: 6px; border: 1px solid #cbd5e1; }}
                .quick-add-form input, .quick-add-form select {{ padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.9rem; flex: 1; min-width: 150px; }}
                .quick-add-form button {{ background: #0f172a; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: 600; cursor: pointer; }}
            </style>
        </head>
        <body>
            <nav>
                <div style="font-weight: bold; font-size: 1.1rem;">🤖 Job Auto-Apply Bot & Test Hub</div>
                <div>
                    <a href="/" class="active">📊 Dashboard</a>
                    <a href="/resume" target="_blank">📄 ATS Resume</a>
                    <a href="/prep">📚 Preparation Hub (QA / Python / AI)</a>
                    <a href="/healthz">🩺 Health Check</a>
                </div>
            </nav>

            <div class="container">
                <h1>🤖 Autonomous Job & Assessment Dashboard</h1>
                <p class="subtitle">Candidate: <b>VARUN M S</b> (BCA Final Year, 2025) &nbsp;|&nbsp; Preference: <b>Online / Remote Internships & Jobs</b></p>
                
                <div class="grid">
                    <div class="stat-card red">
                        <div style="color: #64748b; font-size: 0.85rem;">PENDING TESTS / INTERVIEWS</div>
                        <div style="font-size: 1.8rem; font-weight: bold; color: #dc2626; margin-top: 5px;">{len(pending_tests)}</div>
                    </div>
                    <div class="stat-card green">
                        <div style="color: #64748b; font-size: 0.85rem;">SUBMITTED APPLICATIONS</div>
                        <div style="font-size: 1.8rem; font-weight: bold; color: #15803d; margin-top: 5px;">{len(submitted_jobs)}</div>
                    </div>
                    <div class="stat-card purple">
                        <div style="color: #64748b; font-size: 0.85rem;">INTERVIEWS & OFFERS</div>
                        <div style="font-size: 1.8rem; font-weight: bold; color: #7c3aed; margin-top: 5px;">{active_interviews}</div>
                    </div>
                    <div class="stat-card gray">
                        <div style="color: #64748b; font-size: 0.85rem;">UNSUBMITTED / DISCOVERED</div>
                        <div style="font-size: 1.8rem; font-weight: bold; color: #b45309; margin-top: 5px;">{total - len(submitted_jobs)}</div>
                    </div>
                    <div class="stat-card">
                        <div style="color: #64748b; font-size: 0.85rem;">TOTAL EVALUATED</div>
                        <div style="font-size: 1.8rem; font-weight: bold; color: #1e293b; margin-top: 5px;">{total}</div>
                    </div>
                </div>

                <!-- PART 0: UPCOMING TESTS & ONLINE INTERVIEWS TRACKER -->
                <div class="card card-alert">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #fee2e2; padding-bottom: 10px;">
                        <h2 class="tag-alert" style="margin: 0; border-bottom: none;">🚨 Part 0: Upcoming Tests & Online Sessions Tracker ({len(pending_tests)} Pending)</h2>
                        <a href="/prep" style="font-size: 0.85rem; background: #dc2626; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-weight: 600;">📖 Open Prep Guide</a>
                    </div>
                    <p style="color: #64748b; font-size: 0.88rem; margin-top: 10px;">Detected online assessments (HackerRank, Codility, TestGorilla, Google Meet) and scheduled interview invites.</p>
                    
                    <table>
                        <thead>
                            <tr style="background: #fee2e2;">
                                <th>Company</th><th>Role / Subject</th><th>Platform</th><th>Deadline / Timing</th><th>Topic</th><th>Action</th><th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tests_rows_html}
                        </tbody>
                    </table>

                    <div style="margin-top: 20px;">
                        <h4 style="margin: 0 0 5px 0; color: #334155;">➕ Manually Add Test Link or Interview Invite</h4>
                        <form class="quick-add-form" method="POST" action="/api/assessments">
                            <input type="text" name="company" placeholder="Company (e.g. Siemens)" required>
                            <input type="text" name="role_title" placeholder="Role (e.g. QA Intern)" required>
                            <input type="text" name="platform" placeholder="Platform (e.g. HackerRank / Meet)" required>
                            <input type="url" name="test_url" placeholder="Test URL (e.g. https://...)" required>
                            <input type="text" name="deadline_or_time" placeholder="Deadline / Time (e.g. Nov 15, 6 PM)" required>
                            <select name="prep_topic">
                                <option value="Software Testing / QA">Software Testing / QA</option>
                                <option value="Python & Programming">Python & Programming</option>
                                <option value="AI & Machine Learning">AI & Machine Learning</option>
                                <option value="General Tech">General Tech</option>
                            </select>
                            <button type="submit">Track & Alert</button>
                        </form>
                    </div>
                </div>

                <!-- PART 1: SUBMITTED JOBS & INTERNSHIPS -->
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px;">
                        <h2 class="tag-submitted" style="margin:0; border-bottom:none;">✅ Part 1: Submitted Jobs & Internships ({len(submitted_jobs)})</h2>
                        <a href="/export/applications.csv" style="background:#0f172a; color:white; padding:6px 14px; border-radius:6px; font-size:0.85rem; font-weight:600; text-decoration:none;">📥 Export Applications (CSV)</a>
                    </div>

                    <!-- Search & Filter Bar -->
                    <div style="display:flex; flex-wrap:wrap; gap:10px; margin: 15px 0 15px 0;">
                        <input type="text" id="jobSearch" placeholder="🔍 Search company, role, or keywords..." onkeyup="filterSubmittedJobs()" style="flex:2; min-width:200px; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:0.9rem;">
                        <select id="platformFilter" onchange="filterSubmittedJobs()" style="flex:1; min-width:140px; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:0.9rem; background:white;">
                            <option value="">All Platforms</option>
                            <option value="Internshala">Internshala</option>
                            <option value="LinkedIn">LinkedIn</option>
                            <option value="Wellfound">Wellfound Startups</option>
                            <option value="Freshers">Freshers Portals</option>
                            <option value="RemoteOK">RemoteOK</option>
                            <option value="Jobicy">Jobicy</option>
                        </select>
                        <select id="statusFilter" onchange="filterSubmittedJobs()" style="flex:1; min-width:140px; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:0.9rem; background:white;">
                            <option value="">All Pipeline Statuses</option>
                            <option value="SUBMITTED">SUBMITTED</option>
                            <option value="TEST_GIVEN">TEST GIVEN</option>
                            <option value="INTERVIEWING">INTERVIEWING</option>
                            <option value="OFFERED">OFFERED</option>
                            <option value="REJECTED">REJECTED</option>
                        </select>
                    </div>

                    <table id="submittedTable">
                        <thead>
                            <tr><th style="width:30px;">⭐</th><th>#</th><th>Job Title</th><th>Company</th><th>Platform</th><th>Match Score</th><th>Pipeline Status</th><th>Link</th><th>Outreach</th></tr>
                        </thead>
                        <tbody>
                            {submitted_rows_html}
                        </tbody>
                    </table>
                </div>

                <!-- PART 2: NOT SUBMITTED JOBS -->
                <div class="card">
                    <h2 class="tag-unsubmitted">⏳ Part 2: Not Submitted Jobs ({total - len(submitted_jobs)})</h2>
                    <p style="color: #64748b; font-size: 0.85rem;">Scanned across feeds but filtered out (senior/lead roles, non-tech positions, or ineligible requirements).</p>
                    <table>
                        <thead>
                            <tr><th>#</th><th>Job Title</th><th>Company</th><th>Platform</th><th>Filter Reason</th><th>Link</th></tr>
                        </thead>
                        <tbody>
                            {unsub_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- LinkedIn Cold Outreach Message Modal -->
            <div id="outreachModal" style="display:none; position:fixed; z-index:9999; left:0; top:0; width:100%; height:100%; background:rgba(15,23,42,0.6); align-items:center; justify-content:center;">
                <div style="background:white; padding:25px 30px; border-radius:10px; max-width:580px; width:90%; box-shadow:0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <h3 id="modalTitle" style="margin:0; color:#0f172a; font-size:1.15rem;">✉️ LinkedIn Cold Outreach Message</h3>
                        <span onclick="closeOutreach()" style="cursor:pointer; font-size:1.4rem; color:#64748b;">&times;</span>
                    </div>
                    <p style="color:#64748b; font-size:0.85rem; margin-top:0;">Send this message directly to recruiters, engineering leads, or founders on LinkedIn for this role:</p>
                    <textarea id="outreachText" style="width:100%; height:200px; padding:12px; font-family:-apple-system, BlinkMacSystemFont, sans-serif; font-size:0.9rem; line-height:1.45; border:1px solid #cbd5e1; border-radius:6px; box-sizing:border-box; color:#1e293b; resize:vertical;"></textarea>
                    <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:15px;">
                        <button onclick="copyOutreach()" id="copyBtn" style="background:#2563eb; color:white; border:none; padding:9px 18px; border-radius:6px; font-weight:600; cursor:pointer;">📋 Copy to Clipboard</button>
                        <button onclick="closeOutreach()" style="background:#f1f5f9; color:#475569; border:1px solid #cbd5e1; padding:9px 16px; border-radius:6px; font-weight:600; cursor:pointer;">Close</button>
                    </div>
                </div>
            </div>

            <script>
                function openOutreach(company, role) {{
                    var text = "Hi [Hiring Manager / Recruiter],\\n\\n" +
                               "I came across the " + role + " opportunity at " + company + " and wanted to reach out directly. " +
                               "As a final-year BCA student (Government Science College, Hassan - Graduating 2025) with practical projects in " +
                               "Manual/API Testing, Python scripting, and AI workflows (see my GitHub: https://github.com/varunms89), " +
                               "I would love the opportunity to contribute to your team as an intern or entry-level tester.\\n\\n" +
                               "Would you be open to a quick 5-minute conversation or reviewing my portfolio?\\n\\n" +
                               "Best regards,\\nVARUN M S\\n+91 8861639284 | msvarun89@gmail.com\\nLinkedIn: https://www.linkedin.com/in/varun-m-s-8861639284";
                    document.getElementById('outreachText').value = text;
                    document.getElementById('modalTitle').innerText = "✉️ Outreach for " + company;
                    document.getElementById('copyBtn').innerText = "📋 Copy to Clipboard";
                    document.getElementById('outreachModal').style.display = "flex";
                }}
                function closeOutreach() {{
                    document.getElementById('outreachModal').style.display = "none";
                }}
                function copyOutreach() {{
                    var copyText = document.getElementById("outreachText");
                    copyText.select();
                    document.execCommand("copy");
                    document.getElementById('copyBtn').innerText = "✅ Copied to Clipboard!";
                }}

                function changeJobStatus(jobId, newStatus) {{
                    fetch('/api/jobs/update-status', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ id: jobId, status: newStatus }})
                    }}).then(res => res.json()).then(data => {{
                        console.log('Status updated to', newStatus);
                    }}).catch(err => console.error(err));
                }}

                function toggleStar(jobId, btn) {{
                    fetch('/api/jobs/star', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ id: jobId }})
                    }}).then(res => res.json()).then(data => {{
                        if (data.status === 'success') {{
                            btn.innerText = data.starred ? '⭐' : '☆';
                        }}
                    }}).catch(err => console.error(err));
                }}

                function filterSubmittedJobs() {{
                    let searchVal = document.getElementById('jobSearch').value.toLowerCase();
                    let platformVal = document.getElementById('platformFilter').value.toLowerCase();
                    let statusVal = document.getElementById('statusFilter').value.toLowerCase();
                    let rows = document.querySelectorAll('#submittedTable tbody tr');
                    rows.forEach(row => {{
                        let text = row.innerText.toLowerCase();
                        let matchSearch = !searchVal || text.includes(searchVal);
                        let matchPlatform = !platformVal || text.includes(platformVal);
                        let matchStatus = !statusVal || text.includes(statusVal);
                        row.style.display = (matchSearch && matchPlatform && matchStatus) ? '' : 'none';
                    }});
                }}
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):
        # Silence routine HTTP access logs
        return

def run_web_service():
    # 1. Start background job bot thread
    bot_thread = threading.Thread(target=run_continuous_live_bot, daemon=True)
    bot_thread.start()

    # 2. Start interactive Telegram command listener thread
    try:
        from telegram_listener import run_telegram_listener
        tg_thread = threading.Thread(target=run_telegram_listener, daemon=True)
        tg_thread.start()
    except Exception as e:
        print(f"⚠️ Could not start Telegram listener: {e}")

    # 3. Start HTTP server (satisfies Render Web Service health check on free tier)
    server = HTTPServer(("0.0.0.0", PORT), HealthCheckAndDashboardHandler)
    print(f"🌐 Web Server listening on port {PORT} with Assessment Tracker, Prep Hub & Telegram commands...")
    server.serve_forever()

if __name__ == "__main__":
    run_web_service()
