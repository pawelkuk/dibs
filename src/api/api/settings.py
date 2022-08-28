"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import dj_database_url
from booking import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "a^i=_6tz2@@g!-83zlld8x0(q(y7^+6$wh^38f15s7oo^1o$o@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "api",
    "booking",
    "paying",
    "ticketing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

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

WSGI_APPLICATION = "api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.parse(config.get_postgres_uri("postgres")),
    "booking": dj_database_url.parse(config.get_postgres_uri("postgres_booking")),
    "paying": dj_database_url.parse(config.get_postgres_uri("postgres_paying")),
    "ticketing": dj_database_url.parse(config.get_postgres_uri("postgres_ticketing")),
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

DATABASE_ROUTERS = [
    "booking.routers.BookingRouter",
    "ticketing.routers.TicketingRouter",
    "paying.routers.PayingRouter",
    "api.routers.DefaultRouter",
]
ALLOWED_HOSTS = ["*"]
RABBITMQ_BROKER = "amqp://guest@rabbitmq:5672//"

PAYMENT_SUCCESS_RATE = 0.5
TICKET_RENDER_SUCCESS_RATE = 0.5
CELERY_TASK_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ["pickle"]
CELERY_CREATE_MISSING_QUEUES = True
# CELERY_TASK_ALWAYS_EAGER = True
