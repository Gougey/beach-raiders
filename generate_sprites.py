"""
Beach Raiders sprite generator.

Generates all game assets via OpenAI's gpt-image-1 model with true
alpha-channel transparency.

Walk cycles: each soldier gets a proper 4-pose walk cycle following
classical animation principles:

    Frame 1 — CONTACT (front foot strike)
        Front foot just hit ground, back foot just leaving.
        Body at MIDDLE vertical height. Arms at extreme positions.

    Frame 2 — PASSING (high point on planted leg)
        Back leg passes by planted leg, knee high.
        Planted leg straight. Body at HIGHEST point. Arms central.

    Frame 3 — CONTACT (other foot strike — mirror of 1)
        Other foot just hit ground.
        Body at MIDDLE height. Arms swapped.

    Frame 4 — PASSING (high point on other planted leg)
        Body at HIGHEST point on the other side. Arms central.

Looping 1 -> 2 -> 3 -> 4 -> 1 produces a natural rise/fall walk
without needing programmatic bounce.

Frames 2-4 are produced via the image-edit endpoint with frame 1
as the reference, so the character stays identical.

Usage:
    python generate_sprites.py                  # generate everything
    python generate_sprites.py --only heli      # one asset only
    python generate_sprites.py --skip-existing  # don't overwrite
    python generate_sprites.py --soldiers       # only walk-cycle soldiers
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
Subject centred horizontally, no text, no labels, no scenery, no ground.

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

# ---- Soldier definitions with 4-frame walk cycle -------------------------

# Per-soldier appearance description (re-used across all 4 frames so the
# character stays visually identical between poses).
SOLDIER_APPEARANCE = {
    "infantry_blue": """A chunky cartoon Boom Beach style soldier, side profile facing right.
- Oversized head (~one-third of body height), friendly determined expression, big eyes
- Olive green (#558b2f) army helmet with chinstrap and a small white highlight shine on top
- Warm tan (#ffcc80) skin
- Olive green combat vest over a teal-blue (#1565c0) undershirt - vest has visible pockets
- Olive green trousers, brown leather combat boots
- Holding a small black assault rifle in both hands at chest level, barrel pointing right
- Stocky, slightly bowed cartoon proportions""",

    "infantry_red": """A chunky cartoon Boom Beach style ENEMY soldier, side profile facing right.
- Oversized head (~one-third of body height), slight scowl, menacing but cartoonish
- Crimson red (#c62828) army helmet with darker (#8e0000) shadow tone, chinstrap, white highlight
- Warm tan (#ffcc80) skin
- Dark crimson combat vest with black accents over a black undershirt - vest has visible pockets
- Dark grey trousers, black combat boots
- Holding a small black assault rifle in both hands at chest level, barrel pointing right
- Stocky cartoon proportions, must match player soldier's silhouette/build""",

    "bazooka_blue": """A chunky cartoon Boom Beach style soldier with rocket launcher, side profile facing right.
- Oversized head, friendly determined expression, big eyes
- Olive green (#558b2f) helmet with round goggles pushed up on the brim
- Warm tan (#ffcc80) skin
- Olive green combat vest over a teal-blue (#1565c0) undershirt
- Olive green trousers, brown leather combat boots
- Long dark grey (#37474f) bazooka tube on his RIGHT shoulder, pointing right,
  with a small front sight and visible round opening at the muzzle end
- Both hands gripping the launcher (one near the trigger, one supporting front)
- Stocky cartoon proportions""",

    "bazooka_red": """A chunky cartoon Boom Beach style ENEMY soldier with rocket launcher, side profile facing right.
- Oversized head, slight scowl, menacing but cartoonish
- Crimson red (#c62828) helmet with goggles pushed up on the brim
- Warm tan (#ffcc80) skin
- Dark crimson combat vest with black accents over black undershirt
- Dark grey trousers, black combat boots
- Long dark grey (#37474f) bazooka tube on his RIGHT shoulder, pointing right,
  with a small front sight and visible round opening at the muzzle end
- Both hands gripping the launcher
- Stocky cartoon proportions, must match player bazooka silhouette/build""",
}

# Pose descriptions for each frame of the walk cycle.
# These are the KEY POSES of a classical 4-pose walk cycle.
# Frames 2 and 4 deliberately have the body drawn HIGHER on the canvas
# so the rise-and-fall motion is intrinsic to the art.

POSE_FRAME_1 = """WALK CYCLE FRAME 1 of 4 — LEFT-FOOT CONTACT POSE.
- LEFT leg is forward and STRAIGHT, foot flat on the ground (heel just struck)
- RIGHT leg is back, knee slightly bent, heel lifted, pushing off
- Legs visibly apart in a clear stride
- Body at MIDDLE vertical height
- Right arm swung FORWARD, left arm swung BACK (counter to legs)
- Slight forward lean in the torso
- Centre the figure horizontally, position so feet are near bottom of the canvas"""

POSE_FRAME_2 = """WALK CYCLE FRAME 2 of 4 — DRAMATIC HIGH-STEP, LEFT LEG PLANTED.
- LEFT leg STRAIGHT and PLANTED on the ground (vertical, foot flat).
- RIGHT leg LIFTED HIGH IN THE AIR with the KNEE BENT AT 90 DEGREES,
  the right knee pointing forward at WAIST HEIGHT, right foot completely
  off the ground pointing forward. This is a strong marching/parading high-step.
- Body standing tall and upright (do NOT lean forward).
- IMPORTANT: the character is still holding their weapon in both hands
  exactly as in the contact frames (do not drop or hide the weapon).
- The lifted right knee is the dominant visual feature so the motion reads clearly."""

POSE_FRAME_3 = """WALK CYCLE FRAME 3 of 4 — RIGHT-FOOT CONTACT POSE (mirror of frame 1's leg/arm action).
- RIGHT leg is forward and STRAIGHT, foot flat on the ground (heel just struck)
- LEFT leg is back, knee slightly bent, heel lifted, pushing off
- Legs visibly apart in a clear stride
- Body at MIDDLE vertical height (same height as frame 1)
- Left arm swung FORWARD, right arm swung BACK (counter to legs, opposite of frame 1)
- Slight forward lean in the torso"""

POSE_FRAME_4 = """WALK CYCLE FRAME 4 of 4 — DRAMATIC HIGH-STEP, RIGHT LEG PLANTED (mirror of frame 2).
- RIGHT leg STRAIGHT and PLANTED on the ground (vertical, foot flat).
- LEFT leg LIFTED HIGH IN THE AIR with the KNEE BENT AT 90 DEGREES,
  the left knee pointing forward at WAIST HEIGHT, left foot completely
  off the ground pointing forward.
- Body standing tall and upright (do NOT lean forward).
- IMPORTANT: the character is still holding their weapon in both hands
  exactly as in the contact frames (do not drop or hide the weapon).
- The lifted left knee is the dominant visual feature."""

# Order matters: this is the cycle we'll loop through 1 -> 2 -> 3 -> 4 -> 1
WALK_FRAMES = [
    ("1", POSE_FRAME_1),
    ("2", POSE_FRAME_2),
    ("3", POSE_FRAME_3),
    ("4", POSE_FRAME_4),
]

SOLDIERS = list(SOLDIER_APPEARANCE.keys())  # infantry_blue, infantry_red, bazooka_blue, bazooka_red
SOLDIER_SIZE = "1024x1024"


# ---- Generation helpers --------------------------------------------------

def build_prompt(asset_prompt):
    return f"{STYLE}\n\n{asset_prompt}"


def soldier_prompt(soldier_key, pose_text):
    return build_prompt(
        f"CHARACTER:\n{SOLDIER_APPEARANCE[soldier_key]}\n\n"
        f"POSE:\n{pose_text}\n\n"
        f"The character must look identical to other frames in this same walk cycle - "
        f"same colours, same outfit, same head, same weapon, same proportions. "
        f"Only the leg/arm position and overall body height change between frames."
    )


def soldier_edit_prompt(pose_text):
    """Prompt used when editing frame 1 to produce frames 2/3/4."""
    return (
        "Generate a new pose of THE SAME EXACT CHARACTER shown in the input image. "
        "Keep ALL visual details identical: same colours, same helmet shape, same vest, "
        "same skin tone, same weapon, same face, same body proportions, same outline weight, "
        "same art style. The character must be recognisable as the same soldier between frames.\n\n"
        f"{pose_text}\n\n"
        "True alpha-channel transparent background. No checkerboard. No background fill. "
        "Subject centred horizontally."
    )


def save_b64_png(b64_data, path):
    path.write_bytes(base64.b64decode(b64_data))


def generate_image(prompt, size, name):
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
    print(f"    Done in {time.time() - t0:.1f}s")
    return resp.data[0].b64_json


def edit_image(input_path, prompt, size, name):
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
    print(f"    Done in {time.time() - t0:.1f}s")
    return resp.data[0].b64_json


# ---- Main ----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="Generate just one asset prefix (e.g. 'heli', 'infantry_blue')")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip files that already exist on disk")
    parser.add_argument("--soldiers", action="store_true",
                        help="Only generate the walk-cycle soldier frames")
    args = parser.parse_args()

    print("=" * 60)
    print("BEACH RAIDERS — Sprite Generator")
    print("=" * 60)
    print(f"Output: {ASSETS_DIR}")

    generated = 0

    # Base assets (skip when --soldiers)
    if not args.soldiers:
        for asset in BASE_ASSETS:
            name = asset["name"]
            if args.only and not name.startswith(args.only):
                continue
            path = ASSETS_DIR / name
            if args.skip_existing and path.exists():
                print(f"\n[SKIP] {name}")
                continue
            print(f"\n[GENERATE] {name}")
            try:
                b64 = generate_image(build_prompt(asset["prompt"]), asset["size"], name)
                save_b64_png(b64, path)
                generated += 1
            except Exception as e:
                print(f"  FAILED: {e}")

    # Soldiers — 4-frame walk cycle each
    for soldier_key in SOLDIERS:
        if args.only and not soldier_key.startswith(args.only):
            continue

        # Frame 1: generate from scratch
        f1_path = ASSETS_DIR / f"{soldier_key}_1.png"
        if args.skip_existing and f1_path.exists():
            print(f"\n[SKIP] {f1_path.name}")
        else:
            print(f"\n[GENERATE] {f1_path.name} (contact pose, left foot forward)")
            try:
                b64 = generate_image(
                    soldier_prompt(soldier_key, POSE_FRAME_1),
                    SOLDIER_SIZE,
                    f1_path.name,
                )
                save_b64_png(b64, f1_path)
                generated += 1
            except Exception as e:
                print(f"  FAILED: {e}")
                continue

        # Frames 2-4: edit from frame 1
        for frame_num, pose_text in WALK_FRAMES[1:]:  # 2, 3, 4
            fn_path = ASSETS_DIR / f"{soldier_key}_{frame_num}.png"
            if args.skip_existing and fn_path.exists():
                print(f"[SKIP] {fn_path.name}")
                continue
            label = {"2": "passing pose, left leg planted, body high",
                     "3": "contact pose, right foot forward",
                     "4": "passing pose, right leg planted, body high"}[frame_num]
            print(f"[EDIT]  {fn_path.name} ({label})")
            try:
                b64 = edit_image(
                    f1_path,
                    soldier_edit_prompt(pose_text),
                    SOLDIER_SIZE,
                    fn_path.name,
                )
                save_b64_png(b64, fn_path)
                generated += 1
            except Exception as e:
                print(f"  FAILED: {e}")

    print("\n" + "=" * 60)
    print(f"Done. Generated {generated} images.")
    print(f"Approximate cost: ${generated * 0.17:.2f} (high quality)")
    print("=" * 60)


if __name__ == "__main__":
    main()
