"""Fetch video subtitles from a remote source."""

import contextlib
import tempfile
from pathlib import Path

import deal
import httpx
import yt_dlp
from yt_dlp.extractor import gen_extractors  # type: ignore[attr-defined]
from yt_dlp.utils import DownloadError


@deal.pure
def has_extractor(url: httpx.URL) -> bool:
    """Check if the provided URL is supported by any yt_dlp extractor."""
    return any(
        # The generic extractor always returns suitable, even
        # when it won't run on the URL.
        extractor.suitable(str(url)) and extractor.IE_NAME != "generic"
        for extractor in gen_extractors()
    )


@deal.raises(DownloadError)
def get_subtitles(url: httpx.URL) -> bytes:
    """Extract automatic subtitles from a video URL using yt_dlp."""
    if not has_extractor(url):
        return b""

    class YtLogger:
        """Don't log anything from yt_dlp except errors."""

        def debug(self, msg: str) -> None:
            pass

        def warning(self, msg: str) -> None:
            pass

        def error(self, msg: str) -> None:
            print(msg)

    temp_dir = tempfile.TemporaryDirectory()
    ydl_opts = {
        "skip_download": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "logger": YtLogger(),
        "outtmpl": str(Path(temp_dir.name) / Path("%(id)s.%(ext)s")),
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
        info_dict = ydl.extract_info(str(url))
        video_id = info_dict.get("id")
        subs_filename = Path(temp_dir.name) / Path(f"{video_id}.en.vtt")

    subtitles = ""
    with (
        contextlib.suppress(FileNotFoundError),
        Path.open(subs_filename, encoding="utf-8") as file,
    ):
        subtitles = file.read()

    return subtitles.encode() if subtitles else b""
