from .settings import *
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
CELERY_TASK_ALWAYS_EAGER = True
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
STRIPE_DEMO_MODE = True
SOCIAL_OAUTH_DEMO_MODE = True
