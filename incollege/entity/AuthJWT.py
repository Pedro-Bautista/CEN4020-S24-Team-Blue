from datetime import datetime, timedelta

import jwt

from incollege.config import Config


class AuthJWT:

    def __init__(self, user_id, permissions_group):
        self.user_id = user_id
        self.expiry_datetime = datetime.utcnow() + timedelta(hours=Config.TOKEN_DURATION)
        self.permissions_group = permissions_group

    def encode(self):
        payload = {
            'usr': self.user_id,
            'exp': self.expiry_datetime,
            'grp': self.permissions_group
        }
        return jwt.encode(payload, Config.SECRET, algorithm='HS512')

    def decode(self, token_string):
        try:
            token_bytes = token_string.encode('utf-8')
            token_dict = jwt.decode(token_bytes, Config.SECRET, algorithms=['HS512'])
            self.user_id = token_dict['usr']
            self.expiry_datetime = token_dict['exp']
            self.permissions_group = token_dict['grp']
            return self
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
