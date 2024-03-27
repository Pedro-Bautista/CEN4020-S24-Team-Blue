from incollege.exceptions.ContentException import ContentException


def from_string(status_string: str) -> int:
    upper_status = status_string.upper()
    match upper_status:
        case 'UNDREAD':
            return MessageStatus.UNREAD
        case 'READ':
            return MessageStatus.READ
        case _:
            raise ContentException('No such connection request status.', 400)


class MessageStatus:
    UNREAD = 0
    READ = 1
