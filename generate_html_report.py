"""
Automated CI/CD HTML Test Report Generator (Allure / Playwright Style)
Author: VARUN M S | Software QA & Test Automation Engineer
Executes unit, API, AI self-healing, and Siemens OA test suites and generates test-report.html.
"""

import io
import os
import time
import unittest
from datetime import datetime


def run_suite_and_generate_html(output_path: str = "test-report.html") -> dict:
    start_time = time.time()
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.dirname(os.path.abspath(__file__)), pattern="test_bot.py")

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    elapsed_ms = int((time.time() - start_time) * 1000)

    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total - failures - errors
    pass_rate = round((passed / max(total, 1)) * 100, 1)

    raw_output = stream.getvalue()
    rows_html = []
    for line in raw_output.splitlines():
        if " ... ok" in line or " ... FAIL" in line or " ... ERROR" in line:
            parts = line.split(" ... ")
            test_name = parts[0].strip()
            status_str = parts[1].strip()
            is_ok = "ok" in status_str.lower()
            badge_bg = "#dcfce7; color:#166534;" if is_ok else "#fee2e2; color:#991b1b;"
            badge_txt = "PASSED ✅" if is_ok else "FAILED ❌"
            rows_html.append(f"""
                <tr style="border-bottom:1px solid #e2e8f0;">
                    <td style="padding:10px 14px; font-family:monospace; font-weight:600; color:#0f172a;">{test_name}</td>
                    <td style="padding:10px 14px;"><span style="background:{badge_bg} padding:3px 10px; border-radius:9999px; font-weight:700; font-size:0.78rem;">{badge_txt}</span></td>
                    <td style="padding:10px 14px; color:#475569; font-size:0.85rem;">QA Automation & AI Suite</td>
                </tr>
            """)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CI/CD Automated QA Test Report - VARUN M S</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; background: #f8fafc; color: #0f172a; }}
        .header {{ background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); color: white; padding: 28px 40px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }}
        .container {{ max-width: 1100px; margin: 30px auto; padding: 0 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 25px; }}
        .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-top: 4px solid #2563eb; }}
        .card .val {{ font-size: 2rem; font-weight: 800; margin-top: 6px; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        th {{ background: #0f172a; color: white; text-align: left; padding: 12px 14px; font-size: 0.88rem; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div style="font-size:0.8rem; color:#93c5fd; font-weight:700; text-transform:uppercase;">GitHub Actions CI/CD • Playwright & Pytest Execution Report</div>
            <h1 style="margin:6px 0;">🧪 Enterprise QA & AI Automation Test Report</h1>
            <div style="font-size:0.9rem; color:#cbd5e1;">Author: <b>VARUN M S</b> (BCA Final Year, 2025) • Generated: {timestamp}</div>
        </div>
        <div style="background:rgba(34,197,94,0.2); border:1px solid #4ade80; padding:10px 18px; border-radius:8px; text-align:center;">
            <div style="font-size:0.75rem; color:#bbf7d0;">PIPELINE STATUS</div>
            <div style="font-size:1.3rem; font-weight:800; color:#4ade80;">{pass_rate}% PASSING</div>
        </div>
    </div>

    <div class="container">
        <div class="grid">
            <div class="card" style="border-top-color:#2563eb;">
                <div style="color:#64748b; font-size:0.85rem; font-weight:600;">TOTAL TEST CASES</div>
                <div class="val">{total}</div>
            </div>
            <div class="card" style="border-top-color:#16a34a;">
                <div style="color:#64748b; font-size:0.85rem; font-weight:600;">PASSED</div>
                <div class="val" style="color:#16a34a;">{passed}</div>
            </div>
            <div class="card" style="border-top-color:#dc2626;">
                <div style="color:#64748b; font-size:0.85rem; font-weight:600;">FAILED / ERRORS</div>
                <div class="val" style="color:#dc2626;">{failures + errors}</div>
            </div>
            <div class="card" style="border-top-color:#8b5cf6;">
                <div style="color:#64748b; font-size:0.85rem; font-weight:600;">EXECUTION DURATION</div>
                <div class="val" style="color:#7c3aed;">{elapsed_ms} ms</div>
            </div>
        </div>

        <h2 style="margin-bottom:12px;">📋 Automated Test Case Execution Breakdown</h2>
        <table>
            <thead>
                <tr>
                    <th>Test Method / Specification</th>
                    <th>Status</th>
                    <th>Suite Module</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return {
        "total": total,
        "passed": passed,
        "failed": failures + errors,
        "pass_rate": pass_rate,
        "elapsed_ms": elapsed_ms,
        "report_path": output_path
    }


if __name__ == "__main__":
    summary = run_suite_and_generate_html()
    print(f"[CI/CD Report Generated] {summary['passed']}/{summary['total']} passed ({summary['pass_rate']}%) -> {summary['report_path']}")
