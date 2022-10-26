from aicore.settings import env

# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'aicore.db_backend.mysql',
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "OPTIONS": {"charset": "utf8mb4", "init_command": "SET NAMES 'utf8mb4'"},
    }
}

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
ES_INDEX_PREFIX = env("ES_INDEX_PREFIX", default="")

# MONGODB = {
#     "username": env("MONGODB_USERNAME", default=""),
#     "password": env("MONGODB_PASSWORD", default=""),
#     "database": env("MONGODB_DATABASE", default=""),
#     "host": env("MONGODB_HOST", default=""),
#     "port": env("MONGODB_PORT", default=""),
#     "replicaSet": env("MONGODB_REPLICASET", default=""),
# }
