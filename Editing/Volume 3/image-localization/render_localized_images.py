#!/usr/bin/env python3
"""Deterministic Volume 3 image-localization renderer.

Only the render-ready pages in render-queue.md are handled here.  The script
keeps each source canvas at its exact pixel dimensions and replaces the
specified text regions with the shared Noto typography system.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "Source/Volume 3/images"
OUTPUT = ROOT / "English/Volume 3/localized-images"
STORY = ROOT / "English/Volume 3/Booklet Short Story - I Liked Her First, Though.md"

SANS = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/noto/NotoSans-Bold.ttf"
SERIF_BOLD = "/usr/share/fonts/noto/NotoSerif-Bold.ttf"

BLUE = (0, 55, 111)
RED = (193, 31, 20)
DARK_RED = (121, 0, 0)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def save_png(im: Image.Image, name: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    im.save(OUTPUT / f"{name}.png", optimize=True)


def centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
) -> None:
    draw.text(xy, text, font=fnt, fill=fill, anchor="mm")


def render_p057() -> None:
    path = OUTPUT / "p057.png"
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im).copy()

    # Remove only the failed English glyphs.  The reconstructed gray field from
    # the prior render is retained; dark glyph pixels are replaced with the
    # row-wise median of the untouched field and softly feathered at the edge.
    x0, y0, x1, y1 = 54, 1798, 202, 1872
    crop = arr[y0:y1, x0:x1]
    luminance = crop.mean(axis=2)
    mask = luminance < 175
    mask_im = Image.fromarray((mask.astype(np.uint8) * 255)).filter(
        ImageFilter.MaxFilter(9)
    )
    mask = np.asarray(mask_im) > 0
    for row in range(crop.shape[0]):
        candidates = crop[row][~mask[row]]
        if len(candidates):
            fill = np.median(candidates, axis=0)
        else:
            fill = np.array([213, 213, 213])
        crop[row][mask[row]] = fill
    arr[y0:y1, x0:x1] = crop
    im = Image.fromarray(arr)

    draw = ImageDraw.Draw(im)
    # Source rectangular field: x=48..251, y=1613..2018.
    centered_text(draw, (150, 1816), "Huh?", font(SANS_BOLD, 55), (0, 0, 0))
    save_png(im, "p057")


def diffuse_red_text(im: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    """Clear red type while preserving dark line art crossing the same region."""
    arr = np.asarray(im.convert("RGB")).copy()
    x0, y0, x1, y1 = box
    crop = arr[y0:y1, x0:x1]
    red_mask = (
        (crop[:, :, 0].astype(np.int16) - crop[:, :, 1].astype(np.int16) > 70)
        & (crop[:, :, 0].astype(np.int16) - crop[:, :, 2].astype(np.int16) > 70)
        & (crop[:, :, 1] < 130)
    )
    red_mask = np.asarray(
        Image.fromarray((red_mask.astype(np.uint8) * 255)).filter(
            ImageFilter.MaxFilter(5)
        )
    ) > 0

    # Seed from paper pixels in the same box, then diffuse neighbor values into
    # the glyph shapes.  Non-red wand/lantern linework remains untouched.
    paper = (~red_mask) & (crop.mean(axis=2) > 135)
    seed = np.median(crop[paper], axis=0) if paper.any() else np.array([238, 220, 205])
    work = crop.astype(np.float32)
    work[red_mask] = seed
    for _ in range(180):
        avg = (
            np.roll(work, 1, axis=0)
            + np.roll(work, -1, axis=0)
            + np.roll(work, 1, axis=1)
            + np.roll(work, -1, axis=1)
        ) / 4.0
        work[red_mask] = avg[red_mask]
    crop[red_mask] = np.clip(work[red_mask], 0, 255).astype(np.uint8)
    arr[y0:y1, x0:x1] = crop
    return Image.fromarray(arr)


def draw_tracking(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    tracking: float,
) -> None:
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def draw_scaled_text(
    im: Image.Image,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    scale_x: float = 1.0,
) -> None:
    bbox = fnt.getbbox(text)
    layer = Image.new("RGBA", (bbox[2] + 10, bbox[3] - bbox[1] + 10), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((5, 5 - bbox[1]), text, font=fnt, fill=fill)
    if scale_x != 1.0:
        layer = layer.resize(
            (int(layer.width * scale_x), layer.height),
            Image.Resampling.LANCZOS,
        )
    im.paste(layer, xy, layer)


def render_s_h1() -> None:
    im = Image.open(SOURCE / "s-h1.jpg").convert("RGB")
    im = diffuse_red_text(im, (75, 210, 650, 385))
    im = diffuse_red_text(im, (75, 392, 535, 510))

    # The right title strip is a flat white field, separate from the artwork.
    draw = ImageDraw.Draw(im)
    draw.rectangle((1190, 30, 1439, 1840), fill=(255, 255, 255))

    title_font = font(SERIF_BOLD, 82)
    draw_scaled_text(im, (86, 225), "TOP SECRET", title_font, RED, 0.85)
    draw_scaled_text(im, (86, 305), "FILES", title_font, RED, 0.85)
    brand_font = font(SERIF_BOLD, 51)
    draw_scaled_text(im, (94, 402), "Wand Maker of", brand_font, RED, 0.85)
    draw_scaled_text(im, (94, 457), "the Ruined World", brand_font, RED, 0.85)

    # One rotated phrase preserves the source's deliberate vertical title
    # composition without stacking English a letter at a time.
    overlay = Image.new("RGBA", (1300, 100), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    phrase_font = font(SERIF_BOLD, 58)
    od.text((16, 8), "Wand Maker of the Ruined World", font=phrase_font, fill=DARK_RED)
    bbox = overlay.getbbox()
    overlay = overlay.crop(bbox).rotate(-90, expand=True, resample=Image.Resampling.BICUBIC)
    im.paste(overlay, (1250, 285), overlay)
    save_png(im, "s-h1")


def fit_font(text: str, max_width: int, preferred: int, minimum: int = 27) -> ImageFont.FreeTypeFont:
    for size in range(preferred, minimum - 1, -1):
        fnt = font(SANS_BOLD, size)
        if fnt.getlength(text) <= max_width:
            return fnt
    return font(SANS_BOLD, minimum)


def render_s_p003() -> None:
    im = Image.open(SOURCE / "s-p003.jpg").convert("RGB")
    draw = ImageDraw.Draw(im)
    # Preserve the source Contents header. Rebuild only the listed label field.
    draw.rectangle((525, 410, 1230, 1855), fill=(255, 255, 255))

    entries = [
        ("Character Profiles", "", True),
        ("Okyaku", "4", False),
        ("Murakumo Kariya", "6", False),
        ("Iwatsura", "8", False),
        ("Shirokarasu", "9", False),
        ("Tsubaki, Sekitan, Mokutan", "10", False),
        ("Mermaid Witch", "12", False),
        ("Aokera", "14", False),
        ("Itazu", "15", False),
        ("Sanukino Banzo", "16", False),
        ("Hakata Denjiro", "17", False),
        ("Magic Tool Profiles", "18", True),
        ("Timeline as of Volume 3", "24", True),
        ("The Nameless Epic Hypothesis", "25", True),
        ("Tokyo Sightseeing Guide", "26", True),
        ("Setting Notes", "28", True),
        ("Tohoku Hunting Association Secret Techniques:", "", True),
        ("Guide to Processing Special Materials", "30", True),
        ("Volume 3 Chapter Commentary", "32", True),
        ("Short Stories", "35", True),
        ("Colophon", "39", True),
    ]
    y = 430
    normal_gap = 57
    section_gap = 73
    for label, page, section in entries:
        preferred = 40 if section else 35
        fnt = fit_font(label, 570, preferred, 26)
        x = 552 if section else 625
        draw.text((x, y), label, font=fnt, fill=BLUE)
        if page:
            page_fnt = font(SANS_BOLD, 34)
            page_x = 1198
            page_w = draw.textlength(page, font=page_fnt)
            label_end = x + draw.textlength(label, font=fnt)
            line_y = y + int(fnt.size * 0.72)
            if label_end + 18 < page_x - page_w - 15:
                draw.line(
                    (label_end + 18, line_y, page_x - page_w - 15, line_y),
                    fill=BLUE,
                    width=2,
                )
            draw.text((page_x - page_w, y), page, font=page_fnt, fill=BLUE)
        elif label == "Character Profiles":
            line_y = y + int(fnt.size * 0.72)
            draw.line((x + draw.textlength(label, font=fnt) + 18, line_y, 1190, line_y), fill=BLUE, width=3)
        y += section_gap if section else normal_gap
    save_png(im, "s-p003")


RUBY_RE = re.compile(r"<ruby>(.*?)<rt>(.*?)</rt></ruby>")


def story_lines() -> list[str]:
    return STORY.read_text(encoding="utf-8").splitlines()


def selected_paragraphs(page: int) -> list[str]:
    lines = story_lines()
    if page == 35:
        paragraphs = [line for line in lines[0:38] if line.strip()]
        full = lines[38]
        split = full.index(" (wizard)")
        paragraphs.append(full[:split])
        return paragraphs
    if page == 36:
        full = lines[38]
        split = full.index(" (wizard)")
        return [full[split + 1 :]] + [line for line in lines[40:79] if line.strip()]
    if page == 37:
        return [line for line in lines[80:117] if line.strip()]
    if page == 38:
        return [line for line in lines[118:171] if line.strip()]
    raise ValueError(page)


def line_tokens(
    paragraph: str,
    draw: ImageDraw.ImageDraw,
    body_font: ImageFont.FreeTypeFont,
    ruby_font: ImageFont.FreeTypeFont,
    width: int,
) -> list[list[tuple[str, str | None]]]:
    ruby: list[tuple[str, str]] = []

    def replace_ruby(match: re.Match[str]) -> str:
        ruby.append((match.group(1), match.group(2)))
        return f"§{len(ruby) - 1}§"

    marked = RUBY_RE.sub(replace_ruby, paragraph).replace("[^1]", "¹")
    tokens: list[tuple[str, str | None]] = []
    for token in marked.split():
        marker = re.match(r"§(\d+)§(.*)", token)
        if marker:
            base, rt = ruby[int(marker.group(1))]
            tokens.append((base + marker.group(2), rt))
        else:
            tokens.append((token, None))
    lines: list[list[tuple[str, str | None]]] = []
    current: list[tuple[str, str | None]] = []
    used = 0.0
    space = draw.textlength(" ", font=body_font)
    for base, rt in tokens:
        rt_width = draw.textlength(rt, font=ruby_font) if rt else 0
        token_width = max(draw.textlength(base, font=body_font), rt_width)
        add = token_width + (space if current else 0)
        if current and used + add > width:
            lines.append(current)
            current = [(base, rt)]
            used = token_width
        else:
            current.append((base, rt))
            used += add
    if current:
        lines.append(current)
    return lines


def story_layout_fits(
    paragraphs: list[str],
    size: int,
    top: int,
    bottom: int,
    col_width: int,
) -> tuple[bool, list[list[list[tuple[str, str | None]]]]]:
    body_font = font(SANS, size)
    ruby_font = font(SANS, max(9, int(size * 0.48)))
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    wrapped = [line_tokens(p, dummy, body_font, ruby_font, col_width) for p in paragraphs]
    line_height = int(size * 1.34)
    para_gap = int(size * 0.70)
    available = bottom - top
    height = sum(len(lines) * line_height + para_gap for lines in wrapped)
    return height <= available * 2, wrapped


def render_story_page(page: int) -> None:
    im = Image.open(SOURCE / f"s-p{page:03d}.jpg").convert("RGB")
    draw = ImageDraw.Draw(im)

    # Preserve the yellow top/bottom bands and original page number. The source
    # body region contains text only, so a white reconstruction is exact.
    if page == 35:
        # The Japanese running header descends slightly into the full 114 px
        # source band. Match the sampled paper color, then rebuild body below.
        draw.rectangle((600, 0, 1395, 114), fill=(255, 250, 188))
    draw.rectangle((45, 114, 1395, 1950), fill=(255, 255, 255))
    if page == 35:
        # Clear and localize only the running header in the top band.
        centered_text(draw, (730, 39), "Short Stories", font(SANS_BOLD, 18), BLUE)
        centered_text(
            draw,
            (720, 133),
            "I Liked Her First, Though",
            font(SERIF_BOLD, 44),
            BLUE,
        )
        top = 205
    else:
        top = 110

    left = 75
    right = 1365
    gap = 45
    col_width = (right - left - gap) // 2
    bottom = 1925
    paragraphs = selected_paragraphs(page)

    wrapped = None
    size = 28
    for candidate in range(28, 24, -1):
        fits, candidate_wrapped = story_layout_fits(
            paragraphs, candidate, top, bottom, col_width
        )
        if fits:
            size = candidate
            wrapped = candidate_wrapped
            break
    if wrapped is None:
        _, wrapped = story_layout_fits(paragraphs, 25, top, bottom, col_width)
        size = 25

    body_font = font(SANS, size)
    ruby_font = font(SANS, max(9, int(size * 0.48)))
    line_height = int(size * 1.34)
    para_gap = int(size * 0.70)
    space = draw.textlength(" ", font=body_font)

    col = 0
    x = left
    y = top
    for lines in wrapped:
        para_height = len(lines) * line_height + para_gap
        if y + para_height > bottom and col == 0:
            col = 1
            x = left + col_width + gap
            y = top
        if y + para_height > bottom:
            raise RuntimeError(f"s-p{page:03d} text overflow at {size}px")
        for line in lines:
            cursor = x
            for base, rt in line:
                base_w = draw.textlength(base, font=body_font)
                rt_w = draw.textlength(rt, font=ruby_font) if rt else 0
                token_w = max(base_w, rt_w)
                if rt:
                    draw.text(
                        (cursor + (token_w - rt_w) / 2, y),
                        rt,
                        font=ruby_font,
                        fill=(0, 0, 0),
                    )
                draw.text(
                    (cursor + (token_w - base_w) / 2, y + 8),
                    base,
                    font=body_font,
                    fill=(0, 0, 0),
                )
                cursor += token_w + space
            y += line_height
        y += para_gap
    save_png(im, f"s-p{page:03d}")


def main() -> None:
    render_p057()
    render_s_h1()
    render_s_p003()
    for page in (35, 36, 37, 38):
        render_story_page(page)
    for stem in ("p057", "s-h1", "s-p003", "s-p035", "s-p036", "s-p037", "s-p038"):
        src_stem = stem if stem != "p057" else "p057"
        with Image.open(SOURCE / f"{src_stem}.jpg") as src, Image.open(OUTPUT / f"{stem}.png") as out:
            if src.size != out.size:
                raise RuntimeError(f"{stem}: {out.size} != source {src.size}")
        print(f"rendered {stem}.png")


if __name__ == "__main__":
    main()
