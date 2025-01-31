# prod.py

from .base import *

# 원래는 DEBUG = False가 맞으나 이때 EC2 초반에 테스트 목적으로 True로 설정
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = [ 
	'52.79.140.89',
]

STATIC_URL = 'static/'

# STATIC_ROOT를 써야 하지만 마찬가지로 테스트를 위해 STATICFILES_DIRS 사용
# STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'static',]