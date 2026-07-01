from __future__ import annotations

from io import BytesIO
from pathlib import Path
import difflib
from typing import Dict, Iterable, List, Tuple

import re
import fitz  # PyMuPDF
import pytest
import allure
from PIL import Image, ImageDraw
from pixelmatch.contrib.PIL import pixelmatch

RectTuple = Tuple[int, int, int, int]
MaskConfig = Dict[int, List[RectTuple]]


def _render_pdf_pages(pdf_path: str | Path, zoom: float = 2.0) -> list[Image.Image]:
    doc = fitz.open(str(pdf_path))
    images: list[Image.Image] = []

    try:
        matrix = fitz.Matrix(zoom, zoom)
        for page in doc:
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            img = Image.open(BytesIO(pix.tobytes("png"))).convert("RGBA")
            images.append(img)
    finally:
        doc.close()

    return images


def _apply_masks(
    image: Image.Image,
    masks: Iterable[RectTuple],
    fill=(255, 255, 255, 255),
) -> Image.Image:
    masked = image.copy()
    draw = ImageDraw.Draw(masked)

    for x1, y1, x2, y2 in masks:
        draw.rectangle((x1, y1, x2, y2), fill=fill)

    return masked


def compare_pdf_visual(
    actual_pdf: str | Path,
    expected_pdf: str | Path,
    *,
    masks: MaskConfig | None = None,
    threshold: float = 0.1,
    max_diff_pixels: int = 0,
    output_dir: str | Path = "reports/pdf-visual-diffs",
    name_prefix: str = "pdf_compare",
    zoom: float = 2.0,
) -> None:
    actual_pdf = Path(actual_pdf)
    expected_pdf = Path(expected_pdf)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    masks = masks or {}

    actual_pages = _render_pdf_pages(actual_pdf, zoom=zoom)
    expected_pages = _render_pdf_pages(expected_pdf, zoom=zoom)

    if len(actual_pages) != len(expected_pages):
        pytest.fail(
            f"PDF page count differs. expected={len(expected_pages)}, actual={len(actual_pages)}"
        )

    total_diff_pixels = 0

    for page_index, (actual_img, expected_img) in enumerate(zip(actual_pages, expected_pages)):
        page_no = page_index + 1
        page_masks = masks.get(page_index, [])

        actual_masked = _apply_masks(actual_img, page_masks)
        expected_masked = _apply_masks(expected_img, page_masks)

        if actual_masked.size != expected_masked.size:
            actual_masked.save(output_dir / f"{name_prefix}_page-{page_no}_actual.png")
            expected_masked.save(output_dir / f"{name_prefix}_page-{page_no}_expected.png")
            pytest.fail(
                f"PDF page size differs on page {page_no}. "
                f"expected={expected_masked.size}, actual={actual_masked.size}"
            )

        diff_img = Image.new("RGBA", expected_masked.size)
        diff_pixels = pixelmatch(
            expected_masked,
            actual_masked,
            diff_img,
            threshold=threshold,
        )
        total_diff_pixels += diff_pixels

        actual_path = output_dir / f"{name_prefix}_page-{page_no}_actual.png"
        expected_path = output_dir / f"{name_prefix}_page-{page_no}_expected.png"
        diff_path = output_dir / f"{name_prefix}_page-{page_no}_diff.png"

        actual_masked.save(actual_path)
        expected_masked.save(expected_path)
        diff_img.save(diff_path)

        allure.attach(
            expected_path.read_bytes(),
            name=f"expected_page_{page_no}",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            actual_path.read_bytes(),
            name=f"actual_page_{page_no}",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            diff_path.read_bytes(),
            name=f"diff_page_{page_no}",
            attachment_type=allure.attachment_type.PNG,
        )

    assert total_diff_pixels <= max_diff_pixels, (
        f"PDF visual comparison failed. Different pixels: {total_diff_pixels} "
        f"(allowed: {max_diff_pixels})"
    )

def export_pdf_page_for_masks(
    pdf_path: str | Path,
    *,
    page_index: int = 0,
    output_path: str | Path | None = None,
    zoom: float = 2.0,
    draw_grid: bool = True,
    grid_step: int = 100,
) -> Path:
    pdf_path = Path(pdf_path)

    if output_path is None:
        output_path = Path("reports/pdf-mask-debug") / f"{pdf_path.stem}_page-{page_index + 1}.png"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    try:
        page = doc[page_index]
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        image = Image.open(BytesIO(pix.tobytes("png"))).convert("RGBA")
    finally:
        doc.close()

    if draw_grid:
        draw = ImageDraw.Draw(image)
        width, height = image.size

        for x in range(0, width, grid_step):
            draw.line((x, 0, x, height), fill=(255, 0, 0, 120), width=1)
            draw.text((x + 2, 2), str(x), fill=(255, 0, 0, 255))

        for y in range(0, height, grid_step):
            draw.line((0, y, width, y), fill=(0, 0, 255, 120), width=1)
            draw.text((2, y + 2), str(y), fill=(0, 0, 255, 255))

    image.save(output_path)
    return output_path

def _extract_pdf_text_pages(pdf_path: str | Path, *, sort: bool = True) -> list[str]:
    pdf_path = Path(pdf_path)
    doc = fitz.open(str(pdf_path))
    try:
        return [page.get_text("text", sort=sort) for page in doc]
    finally:
        doc.close()


def _normalize_pdf_text(
    text: str,
    *,
    flatten_to_single_line: bool = False,
) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if flatten_to_single_line:
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)
    else:
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _apply_ignore_patterns(text: str, ignore_patterns: list[str] | None) -> str:
    if not ignore_patterns:
        return text

    for pattern in ignore_patterns:
        text = re.sub(pattern, "__IGNORED__", text, flags=re.MULTILINE)

    return text


def compare_pdf_text(
    actual_pdf: str | Path,
    expected_pdf: str | Path,
    *,
    ignore_patterns: list[str] | None = None,
    normalize_whitespace: bool = True,
    flatten_to_single_line: bool = False,
    sort_text: bool = True,
    output_dir: str | Path = "reports/pdf-text-diffs",
    name_prefix: str = "pdf_text_compare",
) -> None:
    actual_pdf = Path(actual_pdf)
    expected_pdf = Path(expected_pdf)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    actual_pages = _extract_pdf_text_pages(actual_pdf, sort=sort_text)
    expected_pages = _extract_pdf_text_pages(expected_pdf, sort=sort_text)

    if len(actual_pages) != len(expected_pages):
        pytest.fail(
            f"PDF page count differs. expected={len(expected_pages)}, actual={len(actual_pages)}"
        )

    diff_found = False
    all_diffs: list[str] = []

    for page_index, (actual_text, expected_text) in enumerate(zip(actual_pages, expected_pages)):
        page_no = page_index + 1

        if normalize_whitespace:
            actual_text = _normalize_pdf_text(actual_text, flatten_to_single_line=flatten_to_single_line,)
            expected_text = _normalize_pdf_text(expected_text, flatten_to_single_line=flatten_to_single_line,)

        actual_text = _apply_ignore_patterns(actual_text, ignore_patterns)
        expected_text = _apply_ignore_patterns(expected_text, ignore_patterns)

        if actual_text != expected_text:
            diff_found = True

            diff_lines = list(
                difflib.unified_diff(
                    expected_text.splitlines(),
                    actual_text.splitlines(),
                    fromfile=f"expected_page_{page_no}",
                    tofile=f"actual_page_{page_no}",
                    lineterm="",
                )
            )

            diff_text = "\n".join(diff_lines) if diff_lines else "Texts differ, but no unified diff was produced."

            expected_path = output_dir / f"{name_prefix}_page-{page_no}_expected.txt"
            actual_path = output_dir / f"{name_prefix}_page-{page_no}_actual.txt"
            diff_path = output_dir / f"{name_prefix}_page-{page_no}_diff.txt"

            expected_path.write_text(expected_text, encoding="utf-8")
            actual_path.write_text(actual_text, encoding="utf-8")
            diff_path.write_text(diff_text, encoding="utf-8")

            allure.attach(
                expected_text,
                name=f"expected_text_page_{page_no}",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                actual_text,
                name=f"actual_text_page_{page_no}",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                diff_text,
                name=f"diff_text_page_{page_no}",
                attachment_type=allure.attachment_type.TEXT,
            )

            all_diffs.append(f"Page {page_no} differs.\n{diff_text}")

    if diff_found:
        summary_path = output_dir / f"{name_prefix}_summary.txt"
        summary_path.write_text("\n\n".join(all_diffs), encoding="utf-8")
        pytest.fail(f"PDF text comparison failed. See diff files in: {output_dir}")