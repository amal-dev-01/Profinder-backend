"""
Django settings for profinder project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from pathlib import Path
from datetime import timedelta
import os
from django.conf import settings
from decouple import Csv, config
from osgeo import gdal

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="mykey")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# GDAL_LIBRARY_PATH = 'c:\Users\nayan\Downloads\GDAL-3.4.3-cp311-cp311-win_amd64.whl'


ALLOWED_HOSTS = []

AUTH_USER_MODEL = "account.User"

# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "phonenumber_field",
    "rest_framework",
    "corsheaders",
    "account",
    "posts",
    "chat",
    "adminpanel",
    "booking",
    "django.contrib.gis",
    "rest_framework_gis",
    'drf_yasg',
    'django_celery_results',
    'django_celery_beat',
    


]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

ROOT_URLCONF = "profinder.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "profinder.wsgi.application"

ASGI_APPLICATION = "profinder.asgi.application"


# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': "channels.layers.InMemoryChannelLayer"
#         }
#     }

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

STRIPE_ID=config("STRIPE_ID")
STRIPE_SECRET=config("STRIPE_SECRET")

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'dbprofinder',
#        'USER': 'postgres',
#        'PASSWORD': '1234',
#        'HOST': 'localhost',
#        'PORT': '5432',

#    }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "postgisdb",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


SWAGGER_SETTINGS = {
    "TITLE": "Profinder",
    "SERVE_INCLUDE_SCHEMA": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "in": "header",
            "name": "Authorization",
            "type": "apiKey",
   },
},
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# email configuration

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("email")
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    "ROTATE_REFRESH_TOKENS": True,
}


# DEFAULTS = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'ROTATE_REFRESH_TOKENS': False,
#     'USER_ID_FIELD': 'id',
#     'SIGNING_KEY': settings.SECRET_KEY,
#     'USER_ID_CLAIM': 'user_id',
#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',
#     'JTI_CLAIM': 'jti',
#     'SLIDING_TOKEN_LIFETIME': timedelta(days=5),
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=10),
# }

# settings.py

ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
SERVICE_SID = config("SERVICE_SID")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")


CORS_ALLOW_ALL_ORIGINS = True
FRONT_END_URL ='http://localhost:3000/'


CELERY_BROKER_URL = 'redis://127.0.0.1:6379/'
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER ='json'
CELERY_TIMEZONE = 'Asia/kolkata'
CELERY_RESULT_BACKEND = "django-db"



CELERY_BEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "CRITICAL",
            "class": "logging.FileHandler",
            "filename": "./profinder/debug3.log",
        },
    },
    "loggers": {
        "django": {
            "handlers":{"file": {
            "level": "CRITICAL",
            "class": "logging.FileHandler",
            "filename": "./profinder/debug4.log",
        },},
            "level": "CRITICAL",
            "propagate": True,
        },
    },
}