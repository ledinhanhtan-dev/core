from aicore.settings import env

AI_API = "ai_api"

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = ()

LOCAL_APPS = (
    # AI_API
)

IMPORT_EXPORT_USE_TRANSACTIONS = False

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
