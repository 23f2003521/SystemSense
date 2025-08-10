import requests
import socket
import platform
import uuid
from config import REGISTER_ENDPOINT, HEALTH_UPDATE_ENDPOINT, API_TIMEOUT, DEVICE_ID_FILE
from pathlib import Path
import json

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.machine_id = self._load_or_generate_machine_id()

    def _load_or_generate_machine_id(self):
        # If installer registered and wrote device id, use it; else generate ephemeral id
        try:
            if DEVICE_ID_FILE.exists():
                txt = DEVICE_ID_FILE.read_text().strip()
                if txt:
                    return txt
        except Exception:
            pass
        # fallback: stable id based on hostname (non-persistent)
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, socket.gethostname()))

    def register_machine(self, installer_token=None, meta=None):
        """
        Called by installer (one-time) to register machine.
        Installer should run this with network access and write returned device_id to DEVICE_ID_FILE.
        """
        payload = {
            "machine_info": {
                "unique_identifier": self.machine_id,
                "name": socket.gethostname(),
                "model": platform.machine(),
                "serial_number": None
            }
        }
        if meta:
            payload["meta"] = meta
        headers = {}
        if installer_token:
            headers["X-Installer-Token"] = installer_token
        try:
            response = self.session.post(REGISTER_ENDPOINT, json=payload, headers=headers, timeout=API_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[API] Registration failed: {e}")
            return None

    def send_health_update(self, health_data):
        """Send periodic health data. Uses DEVICE_ID_FILE-based machine_id."""
        payload = {
            "machine_id": self.machine_id,
            **health_data
        }
        try:
            response = self.session.post(HEALTH_UPDATE_ENDPOINT, json=payload, timeout=API_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[API] Health update failed: {e}")
            return None
