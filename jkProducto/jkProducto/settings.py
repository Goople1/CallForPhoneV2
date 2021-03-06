"""
Django settings for jkProducto project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/

"""



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import sys
encoding='utf-8'
reload(sys)
sys.setdefaultencoding(encoding)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c7lboe^e6kv97u59+3i)1p+wgtk@al3d1yov40^5(tce2(cc8*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'productos',
    'sucursales',
    'ventas',
    'internetWeb',
    'almacen',
    'asistencia',
    'cliente',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
)

ROOT_URLCONF = 'jkProducto.urls'

WSGI_APPLICATION = 'jkProducto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jkProductoV2',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',# Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
MEDIA_URL = '/media/'
#MEDIA_URL = ( 'static/' ) 

im = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2] + ['sucursales'])
TEMPLATE_DIRS = (
    os.path.join(im,'templates'),
    
)

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
MEDIA_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2] + ['media'])
#MEDIA_ROOT = ( os.path.join(BASE_DIR, 'media') )
STATIC_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2] + ['content'])
""" 
STATIC_PATH = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'
STATIC_DIRS = (STATIC_PATH,)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

""" 
LOGIN_URL = '/login/'


AUTHENTICATION_BACKENDS = (
    'ventas.backendsIniciarSesion.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# STATICFILES_STORAGE ='django.contrib.staticfiles.storage.CachedStaticFilesStorage'
