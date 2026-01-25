import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Core settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key-fallback'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///default_db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False