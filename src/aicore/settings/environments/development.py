import sys
import logging.config
from os.path import join

from aicore.settings import BASE_DIR, env
from aicore.settings.configs.general_settings import LOGFILE_ROOT

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
DEVELOPMENT_LOGGING_CONFIG = {
    "DJANGO": {
        "FORMATTER": env("DJANGO_LOG_FORMATTER", default="verbose"),
        "LEVEL": env("DJANGO_LOG_LEVEL", default="ERROR"),
    },
    "PROJECT": {
        "FORMATTER": env("PROJECT_LOG_FORMATTER", default="verbose"),
        "LEVEL": env("PROJECT_LOG_LEVEL", default="DEBUG"),
    },
    "CONSOLE": {
        "FORMATTER": env("CONSOLE_LOG_FORMATTER", default="simple"),
        "LEVEL": env("CONSOLE_LOG_LEVEL", default="DEBUG"),
    },
    "CRON": {
        "FORMATTER": env("CRON_LOG_FORMATTER", default="simple"),
        "LEVEL": env("CRON_LOG_LEVEL", default="DEBUG"),
    },
    "QUEUE": {
        "FORMATTER": env("QUEUE_LOG_FORMATTER", default="simple"),
        "LEVEL": env("QUEUE_LOG_LEVEL", default="INFO"),
    },
    "QUERY": {
        "LEVEL": env("QUERY_LOG_LEVEL", default="INFO"),
    },
}
LOGGING_CONFIG = None
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} [{pathname}:{lineno}] {message}",
            "datefmt": "%d/%b/%Y %H:%M:%S",
            "style": "{"
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "s3_json": {
            "format": "",  # Lets each Log class format the json data
        }
    },
    "handlers": {
        "django_log_file": {
            "level": DEVELOPMENT_LOGGING_CONFIG.get("DJANGO").get("LEVEL"),
            "class": "logging.FileHandler",
            "filename": join(LOGFILE_ROOT, "django.log"),
            "formatter": DEVELOPMENT_LOGGING_CONFIG.get("DJANGO").get("FORMATTER"),
        },
        "proj_log_file": {
            "level": DEVELOPMENT_LOGGING_CONFIG.get("PROJECT").get("LEVEL"),
            "class": "logging.FileHandler",
            "filename": join(LOGFILE_ROOT, "aicore.log"),
            "formatter": DEVELOPMENT_LOGGING_CONFIG.get("PROJECT").get("FORMATTER"),
        },
        "console": {
            "level": DEVELOPMENT_LOGGING_CONFIG.get("CONSOLE").get("LEVEL"),
            "class": "logging.StreamHandler",
            "formatter": DEVELOPMENT_LOGGING_CONFIG.get("CONSOLE").get("FORMATTER"),
        },
        "cron_log_file": {
            "level": DEVELOPMENT_LOGGING_CONFIG.get("CRON").get("LEVEL"),
            "class": "logging.handlers.WatchedFileHandler",
            "filename": join(LOGFILE_ROOT, "cron_jobs.log"),
            "formatter": DEVELOPMENT_LOGGING_CONFIG.get("CRON").get("FORMATTER"),
        },
        "queue_log_file": {
            "level": DEVELOPMENT_LOGGING_CONFIG.get("QUEUE").get("LEVEL"),
            "class": "logging.handlers.WatchedFileHandler",
            "filename": join(LOGFILE_ROOT, "queue_jobs.log"),
            "formatter": DEVELOPMENT_LOGGING_CONFIG.get("QUEUE").get("FORMATTER"),
        },
        "query": {
            "level": DEVELOPMENT_LOGGING_CONFIG.get("QUERY").get("LEVEL"),
            "class": "logging.FileHandler",
            "filename": join(LOGFILE_ROOT, "queries.log"),
            "formatter": DEVELOPMENT_LOGGING_CONFIG.get("QUERY").get("FORMATTER"),
        },
    },
    "loggers": {
        "console": {
            "handlers": ["console"],
            "propagate": True,
            "level": "DEBUG",
        },
        # "django": {
        #     "handlers": ["django_log_file"],
        #     "level": DEVELOPMENT_LOGGING_CONFIG.get("DJANGO").get("LEVEL"),
        # },
        "django.server": {
            "handlers": ["django_log_file"],
            "level": "DEBUG",
        },
        "project": {
            "handlers": ["proj_log_file"],
            "level": DEVELOPMENT_LOGGING_CONFIG.get("PROJECT").get("LEVEL"),
        },
        "ddtrace": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "cron_job": {
            "handlers": ["cron_log_file"],
            "level": DEVELOPMENT_LOGGING_CONFIG.get("CRON").get("LEVEL"),
        },
        "queue": {
            "handlers": ["queue_log_file"],
            "level": DEVELOPMENT_LOGGING_CONFIG.get("QUEUE").get("LEVEL"),
        },
        "django.db.backends": {
            "handlers": ["query"],
            "level": DEVELOPMENT_LOGGING_CONFIG.get("QUERY").get("LEVEL"),
            "propagate": False,
        },
    }
}
logging.config.dictConfig(LOGGING)
