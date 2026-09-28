"""Generate Quarto pages from the site's structured JSON data."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def write_if_changed(path: Path, content: str) -> None:
    content = content.rstrip() + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8", newline="\n")


def md_link(label: str, url: str) -> str:
    return f"[{label}]({url})"


def render_research() -> str:
    data = load_json("research.json")
    out = [
        "---",
        'title: "Research"',
        'description: "Current and published research in econometrics, causal inference, machine learning, and applied microeconomics."',
        "toc: true",
        'toc-title: "On this page"',
        "---",
        "",
        "<!-- Generated from data/research.json by scripts/generate_pages.py. -->",
        "",
        "Current projects are grouped by research program.",
        "",
        "# Current Research",
    ]

    current_items = [item for item in data["current"] if item.get("public", True)]
    categories = []
    for item in current_items:
        if item["category"] not in categories:
            categories.append(item["category"])

    for category in categories:
        out.extend(["", f"## {category}"])
        for item in [x for x in current_items if x["category"] == category]:
            out.extend(["", "::: {.research-item}", f"### {item['title']}"])
            if item.get("authors"):
                out.append(f"<p class=\"authors\">{html.escape(item['authors'])}</p>")
            out.append(f"<p class=\"status-line\">{html.escape(item['status'])}</p>")
            out.extend(["", item["summary"]])
            if item.get("links"):
                out.extend(["", " · ".join(md_link(x["label"], x["url"]) for x in item["links"])])
            out.append(":::")

    out.extend(["", "# Published Research"])
    main_papers = [item for item in data["published"] if item["group"] != "Meta Papers"]
    meta_papers = [item for item in data["published"] if item["group"] == "Meta Papers"]
    for item in sorted(main_papers, key=lambda x: x["year"], reverse=True):
        out.extend(["", "::: {.publication-entry}", f"### {item['title']}"])
        out.append(f"<p class=\"authors\">{html.escape(item['authors'])}</p>")
        out.append(f"<p class=\"publication-venue\">{html.escape(item['venue'])} ({item['year']})</p>")
        links = []
        if item.get("url"):
            links.append(md_link("Published version", item["url"]))
        if item.get("working_paper"):
            links.append(md_link("Working paper", item["working_paper"]))
        if item.get("preprint"):
            links.append(md_link("Preprint", item["preprint"]))
        if item.get("video"):
            links.append(md_link("Watch video", item["video"]))
        if links:
            out.extend(["", " · ".join(links)])
        out.append(":::")

    if meta_papers:
        out.extend(["", "## Meta Papers"])
        for item in sorted(meta_papers, key=lambda x: x["year"], reverse=True):
            out.extend(["", "::: {.publication-entry}", f"### {item['title']}"])
            out.append(f"<p class=\"authors\">{html.escape(item['authors'])}</p>")
            out.append(f"<p class=\"publication-venue\">{html.escape(item['venue'])} ({item['year']})</p>")
            links = []
            if item.get("url"):
                links.append(md_link("Published version", item["url"]))
            if item.get("working_paper"):
                links.append(md_link("Working paper", item["working_paper"]))
            if item.get("preprint"):
                links.append(md_link("Preprint", item["preprint"]))
            if item.get("video"):
                links.append(md_link("Watch video", item["video"]))
            if links:
                out.extend(["", " · ".join(links)])
            out.append(":::")
    return "\n".join(out)


def render_software() -> str:
    families = load_json("software.json")
    out = [
        "---",
        'title: "Research Software"',
        'description: "Econometric software organized by method and package family, with installation information and implementation authorship."',
        "toc: true",
        'toc-title: "Software families"',
        "---",
        "",
        "<!-- Generated from data/software.json by scripts/generate_pages.py. -->",
    ]
    for family in families:
        out.extend(["", f"## {family['name']} {{#{family['id']}}}", "", family["description"]])
        out.extend(["", "### Implementations"])
        for impl in family["implementations"]:
            display = impl.get("name") or family["name"]
            badge = html.escape(impl["registry"])
            out.extend([
                "",
                "::: {.implementation}",
                f"#### {display} — {impl['language']} <span class=\"registry-pill\">{badge}</span>",
                "",
                f"**Implementation:** {impl['implementer']}<br>",
                f"**Role:** {impl['role']}",
                "",
            ])
            paper_url = family["paper"].get("published_url") or family["paper"].get("url") or family["paper"].get("working_url")
            links = []
            if paper_url:
                links.append(md_link("Paper", paper_url))
            links.extend([md_link("Documentation", impl["docs"]), md_link("GitHub", impl["repository"])])
            video_url = impl.get("video") or family.get("video")
            if video_url:
                links.append(md_link("Video", video_url))
            if impl.get("registry_url"):
                links.append(md_link(impl["registry"], impl["registry_url"]))
            out.append(" · ".join(links))
            if impl.get("install"):
                language = {"Stata": "stata", "R": "r", "Julia": "julia", "Python": "bash"}.get(impl["language"], "text")
                out.extend(["", "**Install**", "", f"```{language}", impl["install"], "```"])
            else:
                out.extend(["", "<p class=\"link-note\">No package-manager installation is documented; use the upstream repository files directly.</p>"])
            out.append(":::")
        out.extend([
            "",
            "### Associated paper",
            "",
            family["paper"]["citation"],
            "",
        ])
        paper_links = []
        if family["paper"].get("published_url"):
            paper_links.append(md_link("Published version", family["paper"]["published_url"]))
        if family["paper"].get("working_url"):
            paper_links.append(md_link("Working paper", family["paper"]["working_url"]))
        if not paper_links and family["paper"].get("url"):
            paper_links.append(md_link("Paper", family["paper"]["url"]))
        if paper_links:
            out.extend([" · ".join(paper_links), ""])
        out.extend([
            "### How to cite",
            "",
            family["cite"],
            "",
            "---",
        ])
    return "\n".join(out)


def render_videos() -> str:
    videos = load_json("videos.json")
    out = [
        "---",
        'title: "Videos"',
        'description: "Research and software videos on econometrics, causal inference, and related projects."',
        "---",
        "",
        "<!-- Generated from data/videos.json by scripts/generate_pages.py. -->",
        "",
        "[View the MattWebbEcon channel on YouTube](https://youtube.com/@MattWebbEcon).",
        "",
        "::: {.video-grid}",
    ]
    for video in videos:
        url = f"https://www.youtube.com/watch?v={video['id']}"
        thumb = f"https://i.ytimg.com/vi/{video['id']}/hqdefault.jpg"
        alt = html.escape(f"Thumbnail for {video['title']}", quote=True)
        out.extend([
            "::: {.video-card}",
            f"[<img src=\"{thumb}\" alt=\"{alt}\" loading=\"lazy\" width=\"480\" height=\"360\">]({url})",
            "",
            f"### {video['title']}",
            "",
            video["description"],
            "",
            f"[Watch on YouTube]({url}) · [{video['related_label']}]({video['related_url']})",
            ":::",
        ])
    out.append(":::")
    return "\n".join(out)


def main() -> None:
    write_if_changed(ROOT / "research.qmd", render_research())
    write_if_changed(ROOT / "software.qmd", render_software())
    write_if_changed(ROOT / "videos.qmd", render_videos())


if __name__ == "__main__":
    main()
