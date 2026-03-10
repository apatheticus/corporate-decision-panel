#!/usr/bin/env python3
"""
Native Results PDF generator for the Corporate Decision Panel.

Generates RESULTS_<issue-slug>.pdf directly from RECORD.md using reportlab,
bypassing the lossy weasyprint HTML-to-PDF conversion. Produces a professionally
styled print-optimized PDF with proper page break control and image embedding.

Usage:
    python3 -m scripts.build_results_pdf --session-dir .cdp-output/2026-03-07_example/

Requires: reportlab, Pillow
"""

import argparse
import os
import re
import sys
import textwrap
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        Image,
        KeepTogether,
        ListFlowable,
        ListItem,
        NextPageTemplate,
        PageBreak,
        PageTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError:
    print("ERROR: reportlab is not installed. Run: pip install reportlab")
    sys.exit(1)

try:
    from PIL import Image as PILImage
except ImportError:
    PILImage = None

# ---------------------------------------------------------------------------
# Color palettes by decision type (matches HTML spec)
# ---------------------------------------------------------------------------
PALETTES = {
    "Strategic": {
        "primary": colors.HexColor("#1B2A4A"),       # navy
        "accent": colors.HexColor("#C5972C"),         # gold
        "light_bg": colors.HexColor("#F5F3EE"),       # warm cream
        "badge_bg": colors.HexColor("#1B2A4A"),
        "badge_fg": colors.white,
    },
    "Financial": {
        "primary": colors.HexColor("#1A3A5C"),       # deep blue
        "accent": colors.HexColor("#2D8A4E"),         # green
        "light_bg": colors.HexColor("#EFF6F0"),
        "badge_bg": colors.HexColor("#1A3A5C"),
        "badge_fg": colors.white,
    },
    "Operational": {
        "primary": colors.HexColor("#2D6A2E"),       # green
        "accent": colors.HexColor("#4A90D9"),         # blue
        "light_bg": colors.HexColor("#EFF6EF"),
        "badge_bg": colors.HexColor("#2D6A2E"),
        "badge_fg": colors.white,
    },
    "Technical": {
        "primary": colors.HexColor("#5B2D8E"),       # purple
        "accent": colors.HexColor("#2AA198"),         # teal
        "light_bg": colors.HexColor("#F3EFF8"),
        "badge_bg": colors.HexColor("#5B2D8E"),
        "badge_fg": colors.white,
    },
    "Personnel": {
        "primary": colors.HexColor("#1A7A7A"),       # teal
        "accent": colors.HexColor("#C5972C"),         # gold
        "light_bg": colors.HexColor("#EFF7F7"),
        "badge_bg": colors.HexColor("#1A7A7A"),
        "badge_fg": colors.white,
    },
    "Compliance": {
        "primary": colors.HexColor("#8B1A1A"),       # deep red
        "accent": colors.HexColor("#5A6978"),         # slate
        "light_bg": colors.HexColor("#F8F0F0"),
        "badge_bg": colors.HexColor("#8B1A1A"),
        "badge_fg": colors.white,
    },
}
DEFAULT_PALETTE = PALETTES["Strategic"]

RECOMMENDATION_COLORS = {
    "approve": colors.HexColor("#2D8A4E"),
    "conditions": colors.HexColor("#D4A017"),
    "oppose": colors.HexColor("#C0392B"),
    "neutral": colors.HexColor("#7F8C8D"),
}


# ---------------------------------------------------------------------------
# RECORD.md parser
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from RECORD.md without pyyaml dependency."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    meta = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(\w+):\s*(.+)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            # Strip quotes
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            # Parse lists
            if val.startswith("[") and val.endswith("]"):
                items = val[1:-1].split(",")
                val = [i.strip().strip("'\"") for i in items if i.strip()]
            meta[key] = val
    return meta


def parse_body(text: str) -> dict:
    """Parse RECORD.md body into structured sections.

    Returns dict with keys:
        executive_summary: str
        sections: dict[int, dict] where each section has 'title' and 'content'
    """
    # Strip frontmatter
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)

    # Extract executive summary (text before first numbered section)
    exec_match = re.search(r"^EXECUTIVE SUMMARY\s*\n(.*?)(?=\n\d+\.\s+[A-Z])", body, re.DOTALL)
    exec_summary = exec_match.group(1).strip() if exec_match else ""

    # Split on numbered sections: "1. TITLE", "2. TITLE", etc.
    section_pattern = re.compile(r"^(\d+)\.\s+([A-Z][A-Z &/\-\(\)]+)\s*$", re.MULTILINE)
    matches = list(section_pattern.finditer(body))

    sections = {}
    for i, m in enumerate(matches):
        num = int(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        sections[num] = {"title": title, "content": content}

    return {"executive_summary": exec_summary, "sections": sections}


def parse_domain_analyses(content: str, section_num: int = 3) -> list:
    """Parse Domain Analyses section into individual domain entries."""
    # Split on "N.X Role -- Description" pattern
    pattern = re.compile(
        rf"^{section_num}\.(\d+)\s+(.+?)$",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(content))
    domains = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        block = content[start:end].strip()

        # Extract fields
        title = m.group(2).strip()
        rec_match = re.search(r"Domain Recommendation:\s*(.+)", block)
        conf_match = re.search(r"Confidence Level:\s*(.+)", block)
        summary_match = re.search(r"Summary:\s*(.+?)(?=\n\n|\n    Team Lead|\n    Key Risks)", block, re.DOTALL)

        recommendation = rec_match.group(1).strip() if rec_match else ""
        confidence = conf_match.group(1).strip() if conf_match else ""
        summary = summary_match.group(1).strip() if summary_match else ""

        # Extract team lead findings table
        tl_match = re.search(r"Team Lead Findings:\s*\n(.*?)(?=\n\n    Key Risks|\n    Key Opportunities|\n    Internal Contradictions|$)", block, re.DOTALL)
        team_leads = []
        if tl_match:
            for row in re.finditer(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*([HML])\s*\|", tl_match.group(1)):
                name = row.group(1).strip()
                if name.startswith("---") or name == "Team Lead":
                    continue
                team_leads.append({
                    "name": name,
                    "finding": row.group(2).strip(),
                    "confidence": row.group(3).strip(),
                })

        # Extract key risks
        risks = []
        risk_match = re.search(rf"Key Risks:\s*\n(.*?)(?=\n    Key Opportunities|\n    Internal|\n\n{section_num}\.|\Z)", block, re.DOTALL)
        if risk_match:
            risks = [line.strip().lstrip("- ") for line in risk_match.group(1).splitlines() if line.strip().startswith("-")]

        # Extract key opportunities
        opps = []
        opp_match = re.search(rf"Key Opportunities:\s*\n(.*?)(?=\n    Internal|\n\n{section_num}\.|\Z)", block, re.DOTALL)
        if opp_match:
            opps = [line.strip().lstrip("- ") for line in opp_match.group(1).splitlines() if line.strip().startswith("-")]

        domains.append({
            "title": title,
            "recommendation": recommendation,
            "confidence": confidence,
            "summary": summary,
            "team_leads": team_leads,
            "risks": risks,
            "opportunities": opps,
        })

    return domains


def parse_fault_lines(content: str) -> dict:
    """Parse Fault Line Analysis section into structured data."""
    result = {"agreements": [], "contentions": [], "premortems": [], "tensions": []}

    # Points of Agreement
    agree_match = re.search(r"Points of Agreement:\s*\n(.*?)(?=\nPoints of Contention:|\Z)", content, re.DOTALL)
    if agree_match:
        result["agreements"] = [
            line.strip().lstrip("- ")
            for line in agree_match.group(1).splitlines()
            if line.strip().startswith("-")
        ]

    # Points of Contention
    contention_match = re.search(r"Points of Contention:\s*\n(.*?)(?=\nPre-Mortem Findings:|\Z)", content, re.DOTALL)
    if contention_match:
        result["contentions"] = [
            line.strip().lstrip("- ")
            for line in contention_match.group(1).splitlines()
            if line.strip().startswith("-")
        ]

    # Pre-Mortem Findings table
    pm_match = re.search(r"Pre-Mortem Findings:\s*\n(.*?)(?=\nUnresolved Tensions:|\Z)", content, re.DOTALL)
    if pm_match:
        for row in re.finditer(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|", pm_match.group(1)):
            role = row.group(1).strip()
            if role.startswith("---") or role == "C-Suite Role":
                continue
            result["premortems"].append({
                "role": role,
                "failure_mode": row.group(2).strip(),
                "severity": row.group(3).strip(),
            })

    # Unresolved Tensions
    tension_match = re.search(r"Unresolved Tensions:\s*\n(.*?)$", content, re.DOTALL)
    if tension_match:
        result["tensions"] = [
            line.strip().lstrip("- ")
            for line in tension_match.group(1).splitlines()
            if line.strip().startswith("-")
        ]

    return result


def parse_decision(content: str) -> dict:
    """Parse Section 7 (CEO Decision) into structured data."""
    result = {}

    # Decision statement
    dec_match = re.search(r"^Decision:\s*\n(.*?)(?=\nMost Determinative|\Z)", content, re.DOTALL)
    if dec_match:
        result["statement"] = dec_match.group(1).strip()

    # Most determinative perspective
    det_match = re.search(r"Most Determinative Perspective:\s*(\w[\w\s]*)\n(.*?)(?=\nDecision Weight Rationale:|\Z)", content, re.DOTALL)
    if det_match:
        result["determinative_role"] = det_match.group(1).strip()
        result["determinative_rationale"] = det_match.group(2).strip()

    # Decision Weight Rationale
    weight_match = re.search(r"Decision Weight Rationale:\s*\n(.*?)(?=\nConditions & Guardrails:|\Z)", content, re.DOTALL)
    if weight_match:
        result["weight_rationale"] = weight_match.group(1).strip()

    # Conditions & Guardrails
    cond_match = re.search(r"Conditions & Guardrails:\s*\n(.*?)(?=\nAccepted Risks:|\Z)", content, re.DOTALL)
    if cond_match:
        result["conditions"] = cond_match.group(1).strip()

    # Accepted Risks
    risk_match = re.search(r"Accepted Risks:\s*\n(.*?)(?=\nMitigations Directed:|\Z)", content, re.DOTALL)
    if risk_match:
        result["accepted_risks"] = [
            line.strip().lstrip("- ")
            for line in risk_match.group(1).splitlines()
            if line.strip().startswith("-")
        ]

    # Mitigations
    mit_match = re.search(r"Mitigations Directed:\s*\n(.*?)$", content, re.DOTALL)
    if mit_match:
        result["mitigations"] = [
            line.strip().lstrip("- ")
            for line in mit_match.group(1).splitlines()
            if line.strip().startswith("-")
        ]

    return result


def parse_dissenting_views(content: str, section_num: int = 6) -> list:
    """Parse Dissenting Views section into structured data."""
    pattern = re.compile(rf"^{section_num}\.(\d+)\s+(.+?)$", re.MULTILINE)
    matches = list(pattern.finditer(content))
    views = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        block = content[start:end].strip()
        title = m.group(2).strip()

        rec_match = re.search(r"Recommendation:\s*(.+)", block)
        obj_match = re.search(r"Core Objection:\s*(.+?)(?=\n    Risk If Ignored:|\Z)", block, re.DOTALL)
        risk_match = re.search(r"Risk If Ignored:\s*(.+?)(?=\n    CEO Response:|\Z)", block, re.DOTALL)
        resp_match = re.search(r"CEO Response:\s*(.+?)$", block, re.DOTALL)

        views.append({
            "title": title,
            "recommendation": rec_match.group(1).strip() if rec_match else "",
            "objection": obj_match.group(1).strip() if obj_match else "",
            "risk": risk_match.group(1).strip() if risk_match else "",
            "response": resp_match.group(1).strip() if resp_match else "",
        })
    return views


def parse_next_steps(content: str) -> dict:
    """Parse Next Steps section."""
    result = {"actions": [], "triggers": []}

    # Action table
    for row in re.finditer(r"\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|", content):
        result["actions"].append({
            "num": row.group(1).strip(),
            "action": row.group(2).strip(),
            "owner": row.group(3).strip(),
            "timeline": row.group(4).strip(),
            "priority": row.group(5).strip(),
        })

    # Review triggers
    trigger_match = re.search(r"Decision Review Triggers?:\s*\n(.*?)$", content, re.DOTALL)
    if trigger_match:
        result["triggers"] = [
            line.strip().lstrip("- ")
            for line in trigger_match.group(1).splitlines()
            if line.strip().startswith("-")
        ]

    return result


def parse_metadata_section(content: str) -> dict:
    """Parse Metadata section."""
    result = {}
    for line in content.splitlines():
        line = line.strip()
        m = re.match(r"^(.+?):\s*(.+)$", line)
        if m and not line.startswith("-") and not line.startswith("|"):
            result[m.group(1).strip()] = m.group(2).strip()

    # Key Assumptions list
    assumptions = []
    assume_match = re.search(r"Key Assumptions:\s*\n(.*?)(?=\n\w|\Z)", content, re.DOTALL)
    if assume_match:
        assumptions = [
            line.strip().lstrip("- ")
            for line in assume_match.group(1).splitlines()
            if line.strip().startswith("-")
        ]
    result["key_assumptions"] = assumptions
    return result


# ---------------------------------------------------------------------------
# Markdown-to-Paragraph converter (reportlab HTML subset)
# ---------------------------------------------------------------------------

def md_to_para(text: str) -> str:
    """Convert basic markdown inline formatting to reportlab paragraph markup."""
    # Escape XML entities first
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Bold: **text** or __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)
    # Italic: *text* or _text_
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<i>\1</i>", text)
    # Line breaks
    text = text.replace("\n", "<br/>")
    return text


def wrap_text(text: str, max_chars: int = 80) -> str:
    """Soft-wrap long text for table cells."""
    lines = text.split("\n")
    wrapped = []
    for line in lines:
        if len(line) > max_chars:
            wrapped.extend(textwrap.wrap(line, max_chars))
        else:
            wrapped.append(line)
    return "\n".join(wrapped)


# ---------------------------------------------------------------------------
# Style factory
# ---------------------------------------------------------------------------

def build_styles(palette: dict) -> dict:
    """Build a complete set of ParagraphStyles for the PDF."""
    base = getSampleStyleSheet()
    primary = palette["primary"]
    accent = palette["accent"]
    light_bg = palette["light_bg"]

    styles = {}

    styles["title"] = ParagraphStyle(
        "PDFTitle",
        parent=base["Title"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        textColor=primary,
        alignment=TA_LEFT,
        spaceAfter=6,
    )

    styles["subtitle"] = ParagraphStyle(
        "PDFSubtitle",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#555555"),
        spaceAfter=4,
    )

    styles["heading1"] = ParagraphStyle(
        "PDFHeading1",
        parent=base["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=26,
        textColor=primary,
        spaceBefore=12,
        spaceAfter=8,
    )

    styles["heading2"] = ParagraphStyle(
        "PDFHeading2",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=primary,
        spaceBefore=10,
        spaceAfter=6,
    )

    styles["heading3"] = ParagraphStyle(
        "PDFHeading3",
        parent=base["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#333333"),
        spaceBefore=8,
        spaceAfter=4,
    )

    styles["body"] = ParagraphStyle(
        "PDFBody",
        parent=base["Normal"],
        fontName="Times-Roman",
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor("#2C3E50"),
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )

    styles["body_small"] = ParagraphStyle(
        "PDFBodySmall",
        parent=styles["body"],
        fontSize=9.5,
        leading=13,
    )

    styles["callout"] = ParagraphStyle(
        "PDFCallout",
        parent=styles["body"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=primary,
        leftIndent=12,
        rightIndent=12,
        spaceBefore=4,
        spaceAfter=4,
    )

    styles["badge"] = ParagraphStyle(
        "PDFBadge",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=TA_CENTER,
    )

    styles["quote"] = ParagraphStyle(
        "PDFQuote",
        parent=styles["body"],
        fontName="Times-Italic",
        fontSize=11,
        leading=15,
        leftIndent=18,
        rightIndent=18,
        textColor=colors.HexColor("#555555"),
        spaceBefore=6,
        spaceAfter=6,
    )

    styles["footer"] = ParagraphStyle(
        "PDFFooter",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#888888"),
    )

    styles["table_header"] = ParagraphStyle(
        "PDFTableHeader",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#333333"),
    )

    styles["table_cell"] = ParagraphStyle(
        "PDFTableCell",
        parent=base["Normal"],
        fontName="Times-Roman",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#333333"),
    )

    styles["risk_text"] = ParagraphStyle(
        "PDFRisk",
        parent=styles["body_small"],
        textColor=colors.HexColor("#8B1A1A"),
        leftIndent=12,
    )

    styles["opportunity_text"] = ParagraphStyle(
        "PDFOpportunity",
        parent=styles["body_small"],
        textColor=colors.HexColor("#2D6A2E"),
        leftIndent=12,
    )

    styles["bullet"] = ParagraphStyle(
        "PDFBullet",
        parent=styles["body"],
        leftIndent=24,
        firstLineIndent=-12,
        spaceBefore=2,
        spaceAfter=2,
    )

    return styles


# ---------------------------------------------------------------------------
# Flowable helpers
# ---------------------------------------------------------------------------

def horizontal_rule(palette: dict, width: float = 6.5 * inch) -> Table:
    """A thin horizontal line spanning the content width."""
    return Table(
        [[""]],
        colWidths=[width],
        rowHeights=[1],
        style=TableStyle([
            ("LINEABOVE", (0, 0), (-1, 0), 0.5, palette["accent"]),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]),
    )


def badge_table(text: str, bg_color, fg_color=colors.white) -> Table:
    """Small inline badge (e.g., decision type, tier)."""
    style = ParagraphStyle(
        "BadgeInline",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=fg_color,
        alignment=TA_CENTER,
    )
    t = Table(
        [[Paragraph(text, style)]],
        colWidths=[len(text) * 5.5 + 16],
        rowHeights=[16],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
    ]))
    return t


def recommendation_color(rec_text: str) -> colors.HexColor:
    """Determine badge color from recommendation text."""
    lower = rec_text.lower()
    if "oppose" in lower:
        return RECOMMENDATION_COLORS["oppose"]
    if "conditions" in lower or "conditional" in lower:
        return RECOMMENDATION_COLORS["conditions"]
    if "approve" in lower:
        return RECOMMENDATION_COLORS["approve"]
    return RECOMMENDATION_COLORS["neutral"]


def embed_image(image_path: str, max_width: float = 5.5 * inch) -> Image | None:
    """Embed a PNG image, preserving aspect ratio, with min 5in width."""
    if not os.path.isfile(image_path):
        return None
    try:
        if PILImage:
            with PILImage.open(image_path) as img:
                w_px, h_px = img.size
        else:
            # Fallback: use reportlab's own image reader
            w_px, h_px = 800, 600  # default guess
        aspect = h_px / w_px if w_px > 0 else 0.75
        display_width = max(5 * inch, min(max_width, 6.5 * inch))
        display_height = display_width * aspect
        # Cap height to avoid single image taking a full page
        max_height = 5 * inch
        if display_height > max_height:
            display_height = max_height
            display_width = display_height / aspect
        return Image(image_path, width=display_width, height=display_height)
    except Exception:
        return None


def callout_box(text: str, styles: dict, palette: dict, border_color=None) -> Table:
    """A styled callout box with left accent border."""
    if border_color is None:
        border_color = palette["accent"]
    para = Paragraph(md_to_para(text), styles["callout"])
    t = Table(
        [[para]],
        colWidths=[6.0 * inch],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), palette["light_bg"]),
        ("LINEBEFORESTYLE", (0, 0), (0, -1), "solid"),
        ("LINEBEFOREWIDTH", (0, 0), (0, -1), 3),
        ("LINEBEFORECOLOR", (0, 0), (0, -1), border_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def make_data_table(headers: list, rows: list, styles: dict, col_widths=None) -> Table:
    """Build a styled reportlab Table from header + row data."""
    header_style = styles["table_header"]
    cell_style = styles["table_cell"]

    data = [[Paragraph(md_to_para(h), header_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(md_to_para(str(c)), cell_style) for c in row])

    if col_widths is None:
        n = len(headers)
        col_widths = [6.5 * inch / n] * n

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#333333")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    # Alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F9F9F9")))
    t.setStyle(TableStyle(style_cmds))
    return t


def bullet_list(items: list, styles: dict, bullet_char: str = "\u2022") -> list:
    """Create a list of Paragraph flowables styled as bullet points."""
    flowables = []
    for item in items:
        text = f"{bullet_char}  {md_to_para(item)}"
        flowables.append(Paragraph(text, styles["bullet"]))
    return flowables


# ---------------------------------------------------------------------------
# Page templates with headers/footers
# ---------------------------------------------------------------------------

def _make_header_footer(canvas, doc, meta: dict, palette: dict):
    """Draw running header and footer on each page."""
    canvas.saveState()
    width, height = letter

    # Header line
    if doc.page > 1:
        canvas.setStrokeColor(palette["accent"])
        canvas.setLineWidth(0.5)
        canvas.line(0.75 * inch, height - 0.55 * inch, width - 0.75 * inch, height - 0.55 * inch)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#888888"))
        title_short = meta.get("issue_title", "Decision Briefing")
        if len(title_short) > 70:
            title_short = title_short[:67] + "..."
        canvas.drawString(0.75 * inch, height - 0.5 * inch, f"Decision Briefing — {title_short}")

    # Footer
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.drawString(0.75 * inch, 0.4 * inch, meta.get("date", ""))
    canvas.drawRightString(width - 0.75 * inch, 0.4 * inch, f"Page {doc.page}")

    canvas.restoreState()


def build_doc(output_path: str, meta: dict, palette: dict) -> BaseDocTemplate:
    """Create the document template with page frames."""
    def on_page(canvas, doc):
        _make_header_footer(canvas, doc, meta, palette)

    def on_first_page(canvas, doc):
        _make_header_footer(canvas, doc, meta, palette)

    doc = BaseDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.65 * inch,
    )

    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="main",
    )

    # Hero page: extra top margin for title area
    hero_frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="hero",
    )

    doc.addPageTemplates([
        PageTemplate(id="hero", frames=[hero_frame], onPage=on_first_page),
        PageTemplate(id="content", frames=[frame], onPage=on_page),
    ])

    return doc


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def build_hero(meta: dict, exec_summary: str, styles: dict, palette: dict) -> list:
    """Hero section: title, badges, decision callout, executive summary."""
    elements = []

    # Title
    title = meta.get("issue_title", "Decision Briefing")
    elements.append(Paragraph(md_to_para(title), styles["title"]))
    elements.append(Spacer(1, 4))

    # Badge row: decision type + tier + mode
    badge_data = []
    dt = meta.get("decision_type", "")
    if dt:
        badge_data.append(badge_table(dt.upper(), palette["badge_bg"], palette["badge_fg"]))
    tier = meta.get("tier", "")
    if tier:
        tier_label = f"TIER {tier}" + (" — Board Meeting" if str(tier) == "3" else " — Working Session" if str(tier) == "2" else "")
        badge_data.append(badge_table(tier_label, colors.HexColor("#555555")))
    mode = meta.get("decision_mode", "")
    if mode:
        badge_data.append(badge_table(f"MODE: {mode.upper()}", palette["accent"]))

    if badge_data:
        badge_row = Table([badge_data], colWidths=[None] * len(badge_data))
        badge_row.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(badge_row)

    elements.append(Spacer(1, 6))

    # Date
    date_str = meta.get("date", "")
    if date_str:
        elements.append(Paragraph(f"Date: {date_str}", styles["subtitle"]))

    elements.append(Spacer(1, 8))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 10))

    # Decision callout - extract first 1-2 sentences from exec summary
    if exec_summary:
        # Use first sentence as the decision callout
        first_sentence_match = re.match(r"(.+?\.)\s", exec_summary)
        callout_text = first_sentence_match.group(1) if first_sentence_match else exec_summary[:300]
        elements.append(callout_box(callout_text, styles, palette, border_color=palette["primary"]))
        elements.append(Spacer(1, 12))

    # Switch to content template after hero
    elements.append(NextPageTemplate("content"))

    # Executive Summary section
    elements.append(Paragraph("Executive Summary", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 6))

    for para_text in exec_summary.split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            elements.append(Paragraph(md_to_para(para_text), styles["body"]))

    return elements


def build_problem_context(section_1: dict, section_2: dict, styles: dict, palette: dict) -> list:
    """Problem Context: Issue Statement + partial CEO Framing."""
    elements = [PageBreak()]
    elements.append(Paragraph("Problem Context", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 6))

    if section_1:
        for para_text in section_1["content"].split("\n\n"):
            para_text = para_text.strip()
            if para_text:
                elements.append(Paragraph(md_to_para(para_text), styles["body"]))

    return elements


def build_analytical_framework(section_2: dict, images_dir: str, styles: dict, palette: dict) -> list:
    """Analytical Framework: CEO Framing + routing diagram."""
    elements = [PageBreak()]
    elements.append(Paragraph("Analytical Framework", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 6))

    content = section_2["content"] if section_2 else ""

    # Extract evaluation dimensions
    dim_match = re.search(r"Evaluation Dimensions:\s*\n(.*?)(?=\nActivated Teams:|\Z)", content, re.DOTALL)
    if dim_match:
        elements.append(Paragraph("Evaluation Dimensions", styles["heading2"]))
        dims = [line.strip().lstrip("- ") for line in dim_match.group(1).splitlines() if line.strip().startswith("-")]
        elements.extend(bullet_list(dims, styles))
        elements.append(Spacer(1, 6))

    # Routing diagram infographic
    routing_img = os.path.join(images_dir, "INFOGRAPHIC_routing-diagram.png")
    img = embed_image(routing_img)
    if img:
        elements.append(Spacer(1, 6))
        elements.append(img)
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("<i>Figure 1: Decision Routing Diagram</i>", styles["footer"]))
        elements.append(Spacer(1, 8))

    # Activated Teams table
    team_match = re.search(r"Activated Teams:\s*\n(.*?)(?=\nExcluded Teams:|\nFull-Activation|\Z)", content, re.DOTALL)
    if team_match:
        elements.append(Paragraph("Activated Teams", styles["heading2"]))
        headers = ["C-Suite Role", "Activation Rationale"]
        rows = []
        for row in re.finditer(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|", team_match.group(1)):
            role = row.group(1).strip()
            if role.startswith("---") or role == "C-Suite Role":
                continue
            rows.append([role, row.group(2).strip()])
        if rows:
            elements.append(make_data_table(headers, rows, styles, col_widths=[1.5 * inch, 5.0 * inch]))
            elements.append(Spacer(1, 8))

    # Full-activation assessment
    full_match = re.search(r"Full-Activation Threshold Assessment:\s*\n(.*?)(?=\nCSO Research|\Z)", content, re.DOTALL)
    if full_match:
        elements.append(Paragraph("Full-Activation Threshold Assessment", styles["heading2"]))
        items = []
        for line in full_match.group(1).splitlines():
            line = line.strip()
            if line and line[0].isdigit():
                items.append(line)
        if items:
            elements.extend(bullet_list(items, styles))
        full_result = re.search(r"Full activation:\s*(YES|NO)", content)
        if full_result:
            elements.append(Spacer(1, 4))
            elements.append(callout_box(f"Full Activation: {full_result.group(1)}", styles, palette))
        elements.append(Spacer(1, 6))

    return elements


def build_domain_analysis(domains: list, images_dir: str, styles: dict, palette: dict) -> list:
    """Domain Analysis Cards: one card per domain, single-column for print."""
    elements = [PageBreak()]
    elements.append(Paragraph("Domain Analysis", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 6))

    # Domain scorecard infographic
    scorecard_img = os.path.join(images_dir, "INFOGRAPHIC_domain-scorecard.png")
    img = embed_image(scorecard_img)
    if img:
        elements.append(img)
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("<i>Figure 2: Domain Scorecard</i>", styles["footer"]))
        elements.append(Spacer(1, 10))

    # Domain cards
    figure_num = 3
    for domain in domains:
        card_elements = []

        # Domain header with recommendation badge
        card_elements.append(Paragraph(domain["title"], styles["heading2"]))

        rec = domain["recommendation"]
        conf = domain["confidence"]
        rec_color = recommendation_color(rec)

        # Recommendation + Confidence line
        badge_info = Table(
            [[
                badge_table(rec.upper(), rec_color),
                Paragraph(f"Confidence: <b>{conf}</b>", styles["body_small"]),
            ]],
            colWidths=[None, None],
        )
        badge_info.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        card_elements.append(badge_info)
        card_elements.append(Spacer(1, 4))

        # Summary
        if domain["summary"]:
            card_elements.append(Paragraph(md_to_para(domain["summary"]), styles["body"]))
            card_elements.append(Spacer(1, 4))

        # Team Lead Findings
        if domain["team_leads"]:
            card_elements.append(Paragraph("Team Lead Findings", styles["heading3"]))
            headers = ["Team Lead", "Key Finding", "Conf."]
            rows = [[tl["name"], tl["finding"], tl["confidence"]] for tl in domain["team_leads"]]
            card_elements.append(make_data_table(
                headers, rows, styles,
                col_widths=[1.3 * inch, 4.4 * inch, 0.5 * inch],
            ))
            card_elements.append(Spacer(1, 4))

        # Key Risks
        if domain["risks"]:
            card_elements.append(Paragraph("Key Risks", styles["heading3"]))
            for risk in domain["risks"]:
                card_elements.append(Paragraph(f"\u26a0  {md_to_para(risk)}", styles["risk_text"]))
            card_elements.append(Spacer(1, 4))

        # Key Opportunities
        if domain["opportunities"]:
            card_elements.append(Paragraph("Key Opportunities", styles["heading3"]))
            for opp in domain["opportunities"]:
                card_elements.append(Paragraph(f"\u2713  {md_to_para(opp)}", styles["opportunity_text"]))

        card_elements.append(Spacer(1, 4))
        card_elements.append(horizontal_rule(palette, width=6.0 * inch))
        card_elements.append(Spacer(1, 8))

        # KeepTogether to prevent card from splitting across pages
        elements.append(KeepTogether(card_elements))

    return elements


def build_fault_lines(fault_data: dict, images_dir: str, styles: dict, palette: dict) -> list:
    """Fault Line Visualization section."""
    elements = [PageBreak()]
    elements.append(Paragraph("Where Perspectives Collide", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 6))

    # Fault line map infographic
    fl_img = os.path.join(images_dir, "INFOGRAPHIC_fault-line-map.png")
    img = embed_image(fl_img)
    if img:
        elements.append(img)
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("<i>Figure 3: Fault Line Map</i>", styles["footer"]))
        elements.append(Spacer(1, 10))

    # Points of Agreement
    if fault_data["agreements"]:
        elements.append(Paragraph("Points of Agreement", styles["heading2"]))
        elements.extend(bullet_list(fault_data["agreements"], styles, bullet_char="\u2714"))
        elements.append(Spacer(1, 8))

    # Points of Contention
    if fault_data["contentions"]:
        elements.append(Paragraph("Points of Contention", styles["heading2"]))
        for item in fault_data["contentions"]:
            elements.append(callout_box(item, styles, palette, border_color=RECOMMENDATION_COLORS["oppose"]))
            elements.append(Spacer(1, 4))
        elements.append(Spacer(1, 8))

    # Pre-Mortem Findings
    if fault_data["premortems"]:
        elements.append(Paragraph("Pre-Mortem Findings", styles["heading2"]))
        headers = ["C-Suite Role", "Predicted Failure Mode", "Severity"]
        rows = [[pm["role"], pm["failure_mode"], pm["severity"]] for pm in fault_data["premortems"]]
        elements.append(make_data_table(
            headers, rows, styles,
            col_widths=[1.0 * inch, 4.5 * inch, 1.0 * inch],
        ))
        elements.append(Spacer(1, 8))

    # Unresolved Tensions
    if fault_data["tensions"]:
        elements.append(Paragraph("Unresolved Tensions", styles["heading2"]))
        for item in fault_data["tensions"]:
            elements.append(callout_box(item, styles, palette, border_color=colors.HexColor("#999999")))
            elements.append(Spacer(1, 4))

    return elements


def build_the_decision(decision_data: dict, images_dir: str, styles: dict, palette: dict) -> list:
    """The Decision section."""
    elements = [PageBreak()]
    elements.append(Paragraph("The Decision", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 8))

    # Decision statement callout
    if "statement" in decision_data:
        elements.append(callout_box(decision_data["statement"], styles, palette, border_color=palette["primary"]))
        elements.append(Spacer(1, 10))

    # Most determinative perspective
    if "determinative_role" in decision_data:
        elements.append(Paragraph("Most Determinative Perspective", styles["heading2"]))
        elements.append(Paragraph(
            f"<b>{decision_data['determinative_role']}</b>",
            styles["body"],
        ))
        if "determinative_rationale" in decision_data:
            elements.append(Paragraph(md_to_para(decision_data["determinative_rationale"]), styles["body"]))
        elements.append(Spacer(1, 6))

    # Decision Weight Rationale
    if "weight_rationale" in decision_data:
        elements.append(Paragraph("Decision Weight Rationale", styles["heading2"]))
        elements.append(Paragraph(md_to_para(decision_data["weight_rationale"]), styles["body"]))
        elements.append(Spacer(1, 6))

    # Risk matrix infographic
    risk_img = os.path.join(images_dir, "INFOGRAPHIC_risk-opportunity-matrix.png")
    img = embed_image(risk_img)
    if img:
        elements.append(Spacer(1, 6))
        elements.append(img)
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("<i>Figure 4: Risk-Opportunity Matrix</i>", styles["footer"]))
        elements.append(Spacer(1, 8))

    # Conditions & Guardrails
    if "conditions" in decision_data:
        elements.append(PageBreak())
        elements.append(Paragraph("Conditions &amp; Guardrails", styles["heading2"]))

        # Parse gate blocks
        gates = re.split(r"\n(?=PRECONDITION GATE|PILOT PHASE)", decision_data["conditions"])
        for gate in gates:
            gate = gate.strip()
            if not gate:
                continue
            # Extract gate title
            title_match = re.match(r"^(PRECONDITION GATE \d+|PILOT PHASE)\s*(\([^)]+\))?:?\s*(.*)", gate)
            if title_match:
                gate_title = title_match.group(1)
                gate_timeline = title_match.group(2) or ""
                gate_subtitle = title_match.group(3) or ""
                elements.append(Paragraph(
                    f"<b>{gate_title}</b> {gate_timeline} {gate_subtitle}",
                    styles["heading3"],
                ))
                # Remaining lines as bullets
                remaining = gate[title_match.end():]
                items = [line.strip().lstrip("- ") for line in remaining.splitlines() if line.strip().startswith("-")]
                if items:
                    elements.extend(bullet_list(items, styles))
                elements.append(Spacer(1, 6))
            else:
                elements.append(Paragraph(md_to_para(gate), styles["body"]))

    # Accepted Risks
    if decision_data.get("accepted_risks"):
        elements.append(Paragraph("Accepted Risks", styles["heading2"]))
        for risk in decision_data["accepted_risks"]:
            elements.append(Paragraph(f"\u26a0  {md_to_para(risk)}", styles["risk_text"]))
            elements.append(Spacer(1, 2))
        elements.append(Spacer(1, 6))

    # Mitigations
    if decision_data.get("mitigations"):
        elements.append(Paragraph("Mitigations Directed", styles["heading2"]))
        elements.extend(bullet_list(decision_data["mitigations"], styles))

    return elements


def build_dissenting_views(views: list, styles: dict, palette: dict) -> list:
    """Dissenting Views section."""
    elements = [PageBreak()]
    elements.append(Paragraph("Dissenting Views", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 8))

    for view in views:
        card = []
        card.append(Paragraph(view["title"], styles["heading2"]))

        if view["recommendation"]:
            rec_color = recommendation_color(view["recommendation"])
            card.append(badge_table(view["recommendation"].upper(), rec_color))
            card.append(Spacer(1, 4))

        if view["objection"]:
            card.append(Paragraph("<b>Core Objection</b>", styles["heading3"]))
            card.append(Paragraph(md_to_para(view["objection"]), styles["body"]))
            card.append(Spacer(1, 4))

        if view["risk"]:
            card.append(Paragraph("<b>Risk If Ignored</b>", styles["heading3"]))
            card.append(Paragraph(f"\u26a0  {md_to_para(view['risk'])}", styles["risk_text"]))
            card.append(Spacer(1, 4))

        if view["response"]:
            card.append(Paragraph("<b>CEO Response</b>", styles["heading3"]))
            card.append(callout_box(view["response"], styles, palette))

        card.append(Spacer(1, 6))
        card.append(horizontal_rule(palette, width=6.0 * inch))
        card.append(Spacer(1, 8))

        elements.append(KeepTogether(card))

    return elements


def build_action_plan(next_steps: dict, images_dir: str, styles: dict, palette: dict) -> list:
    """Action Plan section."""
    elements = [PageBreak()]
    elements.append(Paragraph("Action Plan", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 6))

    # Timeline infographic
    timeline_img = os.path.join(images_dir, "INFOGRAPHIC_action-plan-timeline.png")
    img = embed_image(timeline_img)
    if img:
        elements.append(img)
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("<i>Figure 5: Action Plan Timeline</i>", styles["footer"]))
        elements.append(Spacer(1, 10))

    # Action items table
    if next_steps["actions"]:
        headers = ["#", "Action", "Owner", "Timeline", "Priority"]
        rows = [[a["num"], a["action"], a["owner"], a["timeline"], a["priority"]] for a in next_steps["actions"]]
        elements.append(make_data_table(
            headers, rows, styles,
            col_widths=[0.3 * inch, 2.8 * inch, 1.3 * inch, 1.0 * inch, 0.8 * inch],
        ))
        elements.append(Spacer(1, 10))

    # Decision Review Triggers
    if next_steps["triggers"]:
        elements.append(Paragraph("Decision Review Triggers", styles["heading2"]))
        elements.extend(bullet_list(next_steps["triggers"], styles))

    return elements


def build_metadata_footer(meta_section: dict, meta: dict, styles: dict, palette: dict) -> list:
    """Metadata footer section."""
    elements = [PageBreak()]
    elements.append(Paragraph("Decision Metadata", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 8))

    # Key metadata in a clean table
    info_rows = []
    for key in ["Total Roles Consulted", "Decision Complexity", "Primary Domain", "Dissent Level"]:
        if key in meta_section:
            info_rows.append([key, meta_section[key]])

    # Add from frontmatter
    if meta.get("decision_mode"):
        info_rows.append(["Decision Mode", meta["decision_mode"]])
    if meta.get("decision_type"):
        info_rows.append(["Decision Type", meta["decision_type"]])
    if meta.get("date"):
        info_rows.append(["Date", meta["date"]])

    for key in ["Research Foundation", "Company Profile", "Routing Override"]:
        if key in meta_section:
            info_rows.append([key, meta_section[key]])

    if info_rows:
        elements.append(make_data_table(
            ["Field", "Value"], info_rows, styles,
            col_widths=[2.0 * inch, 4.5 * inch],
        ))
        elements.append(Spacer(1, 10))

    # Key Assumptions
    assumptions = meta_section.get("key_assumptions", [])
    if assumptions:
        elements.append(Paragraph("Key Assumptions", styles["heading2"]))
        elements.extend(bullet_list(assumptions, styles))

    return elements


# ---------------------------------------------------------------------------
# Multi-mode variant support
# ---------------------------------------------------------------------------

def build_mode_comparison(section_content: str, images_dir: str, styles: dict, palette: dict) -> list:
    """Build mode comparison section for comparative decision records."""
    elements = [PageBreak()]
    elements.append(Paragraph("Mode Comparisons", styles["heading1"]))
    elements.append(horizontal_rule(palette))
    elements.append(Spacer(1, 6))

    # Mode comparison infographic
    mode_img = os.path.join(images_dir, "INFOGRAPHIC_mode-comparison.png")
    img = embed_image(mode_img)
    if img:
        elements.append(img)
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("<i>Mode Comparison Divergence Tree</i>", styles["footer"]))
        elements.append(Spacer(1, 8))

    # Render rest as paragraphs
    for para_text in section_content.split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            elements.append(Paragraph(md_to_para(para_text), styles["body"]))

    return elements


# ---------------------------------------------------------------------------
# Main PDF builder
# ---------------------------------------------------------------------------

def build_results_pdf(session_dir: str) -> str:
    """Generate RESULTS_<slug>.pdf from RECORD.md in the given session directory.

    Returns the output file path.
    """
    session_dir = os.path.abspath(session_dir)
    record_path = os.path.join(session_dir, "RECORD.md")
    images_dir = os.path.join(session_dir, "images")

    if not os.path.isfile(record_path):
        print(f"ERROR: RECORD.md not found at {record_path}")
        sys.exit(1)

    with open(record_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Parse
    meta = parse_frontmatter(text)
    body = parse_body(text)
    exec_summary = body["executive_summary"]
    sections = body["sections"]

    # Determine output filename
    slug = meta.get("issue_slug", "decision")
    output_path = os.path.join(session_dir, f"RESULTS_{slug}.pdf")

    # Select palette
    decision_type = meta.get("decision_type", "Strategic")
    palette = PALETTES.get(decision_type, DEFAULT_PALETTE)
    styles = build_styles(palette)

    # Build document
    doc = build_doc(output_path, meta, palette)
    story = []

    # 1. Hero + Executive Summary
    story.extend(build_hero(meta, exec_summary, styles, palette))

    # 2. Problem Context (Section 1 + partial Section 2)
    story.extend(build_problem_context(
        sections.get(1),
        sections.get(2),
        styles,
        palette,
    ))

    # 3. Analytical Framework (Section 2)
    story.extend(build_analytical_framework(
        sections.get(2),
        images_dir,
        styles,
        palette,
    ))

    # 4. Domain Analysis (Section 3)
    if 3 in sections:
        domains = parse_domain_analyses(sections[3]["content"], section_num=3)
        story.extend(build_domain_analysis(domains, images_dir, styles, palette))

    # 5. Fault Lines (Section 4)
    if 4 in sections:
        fault_data = parse_fault_lines(sections[4]["content"])
        story.extend(build_fault_lines(fault_data, images_dir, styles, palette))

    # 6. The Decision (Section 5)
    if 5 in sections:
        decision_data = parse_decision(sections[5]["content"])
        story.extend(build_the_decision(decision_data, images_dir, styles, palette))

    # 7. Dissenting Views (Section 6)
    if 6 in sections:
        views = parse_dissenting_views(sections[6]["content"], section_num=6)
        story.extend(build_dissenting_views(views, styles, palette))

    # 8. Action Plan (Section 7)
    if 7 in sections:
        next_steps = parse_next_steps(sections[7]["content"])
        story.extend(build_action_plan(next_steps, images_dir, styles, palette))

    # 8.5. Multi-mode comparison (if comparative decision record)
    if meta.get("type") == "comparative-decision-record":
        # Look for mode comparison content in the sections
        for sec_num, sec in sections.items():
            if "mode" in sec["title"].lower() and "comparison" in sec["title"].lower():
                story.extend(build_mode_comparison(sec["content"], images_dir, styles, palette))
                break

    # 9. Metadata (Section 8)
    if 8 in sections:
        meta_section = parse_metadata_section(sections[8]["content"])
        story.extend(build_metadata_footer(meta_section, meta, styles, palette))

    # Build
    doc.build(story)

    file_size = os.path.getsize(output_path)
    print(f"OK: {output_path} ({file_size:,} bytes)")
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate Results PDF natively from RECORD.md",
    )
    parser.add_argument(
        "--session-dir",
        required=True,
        help="Path to the session output directory containing RECORD.md",
    )
    args = parser.parse_args()
    build_results_pdf(args.session_dir)


if __name__ == "__main__":
    main()
