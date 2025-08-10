# SystemSense
**Cross-Platform System Utility + Admin Dashboard**  
Monitor, collect, and visualize system health across multiple devices.

## 📌 Project Overview
SystemSense consists of three main components:

- **Utility (Client)** – A cross-platform system utility that runs as a background process and periodically collects:
  - Disk encryption status
  - OS update status
  - Antivirus presence & status
  - Inactivity sleep settings (should be ≤ 10 mins)
  - CPU, memory, and disk usage
  - Reports data to a backend API only if changes are detected

- **Backend Server** – REST API to:
  - Receive system health data from utilities
  - Store the latest health data in a database
  - Provide filtering, listing, and exporting endpoints

- **Frontend (Admin Dashboard)** – Web-based dashboard to:
  - List all reporting machines
  - Display their latest status
  - Highlight issues in configuration
  - Filter and sort results

## 🛠 Architecture
[ Utility ] → [ Backend API + Database ] → [ Admin Dashboard ]
- **Utility**: Python daemon, platform-specific checks, runs via Task Scheduler (Windows) or cron (Linux/macOS)
- **Backend**: Flask + SQLAlchemy REST API
- **Frontend**: Vue.js + Bootstrap UI

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/23f2003521/SystemSense.git
cd SystemSense

2️⃣  Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # (Windows)
# OR
source venv/bin/activate  # (Linux/macOS)

pip install -r requirements.txt
python app.py
#once it runs keep admin credentials from app.py 
and comment out these portion so that each time you run your application it does not run each time db.create_All()
"""db.create_all()
    from models import User  # adjust import if your model name differs
    from werkzeug.security import generate_password_hash
    if not User.query.filter_by(username="admin").first():
        admin_user = User(
            username="admin",
            email="admin@solsphere.com",
            password=generate_password_hash("admin123"),  # strong password recommended
            role="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        print("[INFO] Admin user created: username=admin, password=admin123")
    else:
        print("[INFO] Admin user already exists.")"""    please comment it out in app.py

The backend runs by default at:
http://127.0.0.1:5000

3️⃣ Utility Setup (Client)
Windows
cd utility
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python installer.py
It will ask for username , email and password , provide your details 


Linux / macOS

cd utility
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python installer.py

For Linux/macOS, the installer creates a cron job.

4️⃣ Frontend Setup
cd frontend
npm install
npm run dev
frontend run at
Local:   http://localhost:5173/

▶ Running the Installer and Scheduler
Once installed, you don’t need to manually run scheduler.py — it’s automatically triggered by:

Windows: Task Scheduler
Linux/macOS: cron
To run manually for testing:
cd utility
venv\Scripts\activate
python scheduler.py



📂 Repository Structure
SystemSense/
├── utility/          # Cross-platform health collection utility
├── backend/          # Flask API + DB models
├── frontend/         # Vue.js dashboard
├── .gitignore
└── README.md

✅ Features
Cross-platform support (Windows, Linux, macOS)
Minimal resource usage
Secure API communication
Auto-detection of system health changes
Web dashboard with filters & issue flags



#
