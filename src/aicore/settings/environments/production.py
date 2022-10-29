import sys
import logging.config
from os.path import join

from aicore.settings import BASE_DIR, env
from aicore.settings.configs.general_settings import LOGFILE_ROOT
from aicore.settings.configs.log import (
    LOG_STATS_MONITOR
)

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "0.0.0.0"]
)

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
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
            "class": "logging.handlers.WatchedFileHandler",
            "filename": join(LOGFILE_ROOT, "django.log"),
            "formatter": "verbose",
        },
        "proj_log_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": join(LOGFILE_ROOT, "aicore.log"),
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "cron_log_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": join(LOGFILE_ROOT, "cron_jobs.log"),
            "formatter": "verbose",
        },
        "queue_log_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": join(LOGFILE_ROOT, "queue_jobs.log"),
            "formatter": "verbose",
        },
        "stats_monitor_log_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": join(LOGFILE_ROOT, "stats_monitor.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "console": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
        "django": {
            "handlers": ["django_log_file"],
            "propagate": True,
            "level": "ERROR",
        },
        "django.db": {
            "handlers": ["django_log_file"],
            "propagate": True,
            "level": "ERROR",
        },
        "project": {
            "handlers": ["proj_log_file"],
            "level": "INFO"
        },
        "cron_job": {
            "handlers": ["cron_log_file"],
            "level": "INFO"
        },
        "queue": {
            "handlers": ["queue_log_file"],
            "level": "INFO",
        },

        LOG_STATS_MONITOR: {
            "handlers": ["stats_monitor_log_file"],
            "level": "INFO"
        }
    }
}
logging.config.dictConfig(LOGGING)
