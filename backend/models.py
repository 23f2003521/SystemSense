from database import db
from datetime import datetime
import pytz


    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Added username
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)  # Store hashed password
    role = db.Column(db.String(20), default="user")  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    machines = db.relationship("Machine", backref="owner", lazy=True)


class Machine(db.Model):
    __tablename__ = "machines"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    serial_number = db.Column(db.String(100), nullable=True)
    last_service_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    unique_identifier = db.Column(db.String(255), unique=True, nullable=False)  # e.g., hardware ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    health_records = db.relationship("MachineHealth", backref="machine", lazy=True)


class MachineHealth(db.Model):
    __tablename__ = "machine_health"

    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey("machines.id"), nullable=False)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ Mandatory checks
    disk_encryption_status = db.Column(db.Boolean, nullable=True)  # True = encrypted
    os_update_status = db.Column(db.String(50), nullable=True)  # e.g., "Up-to-date" / "Outdated"
    antivirus_status = db.Column(db.String(50), nullable=True)  # e.g., "Active" / "Not Installed"
    inactivity_sleep_setting = db.Column(db.Integer, nullable=True)  # in minutes

    # System meta
    cpu_usage = db.Column(db.Float, nullable=True)
    memory_usage = db.Column(db.Float, nullable=True)
    disk_usage = db.Column(db.Float, nullable=True)

    issue_detected = db.Column(db.Boolean, default=False)
    issue_description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<MachineHealth {self.machine_id} @ {self.checked_at}>"