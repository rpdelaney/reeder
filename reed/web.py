"""Handle web requests."""

from urllib.parse import urlparse

import deal


deal.activate()
deal.module_load(deal.pure)


@deal.pure
def is_url(string: str) -> bool:
    """Return whether the string is a URL."""
    result = urlparse(string)
    return all([result.scheme, result.netloc])
