from flask import Flask
from flask_session import Session
import os

# Importing blueprints from different modules for authentication, group management, report management, and tutor management.
from blueprints.auth import auth_bp
from blueprints.claa import claa_bp
from blueprints.report import report_bp
from blueprints.tutor import tutor_bp

# Initialize the Flask application
app = Flask(__name__)

# Configuration for session management
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "default_key")  # Secret key for session encryption
app.config["SESSION_TYPE"] = "filesystem"  # Store sessions on the filesystem
app.config["SESSION_FILE_DIR"] = os.path.join(
    app.instance_path, 'flask_session')  # Directory for session files
app.config["SESSION_PERMANENT"] = False  # Sessions will not be permanent
# Use signing to protect the session cookies
app.config["SESSION_USE_SIGNER"] = True

# Initialize session management with the above configurations
Session(app)

# Register blueprints for different sections of the application
app.register_blueprint(auth_bp)  # Blueprint for authentication routes
app.register_blueprint(claa_bp)  # Blueprint for group management routes
app.register_blueprint(report_bp)  # Blueprint for report management routes
app.register_blueprint(tutor_bp)  # Blueprint for tutor management routes

# Run the Flask app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
