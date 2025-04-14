import hypothesis.provisional as pstrats
import hypothesis.strategies as strats
from hypothesis import given

from reed.web import is_url


@given(pstrats.urls())
def test_is_url(url):
    assert is_url(url)


@given(strats.text())
def test_is_not_url(noturl):
    assert not is_url(noturl)
