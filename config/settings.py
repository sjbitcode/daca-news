"""
Django settings for dacanews project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from pythonjsonlogger import jsonlogger
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps.
    'huey.contrib.djhuey',

    # Project apps.
    'articles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Collect all the static files here.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Additional dirs to include when collecting static files.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WHITENOISE_KEEP_ONLY_HASHED_FILES = True


# Huey Task Runner settings
HUEY = {
    'huey_class': 'huey.SqliteHuey',
    'name': 'dacanews-huey',
    # 'results': True,
    # To run Huey in "immediate" mode with a live storage API, specify
    # immediate_use_memory=False.
    # 'immediate_use_memory': False,

    # OR:
    # To run Huey in "live" mode regardless of whether DEBUG is enabled,
    # specify immediate=False.
    'immediate': False,

    # 'consumer': {
    #     'workers': 1,
    #     'worker_type': 'thread',
    #     'initial_delay': 0.1,  # Smallest polling interval, same as -d.
    #     'backoff': 1.15,  # Exponential backoff using this rate, -b.
    #     'max_delay': 10.0,  # Max possible polling interval, -m.
    #     'scheduler_interval': 1,  # Check schedule every second, -s.
    #     'periodic': True,  # Enable crontab feature.
    #     'check_worker_health': True,  # Enable worker health checks.
    #     'health_check_interval': 1,  # Check worker health every second.
    # },
}


# Logging Settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': jsonlogger.JsonFormatter,
            'fmt': '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'json'
        }
    },
    'loggers': {
        # root logger
        '': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
        }
    },
}


# Sentry Settings
SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN and SENTRY_DSN != 'sentry-key':
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])
