import os


class Config:
    SECRET_KEY          = os.environ.get('SECRET_KEY', 'tanaghom-dev-secret-change-me')
    DEBUG               = os.environ.get('DEBUG', 'false').lower() == 'true'
    ADMIN_PASSWORD      = os.environ.get('ADMIN_PASSWORD', 'tanaghom2024')
    MAX_CONTENT_LENGTH  = 100 * 1024 * 1024  # 100 MB
