"""
Trim transparent padding from scenery + base sprites so their content
sits flush with the bottom of the canvas. The game anchors these to the
ground line, so any transparent padding below the visible content
manifests as the asset 'floating' above the beach.

Run after generation:
    python trim_sprites.py
"""

from pathlib import Path
from PIL import Image

ASSETS = Path(__file__).parent / "assets"

# Sprites that should be ground-anchored — trim transparent borders so the
# bottommost visible pixel sits at the image's bottom edge.
TRIM = [
    "palm_tree_1.png",
    "palm_tree_2.png",
    "bush_1.png",
    "rock_1.png",
    "base_blue.png",
    "base_red.png",
]

PADDING = 4  # tiny soft padding to avoid edge clipping when scaling


def trim(name: str) -> None:
    path = ASSETS / name
    if not path.exists():
        print(f"[skip] {name} (missing)")
        return

    img = Image.open(path).convert("RGBA")
    bbox = img.getbbox()
    if not bbox:
        print(f"[skip] {name} (fully transparent)")
        return

    x1, y1, x2, y2 = bbox
    # Add small padding while staying within image bounds
    x1 = max(0, x1 - PADDING)
    y1 = max(0, y1 - PADDING)
    x2 = min(img.width, x2 + PADDING)
    y2 = min(img.height, y2 + PADDING)

    cropped = img.crop((x1, y1, x2, y2))
    before = img.size
    after = cropped.size
    cropped.save(path)
    print(f"[ok]   {name}: {before} -> {after}")


def main():
    for name in TRIM:
        trim(name)


if __name__ == "__main__":
    main()
