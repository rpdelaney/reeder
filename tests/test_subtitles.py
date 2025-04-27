import pytest
from httpx import URL

from reed.subtitles import has_extractor


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (URL("https://www.youtube.com/watch?v=d-7o9xYp7eE"), True),
        (URL("https://youtu.be/d-7o9xYp7eE"), True),
        (URL("https://whitehouse.gov"), False),
    ],
)
def test_has_extractor(url, expected):
    assert has_extractor(url) == expected
