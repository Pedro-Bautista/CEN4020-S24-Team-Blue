from incollege.exceptions.ContentException import ContentException


def from_string(application_status_string):
    upper_status = application_status_string.upper()
    match upper_status:
        case 'PENDING':
            return ApplicationStatus.PENDING
        case 'ACCEPTED':
            return ApplicationStatus.ACCEPTED
        case 'DENIED':
            return ApplicationStatus.DENIED
        case _:
            raise ContentException('No such application status.', 400)


class ApplicationStatus:
    PENDING = 0
    ACCEPTED = 1
    DENIED = 2
