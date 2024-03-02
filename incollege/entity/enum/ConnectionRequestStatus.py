from incollege.exceptions.ContentException import ContentException


class ConnectionRequestStatus:
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2

    def from_string(self, status_string):
        upper_status = status_string.upper()
        match upper_status:
            case 'PENDING':
                return 0
            case 'ACCEPTED':
                return 1
            case 'REJECTED':
                return 2
            case _:
                raise ContentException('No such connection request status.', 400)
