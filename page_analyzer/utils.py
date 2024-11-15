from urllib.parse import urlparse
import validators


class URLValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class URLTooLongError(URLValidationError):
    def __init__(self):
        super().__init__("URL превышает 255 символов")


class InvalidURLError(URLValidationError):
    def __init__(self):
        super().__init__("Некорректный URL")


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    try:
        if len(url) > 255:
            raise URLTooLongError()
        if not validators.url(url):
            raise InvalidURLError()

        return None
    except URLValidationError as e:
        return str(e)
