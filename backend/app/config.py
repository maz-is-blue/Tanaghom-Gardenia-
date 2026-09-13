import os
import warnings


class Config:
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

    SECRET_KEY     = os.environ.get('SECRET_KEY')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

    if not SECRET_KEY:
        SECRET_KEY = 'tanaghom-dev-secret-change-me'
        if not DEBUG:
            warnings.warn(
                'SECRET_KEY is not set — falling back to an insecure default. '
                'Set the SECRET_KEY environment variable before deploying.',
                RuntimeWarning,
            )

    if not ADMIN_PASSWORD:
        ADMIN_PASSWORD = 'tanaghom2024'
        if not DEBUG:
            warnings.warn(
                'ADMIN_PASSWORD is not set — falling back to an insecure default. '
                'Set the ADMIN_PASSWORD environment variable before deploying.',
                RuntimeWarning,
            )

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB

    # Session cookies: not readable by JS, not sent cross-site, HTTPS-only outside debug.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE   = not DEBUG
