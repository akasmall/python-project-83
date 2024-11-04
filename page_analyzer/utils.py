from urllib.parse import urlparse
import validators


class URLValidationError(Exception):
    pass


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    try:
        if len(url) > 255:
            raise URLValidationError("URL превышает 255 символов")
        if not validators.url(url):
            raise URLValidationError("Некорректный URL")

        return True, None
    except Exception as e:
        return False, str(e)
