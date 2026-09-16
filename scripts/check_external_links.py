"""Check external links in a rendered Quarto site.

HTTP 404 and 410 responses are treated as broken. Access-control and rate-limit
responses are reported separately because many journal and profile sites reject
automated link checkers even when the URL works in a browser.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag
from urllib.request import Request, urlopen


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attribute in ("href", "src"):
            url = values.get(attribute) or ""
            if url.startswith(("https://", "http://")):
                self.urls.add(urldefrag(url).url)


def collect_urls(site_dir: Path) -> list[str]:
    parser = LinkParser()
    for page in site_dir.rglob("*.html"):
        parser.feed(page.read_text(encoding="utf-8"))
    return sorted(parser.urls)


def check(url: str) -> tuple[str, int | None, str]:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; academic-site-link-check/1.0)"}
    try:
        request = Request(url, headers=headers, method="HEAD")
        with urlopen(request, timeout=15) as response:
            return url, response.status, "ok"
    except HTTPError as error:
        if error.code == 405:
            try:
                request = Request(url, headers={**headers, "Range": "bytes=0-0"})
                with urlopen(request, timeout=15) as response:
                    return url, response.status, "ok"
            except HTTPError as retry_error:
                error = retry_error
            except URLError as retry_error:
                return url, None, str(retry_error.reason)
        status = "broken" if error.code in {404, 410} else "blocked"
        return url, error.code, status
    except URLError as error:
        return url, None, str(error.reason)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_dir", nargs="?", default="_site", type=Path)
    args = parser.parse_args()

    urls = collect_urls(args.site_dir)
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(check, urls))

    broken = [result for result in results if result[2] == "broken"]
    warnings = [result for result in results if result[2] not in {"ok", "broken"}]
    ok = len(results) - len(broken) - len(warnings)

    for url, status, reason in broken:
        print(f"BROKEN {status}: {url}")
    for url, status, reason in warnings:
        print(f"WARNING {status or '-'} ({reason}): {url}")
    print(f"Checked {len(results)} external URLs: {ok} reachable, "
          f"{len(warnings)} blocked/unresolved, {len(broken)} broken.")
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
