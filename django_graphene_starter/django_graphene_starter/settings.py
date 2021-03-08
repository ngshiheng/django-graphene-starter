import os
from pathlib import Path

import sentry_sdk
from colorlog import ColoredFormatter
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET', 'developmentsecret')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', '0') == '1'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'django-graphene-starter.herokuapp.com']

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'starter',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ratelimit.middleware.RatelimitMiddleware',
]

ROOT_URLCONF = 'django_graphene_starter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'django_graphene_starter', 'templates')],
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


WSGI_APPLICATION = 'django_graphene_starter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
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

# Logging
DEBUG_PROPAGATE_EXCEPTIONS = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed_string': {
            'format': '%(asctime)-15s [%(name)s] %(levelname)s: %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%SZ',
        },
        'colored_formatter': {
            '()': ColoredFormatter,
            'format': '%(asctime)-15s [%(cyan)s%(name)s%(reset)s] %(log_color)s%(levelname)s%(reset)s: %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%SZ',
            'log_colors': {
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored_formatter',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Sentry
sentry_sdk.init(
    dsn="https://914169a8f89542f1a5f3d64c8146f654@o545253.ingest.sentry.io/5666854",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment=ENVIRONMENT,
)

ignore_logger('graphql.execution.utils')


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Graphene-Django
# https://docs.graphene-python.org/projects/django/en/latest/
GRAPHENE = {
    'RELAY_CONNECTION_MAX_LIMIT': 5000,
    'SCHEMA': 'django_graphene_starter.schema.schema',
    'SCHEMA_OUTPUT': 'schema.graphql',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
        'django_graphene_starter.middlewares.LoaderMiddleware',
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}


# Django GraphQL JWT
# https://django-graphql-jwt.domake.io/en/latest/
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Django Rate Limit
# https://django-ratelimit.readthedocs.io/en/stable/
RATELIMIT_VIEW = 'django_graphene_starter.views.ratelimited_error'
RATELIMIT_RATE = os.environ.get('RATELIMIT_RATE', '5/s')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
