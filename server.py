import os
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from database import get_connection, get_job_stats
from live_bot import run_continuous_live_bot

PORT = int(os.environ.get("PORT", 8080))

class HealthCheckAndDashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz" or self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode("utf-8"))
            return

        # Simple web dashboard for Render Free Web Service
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # 1. Submitted Jobs & Internships
            cur.execute("""
                SELECT id, title, company, platform, location, match_score, status, url 
                FROM jobs 
                WHERE status IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED') 
                ORDER BY id DESC
            """)
            submitted_jobs = cur.fetchall()

            # 2. Not Submitted (Discovered / Skipped)
            cur.execute("""
                SELECT id, title, company, platform, location, match_score, match_reasons, url 
                FROM jobs 
                WHERE status NOT IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED') 
                ORDER BY id DESC LIMIT 25
            """)
            not_submitted_jobs = cur.fetchall()

            cur.execute("SELECT count(*) FROM jobs")
            total = cur.fetchone()[0]
            conn.close()
        except Exception as e:
            submitted_jobs = []
            not_submitted_jobs = []
            total = 0

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Job Auto-Apply Bot - Dashboard</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 30px; background: #f8fafc; color: #1e293b; }}
                h1 {{ color: #0f172a; margin-bottom: 5px; }}
                .subtitle {{ color: #64748b; margin-bottom: 25px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }}
                .stat-card {{ background: white; padding: 15px 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-left: 4px solid #3b82f6; }}
                .stat-card.green {{ border-left-color: #22c55e; }}
                .stat-card.gray {{ border-left-color: #94a3b8; }}
                .card {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 30px; }}
                h2 {{ font-size: 1.25rem; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid #f1f5f9; }}
                .tag-submitted {{ color: #15803d; }}
                .tag-unsubmitted {{ color: #b45309; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.92rem; }}
                th, td {{ padding: 12px 14px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
                th {{ background: #f8fafc; color: #475569; font-weight: 600; }}
                tr:hover {{ background: #f8fafc; }}
                .badge-success {{ padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.8rem; background: #dcfce7; color: #166534; }}
                .badge-unsub {{ padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.8rem; background: #fef3c7; color: #92400e; }}
                a {{ color: #2563eb; text-decoration: none; font-weight: 500; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>🤖 AI Job Auto-Apply Bot</h1>
            <p class="subtitle">Candidate: <b>VARUN M S</b> (BCA Final Year) &nbsp;|&nbsp; Target: <b>QA/Software Tester & AI/Programming Internships</b></p>
            
            <div class="grid">
                <div class="stat-card green">
                    <div style="color: #64748b; font-size: 0.85rem;">SUBMITTED APPLICATIONS</div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #15803d; margin-top: 5px;">{len(submitted_jobs)}</div>
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

            <!-- PART 1: SUBMITTED JOBS & INTERNSHIPS -->
            <div class="card">
                <h2 class="tag-submitted">✅ Part 1: Submitted Jobs & Internships ({len(submitted_jobs)})</h2>
                <table>
                    <thead>
                        <tr><th>#</th><th>Job Title</th><th>Company</th><th>Platform</th><th>Match Score</th><th>Status</th><th>Link</th></tr>
                    </thead>
                    <tbody>
                        {''.join([f"<tr><td>{idx}</td><td><b>{r[1]}</b></td><td>{r[2]}</td><td>{r[3]}</td><td><b>{r[5]}/100</b></td><td><span class='badge-success'>{r[6]}</span></td><td><a href='{r[7]}' target='_blank'>View Job ↗</a></td></tr>" for idx, r in enumerate(submitted_jobs, 1)]) if submitted_jobs else "<tr><td colspan='7'>No jobs submitted yet.</td></tr>"}
                    </tbody>
                </table>
            </div>

            <!-- PART 2: NOT SUBMITTED JOBS -->
            <div class="card">
                <h2 class="tag-unsubmitted">⏳ Part 2: Not Submitted Jobs ({total - len(submitted_jobs)})</h2>
                <p style="color: #64748b; font-size: 0.85rem;">These jobs were scanned across feeds but did not meet matching criteria (e.g., senior roles, non-tech positions, or ineligible locations).</p>
                <table>
                    <thead>
                        <tr><th>#</th><th>Job Title</th><th>Company</th><th>Platform</th><th>Filter Reason</th><th>Link</th></tr>
                    </thead>
                    <tbody>
                        {''.join([f"<tr><td>{idx}</td><td><b>{r[1]}</b></td><td>{r[2]}</td><td>{r[3]}</td><td><span class='badge-unsub'>{r[6]}</span></td><td><a href='{r[7]}' target='_blank'>View ↗</a></td></tr>" for idx, r in enumerate(not_submitted_jobs, 1)]) if not_submitted_jobs else "<tr><td colspan='6'>No unsubmitted jobs.</td></tr>"}
                    </tbody>
                </table>
            </div>
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

    # 2. Start HTTP server (satisfies Render Web Service health check on free tier)
    server = HTTPServer(("0.0.0.0", PORT), HealthCheckAndDashboardHandler)
    print(f"🌐 Web Server listening on port {PORT} for Render deployment...")
    server.serve_forever()

if __name__ == "__main__":
    run_web_service()
