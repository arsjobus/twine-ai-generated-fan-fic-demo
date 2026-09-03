#!/usr/bin/env python3

import json
import subprocess
import argparse
from pathlib import Path

# Directory where images are saved
OUTPUT_DIR = Path("./output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Keep track of image names we've already processed
processed_images = set()

# Global counters for progress tracking
total_images_to_generate = 0
images_generated = 0


def count_images_to_generate(passages):
    """
    Count all unique images that still need to be generated.
    Skips images that already exist in OUTPUT_DIR matching {image_name}_*.png
    """
    images = set()

    for passage in passages:
        # Background
        bg_src = passage.get("backgroundImageSrc")
        if bg_src:
            images.add(Path(bg_src).stem)

        # Actors 1-3
        for i in range(1, 4):
            image_src = passage.get(f"actor{i}ImageSrc")
            if image_src:
                images.add(Path(image_src).stem)

    # Remove images that already exist with pattern {image_name}_*.png
    remaining_images = set()
    for image_name in images:
        if not list(OUTPUT_DIR.glob(f"{image_name}_*.png")):
            remaining_images.add(image_name)

    return remaining_images


def print_progress():
    remaining = total_images_to_generate - images_generated
    print(f"\nProgress: Generated {images_generated}/{total_images_to_generate} images. Remaining: {remaining}\n")


def run_generation(
    positive_prompt,
    negative_prompt,
    image_name,
    width,
    height,
):
    global images_generated

    # Skip if already processed in memory
    if image_name in processed_images:
        print(f"Skipping already processed (memory) image: {image_name}")
        return

    # Skip if any file matching {image_name}_*.png exists
    pattern = f"{image_name}_*.png"
    matching_files = list(OUTPUT_DIR.glob(pattern))
    if matching_files:
        print(f"Skipping {image_name}, found existing files: {[f.name for f in matching_files]}")
        processed_images.add(image_name)
        images_generated += 1
        print_progress()
        return

    # Run the generation command
    cmd = [
        "python",
        "pytools/gen-art-anime.py",
        positive_prompt,
        "--negative",
        negative_prompt,
        "--count",
        "5",
        "--image-name",
        image_name,
        "--width",
        str(width),
        "--height",
        str(height),
    ]

    print(f"\nRunning:\n{' '.join(cmd)}\n")
    subprocess.run(cmd, check=True)

    # Mark as processed
    processed_images.add(image_name)
    images_generated += 1
    print_progress()


def process_passage(passage):
    """
    Processes:
      - background prompts
      - actor1 prompts
      - actor2 prompts
      - actor3 prompts
    """

    # =========================
    # Background
    # =========================
    bg_positive = passage.get("backgroundArtPromptPositive")
    bg_negative = passage.get("backgroundArtPromptNegative")
    bg_src = passage.get("backgroundImageSrc")

    if bg_positive and bg_src:
        image_name = Path(bg_src).stem
        run_generation(
            positive_prompt=bg_positive,
            negative_prompt=bg_negative or "",
            image_name=image_name,
            width=768,
            height=512,
        )

    # =========================
    # Actors 1-3
    # =========================
    for i in range(1, 4):
        positive = passage.get(f"actor{i}ArtPromptPositive")
        negative = passage.get(f"actor{i}ArtPromptNegative")
        image_src = passage.get(f"actor{i}ImageSrc")

        if positive and image_src:
            image_name = Path(image_src).stem

            # Append ", solid white background" for actor images
            positive += ", solid white background"

            run_generation(
                positive_prompt=positive,
                negative_prompt=negative or "",
                image_name=image_name,
                width=512,
                height=768,
            )


def main():
    global total_images_to_generate

    parser = argparse.ArgumentParser(
        description="Process Twine JSON and generate anime art prompts."
    )

    parser.add_argument(
        "json_file",
        help="Path to the Twine JSON file"
    )

    args = parser.parse_args()
    json_path = Path(args.json_file)

    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    passages = data.get("passages", [])
    print(f"Found {len(passages)} passages.")

    # Count total images that still need to be generated
    total_images_to_generate = len(count_images_to_generate(passages))
    print(f"Total images to generate (excluding existing files): {total_images_to_generate}")
    print_progress()

    for index, passage in enumerate(passages, start=1):
        passage_name = passage.get("name", f"Passage {index}")

        print("=" * 60)
        print(f"Processing passage {index}: {passage_name}")
        print("=" * 60)

        process_passage(passage)

    print("\nAll done. Generated images:", images_generated)


if __name__ == "__main__":
    main()