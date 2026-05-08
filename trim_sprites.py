"""
Trim transparent padding from scenery + base sprites so their SOLID
content sits flush with the bottom of the canvas.

Critical detail: the AI-generated sprites include soft drop shadows
that taper off at low alpha (1-180 range) below the visible object.
A naive bbox trim (alpha > 0) preserves those shadows, so the visible
trunk/building/bush appears to float above its own shadow.

We trim using a high alpha threshold (≥ ALPHA_SOLID) so the bottom of
the trimmed image is the bottom of the SOLID object, then add a small
padding row to keep edge anti-aliasing intact.

Run after generation:
    python trim_sprites.py
"""

from pathlib import Path
from PIL import Image
import numpy as np

ASSETS = Path(__file__).parent / "assets"

TRIM = [
    "palm_tree_1.png",
    "palm_tree_2.png",
    "bush_1.png",
    "rock_1.png",
    "base_blue.png",
    "base_red.png",
]

ALPHA_SOLID = 200   # consider only nearly-opaque pixels as "real content"
PADDING = 4         # keep a small soft border so edges stay smooth


def trim(name: str) -> None:
    path = ASSETS / name
    if not path.exists():
        print(f"[skip] {name} (missing)")
        return

    img = Image.open(path).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]

    # Bounding box of pixels with alpha >= ALPHA_SOLID
    rows_solid = np.where(alpha.max(axis=1) >= ALPHA_SOLID)[0]
    cols_solid = np.where(alpha.max(axis=0) >= ALPHA_SOLID)[0]

    if rows_solid.size == 0 or cols_solid.size == 0:
        print(f"[skip] {name} (no solid content found)")
        return

    y1, y2 = rows_solid.min(), rows_solid.max() + 1
    x1, x2 = cols_solid.min(), cols_solid.max() + 1

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
