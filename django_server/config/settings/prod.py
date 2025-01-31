# prod.py

from .base import *

DEBUG = False

ALLOWED_HOSTS = [ 
	'52.79.140.89',
]

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'