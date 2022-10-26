from aicore.settings import env

# https://docs.djangoproject.com/en/dev/ref/settings/#caches
REDIS_HOST = env("REDIS_HOST")
