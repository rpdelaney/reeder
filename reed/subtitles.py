"""Fetch video subtitles from a remote source."""

import deal
import httpx
from yt_dlp.extractor import gen_extractors  # type: ignore[attr-defined]


@deal.pure
def has_extractor(url: httpx.URL) -> bool:
    """Check if the provided URL is supported by any yt_dlp extractor."""
    return any(
        # The generic extractor always returns suitable, even
        # when it won't run on the URL.
        extractor.suitable(str(url)) and extractor.IE_NAME != "generic"
        for extractor in gen_extractors()
    )
