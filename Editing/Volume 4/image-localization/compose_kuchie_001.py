#!/usr/bin/env python3
"""Composite the English text field for Volume 4's colour frontispiece."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "Source/Volume 4/images/kuchie-001.jpg"
OUTPUT = ROOT / "English/Volume 4/localized-images/kuchie-001.jpg"
DISPLAY_FONT = Path(
    "/home/yogesh/.local/share/fonts/lightnovel/PlayfairDisplay-500.ttf"
)
SUBTITLE_FONT = Path(
    "/home/yogesh/.local/share/fonts/lightnovel/PlayfairDisplay-400.ttf"
)
CREDIT_FONT = Path(
    "/home/yogesh/.local/share/fonts/lightnovel/Montserrat-300.ttf"
)
GREEN = (168, 209, 130)
FIELD_TOP = 1584
SCALE = 4
MAIN_TITLE_SIZE = 69
SMALL_TITLE_SIZE = 48
SUBTITLE_SIZE = 22
AUTHOR_SIZE = 30
ROLE_SIZE = 24
ILLUSTRATOR_SIZE = 28
NUMERAL_SIZE = 32


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tight_text_mask(text: str, font_path: Path, size: int) -> Image.Image:
    font = ImageFont.truetype(str(font_path), size * SCALE)
    left, top, right, bottom = font.getbbox(text)
    pad = 8 * SCALE
    mask = Image.new("L", (right - left + 2 * pad, bottom - top + 2 * pad), 0)
    draw = ImageDraw.Draw(mask)
    draw.text((pad - left, pad - top), text, font=font, fill=255)
    bbox = mask.getbbox()
    assert bbox is not None
    return mask.crop(bbox)


def tracked_text_mask(
    text: str, font_path: Path, size: int, tracking: float
) -> Image.Image:
    font = ImageFont.truetype(str(font_path), size * SCALE)
    lengths = [font.getlength(char) for char in text]
    width = int(round(sum(lengths) + tracking * SCALE * (len(text) - 1)))
    left, top, right, bottom = font.getbbox(text)
    pad = 8 * SCALE
    mask = Image.new("L", (width + 2 * pad, bottom - top + 2 * pad), 0)
    draw = ImageDraw.Draw(mask)
    x = float(pad)
    for char, length in zip(text, lengths):
        draw.text((round(x), pad - top), char, font=font, fill=255)
        x += length + tracking * SCALE
    bbox = mask.getbbox()
    assert bbox is not None
    return mask.crop(bbox)


def hierarchical_title_mask() -> Image.Image:
    """Render the title on one baseline, with the connective phrase subordinate."""
    main_font = ImageFont.truetype(str(DISPLAY_FONT), MAIN_TITLE_SIZE * SCALE)
    small_font = ImageFont.truetype(str(DISPLAY_FONT), SMALL_TITLE_SIZE * SCALE)
    segments = [
        ("Wand Maker", main_font),
        ("of the", small_font),
        ("Ruined World", main_font),
    ]
    gap = 22 * SCALE
    widths = [font.getlength(text) for text, font in segments]
    ascender = max(
        -font.getbbox(text, anchor="ls")[1] for text, font in segments
    )
    descender = max(
        font.getbbox(text, anchor="ls")[3] for text, font in segments
    )
    pad = 16 * SCALE
    mask = Image.new(
        "L",
        (
            round(sum(widths) + 2 * gap + 2 * pad),
            round(ascender + descender + 2 * pad),
        ),
        0,
    )
    draw = ImageDraw.Draw(mask)
    x = float(pad)
    baseline = pad + ascender
    for index, (text, font) in enumerate(segments):
        draw.text(
            (round(x), round(baseline)),
            text,
            font=font,
            fill=255,
            anchor="ls",
        )
        x += font.getlength(text)
        if index < len(segments) - 1:
            x += gap
    bbox = mask.getbbox()
    assert bbox is not None
    mask = mask.crop(bbox)
    # Downsample the four-times antialiased render without distorting
    # Playfair's natural width.  At 69 px the fitted mask is 985 px wide.
    return mask.resize(
        (round(mask.width / SCALE), round(mask.height / SCALE)),
        Image.Resampling.LANCZOS,
    )


def resized(mask: Image.Image, width: int, height: int) -> Image.Image:
    return mask.resize((width, height), Image.Resampling.LANCZOS)


def place(mask: Image.Image, x: int, y: int, field: Image.Image) -> None:
    color = Image.new("RGB", mask.size, GREEN)
    field.paste(color, (x, y - FIELD_TOP), mask)


def sample_green(source: np.ndarray) -> tuple[int, int, int]:
    """Modal RGB after a 5x5 erosion of the large-title green mask."""
    region = source[1645:1742, 105:1115]
    green = (
        (region[:, :, 1].astype(int) - region[:, :, 0].astype(int) > 20)
        & (region[:, :, 1].astype(int) - region[:, :, 2].astype(int) > 20)
        & (region.mean(axis=2) < 245)
    )
    interior = green.copy()
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            interior &= np.roll(np.roll(green, dy, axis=0), dx, axis=1)
    colors, counts = np.unique(region[interior], axis=0, return_counts=True)
    return tuple(int(v) for v in colors[np.argmax(counts)])


def ink_bbox(image: np.ndarray, nominal: tuple[int, int, int, int]) -> list[int]:
    x0, y0, x1, y1 = nominal
    crop = image[y0:y1, x0:x1]
    # All localized ink has a green excess. JPEG ringing that lacks that hue is ignored.
    distance_from_white = 255 - crop.min(axis=2).astype(int)
    mask = (
        (crop[:, :, 1].astype(int) - crop[:, :, 0].astype(int) > 4)
        & (crop[:, :, 1].astype(int) - crop[:, :, 2].astype(int) > 4)
        & (distance_from_white > 20)
    )
    ys, xs = np.where(mask)
    assert len(xs)
    return [int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max()), int(y0 + ys.max())]


def main() -> None:
    source_before = sha256(SOURCE)
    source_image = Image.open(SOURCE).convert("RGB")
    source = np.asarray(source_image)
    sampled = sample_green(source)
    if sampled != GREEN:
        raise RuntimeError(f"Expected sampled green {GREEN}, got {sampled}")

    field = Image.new("RGB", (1440, 2048 - FIELD_TOP), (255, 255, 255))

    main_mask = hierarchical_title_mask()
    place(main_mask, 113, 1654, field)

    mark = Image.new("L", (72 * SCALE, 64 * SCALE), 0)
    mark_draw = ImageDraw.Draw(mark)
    mark_draw.ellipse(
        (8 * SCALE, 8 * SCALE, 60 * SCALE, 56 * SCALE),
        outline=255,
        width=3 * SCALE,
    )
    four = tight_text_mask("4", DISPLAY_FONT, NUMERAL_SIZE)
    four.thumbnail((24 * SCALE, 30 * SCALE), Image.Resampling.LANCZOS)
    mark.paste(
        four,
        (
            int((mark.width - four.width) / 2),
            int((mark.height - four.height) / 2) - SCALE,
        ),
        four,
    )
    mark = mark.resize((72, 64), Image.Resampling.LANCZOS)
    place(mark, 1110, 1674, field)

    subtitle_mask = resized(
        tracked_text_mask(
            "Wand Maker of the Ruined World",
            SUBTITLE_FONT,
            SUBTITLE_SIZE,
            7.0,
        ),
        528,
        16,
    )
    place(subtitle_mask, 115, 1761, field)

    author_mask = resized(
        tight_text_mask("Kurodome Hagane", CREDIT_FONT, AUTHOR_SIZE), 246, 30
    )
    role_mask = resized(
        tight_text_mask("Illustrator", CREDIT_FONT, ROLE_SIZE), 106, 21
    )
    illustrator_mask = resized(
        tight_text_mask("Kayahara", CREDIT_FONT, ILLUSTRATOR_SIZE), 119, 25
    )
    place(author_mask, 686, 1919, field)
    place(role_mask, 960, 1925, field)
    place(illustrator_mask, 1103, 1924, field)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="kuchie-001-", dir="/tmp") as temp_dir:
        temp = Path(temp_dir)
        field_jpeg = temp / "field-q95-444.jpg"
        field.save(field_jpeg, "JPEG", quality=95, subsampling=0, optimize=False)

        # The edit boundary is an 8-pixel JPEG block boundary.  jpegtran inserts
        # only the rendered field's DCT blocks and retains every source block above.
        subprocess.run(
            [
                "jpegtran",
                "-copy",
                "all",
                "-trim",
                "-drop",
                f"+0+{FIELD_TOP}",
                str(field_jpeg),
                "-outfile",
                str(OUTPUT),
                str(SOURCE),
            ],
            check=True,
        )

    source_after = sha256(SOURCE)
    if source_before != source_after:
        raise RuntimeError("Source hash changed")

    out_image = Image.open(OUTPUT)
    out = np.asarray(out_image.convert("RGB"))
    illustration_diff = np.abs(
        out[:FIELD_TOP].astype(np.int16) - source[:FIELD_TOP].astype(np.int16)
    )
    differing = int(np.any(illustration_diff != 0, axis=2).sum())
    mad = float(illustration_diff.mean())
    if differing or mad:
        raise RuntimeError(
            f"Frozen illustration changed: differing={differing}, MAD={mad}"
        )

    regions = {
        "main_title": (90, 1635, 1105, 1745),
        "circled_4": (1105, 1660, 1195, 1750),
        "sub_title": (100, 1745, 660, 1790),
        "author": (670, 1905, 945, 1960),
        "Illustrator": (945, 1910, 1080, 1960),
        "Kayahara": (1090, 1910, 1235, 1960),
    }
    bboxes = {name: ink_bbox(out, bounds) for name, bounds in regions.items()}

    field_out = out[FIELD_TOP:]
    ink_blocks = np.zeros(field_out.shape[:2], dtype=bool)
    placed_elements = [
        (113, 1654, 1098, 1709),
        (1110, 1674, 1182, 1738),
        (115, 1761, 643, 1777),
        (686, 1919, 932, 1949),
        (960, 1925, 1066, 1946),
        (1103, 1924, 1222, 1949),
    ]
    for x0, y0, x1, y1 in placed_elements:
        y0 -= FIELD_TOP
        y1 -= FIELD_TOP
        block_x0, block_x1 = (x0 // 8) * 8, ((x1 + 7) // 8) * 8
        block_y0, block_y1 = (y0 // 8) * 8, ((y1 + 7) // 8) * 8
        ink_blocks[block_y0:block_y1, block_x0:block_x1] = True
    nonwhite_outside_type_blocks = int(
        np.any(field_out != 255, axis=2)[~ink_blocks].sum()
    )

    print(
        json.dumps(
            {
                "source_sha256_before": source_before,
                "source_sha256_after": source_after,
                "sampled_green_rgb": sampled,
                "output_format": out_image.format,
                "output_mode": out_image.mode,
                "output_size": out_image.size,
                "output_layers": out_image.layer,
                "output_bytes": OUTPUT.stat().st_size,
                "main_title_font": str(DISPLAY_FONT),
                "main_title_size": MAIN_TITLE_SIZE,
                "small_title_font": str(DISPLAY_FONT),
                "small_title_size": SMALL_TITLE_SIZE,
                "small_to_main_size_ratio": (
                    SMALL_TITLE_SIZE / MAIN_TITLE_SIZE
                ),
                "subtitle_font": str(SUBTITLE_FONT),
                "subtitle_size": SUBTITLE_SIZE,
                "subtitle_tracking": 7.0,
                "credit_font": str(CREDIT_FONT),
                "author_size": AUTHOR_SIZE,
                "role_size": ROLE_SIZE,
                "illustrator_size": ILLUSTRATOR_SIZE,
                "numeral_font": str(DISPLAY_FONT),
                "numeral_size": NUMERAL_SIZE,
                "jpeg_quality_setting_for_rendered_field": 95,
                "jpeg_subsampling_setting_for_rendered_field": 0,
                "illustration_mad": mad,
                "illustration_differing_pixels": differing,
                "nonwhite_pixels_outside_type_dct_blocks_in_white_field": (
                    nonwhite_outside_type_blocks
                ),
                "canvas_corners": {
                    "top_left": out[0, 0].tolist(),
                    "top_right": out[0, -1].tolist(),
                    "bottom_left": out[-1, 0].tolist(),
                    "bottom_right": out[-1, -1].tolist(),
                },
                "ink_bboxes_inclusive": bboxes,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
