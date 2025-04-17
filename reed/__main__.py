"""Do the business."""

import sys

import click
import deal
import httpx

from reed.content import ContentRenderer
from reed.web import fetch


@deal.has("stdout")
@deal.raises(RuntimeError, httpx.RequestError, httpx.TimeoutException)
@click.command()
@click.argument("target")
def main(target: str) -> int:
    """Texitfy a URL."""
    webclient = httpx.Client()

    response = fetch(webclient, httpx.URL(target))
    renderer = ContentRenderer(data=response.content)
    content_type = response.headers.get("Content-Type").split(";")[0]

    match content_type:
        case "text/plain":
            print(renderer.render_text())
        case "text/html":
            print(renderer.render_html())
        case "application/pdf":
            print(renderer.render_pdf())
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
