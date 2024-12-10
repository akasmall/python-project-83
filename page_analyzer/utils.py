from urllib.parse import urlparse

import validators

from page_analyzer.exceptions import InvalidURLError, URLTooLongError

URL_LENGTH = 255


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    if len(url) > URL_LENGTH:
        raise URLTooLongError()
    if not validators.url(url):
        raise InvalidURLError()

    return None
