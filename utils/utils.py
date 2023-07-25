import re
from urllib.parse import urlparse


def get_valid_filename(s):
    # Replace characters not allowed for file names with an underscore
    if s.startswith("https://"):
        s = s[8:]

    return re.sub(r'[\\/:*?".<>|]', '_', s)


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def valid_url(url):
    if not url.startswith("https://"):
        url = "https://" + url

    if is_url(url):
        return url
    else:
        raise ValueError

