from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageOps,
    ImageChops
)
import argparse
import os
import math
import random
from collections import deque

# ============================================
# CONFIG
# ============================================

PALETTE_PRESETS = [256, 128, 64, 32, 24, 16, 8]
DEFAULT_SIZE = 256
MAX_COLS = 3

# Background sensitivity
BG_THRESHOLD = 40

# Remove enclosed BG pockets
REMOVE_INNER_BG = True

# Alpha threshold
ALPHA_THRESHOLD = 128


# ============================================
# COLOR HELPERS
# ============================================

def color_distance(c1, c2):
    return math.sqrt(
        (c1[0] - c2[0]) ** 2 +
        (c1[1] - c2[1]) ** 2 +
        (c1[2] - c2[2]) ** 2
    )


def average_color(colors):
    r = sum(c[0] for c in colors) // len(colors)
    g = sum(c[1] for c in colors) // len(colors)
    b = sum(c[2] for c in colors) // len(colors)
    return (r, g, b)


# ============================================
# CANVAS
# ============================================

def expand_to_canvas(img, target_size):

    img = img.convert("RGBA")

    target_w, target_h = target_size
    w, h = img.size

    canvas_w = max(w, target_w)
    canvas_h = max(h, target_h)

    if (w, h) == (canvas_w, canvas_h):
        return img

    canvas = Image.new(
        "RGBA",
        (canvas_w, canvas_h),
        (0, 0, 0, 0)
    )

    offset_x = (canvas_w - w) // 2
    offset_y = (canvas_h - h) // 2

    canvas.paste(img, (offset_x, offset_y), img)

    return canvas


# ============================================
# GRAYSCALE
# ============================================

def to_grayscale(img):

    img = img.convert("RGBA")

    r, g, b, a = img.split()

    gray = Image.merge("RGB", (r, g, b)).convert("L")
    gray_rgb = Image.merge("RGB", (gray, gray, gray))

    return Image.merge(
        "RGBA",
        (*gray_rgb.split(), a)
    )


# ============================================
# VIGNETTE
# ============================================

def add_vignette(img, strength=0.6, blur=120):

    img = img.convert("RGBA")

    w, h = img.size

    cx, cy = w // 2, h // 2
    max_dist = math.sqrt(cx * cx + cy * cy)

    mask = Image.new("L", (w, h), 0)

    for y in range(h):
        for x in range(w):

            dx = x - cx
            dy = y - cy

            dist = math.sqrt(dx * dx + dy * dy)

            val = 255 * (1 - (dist / max_dist))
            val = max(0, min(255, int(val)))

            mask.putpixel((x, y), val)

    mask = mask.filter(
        ImageFilter.GaussianBlur(radius=blur)
    )

    mask = ImageOps.invert(mask)

    if strength != 1.0:
        mask = mask.point(
            lambda p: int(p * strength)
        )

    vignette = Image.new(
        "RGBA",
        (w, h),
        (0, 0, 0, 255)
    )

    vignette.putalpha(mask)

    return Image.alpha_composite(img, vignette)


# ============================================
# DITHER
# ============================================

BAYER_8X8 = [
    [0,48,12,60,3,51,15,63],
    [32,16,44,28,35,19,47,31],
    [8,56,4,52,11,59,7,55],
    [40,24,36,20,43,27,39,23],
    [2,50,14,62,1,49,13,61],
    [34,18,46,30,33,17,45,29],
    [10,58,6,54,9,57,5,53],
    [42,26,38,22,41,25,37,21]
]


def ordered_dither(img, strength=24):

    img = img.convert("RGBA")

    pixels = img.load()

    w, h = img.size

    out_img = Image.new("RGBA", (w, h))
    out = out_img.load()

    for y in range(h):
        for x in range(w):

            r, g, b, a = pixels[x, y]

            if a == 0:
                out[x, y] = (0, 0, 0, 0)
                continue

            threshold = BAYER_8X8[y % 8][x % 8]

            offset = (
                ((threshold / 63.0) - 0.5)
                * strength
            )

            out[x, y] = (
                max(0, min(255, int(r + offset))),
                max(0, min(255, int(g + offset))),
                max(0, min(255, int(b + offset))),
                a
            )

    return out_img


def blue_noise_dither(img, strength=18, seed=1337):

    random.seed(seed)

    img = img.convert("RGBA")

    pixels = img.load()

    w, h = img.size

    noise_field = [
        [random.uniform(-1, 1) for _ in range(w)]
        for _ in range(h)
    ]

    out_img = Image.new("RGBA", (w, h))
    out = out_img.load()

    for y in range(h):
        for x in range(w):

            r, g, b, a = pixels[x, y]

            if a == 0:
                out[x, y] = (0, 0, 0, 0)
                continue

            noise = noise_field[y][x] * strength

            out[x, y] = (
                max(0, min(255, int(r + noise))),
                max(0, min(255, int(g + noise))),
                max(0, min(255, int(b + noise))),
                a
            )

    return out_img


# ============================================
# HALFTONE
# ============================================

def luminance(rgb):

    r, g, b = rgb

    return (
        0.299 * r +
        0.587 * g +
        0.114 * b
    )


def manga_halftone(base, cell=6):

    base = base.convert("RGBA")

    pixels = base.load()

    w, h = base.size

    overlay = Image.new(
        "RGBA",
        (w, h),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    for y in range(0, h, cell):
        for x in range(0, w, cell):

            sample = pixels[
                min(x, w - 1),
                min(y, h - 1)
            ]

            if sample[3] == 0:
                continue

            lum = luminance(sample[:3])

            radius = int(
                (1 - lum / 255) * (cell / 2)
            )

            if radius > 0:

                cx = x + cell // 2
                cy = y + cell // 2

                draw.ellipse(
                    (
                        cx - radius,
                        cy - radius,
                        cx + radius,
                        cy + radius
                    ),
                    fill=(0, 0, 0, 255)
                )

    return overlay


# ============================================
# BACKGROUND REMOVAL
# ============================================

def remove_background(img):

    img = img.convert("RGBA")

    pixels = img.load()

    w, h = img.size

    corner_samples = [
        pixels[0, 0][:3],
        pixels[w - 1, 0][:3],
        pixels[0, h - 1][:3],
        pixels[w - 1, h - 1][:3]
    ]

    bg_color = average_color(corner_samples)

    visited = set()
    queue = deque()

    # Flood-fill from edges
    for x in range(w):
        queue.append((x, 0))
        queue.append((x, h - 1))

    for y in range(h):
        queue.append((0, y))
        queue.append((w - 1, y))

    while queue:

        x, y = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        current = pixels[x, y][:3]

        if (
            color_distance(current, bg_color)
            <= BG_THRESHOLD
        ):

            pixels[x, y] = (0, 0, 0, 0)

            for nx, ny in (
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1)
            ):

                if 0 <= nx < w and 0 <= ny < h:
                    queue.append((nx, ny))

    # Remove enclosed background pockets
    if REMOVE_INNER_BG:

        for y in range(h):
            for x in range(w):

                r, g, b, a = pixels[x, y]

                if a == 0:
                    continue

                if (
                    color_distance(
                        (r, g, b),
                        bg_color
                    )
                    <= BG_THRESHOLD
                ):
                    pixels[x, y] = (0, 0, 0, 0)

    return img


# ============================================
# OUTLINE
# ============================================

def add_white_outline(
    img,
    thickness=1,
    color=(255, 255, 255, 255)
):
    """
    Expand the non-transparent subject outward by N pixels.

    The newly added pixels become the outline color,
    while the original image remains unchanged.
    """

    img = img.convert("RGBA")

    alpha = img.getchannel("A")

    # Binary mask
    alpha = alpha.point(
        lambda a: 255 if a >= ALPHA_THRESHOLD else 0
    )

    # Grow subject mask
    grown = alpha

    for _ in range(thickness):
        grown = grown.filter(
            ImageFilter.MaxFilter(3)
        )

    # Keep only newly added pixels
    outline_mask = ImageChops.subtract(
        grown,
        alpha
    )

    outline = Image.new(
        "RGBA",
        img.size,
        color
    )

    outline.putalpha(outline_mask)

    # Outline behind subject
    return Image.alpha_composite(
        outline,
        img
    )

# ============================================
# ALPHA NORMALIZATION
# ============================================

def normalize_alpha(img):

    img = img.convert("RGBA")

    pixels = img.load()

    w, h = img.size

    for y in range(h):
        for x in range(w):

            r, g, b, a = pixels[x, y]

            if a < ALPHA_THRESHOLD:
                pixels[x, y] = (0, 0, 0, 0)
            else:
                pixels[x, y] = (r, g, b, 255)

    return img


# ============================================
# QUANTIZE
# ============================================

def quantize_single_transparency(rgba, colors):

    rgba = normalize_alpha(rgba)

    w, h = rgba.size

    alpha = rgba.getchannel("A")

    rgb = Image.new(
        "RGB",
        rgba.size,
        (0, 0, 0)
    )

    rgb.paste(rgba, mask=alpha)

    indexed = rgb.quantize(
        colors=max(1, colors - 1),
        method=Image.Quantize.FASTOCTREE,
        dither=Image.Dither.NONE
    )

    indexed_rgba = indexed.convert("RGBA")

    out = Image.new(
        "RGBA",
        rgba.size,
        (0, 0, 0, 0)
    )

    out_pixels = out.load()

    src_pixels = indexed_rgba.load()

    alpha_pixels = alpha.load()

    for y in range(h):
        for x in range(w):

            if alpha_pixels[x, y] == 0:
                out_pixels[x, y] = (
                    0,
                    0,
                    0,
                    0
                )
            else:
                out_pixels[x, y] = src_pixels[x, y]

    return out


# ============================================
# RESIZE
# ============================================

def fit_to_canvas(img, target_size):

    img_w, img_h = img.size

    target_w, target_h = target_size

    scale = min(
        1,
        target_w / img_w,
        target_h / img_h
    )

    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    img_resized = img.resize(
        (new_w, new_h),
        Image.NEAREST
    )

    return expand_to_canvas(
        img_resized,
        target_size
    )


# ============================================
# PIPELINE
# ============================================

def make_version(
    img,
    colors,
    size,
    keep_aspect=False,
    remove_bg_flag=True,
    outline_flag=False,
    outline_size=1,
    dither_strength=16,
    dither_type="ordered",
    vignette_flag=False,
    vignette_strength=0.6,
    vignette_blur=120
):

    if remove_bg_flag:
        img = remove_background(img)

    if keep_aspect:

        img = fit_to_canvas(
            img,
            size
        )

    else:

        target_w, target_h = size

        img = img.resize(
            (target_w, target_h),
            Image.NEAREST
        )

    if dither_type in (
        "ordered",
        "bayer"
    ):

        base = ordered_dither(
            img,
            dither_strength
        )

    elif dither_type == "blue-noise":

        base = blue_noise_dither(
            img,
            dither_strength
        )

    else:
        base = img

    rgba = base.convert("RGBA")

    overlay = None

    if dither_type == "manga-halftone":
        overlay = manga_halftone(rgba)

    if overlay is not None:
        rgba = Image.alpha_composite(
            rgba,
            overlay
        )

    if outline_flag:
        rgba = add_white_outline(
            rgba,
            thickness=outline_size
        )

    if vignette_flag:

        rgba = add_vignette(
            rgba,
            strength=vignette_strength,
            blur=vignette_blur
        )

    rgba = normalize_alpha(rgba)

    indexed = quantize_single_transparency(
        rgba,
        colors
    )

    return indexed


# ============================================
# GRID
# ============================================

def create_grid(images, labels, size):

    padding = 12
    label_h = 28

    cols = min(MAX_COLS, len(images))
    rows = math.ceil(len(images) / cols)

    w = (
        cols * (size[0] + padding)
        + padding
    )

    h = (
        rows * (
            size[1] +
            label_h +
            padding
        )
        + padding
    )

    grid = Image.new(
        "RGBA",
        (w, h),
        (40, 40, 40, 255)
    )

    draw = ImageDraw.Draw(grid)

    for i, (img, label) in enumerate(
        zip(images, labels)
    ):

        r = i // cols
        c = i % cols

        x = padding + c * (
            size[0] + padding
        )

        y = padding + r * (
            size[1] +
            label_h +
            padding
        )

        draw.text(
            (x, y),
            label,
            fill=(255, 255, 255)
        )

        grid.paste(
            img.convert("RGBA"),
            (x, y + label_h),
            img.convert("RGBA")
        )

    return grid


# ============================================
# MAIN
# ============================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("input")

    parser.add_argument(
        "--preview",
        action="store_true"
    )

    parser.add_argument(
        "--colors",
        type=int,
        default=64
    )

    parser.add_argument(
        "--grayscale",
        action="store_true"
    )

    parser.add_argument(
        "--remove-bg",
        action="store_true"
    )

    parser.add_argument(
        "--outline",
        action="store_true"
    )

    parser.add_argument(
        "--outline-size",
        type=int,
        default=1
    )

    parser.add_argument(
        "--dither",
        type=int,
        default=18
    )

    parser.add_argument(
        "--keep-aspect",
        action="store_true"
    )

    parser.add_argument(
        "--dither-type",
        choices=[
            "ordered",
            "bayer",
            "blue-noise",
            "floyd",
            "none",
            "manga-halftone"
        ],
        default="ordered"
    )

    parser.add_argument(
        "--width",
        type=int,
        default=None
    )

    parser.add_argument(
        "--height",
        type=int,
        default=None
    )

    parser.add_argument(
        "--vignette",
        action="store_true"
    )

    parser.add_argument(
        "--vignette-strength",
        type=float,
        default=0.6
    )

    parser.add_argument(
        "--vignette-blur",
        type=int,
        default=120
    )

    args = parser.parse_args()

    img = Image.open(
        args.input
    ).convert("RGBA")

    if args.grayscale:
        img = to_grayscale(img)

    size = (
        args.width
        if args.width
        else DEFAULT_SIZE,

        args.height
        if args.height
        else DEFAULT_SIZE
    )

    if args.preview:

        versions = []
        labels = []

        for c in PALETTE_PRESETS:

            v = make_version(
                img,
                c,
                size,
                remove_bg_flag=args.remove_bg,
                outline_flag=args.outline,
                dither_strength=args.dither,
                dither_type=args.dither_type,
                vignette_flag=args.vignette,
                vignette_strength=args.vignette_strength,
                vignette_blur=args.vignette_blur
            )

            versions.append(v)
            labels.append(f"{c} colors")

        grid = create_grid(
            versions,
            labels,
            size
        )

        out = (
            f"{os.path.splitext(args.input)[0]}"
            f"_preview.png"
        )

        grid.save(out, format="PNG")

        print("saved:", out)

        return

    result = make_version(
        img,
        args.colors,
        size,
        keep_aspect=args.keep_aspect,
        remove_bg_flag=args.remove_bg,
        outline_flag=args.outline,
        outline_size=args.outline_size,
        dither_strength=args.dither,
        dither_type=args.dither_type,
        vignette_flag=args.vignette,
        vignette_strength=args.vignette_strength,
        vignette_blur=args.vignette_blur
    )

    out = (
        f"{os.path.splitext(args.input)[0]}"
        f"_{args.colors}c.png"
    )

    result.save(out, format="PNG")

    print("saved:", out)


if __name__ == "__main__":
    main()