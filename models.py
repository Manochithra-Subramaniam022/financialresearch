from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email_notifications = db.Column(db.Boolean, default=True)
    high_contrast_mode = db.Column(db.Boolean, default=False)
    auto_archive_projects = db.Column(db.Boolean, default=False)
    projects = db.relationship('ResearchProject', backref='user', lazy=True)

class ResearchProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), default="Unknown")
    status = db.Column(db.String(50), default="Pending") # Pending, Completed, Failed
    extracted_data = db.Column(db.Text, nullable=True) # Will store JSON string
    is_archived = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
