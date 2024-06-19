"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$a=0=omhq&u5)_!a62w!susqi&&vnb0op@lyh$f_rjp*wvsnp&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# RESET_FILE = "/home/gorills/project/knc/main/manage.py"

# Application definition

from .local import INSTALLED_APPS
from .local import MIDDLEWARE

ROOT_URLCONF = "main.urls"
theme_name = "core/theme/mb/templates"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'core/admin/templates'),
            os.path.join(BASE_DIR, theme_name),
            ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "home.context_processors.load_settings",
                # "home.context_processors.get_main_menu",
                "home.context_processors.header_menu",
                "home.context_processors.category",
                "home.context_processors.menus",
                "home.context_processors.slider_category",
                "home.context_processors.callback",
                "home.context_processors.reviews",
                "home.context_processors.messanger_header",
                "home.context_processors.messanger_footer",
                "home.context_processors.favorites",
            ],
        },
    },
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.beget.com' 
EMAIL_HOST_USER = 'info@xn----7sbah6bllcobpj.xn--p1ai' 
EMAIL_HOST_PASSWORD = 'Ie51587v' 
EMAIL_FROM = 'info@xn----7sbah6bllcobpj.xn--p1ai' 
EMAIL_PORT = 465 
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False




WSGI_APPLICATION = "main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

from .local import DATABASES


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "core/"
STATIC_ROOT = "/main/core"



STATICFILES_DIRS = [
    BASE_DIR / "core",
    "/core/",
]

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         },
#     },
# }

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
CKEDITOR_UPLOAD_PATH = "uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"


