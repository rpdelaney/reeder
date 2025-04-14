"""Handle web requests."""

from urllib.parse import urlparse

import deal
import httpx


deal.activate()
deal.module_load(deal.pure)


@deal.pure
def is_url(string: str) -> bool:
    """Return whether the string is a URL."""
    result = urlparse(string)
    return all([result.scheme, result.netloc])


@deal.raises(httpx.RequestError, httpx.TimeoutException)
def fetch(client: httpx.Client, url: httpx.URL, timeout: int = 10):
    """Get the content from a page at a URL."""
    return client.get(
        url=url,
        timeout=timeout,
        follow_redirects=True,
    )
