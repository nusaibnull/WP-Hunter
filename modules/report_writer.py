import os
import json
from datetime import datetime

REPORT_FILE = "report/combined_report.json"

def save_report(target, results):
    if not os.path.exists("report"):
        os.makedirs("report")

    report_data = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "results": results
    }

    # Load existing reports if the file exists
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            all_reports = json.load(f)
    else:
        all_reports = []

    # Append new report
    all_reports.append(report_data)

    # Save back to the combined report file
    with open(REPORT_FILE, "w") as f:
        json.dump(all_reports, f, indent=4)

    print(f"\n[+] Report saved: {REPORT_FILE}")
