"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from decouple import config

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','localhost','0.0.0.0','realitas.site']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'graphene_django',
    # 'django_private_chat',
    # 'import_export',
    "corsheaders",
    'kepesertaan',
    'chat',
    'mychats',
    'kunjungan',
    #'channels',
     #graphene
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # personal context processors
                'kepesertaan.context_processors.info_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE':'django.db.backends.mysql',
        'NAME':config('DBNAME'),
        'USER':config('DBUSER'),
        'PASSWORD':config('DBPASS'),
        'HOST':config('DBHOST'),
        'PORT':'',
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': config('DBNAME'),
        # 'USER': config('DBUSER'),
        # 'PASSWORD': config('DBPASS'),
        # 'HOST': config('DBHOST'),
        # 'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'id-ID'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    # BASE_DIR / 'kepesertaan/static'
]

STATIC_ROOT = '/home/reah4319/jrealitas/public/'

# MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_ROOT = '/home/reah4319/jrealitas/media/'
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ASGI_APPLICATION = "core.asgi.application"

#CHANNEL_LAYERS = {
 #   "default":{
        # "BACKEND": "channels.layers.InMemoryChannelLayer"
  #      "BACKEND": "channels_redis.core.RedisChannelLayer",
   #     "CONFIG":{
    #        "hosts":[("127.0.0.1", 6379)],
    #    }
    #}
#}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]


#GRAPHENE
GRAPHENE = {
    "SCHEMA": "kepesertaan.schema.schema"
}

CORS_ALLOWED_ORIGINS = [
    config("SERVER"),
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

CSRF_TRUSTED_ORIGINS = [
    config('SERVER')
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# CHAT_WS_SERVER_HOST = '127.0.0.1'
# CHAT_WS_SERVER_PORT = 5002
# CHAT_WS_SERVER_PROTOCOL = 'ws'