# settings/local.py

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l*1^widpmcfsp%m@z&@1uj9t%rgu7s!e%&clx9=)j$_gmm7(-r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#Email 設定
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #コンソールに表示

if DEBUG:
    def show_toolbar(request):
        return True
    
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE +=(
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK' :show_toolbar,
    }