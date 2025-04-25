"""Handle web requests."""

from urllib.parse import urlparse

import deal
import httpx


deal.activate()
deal.module_load(deal.pure)


@deal.has()
def is_url(string: str) -> bool:
    """Return whether the string is a URL.

    >>> is_url("https://foobarbaz.com")
    True
    >>> is_url("./foobarbaz.com")
    False
    >>> is_url("/path/to/file.pdf")
    False
    """
    result = urlparse(string)
    return bool(result.scheme and result.netloc)


@deal.has("network")
@deal.raises(httpx.RequestError, httpx.TimeoutException)
def fetch(
    client: httpx.Client,
    url: httpx.URL,
    timeout: int = 10,
) -> httpx.Response:
    """Get the content from a page at a URL."""
    return client.get(
        url=url,
        timeout=timeout,
        follow_redirects=True,
    )
