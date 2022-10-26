from .const import Const
from django.conf import settings


class WebSystem(Const):
    LOCALHOST = 0
    SPOTIFY = 1
    STG = 2

    @classmethod
    def to_system_name(cls, system_id=None):
        system_id = system_id or settings.SYSTEM_ID
        return dict(WEB_SYSTEMS).get(system_id, "localhost")

    @classmethod
    def is_production_mode(cls):
        return settings.SYSTEM_ID in [
            cls.SPOTIFY,
            cls.STG
        ]

    @classmethod
    def is_spotify_system(cls):
        return settings.SYSTEM_ID == cls.SPOTIFY

    @classmethod
    def is_stg_system(cls):
        return settings.SYSTEM_ID == cls.STG

    @classmethod
    def is_local_system(cls):
        return settings.SYSTEM_ID == cls.LOCALHOST


WEB_SYSTEMS = [
    (WebSystem.SPOTIFY, "Spotify-Production"),
    (WebSystem.STG, "Spotify-Staging"),
]
