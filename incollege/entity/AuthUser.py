class AuthUser:

    def __init__(self, user_id, username, password_hash, permissions_group):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.permissions_group = permissions_group
