"""Handle web requests."""

from urllib.parse import urlparse

import deal
import httpx


deal.activate()
deal.module_load(deal.pure)


@deal.has()
@deal.raises(ValueError, TypeError)
@deal.reason(
    ValueError,
    lambda string: string == "https://foobarbaz:-a",
    message="""
        urlparse() can raise ValueError if an invalid port
        is specified in the URL.
    """,
)
@deal.reason(
    TypeError,
    lambda _: False,
    message="""
        urlparse() raises TypeError if a single function call mixes
        str and non-str arguments. However, since this function uses only one
        argument to urlparse, this condition cannot be met.
    """,
)
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
    return all([result.scheme, result.netloc])


@deal.has()
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
