from .base import *

# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = [ 
	'52.79.140.89',
]

STATIC_URL = 'static/'

# STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]