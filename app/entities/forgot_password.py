from time import time
from app.utils import AttrDict
from . import Entity

class ForgotPasswordEntity(Entity):
    def __init__(self):
        super().__init__('ForgotPassword')
        self.fields = {
            'name': 'ForgotPassword',
            'email': None,
            'expires_in': 0,
            'expires_at': 0,
            'created_at': 0,
            'is_expired':False,
            'password_updated':False
        }

    @staticmethod
    def calc_expire_time(expires_in):
        return time() + int(expires_in)


class ForgotPassword(AttrDict):
    __strict_attr__ = False

    def is_expired(self):
        return self.expires_at <= time() if self.expires_at else False
