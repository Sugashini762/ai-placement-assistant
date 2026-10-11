from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")  # student | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship("StudentProfile", backref="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    branch = db.Column(db.String(100))
    cgpa = db.Column(db.Float, default=0.0)
    phone = db.Column(db.String(20))

    resume_filename = db.Column(db.String(255))
    resume_text = db.Column(db.Text)
    resume_score = db.Column(db.Integer, default=0)
    resume_feedback = db.Column(db.Text)
    extracted_skills = db.Column(db.Text)  # comma separated

    applications = db.relationship("Application", backref="student", cascade="all, delete-orphan")
    interviews = db.relationship("InterviewSession", backref="student", cascade="all, delete-orphan")

    def skills_list(self):
        if not self.extracted_skills:
            return []
        return [s.strip() for s in self.extracted_skills.split(",") if s.strip()]


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))

    jobs = db.relationship("Job", backref="company", cascade="all, delete-orphan")


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.Text)  # comma separated
    min_cgpa = db.Column(db.Float, default=0.0)
    package_lpa = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(120))
    drive_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)

    applications = db.relationship("Application", backref="job", cascade="all, delete-orphan")

    def skills_list(self):
        if not self.required_skills:
            return []
        return [s.strip() for s in self.required_skills.split(",") if s.strip()]


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)

    match_score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(30), default="Applied")  # Applied, Shortlisted, Rejected, Selected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)


class InterviewSession(db.Model):
    __tablename__ = "interview_sessions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"), nullable=False)

    role = db.Column(db.String(120))
    qa_json = db.Column(db.Text)  # JSON string of [{question, answer, score, feedback}]
    overall_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PlacementNotice(db.Model):
    __tablename__ = "placement_notices"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatLog(db.Model):
    __tablename__ = "chat_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
