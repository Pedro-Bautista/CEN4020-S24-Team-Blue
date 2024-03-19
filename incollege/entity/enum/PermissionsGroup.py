from incollege.exceptions.ContentException import ContentException


def from_string(permissions_group_string):
    upper_group = permissions_group_string.upper()
    match upper_group:
        case 'USER':
            return PermissionsGroup.USER
        case 'ADMIN':
            return PermissionsGroup.ADMIN
        case _:
            raise ContentException('No such permissions group.', 400)


class PermissionsGroup:
    USER = 0
    ADMIN = 1
