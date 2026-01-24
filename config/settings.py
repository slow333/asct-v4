from pathlib import Path

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
    # 'library',
    
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
ACCOUNT_AUTHENTICATION_METHOD = 'username_email' # 로그인 시 아이디/이메일 모두 허용
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
