from aicore.settings import env

# REDIS
REDIS_HOST = env("REDIS_HOST")
REDIS_HOST_REPLICA = env("REDIS_HOST_REPLICA", default=REDIS_HOST)
REDIS_PORT = env("REDIS_PORT", default="6379")
NEUTRAL_REDIS_HOST = env("NEUTRAL_REDIS_HOST", default="")  # nlp
NEUTRAL_REDIS_PORT = env("NEUTRAL_REDIS_PORT", default="6379")
LRU_REDIS_HOST = env("LRU_REDIS_HOST", default=REDIS_HOST)
LRU_REDIS_PORT = env("LRU_REDIS_PORT", default=REDIS_PORT)
ADHOC_REDIS_HOST = env("ADHOC_REDIS_HOST", default=REDIS_HOST)
ADHOC_REDIS_PORT = env("ADHOC_REDIS_PORT", default=REDIS_PORT)
SOCKET_REDIS_HOST = env("SOCKET_REDIS_HOST", default=REDIS_HOST)
SOCKET_REDIS_PORT = env("SOCKET_REDIS_PORT", default=REDIS_PORT)

# REDIS NAMES
REDIS_DEFAULT_NAME = "default"
REDIS_DATA_CACHE_SETTING_NAME = "redis_data_cache"
REDIS_NEUTRAL_CACHE_SETTING_NAME = "redis_neutral_cache"
REDIS_LRU_CACHE_SETTING_NAME = "redis_lru_cache"
REDIS_SOCKET_LISTENER_SETTING_NAME = "redis_web_socket_listener"

# REDIS CONNECTIONS
REDIS_DATA_MAX_CONNECTIONS = env.int("REDIS_DATA_MAX_CONNECTIONS", default=5000)
REDIS_QUEUE_MAX_CONNECTIONS = env.int("REDIS_QUEUE_MAX_CONNECTIONS", default=5000)
REDIS_LRU_CACHE_MAX_CONNECTIONS = env.int("REDIS_LRU_CACHE_MAX_CONNECTIONS", default=5000)

# REDIS SSL
REDIS_SSL = env.int("REDIS_SSL", default=0)
NEUTRAL_REDIS_SSL = env.int("NEUTRAL_REDIS_SSL", default=0)
LRU_REDIS_SSL = env.int("LRU_REDIS_SSL", default=0)
ADHOC_REDIS_SSL = env.int("ADHOC_REDIS_SSL", default=0)
SOCKET_REDIS_SSL = env.int("SOCKET_REDIS_SSL", default=0)

# REDIS PASSWORDS
REDIS_PWD = env("REDIS_PWD", default="")
NEUTRAL_REDIS_PWD = env("NEUTRAL_REDIS_PWD", default="")
LRU_REDIS_PWD = env("LRU_REDIS_PWD", default="")
ADHOC_REDIS_PWD = env("ADHOC_REDIS_PWD", default="")
SOCKET_REDIS_PWD = env("SOCKET_REDIS_PWD", default="")

# CACHE MODEL
MODEL_CACHE_SETTING_NAME = "redis_model_cache"

# REDIS EXPIRES
REDIS_DEFAULT_EXPIRE_TIME = env.int("REDIS_DEFAULT_EXPIRE_TIME", default=86400)  # 1 day
REDIS_DEFAULT_MAX_EXPIRE_TIME = env.int("REDIS_DEFAULT_MAX_EXPIRE_TIME", default=2592000)  # 30 days

# LRU, NEUTRAL, SOCKET DEFAULTS
if LRU_REDIS_HOST == REDIS_HOST:
    LRU_REDIS_SSL = REDIS_SSL
    LRU_REDIS_PWD = REDIS_PWD
if NEUTRAL_REDIS_HOST == REDIS_HOST:
    NEUTRAL_REDIS_SSL = REDIS_SSL
    NEUTRAL_REDIS_PWD = REDIS_PWD
if SOCKET_REDIS_HOST == REDIS_HOST:
    SOCKET_REDIS_SSL = REDIS_SSL
    SOCKET_REDIS_PWD = REDIS_PWD


def __get_url_scheme(ssl_enable=False):
    return "rediss" if ssl_enable else "redis"


# REDIS URL SCHEMES
redis_url_scheme = __get_url_scheme(REDIS_SSL)
lru_redis_url_scheme = __get_url_scheme(LRU_REDIS_SSL)
neutral_redis_url_scheme = __get_url_scheme(NEUTRAL_REDIS_SSL)
socket_redis_url_scheme = __get_url_scheme(SOCKET_REDIS_SSL)

# REDIS OPTIONS
BASE_REDIS_OPTIONS = {
    "CLIENT_CLASS": "django_redis.client.DefaultClient",
    "PICKLE_VERSION": 4,
    "SOCKET_CONNECT_TIMEOUT": 5,  # seconds
    "SOCKET_TIMEOUT": 5,  # seconds
    "CONNECTION_POOL_KWARGS": {
        "max_connections": REDIS_DATA_MAX_CONNECTIONS,
        "retry_on_timeout": True,
    },
    "PASSWORD": f"{REDIS_PWD}",
    "IGNORE_EXCEPTIONS": True
}

# REDIS SETTINGS
BASE_REDIS_SETTINGS = {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": [
        f"{redis_url_scheme}://{REDIS_HOST}:{REDIS_PORT}/1",  # primary
        f"{redis_url_scheme}://{REDIS_HOST_REPLICA}:{REDIS_PORT}/1",  # primary
    ],
    "TIMEOUT": 86400,  # default timeout 24 * 60 * 60
    "OPTIONS": {**BASE_REDIS_OPTIONS}
}

# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    REDIS_DEFAULT_NAME: {**BASE_REDIS_SETTINGS},
    MODEL_CACHE_SETTING_NAME: {**BASE_REDIS_SETTINGS},
    REDIS_DATA_CACHE_SETTING_NAME: {**BASE_REDIS_SETTINGS},
    REDIS_LRU_CACHE_SETTING_NAME: {
        **BASE_REDIS_SETTINGS,
        "LOCATION": f"{redis_url_scheme}://{LRU_REDIS_HOST}:{LRU_REDIS_PORT}/1",
        "OPTIONS": {**BASE_REDIS_SETTINGS, "PASSWORD": LRU_REDIS_PWD, }
    },
    REDIS_SOCKET_LISTENER_SETTING_NAME: {**BASE_REDIS_SETTINGS}
}
