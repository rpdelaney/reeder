from http import HTTPStatus
from unittest.mock import MagicMock, call

import httpx
import hypothesis.provisional as pstrats
import hypothesis.strategies as strats
import pytest
from hypothesis import given

from reed.web import fetch, is_url


@given(pstrats.urls())
def test_is_url(url):
    assert is_url(url)


@given(strats.emails())
def test_is_not_url(noturl):
    assert not is_url(noturl)


class TestFetch:
    @given(
        url_str=pstrats.urls(),
        timeout=strats.integers(min_value=1, max_value=10),
    )
    def test_fetch_success(self, url_str, timeout):
        client = MagicMock(httpx.Client)
        client.get.return_value = httpx.Response(HTTPStatus.OK, content=b"OK")
        url = httpx.URL(url_str)

        response = fetch(client, httpx.URL(url), timeout)

        assert client.method_calls == [
            call.get(url=url, timeout=timeout, follow_redirects=True)
        ]
        assert response.status_code == HTTPStatus.OK
        assert response.content == b"OK"

    @given(
        url=pstrats.urls(),
        timeout=strats.integers(min_value=1, max_value=10),
    )
    def test_exceptions(self, url, timeout):
        for exc in (httpx.RequestError, httpx.TimeoutException):
            client = MagicMock(httpx.Client)
            client.get.side_effect = exc(message="timed out")

            with pytest.raises(exc):
                fetch(client, httpx.URL(url), timeout)
