"""
Configuration module for NSUT Placement Portal
Loads environment variables and provides configuration settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # MySQL Database settings (XAMPP default configuration)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'nsut_placement')
    
    # File upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 2 * 1024 * 1024))  # 2 MB
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Email settings (for auto-generated passwords)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    
    # Application constants
    BRANCHES = ['CSE', 'ECE', 'ME', 'MAC', 'CSAI', 'CSDS', 'BT', 'ITNS', 'ICE']
    ELIGIBLE_YEARS = [3, 4]
    JOB_TYPES = ['Internship', 'Full-time', 'Both']
    APPLICATION_STATUSES = ['Applied', 'Shortlisted', 'Interview', 'Selected', 'Rejected']
    JOB_STATUSES = ['Pending', 'Approved', 'Rejected']
