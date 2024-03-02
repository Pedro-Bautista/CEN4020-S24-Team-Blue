from incollege.exceptions.ContentException import ContentException


class PermissionsGroup:
    USER = 0
    ADMIN = 1

    def from_string(self, permissions_group_string):
        upper_status = permissions_group_string.upper()
        match upper_status:
            case 'USER':
                return 0
            case 'ADMIN':
                return 1
            case _:
                raise ContentException('No such permissions group.', 400)
