from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
]

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]