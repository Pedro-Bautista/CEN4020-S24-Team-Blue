class AuthUser:
    """This object stores data relating to the authentication database

    Attributes:
        user_id (str): Unique identifier for corresponding :obj:`User`.
        username (str): Username for corresponding :obj:`User`.
        password_hash (str): Salted hashed password.
        permissions_group (str): Permissions level as specified by :class:`~PermissionsGroup`
    """

    def __init__(self, user_id: str, username: str, password_hash: str, permissions_group: str):
        """Create an instance based on the specified parameters.

        Args:
            user_id (str): Unique identifier for corresponding :obj:`User`.
            username (str): Username for corresponding :obj:`User`.
            password_hash (str): Salted hashed password.
            permissions_group (str): Permissions level as specified by :class:`~PermissionsGroup`
        """
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.permissions_group = permissions_group
