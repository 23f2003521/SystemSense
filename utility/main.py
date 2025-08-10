import json
from pathlib import Path
from api_client import APIClient
from system_checks import gather_health_info
from config import DEVICE_ID_FILE
import sys

api = APIClient()
LAST_HEALTH_FILE = Path.home() / ".last_machine_health.json"

def run_health_check_once():
    """Run a single health check and send only if changed."""
    raw_health = gather_health_info()

    # ✅ Map raw_health into backend model field names (flat keys)
    health_data = {
        "disk_encryption_status": raw_health.get("disk_encryption_status", False),
        "os_update_status": raw_health.get("os_update_status", "Unknown"),
        "antivirus_status": raw_health.get("antivirus_status", "Unknown"),
        "inactivity_sleep_setting": raw_health.get("inactivity_sleep_setting"),
        "cpu_usage": raw_health.get("cpu_usage"),
        "memory_usage": raw_health.get("memory_usage"),
        "disk_usage": raw_health.get("disk_usage"),
    }

    # ✅ Auto-detect issues
    issues = []
    if not health_data["disk_encryption_status"]:
        issues.append("Disk not encrypted")
    if health_data["os_update_status"] != "Up-to-date":
        issues.append("OS is outdated")
    if health_data["antivirus_status"] != "Active":
        issues.append("Antivirus not active")
    if (
        health_data["inactivity_sleep_setting"] is None
        or health_data["inactivity_sleep_setting"] > 10
    ):
        issues.append("Inactivity sleep > 10 minutes")

    health_data["issue_detected"] = len(issues) > 0
    health_data["issue_description"] = "; ".join(issues) if issues else None

    # ✅ Compare with last sent data
    if LAST_HEALTH_FILE.exists():
        try:
            last_health = json.loads(LAST_HEALTH_FILE.read_text())
            if last_health == health_data:
                if __name__ == "__main__":
                    print("No changes detected, skipping update.")
                return
        except Exception:
            pass

    # ✅ Send to backend
    payload = {"machine_id": api.machine_id, **health_data}
    if __name__ == "__main__":
        print("Sending health data:", json.dumps(payload))

    response = api.send_health_update(payload)
    if response:
        LAST_HEALTH_FILE.write_text(json.dumps(health_data))
        if __name__ == "__main__":
            print("Health update sent:", response)
    else:
        if __name__ == "__main__":
            print("Failed to send health update.")

if __name__ == "__main__":
    run_health_check_once()
