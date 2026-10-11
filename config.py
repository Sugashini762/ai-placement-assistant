import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "placement.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
