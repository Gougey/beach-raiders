#!/usr/bin/env python3
"""Run this locally to generate assets/world_map.png via DALL-E 3.
   Place your OpenAI key in assets/.openai_key  OR  set OPENAI_API_KEY env var.
   Then: python generate_map.py
   Then: git add assets/world_map.png && git commit -m "Add commissioned world map" && git push
"""
import urllib.request, json, base64, sys, os
from pathlib import Path

KEY = (
    os.environ.get("OPENAI_API_KEY")
    or Path("assets/.openai_key").read_text().strip()
)

PROMPT = (
    "A top-down illustrated world map for a mobile strategy game, "
    "rendered in a vibrant hand-painted gouache style like Boom Beach or Clash of Clans. "
    "The map is split into two regions side by side. "
    "LEFT HALF — Coral Coast: deep teal-blue ocean on the far left with white foam shoreline, "
    "shallow turquoise water near the irregular organic coastline, a thin strip of white sandy beach, "
    "and a lush dense dark-green tropical jungle interior with palm tree silhouettes and rocky coral outcrops in the shallows. "
    "RIGHT HALF — Saharan Front: a vast sun-baked desert with warm golden-amber sand, "
    "curved dune-line patterns in slightly lighter gold, rugged dark rocky highland formations across the upper section, "
    "and one small green oasis with two palm trees and a tiny blue pool near the centre-right. "
    "Overall style: saturated colours, painterly brushwork texture, soft aerial perspective, "
    "faint topographic contour lines, a subtle military grid overlay, "
    "an ornate compass rose in the bottom-right corner, "
    "and a thin antique double-line gold border frame around the whole image. "
    "No text, no characters, no UI elements, no icons. Pure game background environment art."
)

payload = json.dumps({
    "model": "dall-e-3",
    "prompt": PROMPT,
    "n": 1,
    "size": "1792x1024",
    "quality": "hd",
    "response_format": "b64_json",
}).encode()

req = urllib.request.Request(
    "https://api.openai.com/v1/images/generations",
    data=payload,
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"},
)

print("Calling DALL-E 3 (hd 1792×1024) — takes ~20 s…")
try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    img = base64.b64decode(result["data"][0]["b64_json"])
    out = Path("assets/world_map.png")
    out.write_bytes(img)
    print(f"Saved {out} — {len(img):,} bytes")
    print("\nNext steps:")
    print("  git add assets/world_map.png")
    print("  git commit -m 'Add commissioned world map'")
    print("  git push")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
    sys.exit(1)
