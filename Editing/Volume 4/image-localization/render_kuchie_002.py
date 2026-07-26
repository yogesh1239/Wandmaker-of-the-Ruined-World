#!/usr/bin/env python3
"""Composite the English kuchie-002 plate using only Pillow and NumPy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, JpegImagePlugin


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "Source/Volume 4/images/kuchie-002.jpg"
OUTPUT = ROOT / "English/Volume 4/localized-images/kuchie-002.jpg"
DEBUG = ROOT / "Editing/Volume 4/image-localization/kuchie-002-inpaint-debug.png"
MASK_DEBUG = ROOT / "Editing/Volume 4/image-localization/kuchie-002-mask-debug.png"
REPORT = ROOT / "Editing/Volume 4/image-localization/kuchie-002-render-report.json"

PLAYFAIR = Path("/home/yogesh/.local/share/fonts/lightnovel/PlayfairDisplay-700.ttf")
SPECTRAL = Path("/home/yogesh/.local/share/fonts/lightnovel/Spectral-400.ttf")

DIALOGUE = {
    "R": (
        (1540, 1030, 2020, 1300),
        "\"Hmm. Cyanos and my amulet are both blue, so... going with cool colors might work. "
        "What about you, Ori? Do you like red? I'm starting to think matching your fire "
        "salamanders' colors could work too.\"",
    ),
    "C1": ((700, 745, 1010, 870), "\"Why would you match the colors to my pets?\""),
    "C2": ((700, 900, 1010, 985), "\"Why...? Well...\""),
    "L": (
        (150, 1100, 620, 1330),
        "\"Your eyes are a really pretty blue, Hiyori, and your hair has a bluish tint too. "
        "If you don't have a particular favorite color, wouldn't a pet that matches your own "
        "distinctive colors suit you better?\"",
    ),
    "E": ((150, 1360, 330, 1400), "\"................\""),
}

LOOK_RECTS = {
    "blue_latin": (168, 683, 280, 696),
    "blue_jp": (108, 707, 285, 741),
    "ori_latin": (1306, 1108, 1451, 1125),
    "ori_jp": (1243, 1129, 1481, 1181),
    "R": (1774, 907, 1950, 1385),
    "C": (690, 725, 848, 1121),
    "L": (155, 1060, 473, 1427),
    "E": (123, 1126, 151, 1263),
}

PROTECTED = {
    "left_girl_face": (180, 180, 640, 560),
    "right_pair_faces": (1150, 150, 1600, 500),
    "pouch_sparrow_inset": (1600, 10, 2010, 300),
    "open_book": (1150, 880, 1450, 1030),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def max_dilate(mask: np.ndarray, size: int) -> np.ndarray:
    image = Image.fromarray((mask.astype(np.uint8) * 255), "L")
    return np.asarray(image.filter(ImageFilter.MaxFilter(size))) > 0


def glyph_components(mask: np.ndarray) -> np.ndarray:
    """Keep glyph-scale connected components and reject broad artwork highlights."""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    kept = np.zeros_like(mask, dtype=bool)
    ys, xs = np.nonzero(mask)
    for sy, sx in zip(ys.tolist(), xs.tolist()):
        if seen[sy, sx]:
            continue
        stack = [(sy, sx)]
        seen[sy, sx] = True
        pixels: list[tuple[int, int]] = []
        min_x = max_x = sx
        min_y = max_y = sy
        while stack:
            y, x = stack.pop()
            pixels.append((y, x))
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if (
                        0 <= ny < h
                        and 0 <= nx < w
                        and mask[ny, nx]
                        and not seen[ny, nx]
                    ):
                        seen[ny, nx] = True
                        stack.append((ny, nx))
        cw = max_x - min_x + 1
        ch = max_y - min_y + 1
        area = len(pixels)
        normal_glyph = cw <= 52 and ch <= 72 and area <= 1800
        slender_bracket = (cw <= 24 and ch <= 180 and area <= 1800) or (
            ch <= 24 and cw <= 180 and area <= 1800
        )
        if normal_glyph or slender_bracket:
            for y, x in pixels:
                kept[y, x] = True
    return kept


def local_blur(channel: np.ndarray, radius: float) -> np.ndarray:
    im = Image.fromarray(np.clip(channel, 0, 255).astype(np.uint8), "L")
    return np.asarray(im.filter(ImageFilter.GaussianBlur(radius)), dtype=np.float32)


def build_mask(rgb: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    """Detect source glyph cores inside the filed look rectangles, then include glow."""
    h, w = rgb.shape[:2]
    mask = np.zeros((h, w), dtype=bool)
    counts: dict[str, int] = {}
    lum = (
        rgb[..., 0].astype(np.float32) * 0.2126
        + rgb[..., 1].astype(np.float32) * 0.7152
        + rgb[..., 2].astype(np.float32) * 0.0722
    )
    chroma = rgb.max(axis=2).astype(np.int16) - rgb.min(axis=2).astype(np.int16)

    for key in ("R", "C", "L", "E"):
        x0, y0, x1, y1 = LOOK_RECTS[key]
        roi = rgb[y0:y1, x0:x1]
        roi_l = lum[y0:y1, x0:x1]
        roi_c = chroma[y0:y1, x0:x1]
        blurred = local_blur(roi_l, 2.2)
        # The source dialogue has a genuinely white core. Requiring both a
        # neutral highlight and positive local contrast avoids masking broad
        # patches of pale skin/window wash.
        core = (
            (roi.min(axis=2) >= 205)
            & (roi_c <= 50)
            & ((roi_l - blurred) >= 5.0)
        )
        # Pure/near-pure white punctuation can be too small for the high-pass
        # test; retain it explicitly.
        core |= (roi.min(axis=2) >= 238) & (roi_c <= 22)
        core = glyph_components(core)
        expanded = max_dilate(core, 15)
        mask[y0:y1, x0:x1] |= expanded
        counts[key] = int(expanded.sum())

    # Violet nameplate: color proximity and blue-violet hue discriminate it
    # from the warm skin and olive clothing underneath.
    target_blue = np.array([111, 77, 159], dtype=np.int16)
    for key in ("blue_latin", "blue_jp"):
        x0, y0, x1, y1 = LOOK_RECTS[key]
        roi = rgb[y0:y1, x0:x1].astype(np.int16)
        dist = np.sqrt(np.sum((roi - target_blue) ** 2, axis=2))
        core = (
            (dist <= 155)
            & (roi[..., 2] >= 55)
            & ((roi[..., 2] - roi[..., 0]) >= 8)
            & ((roi[..., 2] - roi[..., 1]) >= 12)
        )
        core = glyph_components(core)
        expanded = max_dilate(core, 13)
        mask[y0:y1, x0:x1] |= expanded
        counts[key] = int(expanded.sum())

    # Ori nameplate: black letterforms sit on a teal glow. A black-hat style
    # local contrast detector follows the strokes without flattening the glow.
    for key in ("ori_latin", "ori_jp"):
        x0, y0, x1, y1 = LOOK_RECTS[key]
        roi_l = lum[y0:y1, x0:x1]
        blurred = local_blur(roi_l, 3.2)
        core = (roi_l <= 95) & ((blurred - roi_l) >= 3.0)
        core = glyph_components(core)
        expanded = max_dilate(core, 13)
        mask[y0:y1, x0:x1] |= expanded
        counts[key] = int(expanded.sum())

    return mask, counts


def resize_float(array: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    if array.ndim == 2:
        im = Image.fromarray(array.astype(np.float32), "F")
        return np.asarray(im.resize(size, Image.Resampling.BILINEAR), dtype=np.float32)
    channels = [resize_float(array[..., c], size) for c in range(array.shape[2])]
    return np.stack(channels, axis=2)


def gaussian_down(array: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    # Five-tap binomial Gaussian, separable, kept in float so normalized
    # premultiplied colors and confidence weights stay numerically aligned.
    kernel = np.array([1, 4, 6, 4, 1], dtype=np.float32) / 16.0
    work = array.astype(np.float32)
    if work.ndim == 2:
        work = work[..., None]
    padded_x = np.pad(work, ((0, 0), (2, 2), (0, 0)), mode="edge")
    blurred_x = sum(kernel[i] * padded_x[:, i : i + work.shape[1], :] for i in range(5))
    padded_y = np.pad(blurred_x, ((2, 2), (0, 0), (0, 0)), mode="edge")
    blurred = sum(kernel[i] * padded_y[i : i + work.shape[0], :, :] for i in range(5))
    channels = [resize_float(blurred[..., c], size) for c in range(blurred.shape[2])]
    result = np.stack(channels, axis=2)
    return result[..., 0] if array.ndim == 2 else result


def push_pull_fill(rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Normalized multi-scale push-pull with bilinear pull/refinement."""
    image0 = rgb.astype(np.float32)
    valid0 = (~mask).astype(np.float32)
    premul_levels = [image0 * valid0[..., None]]
    weight_levels = [valid0]
    sizes = [(rgb.shape[1], rgb.shape[0])]

    while min(sizes[-1]) > 12:
        prev_w, prev_h = sizes[-1]
        size = (max(1, (prev_w + 1) // 2), max(1, (prev_h + 1) // 2))
        premul_levels.append(gaussian_down(premul_levels[-1], size))
        weight_levels.append(gaussian_down(weight_levels[-1], size))
        sizes.append(size)

    weight = weight_levels[-1]
    estimate = premul_levels[-1] / np.maximum(weight[..., None], 1e-6)
    if np.any(weight < 1e-6):
        fallback = np.mean(image0[~mask], axis=0)
        estimate[weight < 1e-6] = fallback

    for level in range(len(sizes) - 2, -1, -1):
        up = resize_float(estimate, sizes[level])
        weight = weight_levels[level]
        known = premul_levels[level] / np.maximum(weight[..., None], 1e-6)
        # At each level, exact known-valid pixels win; only incomplete/masked
        # pixels receive the bilinearly pulled coarser estimate.
        alpha = np.clip(weight, 0.0, 1.0)[..., None]
        estimate = known * alpha + up * (1.0 - alpha)

    # The estimate is smooth, but a binary paste can reveal the irregular
    # dilation boundary over a painted gradient. Feather inward only: pixels
    # outside the mask remain byte-identical, while glyph cores receive the
    # full pulled estimate and the clean outer margin eases the transition.
    soft = np.asarray(
        Image.fromarray((mask.astype(np.uint8) * 255), "L").filter(
            ImageFilter.GaussianBlur(3.0)
        ),
        dtype=np.float32,
    ) / 255.0
    soft = np.clip((soft - 0.10) / 0.58, 0.0, 1.0)
    alpha = soft[..., None]
    blended = image0 * (1.0 - alpha) + estimate * alpha
    result = image0.copy()
    result[mask] = blended[mask]
    return np.clip(np.rint(result), 0, 255).astype(np.uint8)


def tracked_text_mask(
    text: str, font: ImageFont.FreeTypeFont, spacing: int
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    bboxes = [font.getbbox(ch) for ch in text]
    widths = [font.getlength(ch) for ch in text]
    left = min(b[0] for b in bboxes)
    top = min(b[1] for b in bboxes)
    right = int(np.ceil(sum(widths) + spacing * (len(text) - 1))) + 4
    bottom = max(b[3] for b in bboxes)
    canvas = Image.new("L", (right - left + 4, bottom - top + 4), 0)
    draw = ImageDraw.Draw(canvas)
    x = 2 - left
    for ch, advance in zip(text, widths):
        draw.text((x, 2 - top), ch, font=font, fill=255)
        x += advance + spacing
    return canvas, canvas.getbbox() or (0, 0, 0, 0)


def wrap_text(
    text: str, font: ImageFont.FreeTypeFont, max_width: int
) -> list[str]:
    words = text.split(" ")
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = current + " " + word
        if font.getlength(candidate) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)

    # Avoid orphaned final words by moving one word from the prior line.
    if len(lines) >= 2 and " " not in lines[-1]:
        prior = lines[-2].split(" ")
        if len(prior) > 2:
            moved = prior.pop()
            lines[-2] = " ".join(prior)
            lines[-1] = moved + " " + lines[-1]

    # Avoid article/preposition endings when a phrase can be moved intact.
    orphans = {
        "a", "an", "the", "to", "of", "for", "with", "at", "from", "in", "on",
        "and", "or", "but", "your", "my",
    }
    for i in range(len(lines) - 1):
        parts = lines[i].split(" ")
        if parts and parts[-1].lower().strip("\"'.,?!") in orphans and len(parts) > 1:
            moved = parts.pop()
            candidate_next = moved + " " + lines[i + 1]
            if font.getlength(candidate_next) <= max_width:
                lines[i] = " ".join(parts)
                lines[i + 1] = candidate_next
    return lines


def text_bbox_at(mask: Image.Image, xy: tuple[int, int]) -> tuple[int, int, int, int]:
    bbox = mask.getbbox()
    if bbox is None:
        return (xy[0], xy[1], xy[0], xy[1])
    return (bbox[0] + xy[0], bbox[1] + xy[1], bbox[2] + xy[0], bbox[3] + xy[1])


def render_dialogue(
    base: Image.Image,
) -> tuple[dict[str, tuple[int, int, int, int]], int, dict[str, list[str]]]:
    final_size = None
    final_layout: dict[str, list[str]] = {}
    for size in range(34, 15, -1):
        font = ImageFont.truetype(str(SPECTRAL), size)
        leading = int(round(size * 1.4))
        layout: dict[str, list[str]] = {}
        fits = True
        for key, (box, text) in DIALOGUE.items():
            x0, y0, x1, y1 = box
            lines = wrap_text(text, font, x1 - x0)
            ink_top = min(font.getbbox(line)[1] for line in lines)
            ink_bottom = max(font.getbbox(line)[3] for line in lines)
            height = (len(lines) - 1) * leading + ink_bottom - ink_top
            max_line = max(font.getlength(line) for line in lines)
            if height > (y1 - y0) or max_line > (x1 - x0):
                fits = False
                break
            layout[key] = lines
        if fits:
            final_size = size
            final_layout = layout
            break
    if final_size is None:
        raise RuntimeError("No common dialogue font size fits all boxes")

    font = ImageFont.truetype(str(SPECTRAL), final_size)
    leading = int(round(final_size * 1.4))
    ink_boxes: dict[str, tuple[int, int, int, int]] = {}
    for key, lines in final_layout.items():
        box, _ = DIALOGUE[key]
        x0, y0, x1, y1 = box
        local = Image.new("L", (x1 - x0, y1 - y0), 0)
        draw = ImageDraw.Draw(local)
        first_top = min(font.getbbox(line)[1] for line in lines)
        draw_y = -first_top
        for line in lines:
            draw.text((0, draw_y), line, font=font, fill=255)
            draw_y += leading

        # Soft low-opacity near-black outer glow, matching the source.
        shadow_alpha = local.filter(ImageFilter.GaussianBlur(4.5)).point(
            lambda p: int(round(p * 0.46))
        )
        shadow = Image.new("RGBA", local.size, (8, 10, 14, 0))
        shadow.putalpha(shadow_alpha)
        base.alpha_composite(shadow, (x0, y0))
        white = Image.new("RGBA", local.size, (255, 255, 255, 0))
        white.putalpha(local)
        base.alpha_composite(white, (x0, y0))
        ink_boxes[key] = text_bbox_at(local, (x0, y0))
    return ink_boxes, final_size, final_layout


def render_nameplate(
    base: Image.Image,
    text: str,
    xy: tuple[int, int],
    color: tuple[int, int, int],
    font_size: int,
    tracking: int,
) -> tuple[int, int, int, int]:
    font = ImageFont.truetype(str(PLAYFAIR), font_size)
    mask, _ = tracked_text_mask(text, font, tracking)
    color_layer = Image.new("RGBA", mask.size, (*color, 0))
    color_layer.putalpha(mask)
    base.alpha_composite(color_layer, xy)
    return text_bbox_at(mask, xy)


def mean_abs_diff(a: np.ndarray, b: np.ndarray, box: tuple[int, int, int, int]) -> float:
    x0, y0, x1, y1 = box
    return float(np.mean(np.abs(a[y0:y1, x0:x1].astype(np.int16) - b[y0:y1, x0:x1].astype(np.int16))))


def main() -> None:
    before = sha256(SOURCE)
    with Image.open(SOURCE) as im:
        source_image = im.convert("RGB")
    source = np.asarray(source_image)
    if source.shape != (1456, 2048, 3):
        raise RuntimeError(f"Unexpected source shape: {source.shape}")

    mask, mask_counts = build_mask(source)
    inpainted = push_pull_fill(source, mask)
    DEBUG.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(inpainted, "RGB").save(DEBUG, format="PNG")

    # A source overlay makes it possible to audit that the mask follows glyphs
    # rather than the full look rectangles.
    overlay = source.copy()
    overlay[mask] = np.array([255, 0, 255], dtype=np.uint8)
    Image.fromarray(overlay, "RGB").save(MASK_DEBUG, format="PNG")

    composite = Image.fromarray(inpainted, "RGB").convert("RGBA")
    name_boxes = {
        # tracked_text_mask removes the font's top bearing, so these coordinates
        # are the actual visible-ink origins inside the filed dominant slots.
        "Blue Witch": render_nameplate(
            composite, "Blue Witch", (108, 707), (111, 77, 159), 44, 4
        ),
        "Ori Kenshi": render_nameplate(
            composite, "Ori Kenshi", (1243, 1129), (35, 43, 46), 44, 4
        ),
    }
    dialogue_boxes, dialogue_size, layouts = render_dialogue(composite)
    final = composite.convert("RGB")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    final.save(OUTPUT, format="JPEG", quality=95, subsampling=0, optimize=True)
    after = sha256(SOURCE)
    if before != after:
        raise RuntimeError("Source hash changed")

    with Image.open(OUTPUT) as check:
        check.load()
        saved = np.asarray(check.convert("RGB"))
        sampling = JpegImagePlugin.get_sampling(check)
        output_info = {
            "format": check.format,
            "mode": check.mode,
            "size": list(check.size),
            "quality_save_parameter": 95,
            "subsampling": sampling,
            "bytes": OUTPUT.stat().st_size,
        }

    protected_mad = {
        key: mean_abs_diff(source, saved, box) for key, box in PROTECTED.items()
    }
    # JPEG recompression changes every pixel slightly; compare the pre-encode
    # composite too to prove protected art was never painted.
    final_array = np.asarray(final)
    protected_preencode_mad = {
        key: mean_abs_diff(source, final_array, box) for key, box in PROTECTED.items()
    }

    report = {
        "source_sha256_before": before,
        "source_sha256_after": after,
        "output_sha256": sha256(OUTPUT),
        "output": output_info,
        "mask_pixels": int(mask.sum()),
        "mask_pixels_by_region": mask_counts,
        "nameplate_ink_bboxes": {k: list(v) for k, v in name_boxes.items()},
        "dialogue_ink_bboxes": {k: list(v) for k, v in dialogue_boxes.items()},
        "dialogue_boxes": {k: list(v[0]) for k, v in DIALOGUE.items()},
        "dialogue_font_size": dialogue_size,
        "dialogue_layout": layouts,
        "fonts": {
            "nameplates": str(PLAYFAIR),
            "nameplate_size": 44,
            "nameplate_tracking": 4,
            "dialogue": str(SPECTRAL),
            "dialogue_size": dialogue_size,
            "dialogue_leading": int(round(dialogue_size * 1.4)),
        },
        "protected_mad_saved_jpeg": protected_mad,
        "protected_mad_preencode": protected_preencode_mad,
        "debug_inpaint": str(DEBUG),
        "debug_mask": str(MASK_DEBUG),
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
