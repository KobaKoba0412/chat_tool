# settings/local.py

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l*1^widpmcfsp%m@z&@1uj9t%rgu7s!e%&clx9=)j$_gmm7(-r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#Email 設定
# EMAIL_BACKEND = 'config.email_backends.ReadableSubjectEmailBackend'#コンソールに表示

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'#実際に送信

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

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# mysite/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        "TEST": {
            "NAME": os.path.join(BASE_DIR, "db_test.sqlite3"),
        },
    }
}
