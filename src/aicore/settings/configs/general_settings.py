from aicore.settings import env, BASE_DIR

ROOT_URLCONF = 'aicore.urls'
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "0.0.0.0"]
)
API_PORT = env.int('API_PORT')
SECRET_KEY = env('SECRET_KEY')
WSGI_APPLICATION = 'aicore.wsgi.application'

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = False
USE_TZ = True

STATIC_URL = '/static/'

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