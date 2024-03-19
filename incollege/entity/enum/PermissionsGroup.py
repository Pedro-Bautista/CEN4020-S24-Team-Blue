from incollege.exceptions.ContentException import ContentException


def from_string(permissions_group_string):
    upper_status = permissions_group_string.upper()
    match upper_status:
        case 'USER':
            return PermissionsGroup.USER
        case 'ADMIN':
            return PermissionsGroup.ADMIN
        case _:
            raise ContentException('No such permissions group.', 400)


class PermissionsGroup:
    USER = 0
    ADMIN = 1
