from os.path import join
from aicore.settings import BASE_DIR

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'db.sqlite3'),
    }
}
