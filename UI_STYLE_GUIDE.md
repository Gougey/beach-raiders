# Frontline Extraction — UI Style Guide

A tropical-military combat game with the polish vocabulary of a top-grossing match-3. Chunky 3D icons, glossy bevelled panels, gold trim everywhere it earns its place. Borrowed from Royal Match's craft language; dressed in jungle camo, gunmetal, and rocket-red.

---

## 1. Core Principles

- **Chunky, hand-sculpted 3D icons** with thick black outlines (roughly 4–6 px at 256 px icon size), sitting on richly bevelled panels.
- **Slight 3/4 isometric perspective** — camera tilted ~25–30 degrees from horizontal, ~15 degrees from the side. Every prop reads as a tiny diorama, not a flat sticker.
- **Single warm key light from the upper-left**, cool fill from the lower-right. Specular highlights are crisp; shadows are soft and contact-grounded.
- **Saturated but disciplined palette** — vivid hero objects on calm neutral panels. Never let a HUD element fight a gameplay element for attention.
- **Royal Match polish, military theme.** Everything should feel squeezable, springy, and reactive. Buttons bevel inward when pressed; rewards burst with confetti; currency tallies fly to their destinations on easing curves, not linears.
- **Gold trim is a reward signal**, not decoration. Reserve heavy gold ornamentation for premium panels, currency, win moments. Standard combat HUD stays gunmetal + accent.
- **The military layer expresses itself through props and palette**, not through grit. Frames stay glossy. Camo stencils, ammo crates, dog-tags, and field-radio textures earn their place inside an otherwise cheerful, juicy frame.

---

## 2. Colour Palette

### Team colours (locked — match in-game)
- **Player Blue** `#1565c0` — primary friendly. Highlight `#42a5f5`, shadow `#0d47a1`.
- **Enemy Red** `#c62828` — primary hostile. Highlight `#ef5350`, shadow `#8e0000`.

### Primary UI
- **Jungle Green panel base** `#2e7d32` — main panel fill, mid-tone.
- **Deep Olive shadow** `#1b3a1f` — bottom-bevel and inset shadows on green panels.
- **Lime Highlight** `#7ed957` — top-bevel and rim light on green elements.

### Secondary / neutrals
- **Gunmetal** `#37474f` — mechanical icon bodies, button bases, secondary panels.
- **Steel highlight** `#78909c` — metal rim light.
- **Iron shadow** `#1c262b` — outline interior, deep recesses.
- **Cream parchment** `#f5e7c4` — scroll cards, mission briefings.
- **Sand** `#d9b873` — secondary text on dark panels.

### Accents & rewards
- **Hero Gold** `#ffc107` core, `#ffe082` highlight, `#b8860b` shadow — coins, trophies, premium frames.
- **Reward Gold trim** `#ffd54f` with `#8a6d1b` engraved shadow — corner ornaments, frame edges.
- **Gem Purple** `#9c27b0` core, `#e1bee7` shine, `#4a148c` shadow — premium currency / loot.
- **Energy Cyan** `#26c6da` core, `#84ffff` glow — batteries, EMP, shields.
- **Rocket Orange** `#ff7043` core, `#ffab40` flame highlight — explosives, urgency.

### Semantic
- **Success** `#43a047`
- **Warning** `#ffa726`
- **Danger** `#e53935`
- **Disabled** `#9e9e9e` desaturated, ~60% opacity.

### Backdrops
- **Sky day** `#5fb3ff` to `#bde7ff` vertical gradient.
- **Briefing panel backdrop** `#102a1a` (deep jungle), used behind cards.

---

## 3. Typography

Two faces, no more. We already ship Lilita One and Fredoka — keep them.

- **Display / headings** — **Lilita One**. Used for level numbers, panel titles, big reward callouts ("VICTORY!", "EXTRACTION COMPLETE"). All-caps for combat shouts; mixed case for nav titles.
- **Button labels** — **Fredoka** weight 600. Slightly tighter tracking (-1%) at button sizes. All-caps for primary CTAs ("DEPLOY", "LAUNCH", "CLAIM"); title-case for secondary.
- **Body / tooltips / numbers in cards** — **Fredoka** weight 400 or 500. Tabular numerals on for currency counters so digits don't dance during tally animations.
- **Currency HUD numerals** — Fredoka 700 with a 2 px black stroke and a 1 px gold inner outline on premium counters.

Hierarchy targets at portrait 1080-wide reference:
- H1 panel title: 56 px Lilita One
- H2 section: 36 px Lilita One
- Button label: 28–32 px Fredoka 600
- Body: 22 px Fredoka 400
- HUD numerals: 30 px Fredoka 700

---

## 4. Icon Style Spec

Use these rules to brief an image generator or an artist.

- **Format**: square PNG, transparent background, 512×512 production, exported at 256, 128, 96.
- **Perspective**: 3/4 isometric — camera ~25° pitch, ~15° yaw. Object hero-pose, slightly hero-tilted toward viewer.
- **Outline**: solid black `#0a0d10`, 4–6 px at 256, consistent weight all the way around. No tapered "comic" lines.
- **Base / fill**: bold local colour, lifted ~5% in saturation versus the in-game world tones so icons pop on the HUD.
- **Lighting**: warm key from upper-left (`#fff2c2`), cool fill from lower-right (`#9fc8ff`). Direction stays constant across the whole library.
- **Highlights**: crisp specular dots and short streaks on metals; small soft sheen patches on plastics; tight rim-lights along upper-left silhouette edges.
- **Shadows**: soft drop-shadow under the object (60% black, 12–20 px blur, 8 px Y offset). Contact shadow lives inside the icon; the HUD panel may add its own outer shadow.
- **Materials** —
  - *Metal* (turrets, ammo, vaults): brushed gunmetal `#5c6c75` base, cool highlight, brass or gold accents on rivets/trim. Subtle scratches near edges only.
  - *Glass / energy* (batteries, shields, gems): translucent core with a brighter inner glow, two clear specular streaks (upper-left and lower-right), 1 px inner highlight outline.
  - *Gem* (rewards, premium): faceted, with one large facet catching the key light, internal coloured glow, white star-glint at the brightest point.
  - *Fabric / scroll* (mission cards, banners): slightly worn edges, soft folds, painted insignia, never photorealistic cloth.
  - *Wood / crate*: warm `#8a5a2b` planks with darker `#4a2f17` grain, brass corner braces.
- **Proportions**: cartoony — heads/business-ends larger than they would be in real life. Turret barrels are stubby and bold; gem corners are exaggerated; chests are deep and chunky.
- **No text on icons.** Numbers, prices and counts are layered in UI, not baked.

---

## 5. Buttons

All buttons share a 3-layer build: **base shape → bevel/gloss → label**, with a soft outer drop-shadow.

### Primary (green — Deploy / Confirm / Claim)
- Pill shape, corner radius 24 px on a 96 px tall button.
- Base fill `#43a047`, top-bevel `#7ed957` 6 px, bottom-bevel `#1b5e20` 8 px.
- Inner gloss: white at 35% opacity, half-height arc across the top.
- 2 px outer outline `#0a0d10`, soft drop shadow `0 6px 0` of `#0d3f12` plus blurred `0 10px 18px rgba(0,0,0,0.35)`.
- Label: Fredoka 600, white `#ffffff`, 2 px dark green inner shadow `#1b5e20`.

### Secondary (gunmetal — Cancel / Back / Options)
- Same geometry, base `#546e7a`, top-bevel `#90a4ae`, bottom-bevel `#263238`. Label cream `#f5e7c4`.

### Danger (red — Retreat / Sell)
- Base `#e53935`, top `#ff7961`, bottom `#8e0000`. Label white, with a faint warning chevron pattern at 8% opacity behind the label is acceptable on important moments.

### Premium (gold — Buy / Upgrade)
- Base `#ffc107`, top `#ffe082`, bottom `#b8860b`, with a thin gold-trim border `#fff3a8` 1 px inside the outline. Label deep brown `#3e2723` for contrast — gold buttons read as money, never red-on-red.

### States
- **Idle**: as above.
- **Hover / focus**: lift 2 px, shadow doubles its Y offset, gloss brightens by 8%.
- **Pressed**: drop 4 px (bevel inverts — top becomes shadow, bottom becomes highlight), outer shadow collapses to `0 1px 0`. Use a 90 ms ease-out for press-in, 140 ms cubic ease-out-back for release.
- **Disabled**: desaturate 60%, drop opacity to 55%, kill the gloss, keep outline. No press response.

---

## 6. Panels & Frames

- **Body**: rounded rectangle, corner radius 32 px on full-screen panels, 20 px on smaller cards.
- **Build**: outer 2 px black outline → 4 px gold trim `#ffd54f` with a 1 px engraved shadow `#8a6d1b` along the inside edge → main fill (jungle green `#2e7d32` or deep olive `#102a1a` for darker dialogs) → inner 1 px highlight `#7ed957` along the top edge.
- **Corner ornaments**: small bolted brass plates with a single rivet, at all four corners. On premium panels these become small gold sunburst medallions.
- **Header strip**: a wider banner sitting halfway above the panel top edge. Olive-drab base with a cream centre plaque carrying the title; ends finish in folded ribbon tails on premium / story panels, in cut-steel tabs on combat panels.
- **Internal spacing**: 32 px padding from the gold trim to content. 24 px between stacked rows.
- **Dividers**: 1 px `#7ed957` top, 1 px `#1b3a1f` bottom — two-tone engraved lines, never flat.

---

## 7. Currency & Resource HUD

The existing layout stays: heli HP and ammo top-left; deploy cards + missile + gold along the bottom; minimap top-centre. Replace the placeholder treatment with these specs.

### Top-left cluster (player status)
- **Heli HP bar**: stadium-shaped pill, 16 px tall, jungle-green outer frame, fill gradient `#43a047 → #7ed957`, segmented every 25% with 2 px dark dividers. Pulses red `#e53935` when below 25%.
- **Ammo counter**: small gunmetal plaque, brass corners, ammo icon at left, Fredoka 700 numerals at right with the tabular setting on.

### Top-centre
- **Minimap**: round frame in gunmetal, brass rim, 4 cardinal rivets. Inside, a slow radar sweep at 6 s per rotation. Friendly blips `#42a5f5`, enemy `#ef5350`, objective `#ffc107`.

### Bottom HUD (deploy + currency)
- **Deploy cards**: 180×220 px scroll-card frames. Cream parchment fill, gold trim, unit silhouette painted in jungle ink, cost coin badge bottom-right, cooldown shroud sweeps in radial fill when on cooldown.
- **Missile card**: same scroll-card chassis with rocket-orange accents and a red wax-seal corner.
- **Gold counter**: gold coin icon (see palette) + Fredoka 700 white numerals with 2 px gold inner outline, sitting on a small dark plaque. On increment, tally animates from current to target value over 600 ms ease-out, and the coin icon does a 1.15× scale-pulse on the first tick.
- **CP (Command Points)**: if present, identical treatment but with the cyan energy palette and a small lightning glyph instead of a coin.

### Notification badges
- Red circle `#e53935`, 2 px outline, white Fredoka 700 numeral. Sits at top-right of the host icon, slightly oversized (28 px on a 96 px icon).

---

## 8. Effects & Polish

- **Sparkle dust** — small 4-point white stars at 60–90% opacity, 6–12 px, with one large hero glint twice the size. Drift upward and fade over 600 ms. Use on rewards, level-complete, premium unlocks.
- **Glints** — a single anisotropic white streak that sweeps across gold/gem surfaces every 4–6 s of dwell, 350 ms duration, cubic ease-in-out.
- **Particle bursts** — radial spray of 12–20 polygonal chips on completion (gold coins for currency, green sparks for repair, orange embers for explosions). Lifetime 700 ms, gravity affects the last 300 ms.
- **Easing curves** — default to cubic ease-out (0.22, 1, 0.36, 1). For "pop in" use ease-out-back (0.34, 1.56, 0.64, 1). Avoid linear except for slow ambient loops.
- **Squash & stretch on buttons** — press scales to `0.94, 0.94`, release overshoots to `1.06, 1.06`, settles to `1.0`. Total under 220 ms.
- **Screen shake** — short, snappy. 6 px amplitude, 180 ms, decay curve, applied only on: heavy weapon fire, base destruction, boss hit. Never for UI.
- **Camera/HUD micro-zoom** — on level-complete, push the world camera back 4% and the HUD scales in 3%, then springs back. Reads as a satisfied "exhale".

---

## 9. Reward / Level-Complete Moments

Treat every win like a parade.

1. **Freeze + dim**: world dims to 40% over 200 ms, gameplay pauses.
2. **Banner drop**: "EXTRACTION COMPLETE" banner flies in from the top with ease-out-back (320 ms), settling with a 2-frame bounce. Gold trim, cream plaque, ribbon tails.
3. **Star tally**: 1–3 stars stamp in one at a time, 150 ms apart, each with a scale-in from 1.4 → 1.0, a white flash, and a small sparkle burst at the centre.
4. **Currency flight**: rewarded coins/gems spawn from the banner and fly along a curved Bezier into the HUD counter, with a 30 ms stagger between particles and a satisfying tick on each arrival. Counter tallies up with the 600 ms ease-out described above.
5. **Chest reveal (when applicable)**: chest scales in (ease-out-back), wobbles twice, lid flips open with rotation 0 → 110° in 280 ms, internal glow cyan-to-gold, rays of light fan out, contents rise out one-by-one with a tiny scale-pop each.
6. **Sound cue placeholders** — bright brass stinger on banner drop, single coin chimes on each tally tick, a deeper "kah-chunk" on chest open. (Audio not in scope here, but design the timing slots in advance.)
7. **Continue button** appears last, after all motion settles, with a gentle pulse loop (scale 1.0 ↔ 1.03 at 1.6 s period).

---

## 10. Image-Generation Prompt Templates

Paste-ready. Replace bracketed `{tokens}` per asset. All prompts assume a generator that respects style anchors — pair with 2–3 reference images from the asset sheet for best results.

### A. Deploy card icon (e.g. a unit)
> Mobile game icon of a `{unit description, e.g. a chunky tropical-camo infantry squad leader giving a thumbs up}`, 3/4 isometric perspective with the camera tilted about 25 degrees down and 15 degrees to the side, slight hero pose. Thick solid black outline 4–6 px, bold saturated colours, single warm key light from upper-left and cool fill from lower-right. Crisp specular highlights, soft contact shadow under the figure. Stylised cartoony proportions, hand-sculpted 3D look like a polished mobile match-3 icon. Square 512x512 PNG, fully transparent background, no text, no logos, centred composition with 8% padding.

### B. Powerup / consumable icon
> Mobile game powerup icon of a `{e.g. glowing cyan EMP grenade with brass casing}`, 3/4 isometric, thick black outline 4–6 px, warm key light upper-left, cool fill lower-right. Translucent energy core with inner glow and two clear specular streaks, brass and gunmetal mechanical housing with small rivets, faint sparkle accents around the object. Saturated palette, chunky cartoony proportions, mobile match-3 polish. Square 512x512 PNG, transparent background, no text, no shadow plate, only the contact shadow directly beneath the object.

### C. Currency icon
> Mobile game currency coin showing a `{e.g. crossed-rifles military insignia}` stamped into the face, 3/4 isometric view tilted toward the camera, thick black outline 4–6 px. Polished gold body with a hero specular highlight upper-left, deep amber shadow lower-right, gold rim trim, tiny white star-glint at the brightest point. Faceted-but-friendly cartoony style, no realism. Square 512x512 PNG, transparent background, slight soft drop shadow only, no text.

### D. Panel / frame asset
> Mobile game UI panel frame, jungle-green main body `#2e7d32`, 32 px rounded corners, framed by a 4 px gold trim with engraved shadow on the inside edge, 2 px black outer outline, brass-bolted rivet medallions at all four corners, a wider cream-and-olive header banner sitting halfway above the top edge with folded ribbon tails. Subtle inner top-edge highlight in lime green, soft outer drop shadow. Empty centre ready for content. 1024x768 PNG, transparent background, no text.

### E. Reward chest
> Mobile game treasure chest sitting closed, 3/4 isometric perspective, thick black outline 4–6 px. Dark wood `#8a5a2b` planks with darker grain, polished brass corner braces and a central lock plate, hint of golden glow leaking from the seam. Warm key light upper-left, cool fill lower-right, soft contact shadow underneath, small sparkle particles floating around the chest. Chunky cartoony proportions, polished mobile match-3 look. Square 512x512 PNG, transparent background, no text, centred with 10% padding.

### F. Mission briefing scroll card
> Mobile game scroll-style mission card, 3/4 isometric, cream parchment body `#f5e7c4` with slightly worn rolled edges and soft folds, painted jungle-ink insignia of a `{e.g. helicopter silhouette}` in the centre, red wax seal at the bottom-right corner, thick black outline 4–6 px. Warm key light upper-left, cool fill lower-right, soft contact shadow. No realistic paper texture — stylised flat painted look with chunky cartoony proportions. Portrait 512x768 PNG, transparent background, no text.

---

## Sources

- [Design Deep Dive #02 — Royal Match (Saravanan, IronSource LevelUp / Medium)](https://medium.com/ironsource-levelup/design-deep-dive-02-royal-match-948f7af96f04)
- [Royal Match Dominates Match-3: What Can ALL Designers Learn? (Funovus)](https://www.funovus.com/blogs/royal-match-dominates-match-3-what-can-all-designers-learn/)
- [5 Simple UX Lessons From Royal Match (UserWise)](https://blog.userwise.io/blog/5-simple-ux-lessons-from-royal-match)
- [Game Analysis of Royal Match (Ekin Melis Sezer, Medium)](https://medium.com/@ekinmelissezer/game-analysis-for-royal-match-and-toon-blast-9c4bff8ef48b)
- [The Design Decisions That Made Royal Match a Top-Grossing Game (Cubix)](https://www.cubix.co/blog/the-design-decisions-that-made-royal-match-a-top-grossing-game/)
- [Game UI Database — Royal Match](https://www.gameuidatabase.com/gameData.php?id=1061)
- [Royal Match — The New King from Turkey? (Deconstructor of Fun)](https://www.deconstructoroffun.com/blog/2021/3/21/royal-match-the-new-king-from-turkey)
