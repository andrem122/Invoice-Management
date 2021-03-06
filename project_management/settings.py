"""
Django settings for project_management project.
Generated by 'django-admin startproject' using Django 2.0.2.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import urllib.parse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ.get('DEBUG_VALUE') == 'True')
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['127.0.0.1', 'project-management-novaone.herokuapp.com']

# Application definition

DJANGO_APPS = (
    'django_dramatiq',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'django_twilio',
    'django_forms_bootstrap',
)

LOCAL_APPS = (
    'customer_register.apps.CustomerRegisterConfig',
    'redirect.apps.RedirectConfig',
    'property.apps.PropertyConfig',
    'appointments.apps.AppointmentsConfig',
    'sms_alerts.apps.SmsAlertsConfig',
    'project_details.apps.ProjectDetailsConfig',
    'leads.apps.LeadsConfig',
    'add_expense.apps.AddExpenseConfig',
    'add_payment.apps.AddPaymentConfig',
    'search_submit.apps.SearchSubmitConfig',
    'send_data.apps.SendDataConfig',
    'projects.apps.ProjectsConfig',
    'website.apps.WebsiteConfig',
    'add_house.apps.AddHouseConfig',
    'register.apps.RegisterConfig',
    'jobs.apps.JobsConfig',
    'expenses.apps.ExpensesConfig',
    'jobs_admin.apps.JobsAdminConfig',
    'payment_history.apps.PaymentHistoryConfig',
    'customer_payments.apps.CustomerPaymentsConfig',
    'addjob.apps.AddjobConfig',
    'csv_generator.apps.CSVGeneratorConfig',
    'payment_requests.apps.PaymentRequestsConfig',
    'tenants.apps.TenantsConfig',
)

THIRD_PARTY_APPS = (
    'whitenoise.runserver_nostatic',
    'storages',
    'bootstrap3',
    'bootstrap4',
    'phonenumber_field',
    'multiselectfield',
)

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

# The URL used to configure the options for Rabbitmq
rabbitmq_url = os.environ.get('CLOUDAMQP_URL', 'amqp://localhost:5672')
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": rabbitmq_url,
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ]
}

# Defines which database should be used to persist Task objects when the
# AdminMiddleware is enabled.  The default value is "default".
DRAMATIQ_TASKS_DATABASE = "default"

# The URL used to configure the options for Redis
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKEND_OPTIONS": {
        "url": redis_url,
    },
    "MIDDLEWARE_OPTIONS": {
        "result_ttl": 60000
    }
}

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

ROOT_URLCONF = 'project_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'project_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'default',                      # Or path to database file if using sqlite3.
        'USER': 'genuwine12',                      # Or path to database file if using sqlite3.
        'PASSWORD': '537H%[*tsnap]Ty',                      # Or path to database file if using sqlite3.
        'HOST': '127.0.0.1',                      # Or path to database file if using sqlite3.
        'PORT': '',                      # Or path to database file if using sqlite3.
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Login Redirect
LOGIN_REDIRECT_URL = '/redirect/login'
LOGIN_URL = '/accounts/login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_FINDERS = [
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
]

# Url that will be prepended to any static file path
STATIC_URL = '/static/'

# Where all static files will be collected during deployment of the app
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'login_assets'),
    os.path.join(BASE_DIR, 'logged_in_assets'),
    os.path.join(BASE_DIR, 'thank_you_assets'),
    os.path.join(BASE_DIR, '404_assets'),
]

#Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

redis_url = urllib.parse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6959'))

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
        }
    }
}

#Email
EMAIL_USE_SSL = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 465
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#Stripe
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')

#Twilio
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'US'

#Amazon Web Services
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'us-east-2'

# Apple push notifications
IOS_TEAM_ID = os.environ.get('IOS_TEAM_ID')
IOS_KEY_ID = os.environ.get('IOS_KEY_ID')
IOS_APP_BUNDLE_ID = os.environ.get('IOS_APP_BUNDLE_ID')

# Storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Bootstrap
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Reminder time: how early text messages are sent in advance of appointments
REMINDER_TIME = 30  # minutes

# Security enforce https requests
if DEBUG == False:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals(), logging=False)
