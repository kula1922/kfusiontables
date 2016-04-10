"""
Django settings for kfusiontables project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9v2_!dc+n(ofd8l10wlgep%1@z%1r=wmv&846#*k2t!$d-^g_z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kfusiontables'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kfusiontables.urls'

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

WSGI_APPLICATION = 'kfusiontables.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# KFusionTables section

# KFUSIONTABLES_ACCESS_FILE_PATH = '/home/kula/workspace/sherpanymaps-fcb62c2c8abe.json'
# KFUSIONTABLES_ROW_SYNC_SIGNALS = True
# KFUSIONTABLES_MIGRATE_SYNC_SIGNALS = True
# KFUSIONTABLES_SKIP_ROW_SYNC_ON_MIGRATE = True

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'datefmt': '%d.%m.%Y %H:%M:%S',
#             'format': (
#                 '[%(asctime)08s,%(msecs)03d] %(levelname)-7s [%(processName)s'
#                 ' %(process)d] %(module)s - %(message)s'),
#         },
#         'simple': {
#             'datefmt': '%H:%M:%S',
#             'format': '[%(asctime)08s] %(levelname)-7s %(message)s',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#         'file_debug': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'maxBytes': 1024 * 1024 * 100,  # 100 MB
#             'backupCount': 10,
#             'filename': '/home/kula/tmp/logs/kftdebug.log',
#             'formatter': 'verbose',
#         },
#         'file_info': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'maxBytes': 1024 * 1024 * 100,  # 100 MB
#             'backupCount': 10,
#             'filename': '/home/kula/tmp/logs/kftinfo.log',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'kfusiontables': {
#             'handlers': ['file_debug', 'file_info', 'console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
