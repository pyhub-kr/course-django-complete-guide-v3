"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import sys
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from environ import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env = Env()

ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    with ENV_PATH.open(encoding="utf-8") as f:
        env.read_env(f, overwrite=True)
else:
    print("not found:", ENV_PATH, file=sys.stderr)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(
    "SECRET_KEY",
    default="django-insecure-dn^kymsy5h(e&jtgba0r#jh1v6!9gao1e2#g!5#76b)5=dh2s)",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# Application definition

INSTALLED_APPS = [
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django_components.safer_staticfiles",
    # third apps
    "crispy_forms",
    "crispy_bootstrap5",
    "django_components",
    "django_extensions",
    "django_htmx",
    "template_partials",
    # local apps
    "accounts",
    "core",
    "photolog",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

if DEBUG:
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "core" / "src-django-components",
        ],
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

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Custom User Model
AUTH_USER_MODEL = "accounts.User"


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

LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="ko-kr")

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "core" / "src-django-components",
]


# Media files

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "mediafiles"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

INTERNAL_IPS = env.list("INTERNAL_IPS", default=["127.0.0.1"])


# django-crispy-forms

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


# Email
# https://docs.djangoproject.com/en/4.2/topics/email/#smtp-backend
# (장고 기본 기능) 메일 발송 테스트: python manage.py sendtestemail 수신자_이메일

EMAIL_HOST = env.str("EMAIL_HOST", default=None)

if DEBUG and EMAIL_HOST is None:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    try:
        EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
        EMAIL_PORT = env.int("EMAIL_PORT")
        EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
        EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
        EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
        EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
        DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
    except ImproperlyConfigured as e:
        print("ERROR:", e, file=sys.stderr)
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
