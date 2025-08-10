import platform
import psutil
import subprocess
import re
import uuid
import os
from config import DEFAULT_LOCATION

def get_unique_identifier():
    try:
        mac = uuid.getnode()
        return str(mac)
    except Exception:
        return str(uuid.uuid4())

# -------------------------
# Disk Encryption Check
# -------------------------
def check_disk_encryption():
    system = platform.system().lower()
    try:
        if system == "darwin":  # macOS
            out = subprocess.check_output(["fdesetup", "status"], stderr=subprocess.STDOUT).decode()
            return {"status": "Encrypted" if "FileVault is On" in out else "Not Encrypted", "raw": out}

        elif system == "windows":
            out = subprocess.check_output(["manage-bde", "-status"], stderr=subprocess.STDOUT).decode()
            encrypted = "Percentage Encrypted" in out and "100%" in out
            return {"status": "Encrypted" if encrypted else "Not Encrypted", "raw": out}

        else:  # Linux
            out = subprocess.check_output(["lsblk", "-o", "NAME,TYPE,MOUNTPOINT"], stderr=subprocess.STDOUT).decode()
            encrypted = "crypt" in out or "/dev/mapper" in out
            return {"status": "Encrypted" if encrypted else "Not Encrypted", "raw": out}

    except Exception as e:
        return {"status": "Unknown", "error": str(e)}

# -------------------------
# OS Update Status
# -------------------------
def check_os_update_status():
    system = platform.system().lower()
    try:
        if system == "windows":
            cmd = [
                "powershell",
                "-Command",
                "(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search('IsInstalled=0') | Out-String"
            ]
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
            has_updates = "UpdateID" in out or "Title" in out
            return {"status": "Outdated" if has_updates else "Up-to-date", "raw": out}

        elif system == "darwin":
            out = subprocess.check_output(["softwareupdate", "-l"], stderr=subprocess.STDOUT).decode()
            status = "Up-to-date" if "No new software available" in out else "Outdated"
            return {"status": status, "raw": out}

        else:  # Linux (Debian/Ubuntu)
            subprocess.check_output(["apt-get", "update"], stderr=subprocess.DEVNULL)
            out = subprocess.check_output(["apt", "list", "--upgradable"], stderr=subprocess.STDOUT).decode()
            has_updates = "upgradable" in out.lower()
            return {"status": "Outdated" if has_updates else "Up-to-date", "raw": out}

    except Exception as e:
        return {"status": "Unknown", "error": str(e)}

# -------------------------
# Antivirus Status
# -------------------------
def check_antivirus_status():
    system = platform.system().lower()
    try:
        if system == "windows":
            import wmi
            w = wmi.WMI(namespace="root\\SecurityCenter2")
            avs = w.AntiVirusProduct()
            return {"status": "Active" if avs else "Not Installed", "count": len(avs)}

        elif system == "darwin":
            out = subprocess.check_output(["ps", "aux"], stderr=subprocess.STDOUT).decode().lower()
            av_keywords = ["symantec", "mcafee", "clamav", "sophos", "norton"]
            found = any(k in out for k in av_keywords)
            return {"status": "Active" if found else "Not Installed"}

        else:  # Linux
            try:
                subprocess.check_output(["systemctl", "is-active", "--quiet", "clamav-daemon"])
                return {"status": "Active"}
            except subprocess.CalledProcessError:
                return {"status": "Not Installed"}

    except Exception as e:
        return {"status": "Unknown", "error": str(e)}

# -------------------------
# Inactivity/Sleep Settings
# -------------------------



def check_inactivity_sleep():
    system = platform.system().lower()
    try:
        if system == "windows":
            # This asks powercfg directly for AC sleep timeout
            out = subprocess.check_output(
                ["powercfg", "/query", "SCHEME_CURRENT", "SUB_SLEEP", "STANDBYIDLE"],
                stderr=subprocess.STDOUT
            ).decode(errors="ignore")

            # Look for both AC and DC power settings
            match_ac = re.search(r"AC Power Setting Index:\s*(\d+)", out)
            match_dc = re.search(r"DC Power Setting Index:\s*(\d+)", out)

            minutes_ac = int(match_ac.group(1)) // 60 if match_ac else None
            minutes_dc = int(match_dc.group(1)) // 60 if match_dc else None

            return {
                "status": "Parsed" if (minutes_ac or minutes_dc) is not None else "Unknown",
                "minutes_ac": minutes_ac,
                "minutes_dc": minutes_dc
            }

        elif system == "darwin":  # macOS
            out = subprocess.check_output(["pmset", "-g", "custom"], stderr=subprocess.STDOUT).decode()
            match = re.search(r" sleep\s+(\d+)", out)
            if match:
                return {"status": "Parsed", "minutes": int(match.group(1))}
            return {"status": "Unknown", "raw": out}

        else:  # Linux
            out = subprocess.check_output(["xset", "q"], stderr=subprocess.STDOUT).decode()
            match = re.search(r"timeout:\s+(\d+)", out)
            if match:
                seconds = int(match.group(1))
                minutes = seconds // 60 if seconds > 0 else 0
                return {"status": "Parsed", "minutes": minutes}
            return {"status": "Unknown", "raw": out}

    except Exception as e:
        return {"status": "Unknown", "error": str(e)}

# -------------------------
# CPU, Memory, Disk Usage
# -------------------------
def get_system_usage():
    return {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent
    }

# -------------------------
# Machine Info
# -------------------------
def gather_machine_info():
    return {
        "name": platform.node(),
        "model": platform.machine(),
        "serial_number": None,
        "location": DEFAULT_LOCATION,
        "unique_identifier": get_unique_identifier()
    }

# -------------------------
# All Health Info
# -------------------------
def gather_health_info():
    usage = get_system_usage()

    disk_encryption = check_disk_encryption()
    os_update = check_os_update_status()
    antivirus = check_antivirus_status()
    inactivity_sleep = check_inactivity_sleep()

    # Normalize status to exactly match backend expectations
    disk_encryption_status = True if disk_encryption.get("status") == "Encrypted" else False
    os_update_status = os_update.get("status")  # "Up-to-date" or "Outdated"
    antivirus_status = antivirus.get("status")  # "Active" or "Not Installed"

    # Try to get inactivity sleep in minutes (example parse — adapt as needed)
    inactivity_sleep_setting = None
    raw_sleep = inactivity_sleep.get("raw", "")
    try:
        if raw_sleep and "minutes" in raw_sleep.lower():
            import re
            match = re.search(r"(\d+)\s*minutes", raw_sleep.lower())
            if match:
                inactivity_sleep_setting = int(match.group(1))
    except:
        pass

    # Issue detection
    issues = []
    if not disk_encryption_status:
        issues.append("Disk not encrypted")
    if os_update_status != "Up-to-date":
        issues.append("OS is outdated")
    if antivirus_status != "Active":
        issues.append("Antivirus not active")
    if inactivity_sleep_setting is None or inactivity_sleep_setting > 10:
        issues.append("Inactivity sleep > 10 minutes")

    return {
        "disk_encryption_status": disk_encryption_status,
        "os_update_status": os_update_status,
        "antivirus_status": antivirus_status,
        "inactivity_sleep_setting": inactivity_sleep_setting,
        "cpu_usage": usage["cpu_usage"],
        "memory_usage": usage["memory_usage"],
        "disk_usage": usage["disk_usage"],
        "issue_detected": len(issues) > 0,
        "issue_description": "; ".join(issues) if issues else None
    }

