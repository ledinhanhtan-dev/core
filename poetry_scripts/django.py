from os import environ
from os import path as ospath
from os import system as ossyscall
from pydoc import locate
from sys import argv
from sys import path as syspath

import django
from django.conf import settings
from django.core.management import call_command

PROJECT_ROOT = ospath.dirname(ospath.abspath(__file__)) + "/../src"
MANAGE_PY = f"{PROJECT_ROOT}/manage.py"


def noop(*args, **kwargs):
    pass  # noqa


def boot_django():
    syspath.append(PROJECT_ROOT)
    environ.setdefault("DJANGO_SETTINGS_MODULE", "aicore.settings")
    django.setup()


def rcachemodel_usage():
    boot_django()
    rache_model = locate("aicore.models.RCacheModel")
    getattr(rache_model, "print_all_usage", noop)()


def __getattr__(cmd):
    args = argv[1:]
    boot_django()
    if cmd.endswith("server"):
        if not any(":" in arg for arg in args):
            args.append(f"0.0.0.0:{settings.API_PORT}")
        ossyscall(f"python {MANAGE_PY} {cmd} {' '.join(args)}")
    else:
        call_command(cmd, args)
    return noop
