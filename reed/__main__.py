"""Do the business."""

import fileinput
import sys
import urllib.parse

import httpx
import yt_dlp
from bs4 import BeautifulSoup as Bs
from pdftotext import PDF
from readability import Document
from yt_dlp.utils import DownloadError


def main() -> int:
    """Texitfy a URL."""
    with fileinput.input() as data:
        if not data:
            return 1
        for line in data:
            print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
