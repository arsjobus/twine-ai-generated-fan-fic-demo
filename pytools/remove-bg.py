#!/usr/bin/env python3

import sys
from pathlib import Path

import numpy as np
import cv2
from PIL import Image
from rembg import remove, new_session


def clean_alpha(path: Path):
    img = np.array(Image.open(path).convert("RGBA"))
    alpha = img[:, :, 3]

    kernel = np.ones((3, 3), np.uint8)

    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel)

    img[:, :, 3] = alpha
    Image.fromarray(img).save(path)


def harden_alpha(path: Path):
    img = np.array(Image.open(path).convert("RGBA"))
    alpha = img[:, :, 3]

    # removes faint "ghost background"
    alpha = np.where(alpha > 120, 255, 0).astype(np.uint8)

    img[:, :, 3] = alpha
    Image.fromarray(img).save(path)


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python remove_bg.py <input_image> [output_image]")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    output_path = (
        Path(sys.argv[2])
        if len(sys.argv) == 3
        else input_path.parent / f"{input_path.stem}.nobg.png"
    )

    try:
        print("Loading model: birefnet-general")
        session = new_session("birefnet-general")

        with open(input_path, "rb") as f:
            input_data = f.read()

        print("Removing background...")
        output_data = remove(
            input_data,
            session=session,
            alpha_matting=True,
            alpha_matting_foreground_threshold=250,
            alpha_matting_background_threshold=5,
            alpha_matting_erode_size=3,
        )

        with open(output_path, "wb") as f:
            f.write(output_data)

        print("Cleaning artifacts...")
        clean_alpha(output_path)

        print("Hardening alpha...")
        harden_alpha(output_path)

        print("✓ Done")
        print(f"Output: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()