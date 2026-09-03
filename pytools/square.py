#!/usr/bin/env python3

import sys
from pathlib import Path
from PIL import Image


def make_square(input_file, output_file=None, bg_color=(0, 0, 0, 0)):
    """
    Expand image canvas to a square using the longest side.
    The original image is centered.

    bg_color:
        RGBA tuple. Default is transparent.
    """

    img = Image.open(input_file).convert("RGBA")

    width, height = img.size
    side = max(width, height)

    square = Image.new("RGBA", (side, side), bg_color)

    x = (side - width) // 2
    y = (side - height) // 2

    square.paste(img, (x, y), img)

    if output_file is None:
        src = Path(input_file)
        output_file = src.with_stem(src.stem + "_square")

    square.save(output_file)
    print(f"Saved: {output_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python make_square.py image.png [output.png]")
        sys.exit(1)

    input_file = sys.argv[1]

    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        ext = Path(input_file).suffix
        output_file = str(Path(input_file).with_stem(
            Path(input_file).stem + "_square"
        ))

    make_square(input_file, output_file)


if __name__ == "__main__":
    main()