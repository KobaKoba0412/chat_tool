# settings/production.py

from .base import *

print('production.py read')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
#SECRET_KEY = 'l*1^widpmcfsp%m@z&@1uj9t%rgu7s!e%&clx9=)j$_gmm7(-r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# 本番環境に入力（セキュリティー上GITにはアップしない）
ALLOWED_HOSTS = ['*']

# メールサーバーへの接続設定
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'testchat4649@gmail.com'
EMAIL_HOST_PASSWORD = 'rpviipqgpmneuoeh' #アプリパスワード
# EMAIL_HOST_PASSWORD = 'test40612054'
EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'#実際に送信

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# mysite/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB','chat'),
        'USER': os.environ.get('POSTGRES_USER','kouji'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD','Passw0rd'),
        'HOST': os.environ.get('DATABASE_HOST','localhost'),
        'PORT': os.environ.get('DATABASE_PORT',''),
    }
}
