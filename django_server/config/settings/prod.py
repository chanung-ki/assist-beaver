from .base import *

# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = [
    # 나중에 구매한 도메인, EC2의 퍼블릭 ip등을 명시
]

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'