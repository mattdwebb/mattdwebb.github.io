"""Check rendered internal links and local media references."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(values["href"])
        if tag in {"img", "script", "source"} and values.get("src"):
            self.links.append(values["src"])


def resolve_target(site: Path, page: Path, raw_link: str) -> Path | None:
    parsed = urlsplit(raw_link)
    if parsed.scheme or parsed.netloc or raw_link.startswith(("mailto:", "tel:", "#", "data:")):
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return page
    target = (site / path_text.lstrip("/")) if path_text.startswith("/") else (page.parent / path_text)
    if target.suffix == "":
        target = target / "index.html"
    return target.resolve()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", nargs="?", default="_site")
    args = parser.parse_args()
    site = Path(args.site).resolve()
    failures: list[str] = []
    pages = sorted(site.rglob("*.html"))
    if not pages:
        raise SystemExit(f"No rendered HTML files found in {site}")

    for page in pages:
        parser_obj = LinkParser()
        parser_obj.feed(page.read_text(encoding="utf-8", errors="replace"))
        for link in parser_obj.links:
            target = resolve_target(site, page, link)
            if target is not None and not target.exists():
                failures.append(f"{page.relative_to(site)} -> {link}")

    if failures:
        print("Broken internal links:")
        for failure in failures:
            print(f"  {failure}")
        return 1
    print(f"Checked {len(pages)} HTML pages: all internal links and local assets resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
