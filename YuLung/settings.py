"""
Django settings for YuLung project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.conf.global_settings import EMAIL_BACKEND, EMAIL_USE_TLS
from session_cleanup.settings import weekly_schedule

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ovd0qamby5gf(e)_u$+-)=6(8#a$ui#j8s1v8)4isy#&15d2=l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

#CSRF_USE_SESSIONS = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'rolepermissions',
    'social_django',
    'session_cleanup',
    'ckeditor',
    'YuLung',
    'reservation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'YuLung.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR ,'YuLung' ,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',
            
            ],
        },
    },
]




ROLEPERMISSIONS_MODULE = 'YuLung.roles'

ROLEPERMISSIONS_REDIRECT_TO_LOGIN = True
ROLEPERMISSIONS_REGISTER_ADMIN = True
LOGIN_URL='admin-login'



SOCIAL_AUTH_URL_NAMESPACE = 'social'

AUTHENTICATION_BACKENDS = (
    
    'social_core.backends.facebook.FacebookOAuth2',
    #'social_auth.backends.facebook.FacebookBackend',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '412112655924-6nmhgc8ov9trppfb0imb5l6nq4cq43h9.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'svVS5JNSCtDCWHzVifVjnWMJ'

#yulon.dev
SOCIAL_AUTH_FACEBOOK_KEY = '294797807684724'
SOCIAL_AUTH_FACEBOOK_SECRET = 'addd1c4c10fc3f91e23dbfb5f051b8ce'

#pandaman.dev
#SOCIAL_AUTH_FACEBOOK_KEY = '991808234264199'
#SOCIAL_AUTH_FACEBOOK_SECRET = '5e1dbf5123918d7415601483993cc038'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email', 
}
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.10'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'login-success'

#SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'index'

WSGI_APPLICATION = 'YuLung.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangodb',
        'USER':'admin',
        'PASSWORD':'zhelang#1qaz',
        'HOST':'localhost',
    }
}

CKEDITOR_CONFIGS = {
   'default': {
	'language': 'zh',
        'toolbar': 'Custom',
	'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
	],
        #'height': 400,
        'width': '100%',
        'removePlugins': 'stylesheetparser',
        'extraPlugins': 'codesnippet',
   },
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'all_static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR , 'media')
MEDIA_URL = '/media/'

CELERYBEAT_SCHEDULE = {
    'session_cleanup': weekly_schedule
}

try:
  from local_settings import *
except ImportError:
  pass
