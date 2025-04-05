import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True