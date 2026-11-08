#!/usr/bin/env python3
"""Check the structure of uncompressed draw.io (.drawio) files.

Usage: validate_drawio.py <file.drawio> [<file.drawio> ...]

Errors (exit code 1): malformed XML, wrong structure, compressed content,
missing cells 0/1, duplicate ids, unknown parent/source/target references,
parent loops, edges without endpoints or geometry, vertices without a size.

Warnings (exit code 0): overlapping vertices, vertices with empty labels,
labels whose text would be swallowed as an HTML tag, cells that are neither
vertex nor edge, and pages with no content.

Exit codes: 0 no errors, 1 errors found, 2 bad command-line usage.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass

# Tags draw.io renders as formatting. Anything else in an HTML label, such as
# the <User> in List<User>, is treated as an unknown tag and drops out of view.
HTML_TAGS = {
    "a", "b", "big", "blockquote", "br", "code", "div", "em", "font",
    "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "li", "ol", "p",
    "pre", "s", "small", "span", "strike", "strong", "sub", "sup", "table",
    "tbody", "td", "th", "thead", "tr", "tt", "u", "ul",
}
TAG_RE = re.compile(r"</?([A-Za-z][\w-]*)[^<>]*>")
# First style token of cells that are drawn without any text by design.
UNLABELLED_STYLES = {"group", "line"}
OVERLAP_EXEMPT_SHAPES = ("shape=umlLifeline", "shape=umlFrame")


@dataclass
class Cell:
    id: str
    value: str
    style: str
    parent: str | None
    source: str | None
    target: str | None
    is_vertex: bool
    is_edge: bool
    geometry: ET.Element | None


@dataclass
class Report:
    errors: list[str]
    warnings: list[str]


def parse_cells(root: ET.Element, page: str, report: Report) -> list[Cell]:
    """Read cells, unwrapping the <object>/<UserObject> form draw.io can save."""
    cells = []
    for element in root:
        if element.tag == "mxCell":
            inner, value = element, element.get("value", "")
        elif element.tag in ("object", "UserObject"):
            inner, value = element.find("mxCell"), element.get("label", "")
            if inner is None:
                report.errors.append(
                    f"{page}: <{element.tag}> id={element.get('id')!r} has no <mxCell> inside"
                )
                continue
        else:
            continue
        cell_id = element.get("id")
        if not cell_id:
            report.errors.append(f"{page}: a cell has no id (value={value!r})")
            continue
        geometry = next(
            (g for g in inner.findall("mxGeometry") if g.get("as") == "geometry"), None
        )
        cells.append(
            Cell(
                id=cell_id,
                value=value,
                style=inner.get("style", ""),
                parent=inner.get("parent"),
                source=inner.get("source"),
                target=inner.get("target"),
                is_vertex=inner.get("vertex") == "1",
                is_edge=inner.get("edge") == "1",
                geometry=geometry,
            )
        )
    return cells


def is_relative(cell: Cell) -> bool:
    return cell.geometry is not None and cell.geometry.get("relative") == "1"


def read_rect(cell: Cell) -> tuple[float, float, float, float] | None:
    """Return (x, y, width, height), or None when a number cannot be parsed."""
    if cell.geometry is None:
        return None
    try:
        return tuple(
            float(cell.geometry.get(name, "0")) for name in ("x", "y", "width", "height")
        )
    except ValueError:
        return None


def ancestors(cell: Cell, by_id: dict[str, Cell]) -> list[Cell]:
    """Return the parent chain, nearest first, stopping at a gap or a loop."""
    chain: list[Cell] = []
    seen = {cell.id}
    current = cell
    while current.parent in by_id and current.parent not in seen:
        current = by_id[current.parent]
        seen.add(current.id)
        chain.append(current)
    return chain


def in_parent_loop(cell: Cell, by_id: dict[str, Cell]) -> bool:
    current = cell
    seen = set()
    while current.parent in by_id and current.id not in seen:
        seen.add(current.id)
        current = by_id[current.parent]
        if current.id == cell.id:
            return True
    return False


def absolute_rect(cell: Cell, by_id: dict[str, Cell]):
    """Return the page-level rectangle, or None if it cannot be worked out."""
    rect = read_rect(cell)
    if rect is None or is_relative(cell):
        return None
    x, y, width, height = rect
    for parent in ancestors(cell, by_id):
        if parent.is_edge or is_relative(parent):
            return None
        if parent.is_vertex:
            parent_rect = read_rect(parent)
            if parent_rect is None:
                return None
            x += parent_rect[0]
            y += parent_rect[1]
    return x, y, width, height


def visible_text(value: str) -> str:
    return html.unescape(TAG_RE.sub("", value)).strip()


def check_vertex(cell: Cell, by_id: dict[str, Cell], page: str, report: Report) -> None:
    if cell.geometry is None:
        report.errors.append(f"{page}: vertex '{cell.id}' has no <mxGeometry as=\"geometry\">")
    else:
        rect = read_rect(cell)
        if rect is None:
            report.errors.append(f"{page}: vertex '{cell.id}' has non-numeric geometry")
        else:
            parent = by_id.get(cell.parent or "")
            # Edge labels and ports are positioned relative to something else.
            exempt = is_relative(cell) or (parent is not None and parent.is_edge)
            if not exempt and (rect[2] <= 0 or rect[3] <= 0):
                report.errors.append(
                    f"{page}: vertex '{cell.id}' needs a positive width and height"
                )

    first_style = cell.style.split(";")[0]
    decorative = first_style in UNLABELLED_STYLES or "image=" in cell.style
    if not decorative and not visible_text(cell.value):
        report.warnings.append(f"{page}: vertex '{cell.id}' has an empty label")


def check_edge(cell: Cell, by_id: dict[str, Cell], page: str, report: Report) -> None:
    for end, reference in (("source", cell.source), ("target", cell.target)):
        if not reference:
            report.errors.append(f"{page}: edge '{cell.id}' has no {end}")
        elif reference not in by_id:
            report.errors.append(
                f"{page}: edge '{cell.id}' {end} '{reference}' does not exist"
            )
    if cell.geometry is None:
        report.errors.append(f"{page}: edge '{cell.id}' has no <mxGeometry as=\"geometry\">")


def check_label_tags(cell: Cell, page: str, report: Report) -> None:
    if "html=1" not in cell.style:
        return
    unknown = sorted(
        {tag for tag in TAG_RE.findall(cell.value) if tag.lower() not in HTML_TAGS}
    )
    if unknown:
        tags = ", ".join(f"<{tag}>" for tag in unknown)
        report.warnings.append(
            f"{page}: cell '{cell.id}' label contains {tags}, which draws as an "
            "HTML tag and hides that text; double-escape it (&amp;lt; &amp;gt;)"
        )


def check_overlaps(cells: list[Cell], by_id: dict[str, Cell], page: str, report: Report) -> None:
    rects = []
    for cell in cells:
        # Lifelines are mostly empty space and frames span them by design.
        if cell.is_vertex and not any(s in cell.style for s in OVERLAP_EXEMPT_SHAPES):
            rect = absolute_rect(cell, by_id)
            if rect is not None and rect[2] > 0 and rect[3] > 0:
                rects.append((cell, rect))
    for index, (first, a) in enumerate(rects):
        first_ancestors = {c.id for c in ancestors(first, by_id)}
        for second, b in rects[index + 1:]:
            if second.id in first_ancestors or first.id in {
                c.id for c in ancestors(second, by_id)
            }:
                continue  # A container holding its own child is not an overlap.
            if a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]:
                report.warnings.append(f"{page}: vertices '{first.id}' and '{second.id}' overlap")


def check_page(diagram: ET.Element, number: int, report: Report) -> None:
    name = diagram.get("name") or f"#{number}"
    page = f'page "{name}"'

    model = diagram.find("mxGraphModel")
    if model is None:
        if (diagram.text or "").strip():
            report.errors.append(
                f"{page}: content is compressed; write <mxGraphModel> as uncompressed XML"
            )
        else:
            report.errors.append(f"{page}: <diagram> has no <mxGraphModel>")
        return
    root = model.find("root")
    if root is None:
        report.errors.append(f"{page}: <mxGraphModel> has no <root>")
        return

    cells = parse_cells(root, page, report)
    by_id: dict[str, Cell] = {}
    for cell in cells:
        if cell.id in by_id:
            report.errors.append(f"{page}: duplicate cell id '{cell.id}'")
        else:
            by_id[cell.id] = cell

    if "0" not in by_id:
        report.errors.append(f"{page}: missing root cell id=\"0\"")
    elif by_id["0"].parent:
        report.errors.append(f"{page}: cell id=\"0\" must not have a parent")
    if "1" not in by_id:
        report.errors.append(f"{page}: missing layer cell id=\"1\"")
    elif by_id["1"].parent != "0":
        report.errors.append(f"{page}: cell id=\"1\" must have parent=\"0\"")

    for cell in cells:
        if cell.id != "0" and not cell.parent:
            report.errors.append(f"{page}: cell '{cell.id}' has no parent")
        elif cell.parent and cell.parent not in by_id:
            report.errors.append(f"{page}: cell '{cell.id}' parent '{cell.parent}' does not exist")
        if in_parent_loop(cell, by_id):
            report.errors.append(f"{page}: cell '{cell.id}' is part of a parent loop")

        if cell.is_vertex and cell.is_edge:
            report.errors.append(f"{page}: cell '{cell.id}' is both a vertex and an edge")
        elif cell.is_vertex:
            check_vertex(cell, by_id, page, report)
        elif cell.is_edge:
            check_edge(cell, by_id, page, report)
        elif cell.parent and cell.parent != "0":
            report.warnings.append(f"{page}: cell '{cell.id}' is neither a vertex nor an edge")
        check_label_tags(cell, page, report)

    if not any(cell.is_vertex for cell in cells):
        report.warnings.append(f"{page}: page has no content")

    check_overlaps(cells, by_id, page, report)


def validate_file(path: str) -> Report:
    report = Report(errors=[], warnings=[])
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as error:
        report.errors.append(f"not well-formed XML: {error}")
        return report
    except OSError as error:
        report.errors.append(f"cannot read file: {error.strerror or error}")
        return report

    if root.tag != "mxfile":
        tag = root.tag.rsplit("}", 1)[-1]  # Drop any XML namespace.
        report.errors.append(f"root element must be <mxfile>, found <{tag}>")
        return report
    if root.get("compressed") == "true":
        report.errors.append('<mxfile> is marked compressed="true"; write uncompressed XML')
    diagrams = root.findall("diagram")
    if not diagrams:
        report.errors.append("<mxfile> has no <diagram> pages")
    for number, diagram in enumerate(diagrams, start=1):
        check_page(diagram, number, report)
    return report


def count(number: int, noun: str) -> str:
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the structure of .drawio files.")
    parser.add_argument("files", nargs="+", metavar="file.drawio")
    args = parser.parse_args()

    failed = 0
    warned = 0
    for path in args.files:
        report = validate_file(path)
        if report.errors:
            status = "FAIL"
            failed += 1
        else:
            status = "PASS"
        warned += len(report.warnings)
        print(
            f"{status}  {path}  ({count(len(report.errors), 'error')}, "
            f"{count(len(report.warnings), 'warning')})"
        )
        for message in report.errors:
            print(f"  ERROR  {message}")
        for message in report.warnings:
            print(f"  WARN   {message}")

    if len(args.files) > 1:
        print(
            f"\n{len(args.files) - failed} of {len(args.files)} files passed, "
            f"{count(warned, 'warning')}"
        )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
