from .base import *

DEBUG = False

# Use get() method with a default value for VIRTUAL_HOST
ALLOWED_HOSTS = [os.environ.get('VIRTUAL_HOST', '*')]

# Database configuration for CodeRed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'NAME': os.environ.get('DB_NAME', 'youbuy'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'OPTIONS': {
            'ssl': {},
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_0900_ai_ci',
        },
    }
}

# Email backend for CodeRed
EMAIL_BACKEND = 'django_sendmail_backend.backends.EmailBackend'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True