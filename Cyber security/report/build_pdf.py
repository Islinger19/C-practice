#!/usr/bin/env python3
"""
build_pdf.py
============
Renders Case_Study_Report.md to a print-styled HTML and then to
Case_Study_Report.pdf using the pre-installed Chromium via Playwright.
Used because LibreOffice headless conversion is unavailable in this
environment. Formatting follows the CA-2 notice: Times New Roman, 12pt body,
single column, black & blue only.

Usage: python3 build_pdf.py
"""
import base64
import html
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "Case_Study_Report.md")
HTML_OUT = os.path.join(HERE, "Case_Study_Report.html")
PDF_OUT = os.path.join(HERE, "Case_Study_Report.pdf")


def img_data_uri(relpath):
    path = os.path.normpath(os.path.join(HERE, relpath))
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return "data:image/png;base64," + b64


def inline(text):
    """Escape HTML then apply **bold**, *italic*, `code` and [n] styling."""
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    # citation markers like [1], [8]-[11]
    text = re.sub(r"(\[\d+\](?:[–-]\[\d+\])?)", r'<span class="cite">\1</span>', text)
    return text


def md_to_html(md):
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    while i < n:
        line = lines[i]

        # fenced code block
        if line.startswith("```"):
            close_list()
            i += 1
            buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1  # skip closing fence
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            continue

        # images  ![alt](path)
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if m:
            close_list()
            alt, path = m.group(1), m.group(2)
            try:
                uri = img_data_uri(path)
                out.append(f'<div class="figwrap"><img src="{uri}" alt="{html.escape(alt)}"/></div>')
            except Exception:
                out.append(f'<div class="figwrap"><em>[figure: {html.escape(path)}]</em></div>')
            i += 1
            continue

        # table block
        if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[-:\s|]+\|\s*$", lines[i + 1]):
            close_list()
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ['<table><thead><tr>']
            for h in header:
                t.append(f"<th>{inline(h)}</th>")
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_list()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        # horizontal rule / page-break between major sections
        if re.match(r"^---+\s*$", line):
            close_list()
            out.append('<hr/>')
            i += 1
            continue

        # blockquote
        if line.strip().startswith(">"):
            close_list()
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>")
            continue

        # bullet list
        m = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        if m:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(m.group(2))}</li>")
            i += 1
            continue

        # numbered list -> treat as paragraph-ish list
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue

        # blank line
        if not line.strip():
            close_list()
            i += 1
            continue

        # paragraph
        close_list()
        out.append(f"<p>{inline(line.strip())}</p>")
        i += 1

    close_list()
    return "\n".join(out)


CSS = """
@page { size: A4; margin: 20mm 18mm; }
* { box-sizing: border-box; }
body { font-family: 'Times New Roman', Times, serif; font-size: 12pt;
       color: #000; line-height: 1.5; }
h1 { font-size: 16pt; color: #1F3864; border-bottom: 2px solid #2E74B5;
     padding-bottom: 3px; margin-top: 22px; }
h2 { font-size: 14pt; color: #1F3864; margin-top: 16px; }
h3 { font-size: 12.5pt; color: #2E74B5; margin-top: 12px; }
p  { text-align: justify; margin: 6px 0; }
strong { color: #000; }
code { font-family: 'Consolas','Courier New',monospace; color: #1F3864;
       background: #f2f2f2; padding: 0 2px; font-size: 10.5pt; }
pre { background: #f4f6f9; border: 1px solid #d5dee8; border-radius: 4px;
      padding: 8px 10px; overflow-x: auto; }
pre code { background: none; color: #1F3864; font-size: 9.5pt; line-height: 1.35; }
ul { margin: 6px 0 6px 0; padding-left: 22px; }
li { text-align: justify; margin: 3px 0; }
blockquote { border-left: 4px solid #2E74B5; background: #eef4fb; margin: 10px 0;
             padding: 8px 14px; font-style: italic; color: #1F3864; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 10.5pt; }
th { background: #1F3864; color: #fff; text-align: left; padding: 6px 8px;
     border: 1px solid #9db7d5; }
td { padding: 5px 8px; border: 1px solid #9db7d5; }
tbody tr:nth-child(even) { background: #eaf1fb; }
td:nth-child(2), td:nth-child(3) { text-align: center; color: #1F3864; font-weight: bold; }
.figwrap { text-align: center; margin: 12px 0; page-break-inside: avoid; }
.figwrap img { max-width: 92%; height: auto; border: 1px solid #e3e3e3; }
.cite { color: #2E74B5; }
hr { border: none; border-top: 1px solid #c9d6e6; margin: 14px 0; }
h1 { page-break-after: avoid; } h2, h3 { page-break-after: avoid; }
"""


def main():
    with open(MD, encoding="utf-8") as f:
        md = f.read()
    body = md_to_html(md)
    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Case Study Report</title><style>{CSS}</style></head>
<body>{body}</body></html>"""
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print("wrote", HTML_OUT)

    # Render to PDF with Playwright/Chromium
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not available; HTML written, PDF skipped.", file=sys.stderr)
        return
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("file://" + HTML_OUT)
        page.pdf(path=PDF_OUT, format="A4", print_background=True,
                 margin={"top": "18mm", "bottom": "18mm",
                         "left": "16mm", "right": "16mm"})
        browser.close()
    print("wrote", PDF_OUT)


if __name__ == "__main__":
    main()
