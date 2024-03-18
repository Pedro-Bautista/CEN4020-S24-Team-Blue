from incollege.exceptions.ContentException import ContentException


def from_string(status_string: str) -> int:
    upper_status = status_string.upper()
    match upper_status:
        case 'PENDING':
            return ConnectionRequestStatus.PENDING
        case 'ACCEPTED':
            return ConnectionRequestStatus.ACCEPTED
        case 'REJECTED':
            return ConnectionRequestStatus.REJECTED
        case _:
            raise ContentException('No such connection request status.', 400)


class ConnectionRequestStatus:
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
