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
        'description: "Current and published research by Matthew D. Webb in econometrics, causal inference, machine learning, and applied microeconomics."',
        "toc: true",
        'toc-title: "On this page"',
        "---",
        "",
        "<!-- Generated from data/research.json by scripts/generate_pages.py. -->",
        "",
        "Current projects appear first. Publication status follows the current CV; public links are included only where verified.",
        "",
        "# Current Research",
    ]

    categories = []
    for item in data["current"]:
        if item["category"] not in categories:
            categories.append(item["category"])

    for category in categories:
        out.extend(["", f"## {category}"])
        for item in [x for x in data["current"] if x["category"] == category]:
            out.extend(["", "::: {.research-item}", f"### {item['title']}"])
            if item.get("authors"):
                out.append(f"<p class=\"authors\">{html.escape(item['authors'])}</p>")
            out.append(f"<p class=\"status-line\">{html.escape(item['status'])}</p>")
            out.extend(["", item["summary"]])
            if item.get("links"):
                out.extend(["", " · ".join(md_link(x["label"], x["url"]) for x in item["links"])])
            if item.get("link_note"):
                out.extend(["", f"<p class=\"link-note\">{html.escape(item['link_note'])}</p>"])
            out.append(":::")

    out.extend(["", "# Published Research"])
    groups = []
    for item in data["published"]:
        if item["group"] not in groups:
            groups.append(item["group"])
    for group in groups:
        out.extend(["", f"## {group}"])
        for item in [x for x in data["published"] if x["group"] == group]:
            out.extend(["", "::: {.publication-entry}", f"### {item['title']}"])
            out.append(f"<p class=\"authors\">{html.escape(item['authors'])}</p>")
            out.append(f"<p class=\"publication-venue\">{html.escape(item['venue'])} ({item['year']})</p>")
            links = []
            if item.get("url"):
                links.append(md_link("Article", item["url"]))
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
        'description: "A method-first guide to econometric software associated with Matthew D. Webb\'s research, with verified installation channels and transparent implementation credit."',
        "toc: true",
        'toc-title: "Software families"',
        "---",
        "",
        "<!-- Generated from data/software.json by scripts/generate_pages.py. -->",
        "",
        "This page is organized by research method rather than repository. Registry labels and installation commands are shown at the implementation level. Forked repositories are linked to their upstream authors so implementation credit remains explicit.",
    ]
    for family in families:
        out.extend(["", f"## {family['name']} {{#{family['id']}}}", "", family["description"]])
        if family.get("video"):
            out.extend(["", md_link("Watch video", family["video"])])
        out.extend(["", "### Implementations"])
        for impl in family["implementations"]:
            display = impl.get("name") or family["name"]
            badge = html.escape(impl["registry"])
            out.extend([
                "",
                "::: {.implementation}",
                f"#### {display} — {impl['language']} <span class=\"registry-pill\">{badge}</span>",
                "",
                f"**Implementation:** {impl['implementer']}  ",
                f"**Role:** {impl['role']}",
                "",
            ])
            links = [md_link("GitHub", impl["repository"]), md_link("Documentation", impl["docs"])]
            if impl.get("registry_url"):
                links.insert(0, md_link(impl["registry"], impl["registry_url"]))
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
            f"[{family['paper']['citation']}]({family['paper']['url']})",
            "",
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
        'description: "Short research and econometrics videos from Matthew D. Webb, with links to the associated papers and software."',
        "---",
        "",
        "<!-- Generated from data/videos.json by scripts/generate_pages.py. -->",
        "",
        "Short research explainers and software-oriented introductions from [MattWebbEcon on YouTube](https://youtube.com/@MattWebbEcon). Thumbnails link to YouTube; no tracking-heavy iframe wall is embedded on this page.",
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
