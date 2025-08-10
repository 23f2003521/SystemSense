import subprocess
import platform
import sys
import os
import ctypes

def is_admin():
    """Check if the script is running as admin on Windows or root on Unix-like systems."""
    system = platform.system().lower()
    if system == 'windows':
        try:
            # Check if the script is running as Administrator on Windows using ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception as e:
            print(f"Error checking admin status on Windows: {e}")
            return False
    else:
        # On Unix-like systems, check if the script is running as root
        return os.geteuid() == 0


def run_as_admin():
    """Run the script with elevated privileges."""
    system = platform.system().lower()

    if system == 'windows':
        # On Windows, trigger a UAC prompt for Administrator privileges
        try:
            # Specify the full path to the python executable and script
            script_path = os.path.abspath(sys.argv[0])
            python_executable = sys.executable
            command = f'"{python_executable}" "{script_path}"'

            # Using 'runas' to elevate the command
            subprocess.run(['runas', '/user:Administrator', command], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to elevate on Windows: {e}")
    else:
        # On Unix-like systems (Linux/macOS), use sudo
        try:
            subprocess.run(['sudo', sys.executable] + sys.argv, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to elevate on Unix-like system: {e}")

def check_disk_encryption():
    system = platform.system().lower()

    if not is_admin():
        print("This script requires Administrator (root) privileges. Attempting to elevate...")
        run_as_admin()
        return  # Exit after elevation attempt

    if system == "darwin":  # macOS
        try:
            output = subprocess.check_output(["fdesetup", "status"]).decode()
            return "On" in output  # Encryption enabled status
        except subprocess.CalledProcessError:
            return "Unknown"

    elif system == "windows":  # Windows
        try:
            # Ensure 'manage-bde' is available and run the BitLocker status command
            output = subprocess.check_output(["manage-bde", "-status"]).decode()
            print(output)  # Debug: Print output for inspection
            if "Percentage Encrypted" in output:
                return True  # BitLocker encryption is enabled
            return False
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode() if e.stderr else "Unknown error"
            print(f"Error executing manage-bde: {error_message}")
            return "Unknown"
        except FileNotFoundError:
            print("manage-bde not found. Ensure you are on a Windows system with BitLocker.")
            return "Unknown"
        except PermissionError:
            print("Permission error. Ensure you are running as Administrator.")
            return "Unknown"

    elif system == "linux":  # Linux
        try:
            encrypted_devices = subprocess.check_output(["lsblk", "-o", "NAME,TYPE,MOUNTPOINT", "-l"]).decode()
            if "crypt" in encrypted_devices:
                return True  # LUKS encryption is enabled
            return False
        except subprocess.CalledProcessError:
            return "Unknown"

    else:
        return "Unknown system type"


# Example usage:
status = check_disk_encryption()
print(f"Disk encryption status: {status}")
