from pathlib import Path

import pytest

from reed.content import ContentRenderer


def bytes_from_file(fixture_name: str):
    """Fixture providing base64-encoded binary data."""
    path = Path("tests", "fixtures", fixture_name)

    return path.read_bytes()


@pytest.fixture
def pdf_file():
    return bytes_from_file("traffic_stop_card.pdf")


@pytest.fixture
def pdf_text():
    return bytes_from_file("traffic_stop_card.txt").decode().strip()


class TestContentRenderer:
    @pytest.mark.skip(reason="Not yet tested, but should be")
    def test_html(self):
        assert False

    @pytest.mark.skip(reason="Not yet tested, but should be")
    def test_html_readable(self):
        assert False

    def test_pdf(self, pdf_file, pdf_text):
        renderer = ContentRenderer(data=pdf_file)

        assert renderer.pdf() == pdf_text
