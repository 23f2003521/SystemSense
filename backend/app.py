# app.py
from flask import Flask
from flask_cors import CORS
from database import db, migrate
from config import LocalDevelopmentConfig
from security import jwt
# from controllers import auth_bp, machine_bp
# Import your controllers AFTER app creation to avoid circular imports
# from backend.controllers import *

app = None

def create_app():
    app=Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])
    db.init_app(app)
    migrate.init_app(app, db)
    # datastore=SQLAlchemyUserDatastore(db, User, Role)
    jwt.init_app(app)
    app.app_context().push()
    return app


app=create_app()
# app.register_blueprint(auth_bp)
# app.register_blueprint(machine_bp)
# with app.app_context():
#     db.create_all()
#     from models import User  # adjust import if your model name differs
#     from werkzeug.security import generate_password_hash
#     if not User.query.filter_by(username="admin").first():
#         admin_user = User(
#             username="admin",
#             email="admin@solsphere.com",
#             password=generate_password_hash("admin123"),  # strong password recommended
#             role="admin"
#         )
#         db.session.add(admin_user)
#         db.session.commit()
#         print("[INFO] Admin user created: username=admin, password=admin123")
#     else:
#         print("[INFO] Admin user already exists.")
# Import controllers after app is created
from controllers import *

if __name__ == "__main__":
    app.run(debug=True, port=5000)
