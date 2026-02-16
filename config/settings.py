from pathlib import Path
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-sc%u%h2dap2jwnm2y9-#2*@cr54j1)9-2wh306x(j!+_ra-4#o'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Local apps
    'asct',
    'users',
    'docs',
    'blog',
    'polls',
    'events',
    'eshop',
    'library',
    
    # Third-party apps
    "debug_toolbar",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # "allauth.socialaccount.providers",
    "allauth.socialaccount.providers.naver",
    # "allauth.socialaccount.providers.kakao",
    # "allauth.socialaccount.providers.github",
    # "allauth.socialaccount.providers.twitter",
    # "allauth.socialaccount.providers.facebook",
    # "allauth.socialaccount.providers.linkedin_oauth2",
    # "allauth.socialaccount.providers.instagram",
    "django_celery_beat",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
# 소셜 로그인에 필요
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID = 1

DEBUG_TOOLBAR_CONFIG = {
    # Set a high z-index to ensure the toolbar appears above other elements.
    'RESULTS_CACHE_SIZE': 100,
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,    
}

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'asct_v4',
        'USER': 'postgres',
        'PASSWORD': "1111",
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# Encoding
FILE_CHARSET = 'utf-8'
DEFAULT_CHARSET = 'utf-8'

STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = 'main-index'
LOGOUT_REDIRECT_URL = 'main-index'
# allauth 관련
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'username','email'}
# ACCOUNT_AUTHENTICATION_METHOD = 'username_email' # 로그인 시 아이디/이메일 모두 허용
ACCOUNT_EMAIL_VERIFICATION = 'optional' # 이메일 인증 설정 (mandatory, optional, none)

LOGIN_URL = 'login'
# LOGIN_URL = 'users:login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ml.python.ai@gmail.com'
EMAIL_HOST_PASSWORD = 'dtty tgfa lxzm bhue'

CART_ID = 'cart_in_session'

# settings.py
CELERY_BEAT_SCHEDULE = {
    "collect-disk-usage-every-10-min": {
        "task": "asct.tasks.schedule_disk_usage_collection",
        "schedule": crontab(minute='*/10'),
    },
    "collect-server-info-every-1-hour": {
        "task": "asct.tasks.schedule_server_info_collection",
        "schedule": crontab(minute=0),  # 매 시간 정각
    },
    "collect-cpu-usage-daily-01": {
        "task": "asct.tasks.schedule_cpu_usage_collection",
        "schedule": crontab(hour=1, minute=0),
    },
    "collect-memory-usage-daily-01": {
        "task": "asct.tasks.schedule_memory_usage_collection",
        "schedule": crontab(hour=1, minute=0),
    },
    "collect-traffic-usage-daily-01": {
        "task": "asct.tasks.schedule_traffic_usage_collection",
        "schedule": crontab(hour=1, minute=0),
    },
    "cleanup-old-data-daily-03": {
        "task": "asct.tasks.cleanup_old_data",
        "schedule": crontab(hour=3, minute=0),
        "args": (30,),  # 30일 경과 데이터 삭제
    },
}

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
# DB 기반 스케줄러 사용 (django-celery-beat)
# 이 설정을 추가하면 위쪽의 CELERY_BEAT_SCHEDULE 딕셔너리는 무시되고 DB의 내용을 따릅니다.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# 로깅 설정
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

import os
SERVICE_TYPE = os.environ.get('SERVICE_TYPE', 'web')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{name}:{lineno}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    }, 
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 파일명에 서비스 타입을 포함시켜 충돌 방지
            # 예: asct_system_web.log, asct_system_worker.log, asct_system_beat.log
            'filename': str(LOG_DIR / f'asct_system_{SERVICE_TYPE}.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        # 'asct' 앱에 대한 로거 설정
        'asct': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
