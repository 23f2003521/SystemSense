import platform
import subprocess
import sys
import shutil
from pathlib import Path
import os
import uuid
import getpass
import requests

from config import DEVICE_ID_FILE, CHECK_INTERVAL_MINUTES

API_URL = "http://localhost:5000/api/register"  # Change if needed


def is_admin_windows():
    import ctypes
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def write_device_id(device_id):
    DEVICE_ID_FILE.write_text(str(device_id))
    print(f"Wrote device id to {DEVICE_ID_FILE}")


def collect_user_info():
    print("=== Solsphere Installer ===")
    username = input("Enter your username: ").strip()
    email = input("Enter your email: ").strip()
    password = getpass.getpass("Enter your password: ").strip()
    return username, email, password


def collect_machine_info():
    return {
        "name": platform.node(),
        "model": platform.machine(),
        "serial_number": str(uuid.uuid4())[:8],  # Replace with real fetch if needed
        "unique_identifier": str(uuid.uuid4())   # Replace with hardware UUID if needed
    }

def register_with_backend():
    username, email, password = collect_user_info()
    machine_info = collect_machine_info()

    payload = {
        "username": username,
        "password": password,
        "email": email,
        "machine_info": machine_info
    }

    try:
        resp = requests.post(API_URL, json=payload)
        if resp.status_code == 201:
            device_id = resp.json().get("device_id", machine_info["unique_identifier"])
            write_device_id(device_id)
            print("[OK] Registration successful.")
            return True
        elif resp.status_code == 400 and "User already exists" in resp.text:
            print("[INFO] User already exists. Skipping registration.")
            # Still store device ID if provided
            device_id = resp.json().get("device_id", machine_info["unique_identifier"])
            write_device_id(device_id)
            return True
        else:
            print(f"[ERROR] Registration failed: {resp.status_code} {resp.text}")
            write_device_id(machine_info["unique_identifier"])
            return False
    except Exception as e:
        print(f"[ERROR] Could not connect to backend: {e}")
        write_device_id(machine_info["unique_identifier"])
        return False



def install_windows(service_user="SYSTEM"):
    python_exe = shutil.which("python3") or sys.executable
    python_exe = os.path.realpath(python_exe)
    script_path = Path(__file__).resolve().parent / "scheduler.py"
    task_name = "SolsphereHealthMonitor"
    interval = CHECK_INTERVAL_MINUTES

    # Build one single command string for /TR
    task_command = f'"{python_exe}" "{script_path}"'

    cmd = [
        "schtasks", "/Create",
        "/SC", "MINUTE",
        "/MO", str(interval),
        "/TN", task_name,
        "/TR", task_command,
        "/RU", service_user,
        "/F"
    ]
    print("Creating scheduled task:", " ".join(cmd))
    subprocess.check_call(cmd, shell=True)
    print("Task created.")



def install_systemd():
    service_name = "solsphere-health.service"
    service_path = f"/etc/systemd/system/{service_name}"
    python_exe = shutil.which("python3") or sys.executable
    python_exe = os.path.realpath(python_exe)
    script_path = Path(__file__).resolve().parent / "scheduler.py"

    service_unit = f"""[Unit]
Description=Solsphere System Health Monitor
After=network.target

[Service]
Type=simple
ExecStart={python_exe} {script_path}
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
"""

    print(f"Writing systemd unit to {service_path}")
    with open(service_path, "w") as f:
        f.write(service_unit)

    os.chmod(service_path, 0o644)
    subprocess.check_call(["systemctl", "daemon-reload"])
    subprocess.check_call(["systemctl", "enable", service_name])
    subprocess.check_call(["systemctl", "start", service_name])
    print("systemd service installed and started.")


def install_launchd():
    plist_path = "/Library/LaunchDaemons/com.solsphere.health.plist"
    python_exe = shutil.which("python3") or sys.executable
    python_exe = os.path.realpath(python_exe)
    script_path = Path(__file__).resolve().parent / "scheduler.py"

    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key><string>com.solsphere.health</string>
    <key>ProgramArguments</key>
    <array>
      <string>{python_exe}</string>
      <string>{script_path}</string>
    </array>
    <key>StartInterval</key><integer>{CHECK_INTERVAL_MINUTES * 60}</integer>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
  </dict>
</plist>"""

    print(f"Writing launchd plist to {plist_path}")
    with open(plist_path, "w") as f:
        f.write(plist)
    os.chmod(plist_path, 0o644)

    subprocess.check_call(["launchctl", "load", plist_path])
    print("launchd plist installed and loaded.")


def main():
    sys_platform = platform.system().lower()
    print("Installer running on", sys_platform)

    register_with_backend()

    if sys_platform == "windows":
        if not is_admin_windows():
            print("This installer must be run as Administrator on Windows.")
            return
        install_windows()
    elif sys_platform == "linux":
        if os.geteuid() != 0:
            print("Please run installer as root (sudo).")
            return
        install_systemd()
    elif sys_platform == "darwin":
        if os.geteuid() != 0:
            print("Please run installer as root (sudo).")
            return
        install_launchd()
    else:
        print(f"Unsupported platform: {sys_platform}")


if __name__ == "__main__":
    main()
