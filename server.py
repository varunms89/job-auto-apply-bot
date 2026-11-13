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
            stats = get_job_stats()
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM jobs")
            total = cur.fetchone()[0]
            cur.execute("SELECT title, company, location, match_score, status, url FROM jobs WHERE status IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED') ORDER BY id DESC LIMIT 10")
            recent = cur.fetchall()
            conn.close()
        except Exception as e:
            stats = {"error": str(e)}
            total = 0
            recent = []

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Job Auto-Apply Bot - Render Dashboard</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 30px; background: #f8fafc; color: #1e293b; }}
                h1 {{ color: #0f172a; }}
                .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
                th {{ background: #f1f5f9; }}
                .badge {{ padding: 4px 8px; border-radius: 4px; font-weight: bold; background: #dcfce7; color: #15803d; }}
            </style>
        </head>
        <body>
            <h1>🤖 AI Job Auto-Apply Bot (Render 24/7)</h1>
            <div class="card">
                <h3>System Status: <span class="badge">LIVE & RUNNING</span></h3>
                <p>Candidate: <b>VARUN M S</b> (BCA Final Year)</p>
                <p>Target: <b>Software Tester / QA & Allied Tech Support (Remote & Bangalore)</b></p>
                <p>Total Scanned Jobs: <b>{total}</b> | Stats: {stats}</p>
            </div>
            <div class="card">
                <h3>Recent Applications</h3>
                <table>
                    <tr><th>Title</th><th>Company</th><th>Location</th><th>Score</th><th>Status</th></tr>
                    {''.join([f"<tr><td><a href='{r[5]}' target='_blank'>{r[0]}</a></td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td><span class='badge'>{r[4]}</span></td></tr>" for r in recent]) if recent else "<tr><td colspan='5'>Monitoring live feeds...</td></tr>"}
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
