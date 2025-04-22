"""Do the business."""

import sys

import click
import deal
import httpx

from reed.content import ContentRenderer
from reed.web import fetch, is_url


deal.activate()
deal.module_load(deal.pure)


@deal.has("stdout", "network")
@deal.raises(
    RuntimeError,
    NotImplementedError,
    httpx.RequestError,
    httpx.TimeoutException,
)
@click.command()
@click.argument("target")
def main(target: str) -> int:
    """Texitfy content found at TARGET. TARGET can be a URL or a file path."""
    if not is_url(target):
        msg = (
            "TARGET must be a URL accessible via networking. "
            "Local filesystem is not yet supported."
        )
        raise NotImplementedError(msg)

    webclient = httpx.Client()

    response = fetch(webclient, httpx.URL(target))
    renderer = ContentRenderer(data=response.content)
    content_type = response.headers.get("Content-Type").split(";")[0]

    match content_type:
        case "text/plain":
            print(renderer.text())
        case "text/html":
            print(renderer.html_readable())
        case "application/pdf":
            print(renderer.pdf())
        case _:
            msg = (
                "Unsupported Content-Type: "
                f"{response.headers.get('Content-Type')}"
            )
            raise RuntimeError(msg)

    return 0


if __name__ == "__main__":
    try:
        exit_status = main()
    except Exception as e:  # noqa: BLE001
        print("An unhandled exception occurred: ", e, file=sys.stderr)
        exit_status = 1
    sys.exit(exit_status)
