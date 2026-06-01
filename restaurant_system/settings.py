import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# BASE DIRECTORY

BASE_DIR = Path(__file__).resolve().parent.parent

# LOAD ENV FILE

load_dotenv(BASE_DIR / '.env')

# SECURITY

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'dev-secret-key-change-in-production'
)

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1,*'
    ).split(',')
    if h.strip()
]

# INSTALLED APPS

INSTALLED_APPS = [
    # DJANGO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # THIRD PARTY
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'social_django',

    # LOCAL APPS
    'accounts',
    'restaurant',
    'orders',
    'payments',
    'frontend',
]

# MIDDLEWARE

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLS

ROOT_URLCONF = 'restaurant_system.urls'

# TEMPLATES

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'frontend' / 'templates'
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # GOOGLE OAUTH
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# WSGI

WSGI_APPLICATION = 'restaurant_system.wsgi.application'

# DATABASE

if os.getenv('USE_SQLITE', 'False') == 'True':

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'restaurant_db'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'root123'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3307'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }

# PASSWORD VALIDATORS

AUTH_PASSWORD_VALIDATORS = []

# INTERNATIONALIZATION

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True

# STATIC FILES

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'static',
]

# MEDIA FILES

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# DEFAULT PRIMARY KEY

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN / LOGOUT

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/menu/'

LOGOUT_REDIRECT_URL = '/'

# AUTHENTICATION BACKENDS

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# GOOGLE OAUTH2

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv(
    'GOOGLE_OAUTH_CLIENT_ID',
    ''
)

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv(
    'GOOGLE_OAUTH_CLIENT_SECRET',
    ''
)

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'email',
    'profile',
]

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# DJANGO REST FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),

    'DEFAULT_SCHEMA_CLASS':
        'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# JWT

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# DRF SPECTACULAR

SPECTACULAR_SETTINGS = {
    'TITLE': 'Restaurant Order Management API',

    'DESCRIPTION':
        'Django/DRF restaurant ordering system '
        'with OAuth2 login, online/offline payments, '
        'and async queue tasks.',

    'VERSION': '1.0.0',
}

# CELERY

CELERY_BROKER_URL = os.getenv(
    'CELERY_BROKER_URL',
    'amqp://guest:guest@localhost:5672//'
)

CELERY_RESULT_BACKEND = os.getenv(
    'CELERY_RESULT_BACKEND',
    'rpc://'
)

CELERY_TASK_ALWAYS_EAGER = (
    os.getenv('CELERY_TASK_ALWAYS_EAGER', 'False')
    == 'True'
)

CELERY_TASK_EAGER_PROPAGATES = True

CELERY_WORKER_ENABLE_REMOTE_CONTROL = False
CELERY_WORKER_SEND_TASK_EVENTS = False
CELERY_TASK_SEND_SENT_EVENT = False
CELERY_TASK_IGNORE_RESULT = True

# STRIPE

STRIPE_SECRET_KEY = os.getenv(
    'STRIPE_SECRET_KEY',
    ''
)

STRIPE_CURRENCY = os.getenv(
    'STRIPE_CURRENCY',
    'pln'
)

STRIPE_DEMO_MODE = (
    os.getenv('STRIPE_DEMO_MODE', 'True')
    == 'True'
)