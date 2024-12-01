from urllib.parse import urlparse

import validators

URL_LENGTH = 255


class URLValidationError(Exception):
    pass


class URLTooLongError(URLValidationError):
    pass


class InvalidURLError(URLValidationError):
    pass


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    if len(url) > URL_LENGTH:
        raise URLTooLongError(URL_LENGTH)
    if not validators.url(url):
        raise InvalidURLError("url_incorrect")

    return None
