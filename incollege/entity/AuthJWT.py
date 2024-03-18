from datetime import datetime, timedelta

import jwt

from incollege.config import Config


class AuthJWT:
    """This object stores the metadata for authentication :obj:`jwt` objects provided to/from clients.

    Attributes:
        user_id (str): Unique user identifier from :obj:`User` object.
        permissions_group (str): Permissions level as provided by :class:`~PermissionsGroup`
    """

    def __init__(self, user_id: str = None, permissions_group: str = None):
        """Create an instance expiring after the time period specified in :class:`Config`.

        Args:
            user_id (str, optional): Unique user identifier from :obj:`User` object.
                Defaults to None.
            permissions_group (str, optional): Permissions level as provided by :class:`~PermissionsGroup`.
                Defaults to None.
        """
        self.user_id = user_id
        self.expiry_datetime = datetime.utcnow() + timedelta(hours=Config.TOKEN_DURATION)
        self.permissions_group = permissions_group

    def encode(self) -> str:
        """Encode a :obj:`jwt` based on the attributes of this instance.

        Returns:
            str: String representation of :obj:`jwt`.
        """
        payload = {
            'usr': self.user_id,
            'exp': self.expiry_datetime,
            'grp': self.permissions_group
        }
        return jwt.encode(payload, Config.SECRET, algorithm='HS512')

    def decode(self, token_string: str) -> 'AuthJWT | None':
        """Accepts an encoded string representation of a :obj:`jwt` and outputs a matching instance of this class.

        Args:
            token_string (str): The encoded token string.

        Returns:
            AuthJWT:

        Examples:
            >>> # Example 1: Decoding a token
            >>> aJWT = AuthJWT('some_user_id', 'some_permissions_group')
            >>> aJWT_string = aJWT.encode()
            >>> aJWT_2 = AuthJWT().decode(aJWT_string)
            aJWT_2 now contains the same metadata we set for aJWT on construction.
        """
        try:
            token_bytes = token_string.encode('utf-8')
            token_dict = jwt.decode(token_bytes, Config.SECRET, algorithms=['HS512'])
            self.user_id = token_dict['usr']
            self.expiry_datetime = token_dict['exp']
            self.permissions_group = token_dict['grp']
            return self
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
