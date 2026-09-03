import argparse
from PIL import Image

def calculate_packing_efficiency(image_path, bg_color=(0, 0, 0), tolerance=0):
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()

    width, height = img.size
    total_pixels = width * height
    used_pixels = 0

    def is_background(pixel):
        return all(abs(pixel[i] - bg_color[i]) <= tolerance for i in range(3))

    for y in range(height):
        for x in range(width):
            if not is_background(pixels[x, y]):
                used_pixels += 1

    efficiency = (used_pixels / total_pixels) * 100
    return efficiency


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Texture packing efficiency checker")
    
    parser.add_argument("file", help="Path to the texture image")
    parser.add_argument("--bg", nargs=3, type=int, default=[0, 0, 0],
                        help="Background color as R G B (default: 0 0 0)")
    parser.add_argument("--tolerance", type=int, default=0,
                        help="Color tolerance (default: 0)")

    args = parser.parse_args()

    efficiency = calculate_packing_efficiency(
        args.file,
        tuple(args.bg),
        args.tolerance
    )

    print(f"Texture packing efficiency: {efficiency:.2f}%")