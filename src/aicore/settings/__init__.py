from os.path import dirname, join
from os.path import exists

import environ
from django.db.models.query import QuerySet
from split_settings.tools import include, optional

env = environ.Env()
BASE_DIR = dirname(dirname(dirname(__file__)))

env_file = join(dirname(BASE_DIR), "config.env")
if exists(env_file):
    environ.Env.read_env(str(env_file))

APP_ENVIRONMENT = env.str("APP_ENVIRONMENT", default="production")

# Managing environment via `APP_ENVIRONMENT` variable:
_base_settings = (
    "configs/companies/[!_]*.py"
    "configs/[!_]*.py",
    f"environments/${APP_ENVIRONMENT}.py",
    optional("environments/l")
)
