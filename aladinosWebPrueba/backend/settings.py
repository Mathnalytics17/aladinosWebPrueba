import os
from pathlib import Path
from dotenv import load_dotenv
from apps.formulario.services import initialize_gspread

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import os
from dotenv import load_dotenv

load_dotenv()
get_env = os.getenv



 # Starting the gspread client when our server starts speeds things up; it avoids re-authenticating on each request
load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o9i3*_jip48zmz1xmf(-h@pnrh9zbq+t+x3m1d)h)_0m9saxqy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

if DEBUG:
    WEBSITE_URL='http://localhost:8000'
else:
    WEBSITE_URL= "http://82.112.250.23:1337"

# Application definition

INSTALLED_APPS = [ 'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles','rest_framework','apps.areaPrivada','apps.formulario'
]

MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
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

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React/Vue/Angular en desarrollo
    "http://82.112.250.23",  # Dominio en producción
    "http://82.112.250.23:1337"
]


CORS_TRUSTED_ORIGINS = [
    "http://localhost:3000",  # React/Vue/Angular en desarrollo
    "http://82.112.250.23",  # Dominio en producción
    "http://82.112.250.23:1337"
]


CORS_ORIGINS_WHITELIST = [
    "http://localhost:3000",  # React/Vue/Angular en desarrollo
    "http://82.112.250.23",  # Dominio en producción
    "http://82.112.250.23:1337"
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Apunta a dev/templates
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aladinosWeb',  # Reemplaza con el nombre de tu base de datos
        'USER': 'postgres',     # Reemplaza con tu nombre de usuario de PostgreSQL
        'PASSWORD':'1',  # Reemplaza con tu contraseña de PostgreSQL
        'HOST': 'localhost',  # Reemplaza con la dirección de tu servidor PostgreSQL (puede ser 'localhost' o una IP)
        'PORT': '5432',        # Reemplaza con el puerto de tu servidor PostgreSQL (el puerto por defecto es 5432)
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = get_env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD')
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SPREAD_CLIENT = initialize_gspread() 