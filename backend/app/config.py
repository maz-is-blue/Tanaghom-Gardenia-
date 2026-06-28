import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
