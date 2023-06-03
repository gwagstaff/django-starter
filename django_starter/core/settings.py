"""
Django settings for django_starter project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import secrets
import sys
from functools import cache
from pathlib import Path

from pydantic import AmqpDsn, BaseSettings, Field, RedisDsn

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = os.environ.get("ENV_FILE", "test.env" if "pytest" in sys.modules else ".env")


class Settings(BaseSettings):
    """
    Pydantic-powered settings, to provide consistent error messages, strong
    typing, consistent prefixes, .venv support, etc.

    """

    #: Should django run in debug mode?
    DEBUG: bool = False

    #: Set a secret key used for signing values such as sessions. Randomized
    #: by default, so you'll logout everytime the process restarts.
    SECRET_KEY: str = Field(default_factory=lambda: "autokey-" + secrets.token_hex(128))

    #: If set, a list of allowed values for the HOST header. The default value
    #: of '*' means any host will be accepted.
    ALLOWED_HOSTS: list[str] = Field(default_factory=lambda: ["*"])

    #: If set, a list of hosts to accept for CORS.
    CORS_HOSTS: list[str] = Field(default_factory=list)

    #: If set, a list of hosts to accept for CSRF.
    CSRF_HOSTS: list[str] = Field(default_factory=list)

    #: Database Settings
    PGHOST: str | None = "localhost"
    PGPORT: int | None = 5432
    PGNAME: str = "postgres"
    PGUSER: str = "postgres"
    PGPASSWORD: str | None = None

    #: Celery Settings
    BROKER_URL: AmqpDsn = "amqp://localhost:5672//"
    BACKEND_URL: RedisDsn = "redis://localhost:6379/0"

    class Config:
        env_prefix = "APP_"
        env_file = str(BASE_DIR / ENV_FILE)
        env_file_encoding = "utf-8"
        # Case sensitivity doesn't work on Windows, so might as well be
        # consistent from the get-go.
        case_sensitive = False

        # Override the env_prefix so these fields load without TAKAHE_
        fields = {
            "PGHOST": {"env": "PGHOST"},
            "PGPORT": {"env": "PGPORT"},
            "PGNAME": {"env": "PGNAME"},
            "PGUSER": {"env": "PGUSER"},
            "PGPASSWORD": {"env": "PGPASSWORD"},
        }


@cache
def get_settings() -> Settings:
    return Settings()


config = get_settings()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.DEBUG

ALLOWED_HOSTS = config.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": config.PGHOST,
        "PORT": config.PGPORT,
        "NAME": config.PGNAME,
        "USER": config.PGUSER,
        "PASSWORD": config.PGPASSWORD,
    }
}


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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Celery Settings (must be specified in uppercase instead of lowercase and start with CELERY_)
#: https://docs.celeryq.dev/en/stable/userguide/configuration.html#configuration
CELERY_BROKER_URL = config.BROKER_URL
CELERY_RESULT_BACKEND = config.BACKEND_URL
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TIMEZONE = "UTC"