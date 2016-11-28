"""
Django settings for base project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ldap
from libs.dane_auth_ldap.config import DaneLDAPSearch

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1&us78_67b3$2&qtyg)oo5x@419%laa#nq0r2ope445h3o4o4='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
SESSION_COOKIE_AGE = 3*60*60 #Three Hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition
INSTALLED_APPS = (
    'apps.DaneUsers',                  
    'apps.statistical_society',                  
    'apps.kiosco_app',                  
    'apps.services_requests',                  
    'apps.storage_files_server',                  
    'apps.shop',
#    'apps.cart',
    'apps.file_server',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'custom_user',
    'import_export',
    'libs.django_smart_selects.smart_selects',
    'grappelli',
    'filebrowser',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.DaneUsers.middleware.RestringedSitesMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'base.urls'
WSGI_APPLICATION = 'base.wsgi.application'
LOGIN_URL = 'users/login'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
gettext = lambda s: s
LANGUAGES = (
    ('es', gettext('Spanish')),
    ('en_US', gettext('English')),
)
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
COUNTRIES_FIRST = ['CO']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = "media"

# Templates configuration 
TEMPLATE_LOADERS =( 
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR,'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',    # add this line
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True,
        }
    }
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),)

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if DEBUG:
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'testing@kiosco.com'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
    
AUTH_USER_MODEL = 'DaneUsers.BasicDaneUser'
AUTH_PROFILE_MODULE = 'DaneUsers.UserProfile'
#LDAP authentication config
AUTH_LDAP_SERVER_URI = "ldap://dane.gov.co"
AUTH_LDAP_BIND_DN = "aplicaciones"
AUTH_LDAP_BIND_PASSWORD = "app2015"
AUTH_LDAP_USER_SEARCH = DaneLDAPSearch("OU=DANE,DC=DANE,DC=GOV,DC=CO",
    ldap.SCOPE_SUBTREE, "(&(mail=*)(cn=%(user)s))")  #A user must have an email, this is for avoid duplicated cns


AUTHENTICATION_BACKENDS = (                      
    'libs.dane_auth_ldap.backend.DaneLDAPBackend', 
    'django.contrib.auth.backends.ModelBackend',
)


USE_DJANGO_JQUERY = True

ACCOUNT_ACTIVATION_DAYS = 7

# logger = logging.getLogger('django_auth_ldap')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

####  CART CONFIGURATION ########
CART_SESSION_ID = 'cart'

LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'filters': {
                'require_debug_false': {
                        '()': 'django.utils.log.RequireDebugFalse',
                },
                'require_debug_true': {
                        '()': 'django.utils.log.RequireDebugTrue',
                }
        },
        'formatters': {
                'simple': {
                        'format': '[%(asctime)s] %(levelname)s %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S',
                },
                'verbose': {
                        'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S'
                },
        }, 
        'handlers': {
                'console': {
                        'level': 'DEBUG',
                        'filters': ['require_debug_true'],
                        'class': 'logging.StreamHandler',
                },
                'development_logfile': {
                        'level': 'DEBUG',
                        'filters': ['require_debug_true'],
                        'class': 'logging.FileHandler',
                        'filename': 'django_dev.log',
                        'formatter': 'verbose',
                },
        },
        'loggers': {
                'apps.file_server': {
                        'handlers': ['console', 'development_logfile'],
                        'level': 'DEBUG',
                },
                'db': {
                        'handlers': ['console', 'development_logfile'],
                        'level': 'DEBUG',
                },
                'django': {
                        'handlers': ['console'],
                        'level': 'CRITICAL',
                },
                'py.warnings': {
                        'handlers': ['console'],
                },
        },

}
