#!/usr/bin/env python3
"""
video_to_spritesheet.py

Convert every frame of an MP4 (or other OpenCV-supported video) into a single
horizontal PNG sprite sheet suitable for importing into Aseprite.

Usage:
    python video_to_spritesheet.py input.mp4 output.png

Optional:
    python video_to_spritesheet.py input.mp4 output.png --every 2
        Export every 2nd frame.

Requirements:
    pip install opencv-python pillow numpy
"""

import argparse
import cv2
import numpy as np
from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input video")
    parser.add_argument("output", help="Output sprite sheet PNG")
    parser.add_argument(
        "--every",
        type=int,
        default=1,
        help="Use every Nth frame (default: 1)",
    )
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.input)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {args.input}")

    frames = []
    frame_index = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        if frame_index % args.every == 0:
            # OpenCV uses BGR -> RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)

        frame_index += 1

    cap.release()

    if not frames:
        raise RuntimeError("No frames extracted.")

    frame_height, frame_width = frames[0].shape[:2]

    sheet_width = frame_width * len(frames)
    sheet_height = frame_height

    sheet = Image.new("RGBA", (sheet_width, sheet_height))

    for i, frame in enumerate(frames):
        img = Image.fromarray(frame).convert("RGBA")
        sheet.paste(img, (i * frame_width, 0))

    sheet.save(args.output)

    print(f"Saved {len(frames)} frames")
    print(f"Frame size : {frame_width}x{frame_height}")
    print(f"Sheet size : {sheet_width}x{sheet_height}")
    print(f"Output     : {args.output}")


if __name__ == "__main__":
    main()