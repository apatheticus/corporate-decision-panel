#!/usr/bin/env python3
"""
Build script for producing Results PDF and Session Capsule PDF.

Results PDF: Print-quality rendering of the distribution page (index.html).
Capsule PDF: Comprehensive layered archive of the full session.
"""

import base64
import glob
import os
import re
import sys
from pathlib import Path

import markdown
import weasyprint


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SESSION_DIR = Path(__file__).resolve().parent.parent
BUILD_DIR = SESSION_DIR / "build"
INDEX_HTML = SESSION_DIR / "index.html"
IMAGES_DIR = SESSION_DIR / "images"
SESSION_DATA = SESSION_DIR / "session"

RESULTS_PDF = SESSION_DIR / "RESULTS_team-of-teams.pdf"
CAPSULE_PDF = SESSION_DIR / "CAPSULE_team-of-teams.pdf"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str:
    """Read a file and return its contents."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def image_to_data_uri(path: str) -> str:
    """Convert an image file path to a base64 data URI."""
    ext = Path(path).suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
    }
    mime = mime_map.get(ext, "application/octet-stream")
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{data}"


def resolve_image_path(src: str, base_dir: Path) -> str | None:
    """Resolve a relative or absolute image src to an actual file path."""
    if src.startswith("data:"):
        return None  # Already a data URI
    # Try relative to base_dir
    candidate = base_dir / src
    if candidate.exists():
        return str(candidate)
    # Try relative to session dir
    candidate = SESSION_DIR / src
    if candidate.exists():
        return str(candidate)
    return None


def embed_images_in_html(html: str, base_dir: Path) -> str:
    """Replace image src attributes with base64 data URIs."""
    def replace_src(match):
        prefix = match.group(1)
        src = match.group(2)
        resolved = resolve_image_path(src, base_dir)
        if resolved:
            data_uri = image_to_data_uri(resolved)
            return f'{prefix}"{data_uri}"'
        return match.group(0)

    # Match src="..." in img tags
    html = re.sub(r'(src=)"([^"]+)"', replace_src, html)
    html = re.sub(r"(src=)'([^']+)'", replace_src, html)

    # Also handle CSS url() references
    def replace_css_url(match):
        prefix = match.group(1)
        src = match.group(2)
        resolved = resolve_image_path(src, base_dir)
        if resolved:
            data_uri = image_to_data_uri(resolved)
            return f'{prefix}"{data_uri}")'
        return match.group(0)

    html = re.sub(r'(url\()(["\']?)([^)"\'"]+)\2\)', lambda m: (
        f'{m.group(1)}"{image_to_data_uri(r)}")'
        if (r := resolve_image_path(m.group(3), base_dir))
        else m.group(0)
    ), html)

    return html


def md_to_html(md_text: str) -> str:
    """Convert Markdown text to HTML."""
    extensions = ["tables", "fenced_code", "codehilite", "toc", "nl2br"]
    return markdown.markdown(md_text, extensions=extensions)


def strip_scripts(html: str) -> str:
    """Remove all <script> blocks from HTML."""
    return re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.IGNORECASE)


# ---------------------------------------------------------------------------
# Results PDF
# ---------------------------------------------------------------------------

PRINT_CSS = """
<style>
@page {
    size: A4;
    margin: 1.5cm 1.8cm;
}

/* Force visibility for scroll-reveal animations */
.reveal, [class*="reveal"], [data-reveal], [data-aos] {
    opacity: 1 !important;
    transform: none !important;
    visibility: visible !important;
    transition: none !important;
}

/* Disable animations and transitions */
*, *::before, *::after {
    animation: none !important;
    animation-delay: 0s !important;
    transition: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
}

/* Remove fixed/sticky positioning */
nav, header, .navbar, .nav, [class*="fixed"], [class*="sticky"] {
    position: static !important;
}

/* Print-friendly adjustments */
body {
    font-size: 11pt !important;
    line-height: 1.5 !important;
    color: #1a1a1a !important;
    background: white !important;
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Page break hints */
section, .section, [class*="section"] {
    page-break-inside: avoid;
    break-inside: avoid;
}

h1, h2, h3 {
    page-break-after: avoid;
    break-after: avoid;
}

/* Ensure images fit */
img {
    max-width: 100% !important;
    height: auto !important;
    page-break-inside: avoid;
}

/* Tables */
table {
    page-break-inside: avoid;
    font-size: 9pt;
}

/* Hide elements that don't print well */
.scroll-indicator, .scroll-top, [class*="scroll"] {
    display: none !important;
}

/* Links show URL */
a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 8pt;
    color: #666;
    word-break: break-all;
}

/* Code blocks */
pre, code {
    font-size: 9pt !important;
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
}
</style>
"""


def build_results_pdf():
    """Build the Results PDF from index.html."""
    print("Building Results PDF...")

    if not INDEX_HTML.exists():
        print(f"ERROR: {INDEX_HTML} not found")
        return False

    html = read_file(INDEX_HTML)

    # Strip scripts
    html = strip_scripts(html)

    # Embed images as data URIs
    html = embed_images_in_html(html, SESSION_DIR)

    # Inject print CSS before </head>
    if "</head>" in html:
        html = html.replace("</head>", PRINT_CSS + "\n</head>")
    else:
        html = PRINT_CSS + html

    # Write to PDF
    doc = weasyprint.HTML(string=html, base_url=str(SESSION_DIR))
    doc.write_pdf(str(RESULTS_PDF))

    print(f"  -> {RESULTS_PDF} ({RESULTS_PDF.stat().st_size:,} bytes)")
    return True


# ---------------------------------------------------------------------------
# Session Capsule PDF
# ---------------------------------------------------------------------------

CAPSULE_CSS = """
@page {
    size: A4;
    margin: 2cm 2cm;
    @bottom-center {
        content: counter(page);
        font-size: 9pt;
        color: #888;
    }
}

@page :first {
    margin: 0;
    @bottom-center { content: none; }
}

:root {
    --primary: #1a365d;
    --accent: #2b6cb0;
    --light: #ebf4ff;
    --text: #1a202c;
    --muted: #718096;
    --border: #e2e8f0;
    --success: #38a169;
    --warning: #d69e2e;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.6;
    color: var(--text);
    background: white;
}

/* Cover page */
.cover {
    page-break-after: always;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 50%, #3182ce 100%);
    color: white;
    padding: 3cm;
}

.cover h1 {
    font-size: 28pt;
    font-weight: 700;
    margin-bottom: 0.5em;
    letter-spacing: -0.5px;
}

.cover .subtitle {
    font-size: 14pt;
    font-weight: 300;
    margin-bottom: 2em;
    opacity: 0.9;
}

.cover .thesis {
    font-size: 12pt;
    font-style: italic;
    max-width: 80%;
    margin: 0 auto 2em;
    opacity: 0.85;
    line-height: 1.8;
}

.cover .date {
    font-size: 11pt;
    opacity: 0.7;
    margin-top: auto;
}

.cover .label {
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 3px;
    opacity: 0.5;
    margin-bottom: 0.5em;
}

/* Layer headers */
.layer-header {
    page-break-before: always;
    background: var(--primary);
    color: white;
    padding: 1.5cm 2cm;
    margin: -2cm -2cm 1.5cm -2cm;
}

.layer-header h2 {
    font-size: 20pt;
    font-weight: 700;
    margin-bottom: 0.3em;
}

.layer-header .layer-num {
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 2px;
    opacity: 0.7;
    margin-bottom: 0.5em;
}

.layer-header .layer-desc {
    font-size: 11pt;
    opacity: 0.85;
}

/* Content styling */
.content {
    padding: 0;
}

h1 {
    font-size: 18pt;
    color: var(--primary);
    margin: 1.5em 0 0.5em;
    padding-bottom: 0.3em;
    border-bottom: 2px solid var(--accent);
}

h2 {
    font-size: 15pt;
    color: var(--primary);
    margin: 1.2em 0 0.4em;
}

h3 {
    font-size: 12pt;
    color: var(--accent);
    margin: 1em 0 0.3em;
}

h4 {
    font-size: 11pt;
    color: var(--text);
    margin: 0.8em 0 0.3em;
}

p {
    margin: 0.5em 0;
    text-align: justify;
    hyphens: auto;
}

ul, ol {
    margin: 0.5em 0 0.5em 1.5em;
}

li {
    margin: 0.2em 0;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

th {
    background: var(--primary);
    color: white;
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
}

td {
    padding: 6px 10px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
}

tr:nth-child(even) td {
    background: #f7fafc;
}

/* Code blocks */
pre {
    background: #f7fafc;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    padding: 0.8em 1em;
    margin: 0.8em 0;
    font-size: 8.5pt;
    line-height: 1.5;
    white-space: pre-wrap;
    word-wrap: break-word;
    page-break-inside: avoid;
}

code {
    font-family: "SF Mono", "Fira Code", Menlo, monospace;
    font-size: 9pt;
    background: #edf2f7;
    padding: 1px 4px;
    border-radius: 3px;
}

pre code {
    background: none;
    padding: 0;
}

/* Block quotes */
blockquote {
    border-left: 4px solid var(--accent);
    margin: 1em 0;
    padding: 0.5em 1em;
    background: var(--light);
    font-style: italic;
}

/* Horizontal rules */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5em 0;
}

/* Document sections */
.document {
    margin-bottom: 2em;
    page-break-inside: avoid;
}

.document-title {
    font-size: 13pt;
    color: var(--primary);
    font-weight: 700;
    margin-bottom: 0.5em;
    padding: 0.5em 0;
    border-bottom: 1px solid var(--border);
}

.document-meta {
    font-size: 9pt;
    color: var(--muted);
    margin-bottom: 1em;
}

/* Images */
img {
    max-width: 100%;
    height: auto;
    margin: 1em auto;
    display: block;
    page-break-inside: avoid;
}

/* TOC */
.toc {
    margin: 1em 0;
}

.toc ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.toc li {
    padding: 0.3em 0;
    border-bottom: 1px dotted var(--border);
}

.toc .toc-layer {
    font-weight: 700;
    color: var(--primary);
    margin-top: 0.8em;
    font-size: 11pt;
}

.toc .toc-item {
    padding-left: 1.5em;
    font-size: 10pt;
}

/* Separator between documents */
.doc-separator {
    border: none;
    border-top: 2px solid var(--accent);
    margin: 2em 0;
}

/* Infographic images */
.infographic {
    text-align: center;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.infographic img {
    max-width: 90%;
    border: 1px solid var(--border);
    border-radius: 4px;
}

.infographic .caption {
    font-size: 9pt;
    color: var(--muted);
    margin-top: 0.5em;
}
"""


def collect_files(directory: Path, pattern: str = "*.md") -> list[Path]:
    """Collect files matching a pattern from a directory, sorted by name."""
    files = sorted(directory.glob(pattern))
    return files


def build_toc(sections: list[dict]) -> str:
    """Build a table of contents from section definitions."""
    html = '<div class="toc">\n<ul>\n'
    for section in sections:
        layer = section.get("layer", "")
        title = section.get("title", "")
        items = section.get("items", [])
        html += f'<li class="toc-layer">{layer}: {title}</li>\n'
        for item in items:
            html += f'<li class="toc-item">{item}</li>\n'
    html += "</ul>\n</div>\n"
    return html


def build_capsule_html() -> str:
    """Build the complete HTML for the Session Capsule PDF."""

    # ---- Read the vision doc for cover info ----
    vision_text = read_file(SESSION_DATA / "VISION_team-of-teams.md")
    session_summary = read_file(SESSION_DATA / "SESSION_SUMMARY.md")

    # Extract thesis line from vision
    thesis = "A Company OS that gives any founder, leader, or team the analytical power of a full executive committee -- with the structural integrity of mandated dissent."

    # ---- Cover Page ----
    cover = f"""
    <div class="cover">
        <div class="label">Session Capsule</div>
        <h1>Team of Teams Agent Skill</h1>
        <div class="subtitle">Comprehensive Design Vision for Organizational AI</div>
        <div class="thesis">{thesis}</div>
        <div class="date">Ideation Session -- February 22, 2026</div>
    </div>
    """

    # ---- Layer 1: Overview ----
    # Collect inventory of all content
    briefs = collect_files(SESSION_DATA / "briefs")
    idea_reports = collect_files(SESSION_DATA / "idea-reports")
    research_files = collect_files(SESSION_DATA / "research")
    snapshots = collect_files(SESSION_DATA / "snapshots")
    sources = collect_files(SESSION_DATA / "sources")
    images = sorted(IMAGES_DIR.glob("*.png")) + sorted(IMAGES_DIR.glob("*.jpg"))

    toc_sections = [
        {
            "layer": "Layer 1",
            "title": "Overview",
            "items": ["Table of Contents", "Content Inventory"],
        },
        {
            "layer": "Layer 2",
            "title": "Vision",
            "items": ["Vision Document: The Team of Teams Agent Skill"],
        },
        {
            "layer": "Layer 3",
            "title": "Exploration",
            "items": (
                [f.stem.replace("BRIEF_", "Brief: ").replace("-", " ").title() for f in briefs]
                + [f"Infographic: {f.stem}" for f in images]
                + [f.stem.replace("RESEARCH_", "Research: ").replace("-", " ").title() for f in research_files]
            ),
        },
        {
            "layer": "Layer 4",
            "title": "Origins",
            "items": [f.stem.replace("_", " ").title() for f in sources],
        },
        {
            "layer": "Layer 5",
            "title": "Process",
            "items": (
                ["Ideation Graph"]
                + [f.stem.replace("SNAPSHOT_", "Snapshot ") for f in snapshots]
                + [f.stem.replace("IDEA_", "Idea Report: ").replace("-", " ").title() for f in idea_reports]
                + ["Session Summary"]
            ),
        },
    ]

    inventory_table = """
    <h3>Content Inventory</h3>
    <table>
        <thead>
            <tr><th>Category</th><th>Count</th><th>Files</th></tr>
        </thead>
        <tbody>
    """
    inventory_items = [
        ("Vision Document", 1, "VISION_team-of-teams.md"),
        ("Idea Briefs", len(briefs), ", ".join(f.name for f in briefs)),
        ("Idea Reports", len(idea_reports), ", ".join(f.name for f in idea_reports)),
        ("Research Reports", len(research_files), ", ".join(f.name for f in research_files)),
        ("Infographics", len(images), ", ".join(f.name for f in images) if images else "(none yet)"),
        ("Snapshots", len(snapshots), ", ".join(f.name for f in snapshots)),
        ("Source Materials", len(sources), ", ".join(f.name for f in sources)),
        ("Session Summary", 1, "SESSION_SUMMARY.md"),
        ("Ideation Graph", 1, "ideation-graph.md"),
    ]
    for cat, count, files in inventory_items:
        inventory_table += f"<tr><td>{cat}</td><td>{count}</td><td style='font-size:8pt'>{files}</td></tr>\n"
    inventory_table += "</tbody></table>\n"

    layer1 = f"""
    <div class="layer-header">
        <div class="layer-num">Layer 1</div>
        <h2>Overview</h2>
        <div class="layer-desc">Navigation and content inventory for the session archive</div>
    </div>
    <div class="content">
        <h3>Table of Contents</h3>
        {build_toc(toc_sections)}
        {inventory_table}
    </div>
    """

    # ---- Layer 2: Vision ----
    vision_html = md_to_html(vision_text)

    layer2 = f"""
    <div class="layer-header">
        <div class="layer-num">Layer 2</div>
        <h2>Vision</h2>
        <div class="layer-desc">Core thesis, governing principles, pillars, design decisions, and boundaries</div>
    </div>
    <div class="content">
        {vision_html}
    </div>
    """

    # ---- Layer 3: Exploration ----
    layer3_content = ""

    # Briefs
    for brief_file in briefs:
        brief_text = read_file(brief_file)
        brief_html = md_to_html(brief_text)
        layer3_content += f"""
        <div class="document">
            <div class="document-meta">Source: {brief_file.name}</div>
            {brief_html}
        </div>
        <hr class="doc-separator">
        """

    # Infographic images
    for img_file in images:
        data_uri = image_to_data_uri(str(img_file))
        caption = img_file.stem.replace("_", " ").replace("-", " ").title()
        layer3_content += f"""
        <div class="infographic">
            <img src="{data_uri}" alt="{caption}">
            <div class="caption">{caption}</div>
        </div>
        <hr class="doc-separator">
        """

    # Research
    for research_file in research_files:
        research_text = read_file(research_file)
        research_html = md_to_html(research_text)
        layer3_content += f"""
        <div class="document">
            <div class="document-meta">Source: {research_file.name}</div>
            {research_html}
        </div>
        <hr class="doc-separator">
        """

    layer3 = f"""
    <div class="layer-header">
        <div class="layer-num">Layer 3</div>
        <h2>Exploration</h2>
        <div class="layer-desc">Idea briefs, infographic images, and research findings</div>
    </div>
    <div class="content">
        {layer3_content}
    </div>
    """

    # ---- Layer 4: Origins ----
    layer4_content = ""
    for source_file in sources:
        source_text = read_file(source_file)
        if source_file.suffix == ".md":
            source_html = md_to_html(source_text)
        else:
            source_html = f"<pre>{source_text}</pre>"
        layer4_content += f"""
        <div class="document">
            <div class="document-title">{source_file.name}</div>
            <div class="document-meta">Original source material</div>
            {source_html}
        </div>
        <hr class="doc-separator">
        """

    layer4 = f"""
    <div class="layer-header">
        <div class="layer-num">Layer 4</div>
        <h2>Origins</h2>
        <div class="layer-desc">Original user request and all captured source materials</div>
    </div>
    <div class="content">
        {layer4_content}
    </div>
    """

    # ---- Layer 5: Process ----
    layer5_content = ""

    # Ideation graph
    graph_text = read_file(SESSION_DATA / "ideation-graph.md")
    graph_html = md_to_html(graph_text)
    layer5_content += f"""
    <div class="document">
        <div class="document-title">Ideation Graph</div>
        <div class="document-meta">Living document updated in real-time during the session</div>
        {graph_html}
    </div>
    <hr class="doc-separator">
    """

    # Snapshots
    for snap_file in snapshots:
        snap_text = read_file(snap_file)
        snap_html = md_to_html(snap_text)
        layer5_content += f"""
        <div class="document">
            <div class="document-meta">Source: {snap_file.name}</div>
            {snap_html}
        </div>
        <hr class="doc-separator">
        """

    # Idea Reports
    for report_file in idea_reports:
        report_text = read_file(report_file)
        report_html = md_to_html(report_text)
        layer5_content += f"""
        <div class="document">
            <div class="document-meta">Source: {report_file.name}</div>
            {report_html}
        </div>
        <hr class="doc-separator">
        """

    # Session Summary
    summary_html = md_to_html(session_summary)
    layer5_content += f"""
    <div class="document">
        <div class="document-title">Session Summary</div>
        {summary_html}
    </div>
    """

    layer5 = f"""
    <div class="layer-header">
        <div class="layer-num">Layer 5</div>
        <h2>Process</h2>
        <div class="layer-desc">Ideation graph, snapshots, idea reports, and session summary</div>
    </div>
    <div class="content">
        {layer5_content}
    </div>
    """

    # ---- Assemble full HTML ----
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Session Capsule: Team of Teams Agent Skill</title>
    <style>
        {CAPSULE_CSS}
    </style>
</head>
<body>
    {cover}
    {layer1}
    {layer2}
    {layer3}
    {layer4}
    {layer5}
</body>
</html>
"""
    return full_html


def build_capsule_pdf():
    """Build the Session Capsule PDF."""
    print("Building Capsule PDF...")

    html = build_capsule_html()

    # Embed any images referenced in the HTML
    html = embed_images_in_html(html, SESSION_DIR)

    # Write to PDF
    doc = weasyprint.HTML(string=html, base_url=str(SESSION_DIR))
    doc.write_pdf(str(CAPSULE_PDF))

    print(f"  -> {CAPSULE_PDF} ({CAPSULE_PDF.stat().st_size:,} bytes)")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("PDF Build Script")
    print(f"Session: {SESSION_DIR}")
    print("=" * 60)

    results_ok = False
    capsule_ok = False

    # Build Results PDF (requires index.html)
    if INDEX_HTML.exists():
        results_ok = build_results_pdf()
    else:
        print(f"SKIP: Results PDF -- {INDEX_HTML} does not exist yet")

    # Build Capsule PDF
    capsule_ok = build_capsule_pdf()

    print()
    print("=" * 60)
    print("Build Summary:")
    print(f"  Results PDF: {'OK' if results_ok else 'SKIPPED/FAILED'}")
    print(f"  Capsule PDF: {'OK' if capsule_ok else 'FAILED'}")
    print("=" * 60)

    if not results_ok or not capsule_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
