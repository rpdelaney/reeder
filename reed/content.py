"""Provide content handling."""

import io

import deal
import readability
from bs4 import BeautifulSoup as Bs
from pdftotext import PDF


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
    def render_text(self) -> str:
        """Render text from... text."""
        return self._data.decode(encoding="utf-8", errors="replace")

    @deal.pure
    def render_html(self, *, make_readable: bool = True) -> str:
        """Render text from HTML.

        If make_readable is True, try to extract the text content with
        python-readability.
        """
        if not make_readable:
            soup = Bs(self._data, "html.parser")
            return soup.get_text()

        readable_doc = readability.parse(self.render_text())
        title: str = readable_doc.title
        summary: str = readable_doc.text_content
        return f"{title}\n{summary}"

    @deal.pure
    def render_pdf(self) -> str:
        """Render text from PDF."""
        return "\n\n".join(PDF(io.BytesIO(self._data)))
