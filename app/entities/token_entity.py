from time import time

from app.utils import AttrDict
from . import Entity


class TokenEntity(Entity):
    def __init__(self):
        super().__init__('Token')
        self.fields = {
            'provider': None,
            'token_type': None,
            'access_token': None,
            'expires_in': 0,
            'expires_at': 0,
            'created_at': 0,
            'updated_at': 0,
        }

    @staticmethod
    def calc_expire_time(expires_in):
        return time() + int(expires_in)


class TokenModel(AttrDict):
    __strict_attr__ = False

    def is_expired(self):
        return self.expires_at <= time() if self.expires_at else False
