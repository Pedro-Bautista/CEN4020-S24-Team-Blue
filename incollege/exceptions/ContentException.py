from incollege.exceptions.EndpointException import EndpointException


class ContentException(EndpointException):
    def __init__(self, message, http_code=400):
        self.message = message
        self.http_code = http_code
        super().__init__(self.message, self.http_code)
