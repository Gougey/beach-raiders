"""
Beach Raiders sprite generator.

Generates all game assets via OpenAI's gpt-image-1 model with true
alpha-channel transparency.

Soldier walk cycle: 8 frames following classical animation principles.
Each frame is a key pose with deliberate vertical body height and
arms-counter-to-legs swing. The cycle loops F8 -> F1 cleanly.

Frame plan (right-facing soldier):

    F1  RIGHT CONTACT       — right heel strikes ahead, left foot pushing off
                              behind. Left arm fwd, right arm back. Neutral height.
    F2  RECOIL              — body drops slightly, right knee bends to absorb,
                              left foot lifts. Arms crossing toward neutral.
    F3  MIDSTANCE (LOWEST)  — body at LOWEST point. Right leg straight under
                              body bearing weight. Left leg swinging forward,
                              knee bent. Arms at neutral.
    F4  PUSH-OFF (HIGHEST)  — body RISES as right leg extends pushing back.
                              Left leg nearly extended swinging fwd. Arms
                              crossing toward opposite side.
    F5  LEFT CONTACT        — mirror of F1. Left heel strikes, right pushes off.
    F6  RECOIL              — mirror of F2.
    F7  MIDSTANCE (LOWEST)  — mirror of F3, body lowest again.
    F8  PUSH-OFF (HIGHEST)  — mirror of F4.

In-game timings (variable per frame):
    F1: 80ms, F2: 55ms, F3: 55ms, F4: 70ms,
    F5: 80ms, F6: 55ms, F7: 55ms, F8: 70ms     -> ~520ms full cycle

Frames 2-8 are produced via the image-edit endpoint with frame 1 as
the reference image to keep the character visually consistent.

Usage:
    python generate_sprites.py
    python generate_sprites.py --only infantry_blue --soldiers
    python generate_sprites.py --soldiers --skip-existing
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

# ---- Style guide ---------------------------------------------------------

STYLE = """2D cartoon game sprite in the visual style of Supercell's Boom Beach.
Hand-drawn vector cartoon with THICK BLACK OUTLINES (3-4px stroke).
Chunky exaggerated proportions, oversized heads on units.
Bright saturated cel-shaded colours: base colour + shadow tone + highlight.
Cheerful tropical military aesthetic, never realistic, never gritty.
Strict side profile view facing RIGHT.
TRUE ALPHA-CHANNEL TRANSPARENT BACKGROUND - the only visible pixels should be the subject itself.
Subject centred horizontally, no text, no labels, no scenery, no ground.

COLOUR CODING:
- PLAYER (blue) team: cobalt blue #1565c0, sky blue #42a5f5, olive green #558b2f uniforms
- ENEMY (red) team: crimson red #c62828, dark red #8e0000, dark crimson uniforms with black accents
- Skin tone: warm tan #ffcc80
- Neutrals: brown wood #5d4037, grey metal #546e7a"""

# ---- Background scenery & UI assets --------------------------------------

ENVIRONMENT_ASSETS = [
    {
        "name": "palm_tree_1.png",
        "size": "1024x1536",
        "prompt": """A single chunky cartoon tropical palm tree, full plant from base to crown.
Curved brown trunk with cross-hatched bark texture in warm browns (#8d6e63 base, #5d4037 shadow).
3-4 coconuts clustered at the top of the trunk in dark brown (#4e342e).
6-8 large palm fronds fanning out in two shades of green (#558b2f base, #33691e shadow),
each frond drawn as a curved leaf with visible vein lines and serrated edges.
Thick black outlines (3-4px), saturated cel-shaded colours, Boom Beach style.
True alpha-channel transparent background. Tree centred. No ground, no sky."""
    },
    {
        "name": "palm_tree_2.png",
        "size": "1024x1536",
        "prompt": """A single tall slender cartoon tropical palm tree, full plant from base to crown,
slightly different shape from a typical palm — taller, thinner, leaning right by ~15 degrees.
Curved tan/brown trunk with cross-hatch bark texture (#a1887f base, #6d4c41 shadow).
Coconuts at the crown.
5-7 long drooping palm fronds in two shades of green (#66bb6a base, #2e7d32 shadow),
fronds curve downward more dramatically than a typical palm.
Thick black outlines (3-4px), Boom Beach style.
True alpha-channel transparent background. Tree centred. No ground, no sky."""
    },
    {
        "name": "bush_1.png",
        "size": "1024x1024",
        "prompt": """A single tropical jungle bush — small clump of dense leafy greenery on the ground.
Multiple overlapping rounded leaves in two greens (#43a047 base, #1b5e20 shadow).
Two or three bright tropical flowers (pink #e91e63, orange #ff9800, yellow #ffeb3b)
peeking through the leaves.
Thick black outlines (3-4px), chunky cartoon Boom Beach style.
The bush should be wider than it is tall, nestled into ground level, fitting in the lower half of the canvas.
True alpha-channel transparent background. Bush centred horizontally. No ground line, no sky, no other elements."""
    },
    {
        "name": "rock_1.png",
        "size": "1024x1024",
        "prompt": """A single chunky grey beach rock / boulder, low and rounded.
Stone-grey body (#90a4ae base, #546e7a shadow) with a small white highlight on top-left.
A few small cracks and texture lines.
A tiny bit of moss/grass on top in green.
Thick black outlines (3-4px), chunky cartoon Boom Beach style.
The rock should be wider than tall, fitting in the lower half of the canvas.
True alpha-channel transparent background. Rock centred horizontally. No ground, no sky, no other elements."""
    },
    {
        "name": "cloud_1.png",
        "size": "1536x1024",
        "prompt": """A single fluffy cartoon cloud, classic puffy chunky shape.
Bright white body (#ffffff) with subtle pale-blue shadow underneath (#e1f5fe).
Multiple rounded lobes giving a bumpy bubbly outline.
Thin grey-blue outline (~2-3px) for that cartoon look.
True alpha-channel transparent background. Cloud centred. No sky."""
    },
    {
        "name": "mountain_bg.png",
        "size": "1536x1024",
        "prompt": """A SCENERY-ONLY background image of distant tropical jungle mountain silhouettes.
Two or three rounded green-blue mountain hills layered behind each other,
furthest in pale teal (#80cbc4), middle in muted green (#66bb6a), nearest in deeper jungle green (#388e3c).
Each mountain has tiny palm tree silhouettes visible along its ridgeline.
Soft hazy atmospheric depth, flat painterly cartoon style.
Mountains span the FULL WIDTH of the image, occupying mainly the lower two-thirds.

CRITICAL CONSTRAINTS:
- ABSOLUTELY NO characters, soldiers, people, animals, vehicles, helicopters, tanks, weapons, or military elements.
- NO foreground elements, NO buildings, NO bases.
- The image is ONLY mountain silhouette shapes.
- Everything above the mountains and outside their silhouette must be TRUE TRANSPARENT (alpha = 0).
- This is a clean parallax background layer for a side-scrolling game.
Boom Beach scenery style — distant island chain on the horizon."""
    },
    {
        "name": "logo.png",
        "size": "1536x1024",
        "prompt": """A bold chunky 3D cartoon video game logo wordmark for a mobile game called
"FRONTLINE EXTRACTION".

Two-line layout:
- Top word: "FRONTLINE" — large bold extruded sans-serif letters
- Bottom word: "EXTRACTION" — slightly smaller, same style

Visual style:
- Thick chunky letters with a strong 3D extruded depth (light yellow-orange faces #ffd54f,
  darker red-orange sides #e65100 for the depth)
- Bold black outline around every letter (~4-6px)
- Subtle white highlight glints on the top edges of letters
- A soft drop shadow underneath
- Letter style: condensed bold cartoon with slight perspective, like Boom Beach / Clash Royale logos
- Optional small decorative elements: a couple of palm leaves crossed behind the wordmark,
  or a small military star emblem — keep them minor, the wordmark is the hero
- Tropical military feel — bright, exciting, not gritty

True alpha-channel transparent background. The logo fills ~90% of the canvas.
No background colours, no scenery, just the logo on transparency."""
    },
]

# ---- Base assets (helicopter, tanks, bases) ------------------------------

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
Rounded turret on top with a long cannon barrel pointing right.
Visible track tread along the bottom with 5-6 round road wheels showing through (dark grey).
White skull emblem on the side of the turret.
Wedge-shaped angled front armour plate. Slightly menacing but still cartoonish."""
    },
    {
        "name": "base_blue.png",
        "size": "1024x1024",
        "prompt": """Tropical military headquarters building, slight 3/4 front view.
Cobalt blue (#1565c0) painted wooden plank walls with corrugated metal reinforcement strips.
Stack of warm-tan sandbags around the base/foundation with visible stitching.
Corrugated grey metal roof with palm-leaf camouflage draped on top.
Tall thin radio antenna with a tiny red blinking light at the tip.
Wooden front door with metal hinges. Two small square windows with bright glowing yellow interior light.
Sky blue (#42a5f5) flag with a single white star on a flagpole, fluttering to the right."""
    },
    {
        "name": "base_red.png",
        "size": "1024x1024",
        "prompt": """Dark menacing military fortress, slight 3/4 front view.
Dark grey stone block walls with crimson red (#c62828) accent stripe across the middle.
Two squat guard towers flanking a central gate, each tower with a narrow slit window glowing red.
Battlements (crenellations) along the top edge.
Large white skull emblem above heavy iron-banded wooden gate.
Coiled barbed wire along the top of the walls.
Dark red (#8e0000) flag with a white skull on a flagpole."""
    },
]

# ---- Soldier appearance --------------------------------------------------

SOLDIER_APPEARANCE = {
    "infantry_blue": """Chunky cartoon Boom Beach style soldier, strict side profile facing right.
- Oversized head (~one-third of body height), friendly determined expression, big eyes
- Olive green (#558b2f) army helmet with chinstrap and a small white highlight shine
- Warm tan (#ffcc80) skin
- Olive green combat vest over a teal-blue (#1565c0) undershirt - vest has visible pockets
- Olive green trousers, brown leather combat boots
- Holding a small black assault rifle in BOTH HANDS at chest level, barrel pointing RIGHT
- Stocky cartoon proportions""",

    "infantry_red": """Chunky cartoon Boom Beach style ENEMY soldier, strict side profile facing right.
- Oversized head (~one-third of body height), slight scowl, menacing but cartoonish
- Crimson red (#c62828) army helmet with darker (#8e0000) shadow tone, chinstrap, white highlight
- Warm tan (#ffcc80) skin
- Dark crimson combat vest with black accents over a black undershirt
- Dark grey trousers, black combat boots
- Holding a small black assault rifle in BOTH HANDS at chest level, barrel pointing RIGHT
- Stocky cartoon proportions""",

    "bazooka_blue": """Chunky cartoon Boom Beach style soldier with rocket launcher, strict side profile facing right.
- Oversized head, friendly determined expression, big eyes
- Olive green (#558b2f) helmet with round goggles pushed up on the brim
- Warm tan (#ffcc80) skin
- Olive green combat vest over a teal-blue (#1565c0) undershirt
- Olive green trousers, brown leather combat boots
- Long dark grey (#37474f) bazooka tube on his RIGHT shoulder, pointing RIGHT,
  with a small front sight and visible round opening at the muzzle end
- Both hands gripping the launcher (one at trigger, one supporting front)
- Stocky cartoon proportions""",

    "bazooka_red": """Chunky cartoon Boom Beach style ENEMY soldier with rocket launcher, strict side profile facing right.
- Oversized head, slight scowl, menacing but cartoonish
- Crimson red (#c62828) helmet with goggles pushed up on the brim
- Warm tan (#ffcc80) skin
- Dark crimson combat vest with black accents over black undershirt
- Dark grey trousers, black combat boots
- Long dark grey (#37474f) bazooka tube on his RIGHT shoulder, pointing RIGHT
- Both hands gripping the launcher
- Stocky cartoon proportions""",
}

# ---- 8-pose walk cycle prompts -------------------------------------------

# Each pose specifies leg/arm position AND the body's vertical position,
# so the rise-and-fall is intrinsic to the art (no programmatic bounce).

POSES = [
    ("1", "RIGHT CONTACT", """RIGHT-FOOT CONTACT POSE (frame 1 of 8).
- The RIGHT foot has just struck the ground AHEAD of the body, heel down, leg straight forward.
- The LEFT foot is BEHIND the body with the heel lifted, toes pushing off the ground.
- LEGS APART in a clear forward stride.
- LEFT arm swung FORWARD, RIGHT arm swung BACK (arms always opposite to legs).
- TORSO leans very slightly BACKWARD on impact.
- Body at NEUTRAL vertical height — feet near bottom of canvas.
- Weapon held in both hands as in the appearance description."""),

    ("2", "RECOIL", """RECOIL POSE (frame 2 of 8).
- RIGHT leg now supporting weight, the right KNEE BENDS slightly to absorb the impact.
- LEFT foot has just lifted off the ground behind the body.
- Body drops SLIGHTLY (a few pixels lower than the contact frame).
- Arms moving toward NEUTRAL — left arm coming back, right arm coming forward, both nearer the body.
- Torso almost upright.
- Weapon held in both hands."""),

    ("3", "MIDSTANCE LOW", """MIDSTANCE / LOW POINT (frame 3 of 8).
- Body at its LOWEST vertical position of the entire walk cycle.
- RIGHT leg STRAIGHT, planted DIRECTLY UNDER the body bearing full weight.
- LEFT leg passing forward in mid-air, knee BENT, foot off ground.
- Both arms hang at neutral, near the body's centreline.
- Torso upright.
- The body should be drawn LOWER on the canvas than frames 1, 2, 4.
- Weapon held in both hands."""),

    ("4", "PUSH-OFF HIGH", """PUSH-OFF / HIGH POINT (frame 4 of 8).
- Body RISES to its HIGHEST vertical position — drawn HIGHER on the canvas.
- RIGHT leg EXTENDING and pushing BACKWARD off the ground (toes pointing back).
- LEFT leg swinging FORWARD almost fully extended, knee nearly straight, foot still off the ground.
- Arms crossing through neutral toward the OPPOSITE positions: LEFT arm starting back, RIGHT arm coming forward.
- Torso leans very slightly FORWARD on push-off.
- Weapon held in both hands."""),

    ("5", "LEFT CONTACT", """LEFT-FOOT CONTACT POSE (frame 5 of 8) — exact mirror of frame 1's leg/arm action.
- The LEFT foot has just struck the ground AHEAD of the body, heel down, leg straight forward.
- The RIGHT foot is BEHIND the body with heel lifted, toes pushing off.
- LEGS APART in a clear forward stride.
- RIGHT arm swung FORWARD, LEFT arm swung BACK (mirror of frame 1).
- Torso leans very slightly BACKWARD on impact.
- Body at NEUTRAL vertical height (same as frame 1).
- Weapon held in both hands."""),

    ("6", "RECOIL", """RECOIL POSE (frame 6 of 8) — mirror of frame 2.
- LEFT leg now supporting weight, the left KNEE BENDS slightly to absorb impact.
- RIGHT foot has just lifted off the ground behind the body.
- Body drops SLIGHTLY (a few pixels lower than contact).
- Arms moving toward NEUTRAL — right arm coming back, left arm coming forward.
- Torso almost upright.
- Weapon held in both hands."""),

    ("7", "MIDSTANCE LOW", """MIDSTANCE / LOW POINT (frame 7 of 8) — mirror of frame 3.
- Body at its LOWEST vertical position again — drawn LOW on the canvas.
- LEFT leg STRAIGHT, planted DIRECTLY UNDER the body bearing full weight.
- RIGHT leg passing forward in mid-air, knee BENT, foot off ground.
- Both arms hang at neutral.
- Torso upright.
- Weapon held in both hands."""),

    ("8", "PUSH-OFF HIGH", """PUSH-OFF / HIGH POINT (frame 8 of 8) — mirror of frame 4.
- Body RISES to its HIGHEST vertical position again — drawn HIGH on the canvas.
- LEFT leg EXTENDING and pushing BACKWARD off the ground.
- RIGHT leg swinging FORWARD almost fully extended.
- Arms crossing through neutral toward the OPPOSITE positions: RIGHT arm starting back, LEFT arm coming forward.
- Torso leans very slightly FORWARD on push-off.
- This frame must loop cleanly back into frame 1 (right-foot contact).
- Weapon held in both hands."""),
]

SOLDIERS = list(SOLDIER_APPEARANCE.keys())
SOLDIER_SIZE = "1024x1024"


# ---- Generation helpers --------------------------------------------------

def soldier_generate_prompt(soldier_key, pose_text):
    """Frame 1: generated from scratch."""
    return (
        f"{STYLE}\n\n"
        f"CHARACTER:\n{SOLDIER_APPEARANCE[soldier_key]}\n\n"
        f"POSE:\n{pose_text}\n\n"
        f"This is the first frame of an 8-frame walk cycle. The character must be "
        f"recognisably the same across all frames - same colours, outfit, helmet, weapon, "
        f"face, proportions. Only the leg/arm position and overall body height vary."
    )


def soldier_edit_prompt(pose_text):
    """Frames 2-8: edited from frame 1."""
    return (
        "Generate a new pose of THE SAME EXACT CHARACTER shown in the input image. "
        "Keep ALL visual details identical: same colours, same helmet shape, same vest, "
        "same skin tone, SAME WEAPON held in both hands, same face, same body proportions, "
        "same outline weight, same art style. The character must be unmistakably the same "
        "soldier between frames - if you remove or change the weapon, the cycle is broken.\n\n"
        f"{pose_text}\n\n"
        "True alpha-channel transparent background. No checkerboard. No background fill. "
        "Subject centred horizontally."
    )


def save_b64_png(b64_data, path):
    path.write_bytes(base64.b64decode(b64_data))


def generate_image(prompt, size, name):
    print(f"  Generating {name}...")
    t0 = time.time()
    resp = client.images.generate(
        model="gpt-image-1", prompt=prompt, size=size,
        background="transparent", quality="high", n=1,
    )
    print(f"    Done in {time.time() - t0:.1f}s")
    return resp.data[0].b64_json


def edit_image(input_path, prompt, size, name):
    print(f"  Editing {name}...")
    t0 = time.time()
    with open(input_path, "rb") as f:
        resp = client.images.edit(
            model="gpt-image-1", image=f, prompt=prompt, size=size,
            background="transparent", quality="high", n=1,
        )
    print(f"    Done in {time.time() - t0:.1f}s")
    return resp.data[0].b64_json


# ---- Main ----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="Generate just one asset prefix")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--soldiers", action="store_true",
                        help="Only generate the walk-cycle soldier frames")
    parser.add_argument("--environment", action="store_true",
                        help="Only generate environment + logo assets")
    args = parser.parse_args()

    print("=" * 60)
    print("BEACH RAIDERS — Sprite Generator")
    print("=" * 60)

    generated = 0

    # Environment + logo assets
    if not args.soldiers:
        for asset in ENVIRONMENT_ASSETS:
            name = asset["name"]
            if args.only and not name.startswith(args.only):
                continue
            path = ASSETS_DIR / name
            if args.skip_existing and path.exists():
                print(f"\n[SKIP] {name}")
                continue
            print(f"\n[GENERATE] {name}")
            # Logo gets a self-contained prompt — no side-profile style guide
            full_prompt = asset["prompt"] if name == "logo.png" else f"{STYLE}\n\n{asset['prompt']}"
            try:
                b64 = generate_image(full_prompt, asset["size"], name)
                save_b64_png(b64, path)
                generated += 1
            except Exception as e:
                print(f"  FAILED: {e}")

    # Base assets (skip when --soldiers or --environment)
    if not args.soldiers and not args.environment:
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
                b64 = generate_image(f"{STYLE}\n\n{asset['prompt']}", asset["size"], name)
                save_b64_png(b64, path)
                generated += 1
            except Exception as e:
                print(f"  FAILED: {e}")

    # Soldiers — 8-frame walk cycle each
    for soldier_key in SOLDIERS:
        if args.only and not soldier_key.startswith(args.only):
            continue

        # Frame 1: generate
        f1_path = ASSETS_DIR / f"{soldier_key}_1.png"
        if args.skip_existing and f1_path.exists():
            print(f"\n[SKIP] {f1_path.name}")
        else:
            print(f"\n[GENERATE] {f1_path.name} (right-foot contact)")
            try:
                b64 = generate_image(
                    soldier_generate_prompt(soldier_key, POSES[0][2]),
                    SOLDIER_SIZE, f1_path.name,
                )
                save_b64_png(b64, f1_path)
                generated += 1
            except Exception as e:
                print(f"  FAILED: {e}")
                continue

        # Frames 2-8: edit from frame 1
        for frame_num, label, pose_text in POSES[1:]:
            fn_path = ASSETS_DIR / f"{soldier_key}_{frame_num}.png"
            if args.skip_existing and fn_path.exists():
                print(f"[SKIP] {fn_path.name}")
                continue
            print(f"[EDIT]  {fn_path.name} ({label})")
            try:
                b64 = edit_image(
                    f1_path, soldier_edit_prompt(pose_text),
                    SOLDIER_SIZE, fn_path.name,
                )
                save_b64_png(b64, fn_path)
                generated += 1
            except Exception as e:
                print(f"  FAILED: {e}")

    print("\n" + "=" * 60)
    print(f"Done. Generated {generated} images.")
    print(f"Approximate cost: ${generated * 0.17:.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
