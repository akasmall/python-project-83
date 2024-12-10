class URLValidationError(Exception):
    pass


class URLTooLongError(URLValidationError):
    pass


class InvalidURLError(URLValidationError):
    pass
