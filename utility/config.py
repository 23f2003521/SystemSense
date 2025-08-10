import os
from pathlib import Path

# ==== API SETTINGS ====
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/api")
REGISTER_ENDPOINT = f"{API_BASE_URL}/register"           # User + machine registration
HEALTH_UPDATE_ENDPOINT = f"{API_BASE_URL}/machine-health"  # Health updates, no auth

API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))

# ==== MACHINE INFO ====
DEFAULT_LOCATION = "Unknown"
OS_TYPE = os.name  # posix, nt
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "15"))

# File where the installer writes the device id / token that the service will use
DEVICE_ID_FILE = Path.home() / ".solsphere_device_id"

# ==== DEBUG ====
DEBUG = True
