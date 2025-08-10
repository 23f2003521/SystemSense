from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from flask import current_app as app
from database import db
from models import User, Machine, MachineHealth
from sqlalchemy import desc

# ----------------------
# Role-based access decorator
# ----------------------
def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if not current_user:
                return jsonify({"message": "Authentication required"}), 401
            if current_user.role != required_role:
                return jsonify({"message": "Access forbidden: insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# ----------------------
# Blueprints
# ----------------------

# Home (Optional)
@app.route("/", methods=["GET"])
def home():
    return "<h1>Machine Health Monitoring API</h1>"

# ----------------------
# User Registration
# ----------------------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return jsonify({"message": "All fields are required"}), 400

    # Check for duplicate email or username
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({"message": "User already exists"}), 400

    # Create new user
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, email=email, role="user")
    db.session.add(user)
    db.session.commit()

    # Register machine automatically if machine data is provided
    machine_info = data.get("machine_info")
    if machine_info:
        unique_id = machine_info.get("unique_identifier")
        if unique_id:
            # Check if the machine already exists
            existing_machine = Machine.query.filter_by(unique_identifier=unique_id).first()
            if not existing_machine:
                machine = Machine(
                    user_id=user.id,
                    name=machine_info.get("name"),
                    model=machine_info.get("model"),
                    serial_number=machine_info.get("serial_number"),
                    unique_identifier=unique_id
                )
                db.session.add(machine)
                db.session.commit()

    # Return success response
    return jsonify({
        "message": "User (and machine) registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }), 201

# ----------------------
# Login
# ----------------------
@app.route("/api/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 400

    access_token = create_access_token(identity=user)
    return jsonify({"access_token": access_token, "role": user.role}), 200

# ----------------------
# Machine Health Updates
# ----------------------

# ----------------------
# Health Payload Normalization
# ----------------------
def normalize_health_payload(payload):
    """
    Ensures backward compatibility with old nested payloads 
    while supporting new flat key structure.
    """
    return {
        "disk_encryption_status": payload.get("disk_encryption_status") or (
            True if payload.get("disk_encryption", {}).get("status") == "Encrypted" else False
        ),
        "os_update_status": payload.get("os_update_status") or payload.get("os_update", {}).get("status"),
        "antivirus_status": payload.get("antivirus_status") or payload.get("antivirus", {}).get("status"),
        "inactivity_sleep_setting": payload.get("inactivity_sleep_setting") or payload.get("sleep_settings", {}).get("inactivity_minutes"),
        "cpu_usage": payload.get("cpu_usage"),
        "memory_usage": payload.get("memory_usage"),
        "disk_usage": payload.get("disk_usage"),
        "issue_detected": payload.get("issue_detected"),  # If client already sends this
        "issue_description": payload.get("issue_description"),
        "machine_id": payload.get("machine_id") or payload.get("unique_identifier")
    }


@app.route("/api/machine-health", methods=["POST"])
def receive_health_data():
    raw_data = request.get_json()
    data = normalize_health_payload(raw_data)

    unique_identifier = data.get("machine_id")
    # This is actually UUID
    if not unique_identifier:
        return jsonify({"message": "machine_id is required"}), 400

    machine = Machine.query.filter_by(unique_identifier=unique_identifier).first()
    if not machine:
        return jsonify({"message": "Machine not found"}), 404

    # Extract and compute issue status
    inactivity_limit = data.get("inactivity_sleep_setting", 0)
    issue_detected = (
        not data.get("disk_encryption_status", True)
        or data.get("os_update_status") != "Up-to-date"
        or data.get("antivirus_status") != "Active"
        or inactivity_limit > 10
    )
    health = MachineHealth.query.filter_by(machine_id=machine.id).first()
    if health:
        # Update existing record
        health.checked_at = datetime.utcnow()
        health.disk_encryption_status = data.get("disk_encryption_status")
        health.os_update_status = data.get("os_update_status")
        health.antivirus_status = data.get("antivirus_status")
        health.inactivity_sleep_setting = data.get("inactivity_sleep_setting")
        health.cpu_usage = data.get("cpu_usage")
        health.memory_usage = data.get("memory_usage")
        health.disk_usage = data.get("disk_usage")
        health.issue_detected = issue_detected
        health.issue_description = "Auto-detected issues" if issue_detected else None
    else:
        # Create a new record if it doesn't exist yet
        health = MachineHealth(
            machine_id=machine.id,
            checked_at=datetime.utcnow(),
            disk_encryption_status=data.get("disk_encryption_status"),
            os_update_status=data.get("os_update_status"),
            antivirus_status=data.get("antivirus_status"),
            inactivity_sleep_setting=data.get("inactivity_sleep_setting"),
            cpu_usage=data.get("cpu_usage"),
            memory_usage=data.get("memory_usage"),
            disk_usage=data.get("disk_usage"),
            issue_detected=issue_detected,
            issue_description="Auto-detected issues" if issue_detected else None
        )
        db.session.add(health)

    db.session.commit()

    return jsonify({"message": "Health data recorded"}), 200
# ----------------------
# Dashboard (Admin/Normal User View)
# ----------------------
@app.route("/api/dashboard", methods=["GET","POST"])
@jwt_required()
def get_dashboard():
    user_id = current_user.id
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    # If Admin → Return all machines
    if user.role == "admin":
        all_machines = Machine.query.all()
        machine_data = []

        for machine in all_machines:
            latest_health = MachineHealth.query.filter_by(machine_id=machine.id)\
                                               .order_by(desc(MachineHealth.checked_at)).first()
            owner = machine.owner.username if machine.owner else ""
            
            machine_data.append({
                "id": machine.id,
                "name": machine.name,
                "owner": owner,
                "model": machine.model,
                "serial_number": machine.serial_number,
                "last_service_date": str(machine.last_service_date),
                "unique_identifier": machine.unique_identifier,
                "last_checkin": str(latest_health.checked_at) if latest_health else None,
                "issue_detected": latest_health.issue_detected if latest_health else None,
                "os_update_status": latest_health.os_update_status if latest_health else None,
                "disk_encryption_status": latest_health.disk_encryption_status if latest_health else None,
                "antivirus_status": latest_health.antivirus_status if latest_health else None,
                "cpu_usage": latest_health.cpu_usage if latest_health else None,
                "memory_usage": latest_health.memory_usage if latest_health else None,
                "disk_usage": latest_health.disk_usage if latest_health else None
            })

        return jsonify({
            "role": "admin",
            "username": user.username,
            "machines": machine_data
        }), 200

    # If Regular User → Return only their machines
    else:
        user_machines = user.machines
        machine_data = []

        for machine in user_machines:
            latest_health = MachineHealth.query.filter_by(machine_id=machine.id)\
                                               .order_by(desc(MachineHealth.checked_at)).first()
            
            

            machine_data.append({
                "id": machine.id,
                "name": machine.name,
                "model": machine.model,
                "serial_number": machine.serial_number,
                "last_service_date": str(machine.last_service_date),
                "unique_identifier": machine.unique_identifier,
                "last_checkin": str(latest_health.checked_at) if latest_health else None,
                "issue_detected": latest_health.issue_detected if latest_health else None,
                "os_update_status": latest_health.os_update_status if latest_health else None,
                "disk_encryption_status": latest_health.disk_encryption_status if latest_health else None,
                "antivirus_status": latest_health.antivirus_status if latest_health else None,
                "cpu_usage": latest_health.cpu_usage if latest_health else None,
                "memory_usage": latest_health.memory_usage if latest_health else None,
                "disk_usage": latest_health.disk_usage if latest_health else None
            })

        return jsonify({
            "role": "user",
            "username": user.username,
            "machines": machine_data
        }), 200
