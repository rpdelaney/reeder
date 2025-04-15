"""Provide content handling."""

import io

import readability
from bs4 import BeautifulSoup as Bs
from pdftotext import PDF


class ContentRenderer:
    """Provide rendering for various document types."""

    def __init__(self, data: bytes) -> None:
        """Initialize a renderer."""
        self._data: bytes = data

    @property
    def data(self) -> bytes:
        """Provide read-only access to the data."""
        return self._data

    def render_text(self) -> str:
        """Render text from... text."""
        return self._data.decode(encoding="utf-8", errors="replace")

    def render_html(self, *, make_readable: bool = True) -> str:
        """Render text from HTML.

        If make_readable is True, try to extract the text content with
        pyreadability.
        """
        soup = Bs(self._data, "html.parser")
        doctext = soup.get_text()
        if make_readable:
            readable_doc = readability.Document(doctext)
            title: str = readable_doc.short_title()
            summary: str = Bs(readable_doc.summary(), "lxml").text
            return f"{title}\n{summary}"
        return doctext

    def render_pdf(self) -> str:
        """Render text from PDF."""
        return "\n\n".join(PDF(io.BytesIO(self._data)))
