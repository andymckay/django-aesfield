import os

DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'aesfield',
)

SECRET_KEY = 'aesfield-test-key'

AES_KEYS = {
    'default': os.path.join(os.path.dirname(__file__), 'sample.key')
}
