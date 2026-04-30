"""
Beach Raiders sprite generator.

Generates all game assets via OpenAI's gpt-image-1 model with true
alpha-channel transparency. Uses the edit endpoint to keep walk-cycle
frames consistent (same character, only legs change).

Usage:
    python generate_sprites.py            # generate all
    python generate_sprites.py --only heli  # generate one
    python generate_sprites.py --skip-existing  # don't redo done ones
"""

import argparse
import base64
import sys
import time
from pathlib import Path

from openai import OpenAI

# ---- Setup ---------------------------------------------------------------

KEY_PATH = Path.home() / ".openai_key"
ASSETS_DIR = Path(__file__).parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

if not KEY_PATH.exists():
    print(f"ERROR: API key not found at {KEY_PATH}")
    sys.exit(1)

api_key = KEY_PATH.read_text().strip()
client = OpenAI(api_key=api_key)

# ---- Style guide prepended to every prompt -------------------------------

STYLE = """2D cartoon game sprite in the visual style of Supercell's Boom Beach.
Hand-drawn vector cartoon with THICK BLACK OUTLINES (3-4px stroke).
Chunky exaggerated proportions, oversized heads on units.
Bright saturated cel-shaded colours: base colour + shadow tone + highlight.
Cheerful tropical military aesthetic, never realistic, never gritty.
Strict side profile view facing RIGHT for vehicles and units.
Slight 3/4 front view for buildings.
TRUE ALPHA-CHANNEL TRANSPARENT BACKGROUND - the only visible pixels should be the subject itself.
Subject centred, fills ~80% of canvas, no text, no labels, no scenery, no ground.

COLOUR CODING:
- PLAYER (blue) team: cobalt blue #1565c0, sky blue #42a5f5, olive green #558b2f uniforms
- ENEMY (red) team: crimson red #c62828, dark red #8e0000, dark crimson uniforms with black accents
- Skin tone: warm tan #ffcc80
- Neutrals: brown wood #5d4037, grey metal #546e7a"""

# ---- Asset definitions ---------------------------------------------------

# Each base asset: filename, size, prompt
BASE_ASSETS = [
    {
        "name": "heli.png",
        "size": "1536x1024",
        "prompt": """Subject: chunky cartoon military attack helicopter, strict side profile facing right.
Cobalt blue (#1565c0) hull with sky blue (#42a5f5) accent stripe along the body.
Glossy clear cockpit bubble dome with white reflection highlight on top-left.
Underslung minigun barrel mounted below the nose pointing right.
Main rotor shown as soft semi-transparent motion-blur ellipse above the cabin.
Tail boom extending left ending in a small tail rotor.
Black landing skids underneath the body.
Cute, friendly, but capable looking. Soft drop shadow underneath."""
    },
    {
        "name": "tank_blue.png",
        "size": "1536x1024",
        "prompt": """Subject: chunky cartoon military tank, strict side profile facing right.
Cobalt blue (#1565c0) hull with grey-blue (#546e7a) armour plates and visible rivet details.
Rounded turret on top with a long cannon barrel pointing right (barrel ~one third of hull length).
Visible track tread along the bottom with 5-6 round road wheels showing through.
Bright sky-blue (#42a5f5) star emblem on the side of the turret.
Wedge-shaped angled front armour plate.
Subtle highlight stripe along top of hull and turret. Soft drop shadow underneath."""
    },
    {
        "name": "tank_red.png",
        "size": "1536x1024",
        "prompt": """Subject: chunky cartoon military tank, strict side profile facing right.
Crimson red (#c62828) hull with dark red (#8e0000) armour plates and visible rivet details.
Rounded turret on top with a long cannon barrel pointing right (barrel ~one third of hull length).
Visible track tread along the bottom with 5-6 round road wheels showing through (dark grey).
White skull emblem on the side of the turret.
Wedge-shaped angled front armour plate. Slightly menacing but still cartoonish.
Subtle highlight stripe along top of hull and turret. Soft drop shadow underneath.
MUST match the silhouette of the player tank exactly - same proportions, only colours and emblem differ."""
    },
    {
        "name": "base_blue.png",
        "size": "1024x1024",
        "prompt": """Subject: tropical military headquarters building, slight 3/4 front view.
Cobalt blue (#1565c0) painted wooden plank walls with corrugated metal reinforcement strips.
Stack of warm-tan sandbags around the base/foundation with visible stitching.
Corrugated grey metal roof with palm-leaf camouflage draped on top.
Tall thin radio antenna on the roof with a tiny red blinking light at the tip.
Wooden front door with metal hinges. Two small square windows with bright glowing yellow interior light.
Sky blue (#42a5f5) flag with a single white star on a flagpole, fluttering to the right.
Looks like a friendly tropical military hut. Soft drop shadow underneath."""
    },
    {
        "name": "base_red.png",
        "size": "1024x1024",
        "prompt": """Subject: dark menacing military fortress, slight 3/4 front view.
Dark grey stone block walls with crimson red (#c62828) accent stripe across the middle.
Two squat guard towers flanking a central gate, each tower with a narrow slit window glowing red.
Battlements (crenellations) along the top edge of the walls.
Large white skull emblem mounted above heavy iron-banded wooden gate.
Coiled barbed wire along the top of the walls.
Dark iron reinforcement bands and rivets on the gate.
Dark red (#8e0000) flag with a white skull on a flagpole on top of one tower.
Menacing but still cartoonish, never horror. Soft drop shadow underneath."""
    },
]

# Soldier definitions — each has frame 1 prompt; frame 2 made by edit
SOLDIERS = [
    {
        "base_name": "infantry_blue",
        "size": "1024x1024",
        "frame1_prompt": """Subject: chunky cartoon soldier, strict side profile facing right.
Standing/marching pose with LEFT LEG FORWARD, right leg back (mid-stride).
Oversized head (~one-third of body height) with friendly determined expression, big eyes.
Olive green (#558b2f) army helmet with chinstrap and small white highlight shine on top.
Warm tan (#ffcc80) skin.
Olive green combat vest over a teal-blue (#1565c0) undershirt - vest has visible pockets.
Olive green trousers, brown leather boots.
Holding a small black assault rifle in both hands at waist level, barrel pointing right.
Stocky build, short legs, slightly bowed stance. Soft drop shadow at feet."""
    },
    {
        "base_name": "infantry_red",
        "size": "1024x1024",
        "frame1_prompt": """Subject: chunky cartoon enemy soldier, strict side profile facing right.
Standing/marching pose with LEFT LEG FORWARD, right leg back (mid-stride).
Oversized head (~one-third of body height) with slight scowl, menacing but cartoonish.
Crimson red (#c62828) army helmet with darker (#8e0000) shadow tone, chinstrap and white highlight.
Warm tan (#ffcc80) skin.
Dark crimson combat vest with black accents over a black undershirt - vest has visible pockets.
Dark grey trousers, black boots.
Holding a small black assault rifle in both hands at waist level, barrel pointing right.
Stocky build, short legs. Soft drop shadow at feet.
MUST match player infantry proportions and silhouette exactly - only team colours and expression differ."""
    },
    {
        "base_name": "bazooka_blue",
        "size": "1024x1024",
        "frame1_prompt": """Subject: chunky cartoon soldier with rocket launcher, strict side profile facing right.
Standing/marching pose with LEFT LEG FORWARD, right leg back (mid-stride).
Oversized head with friendly determined expression and big eyes.
Olive green (#558b2f) helmet with round goggles pushed up on the brim.
Warm tan (#ffcc80) skin.
Olive green combat vest over teal-blue (#1565c0) undershirt.
Olive green trousers, brown leather boots.
A long dark grey (#37474f) bazooka tube resting on his RIGHT shoulder, pointing right,
with a small front sight and a clearly visible round opening at the muzzle end.
Both hands gripping the launcher. Stocky build. Soft drop shadow at feet."""
    },
    {
        "base_name": "bazooka_red",
        "size": "1024x1024",
        "frame1_prompt": """Subject: chunky cartoon enemy soldier with rocket launcher, strict side profile facing right.
Standing/marching pose with LEFT LEG FORWARD, right leg back (mid-stride).
Oversized head with slight scowl, menacing but cartoonish.
Crimson red (#c62828) helmet with goggles pushed up on the brim.
Warm tan (#ffcc80) skin.
Dark crimson combat vest with black accents over black undershirt.
Dark grey trousers, black boots.
A long dark grey (#37474f) bazooka tube resting on his RIGHT shoulder, pointing right,
with a small front sight and a clearly visible round opening at the muzzle end.
Both hands gripping the launcher. Stocky build. Soft drop shadow at feet.
MUST match player bazooka soldier proportions and silhouette exactly - only colours differ."""
    },
]

# Frame 2 prompt for walk cycle (used with image edit)
FRAME2_EDIT_PROMPT = """Same exact character, identical colours, identical proportions, identical outline weight,
identical face, identical helmet, identical vest, identical weapon, identical pose of upper body.

ONLY CHANGE: the leg position. Now show the OPPOSITE stride - RIGHT LEG FORWARD, left leg back.
This is the second frame of a 2-frame walk cycle so the legs must clearly be in mirrored stride position
to the input image. Keep everything above the waist absolutely identical.

True alpha-channel transparent background. No checkerboard. No background fill."""


# ---- Generation helpers --------------------------------------------------

def build_prompt(asset_prompt):
    return f"{STYLE}\n\n{asset_prompt}"


def save_b64_png(b64_data, path):
    path.write_bytes(base64.b64decode(b64_data))


def generate_image(prompt, size, name):
    """Call gpt-image-1 generate endpoint with transparent background."""
    print(f"  Generating {name} (size={size})...")
    t0 = time.time()
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=size,
        background="transparent",
        quality="high",
        n=1,
    )
    elapsed = time.time() - t0
    print(f"    Done in {elapsed:.1f}s")
    return resp.data[0].b64_json


def edit_image(input_path, prompt, size, name):
    """Call gpt-image-1 edit endpoint - frame 2 of walk cycle."""
    print(f"  Editing {name} (size={size})...")
    t0 = time.time()
    with open(input_path, "rb") as f:
        resp = client.images.edit(
            model="gpt-image-1",
            image=f,
            prompt=prompt,
            size=size,
            background="transparent",
            quality="high",
            n=1,
        )
    elapsed = time.time() - t0
    print(f"    Done in {elapsed:.1f}s")
    return resp.data[0].b64_json


# ---- Main ----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="Generate just one asset by name (without .png)")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip files that already exist")
    args = parser.parse_args()

    print("=" * 60)
    print("BEACH RAIDERS — Sprite Generator")
    print("=" * 60)
    print(f"Output: {ASSETS_DIR}")

    generated = 0

    # Base assets
    for asset in BASE_ASSETS:
        name = asset["name"]
        if args.only and not name.startswith(args.only):
            continue

        path = ASSETS_DIR / name
        if args.skip_existing and path.exists():
            print(f"\n[SKIP] {name} already exists")
            continue

        print(f"\n[GENERATE] {name}")
        prompt = build_prompt(asset["prompt"])
        try:
            b64 = generate_image(prompt, asset["size"], name)
            save_b64_png(b64, path)
            print(f"  Saved {path}")
            generated += 1
        except Exception as e:
            print(f"  FAILED: {e}")

    # Soldiers — generate frame 1, then edit for frame 2
    for soldier in SOLDIERS:
        base_name = soldier["base_name"]
        if args.only and not base_name.startswith(args.only):
            continue

        f1_path = ASSETS_DIR / f"{base_name}_1.png"
        f2_path = ASSETS_DIR / f"{base_name}_2.png"

        # Frame 1
        if args.skip_existing and f1_path.exists():
            print(f"\n[SKIP] {f1_path.name} already exists")
        else:
            print(f"\n[GENERATE] {f1_path.name}")
            prompt = build_prompt(soldier["frame1_prompt"])
            try:
                b64 = generate_image(prompt, soldier["size"], f1_path.name)
                save_b64_png(b64, f1_path)
                print(f"  Saved {f1_path}")
                generated += 1
            except Exception as e:
                print(f"  FAILED: {e}")
                continue  # can't edit if frame 1 failed

        # Frame 2 — edit from frame 1
        if args.skip_existing and f2_path.exists():
            print(f"[SKIP] {f2_path.name} already exists")
        else:
            print(f"[EDIT]  {f2_path.name}")
            try:
                b64 = edit_image(f1_path, FRAME2_EDIT_PROMPT, soldier["size"], f2_path.name)
                save_b64_png(b64, f2_path)
                print(f"  Saved {f2_path}")
                generated += 1
            except Exception as e:
                print(f"  FAILED: {e}")

    print("\n" + "=" * 60)
    print(f"Done. Generated {generated} images.")
    print(f"Approximate cost: ${generated * 0.17:.2f} (high quality)")
    print("=" * 60)


if __name__ == "__main__":
    main()
