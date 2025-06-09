"""Provide content handling."""

import io
import string

import deal
import readability
from bs4 import BeautifulSoup as Bs
from pdfminer.high_level import extract_text


class ContentRenderer:
    """Provide rendering for various document types."""

    @deal.pure
    def __init__(self, data: bytes) -> None:
        """Initialize a renderer."""
        self._data: bytes = data

    @property
    @deal.pure
    def data(self) -> bytes:
        """Provide read-only access to the data.

        >>> r = ContentRenderer(b"aaa")
        >>> r.data
        b'aaa'
        """
        return self._data

    @deal.pure
    @deal.post(lambda result: not result.startswith(tuple(string.whitespace)))
    @deal.post(lambda result: not result.endswith(tuple(string.whitespace)))
    def text(self) -> str:
        r"""Render text from... text.

        >>> r = ContentRenderer(b"\taaa\xff\xfe\xfd\t \n ")
        >>> r.text()
        'aaa���'
        """
        return self._data.decode(encoding="utf-8", errors="replace").strip(
            string.whitespace
        )

    @deal.pure
    @deal.post(lambda result: not result.startswith(tuple(string.whitespace)))
    @deal.post(lambda result: not result.endswith(tuple(string.whitespace)))
    def html(self) -> str:
        """Render text from HTML."""
        soup = Bs(self._data, "html.parser")
        return soup.get_text().strip(string.whitespace)

    @deal.pure
    @deal.post(
        lambda result: all(
            not term.startswith(tuple(string.whitespace)) for term in result
        )
    )
    @deal.post(
        lambda result: all(
            not term.endswith(tuple(string.whitespace)) for term in result
        )
    )
    def html_readable(self) -> tuple[str, str]:
        """Render text from HTML, using python-readability."""
        readable_doc = readability.parse(self.text())

        title: str = readable_doc.title.strip(string.whitespace)
        summary: str = readable_doc.text_content.strip(string.whitespace)

        return title, summary

    @deal.pure
    @deal.post(lambda result: not result.startswith(tuple(string.whitespace)))
    @deal.post(lambda result: not result.endswith(tuple(string.whitespace)))
    def pdf(self) -> str:
        """Render text from PDF."""
        return extract_text(io.BytesIO(self._data)).strip(string.whitespace)
