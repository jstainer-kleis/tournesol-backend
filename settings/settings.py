"""
Django settings for settings project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import yaml

from collections import OrderedDict
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


server_settings = {}
SETTINGS_FILE = 'SETTINGS_FILE' in os.environ and os.environ['SETTINGS_FILE'] or '/etc/django/settings-tournesol.yaml'
try:
    with open(SETTINGS_FILE, 'r') as f:
        server_settings = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError:
    print('No local settings.')
    pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SECRET_KEY' in server_settings and server_settings['SECRET_KEY'] or 'django-insecure-(=8(97oj$3)!#j!+^&bh_+5v5&1pfpzmaos#z80c!ia5@9#jz1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEBUG' in server_settings and server_settings['DEBUG'] or False

ALLOWED_HOSTS = 'ALLOWED_HOSTS' in server_settings and server_settings['ALLOWED_HOSTS'] or ['0.0.0.0', '127.0.0.1', 'localhost']

STATIC_URL = '/static/'
STATIC_ROOT = 'STATIC_ROOT' in server_settings and server_settings['STATIC_ROOT'] or '/tmp/static/'
MEDIA_ROOT = 'MEDIA_ROOT' in server_settings and server_settings['MEDIA_ROOT'] or '/tmp/media/'
MEDIA_URL = '/media/'

MAIN_URL = 'MAIN_URL' in server_settings and server_settings['MAIN_URL'] or 'http://localhost:8000/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'tournesol',
    'oauth2_provider',
    'rest_framework',
]

# Mod??le utilisateur utilis?? par Django (1.5+)
AUTH_USER_MODEL = 'core.user'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = OrderedDict([
    ['default', {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DATABASE_NAME' in server_settings and server_settings['DATABASE_NAME'] or 'tournesol',
        'USER': 'DATABASE_USER' in server_settings and server_settings['DATABASE_USER'] or 'postgres',
        'PASSWORD': 'DATABASE_PASSWORD' in server_settings and server_settings['DATABASE_PASSWORD'] or '',
        'HOST': "DATABASE_HOST" in server_settings and server_settings["DATABASE_HOST"] or 'localhost',
        'PORT': 5432,
        'NUMBER': 42
    }]
])

DRF_RECAPTCHA_PUBLIC_KEY = "DRF_RECAPTCHA_PUBLIC_KEY" in server_settings and server_settings["DRF_RECAPTCHA_PUBLIC_KEY"] or 'dsfsdfdsfsdfsdfsdf'
DRF_RECAPTCHA_SECRET_KEY = "DRF_RECAPTCHA_SECRET_KEY" in server_settings and server_settings["DRF_RECAPTCHA_SECRET_KEY"] or 'dsfsdfdsfsdf'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 30,

    # important to have no basic auth here
    # as we are using Apache with basic auth
    # https://stackoverflow.com/questions/40094823/django-rest-framework-invalid-username-password
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),

    # custom exception handling
    'EXCEPTION_HANDLER': 'backend.api_v2.exception.handler',

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/hour',
        'user': '1000000/hour'
    }
}


# Maximal value for a rating (0-100)
# 0 means left video is best, 100 means right video is best
MAX_VALUE = 100.

VIDEO_FIELDS_DICT = OrderedDict([
    ('largely_recommended', 'Should be largely recommended'),
    ('reliability', "Reliable and not misleading"),
    ('importance', "Important and actionable"),
    ('engaging', "Engaging and thought-provoking"),
    ('pedagogy', "Clear and pedagogical"),
    ('layman_friendly', "Layman-friendly"),
    ('diversity_inclusion', "Diversity and Inclusion"),
    ('backfire_risk', "Resilience to backfiring risks"),
    ('better_habits', 'Encourages better habits'),
    ('entertaining_relaxing', 'Entertaining and relaxing'),
])

VIDEO_FIELDS = list(VIDEO_FIELDS_DICT.keys())

# maximal weight to assign to a rating for a particular feature, see #41
MAX_FEATURE_WEIGHT = 8