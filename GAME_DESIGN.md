# Frontline Extraction — Game Design Document

**Version:** 0.1 draft
**Owner:** Paul (designer), THOR (synthesis)
**Status:** Living document. Sections marked **[OPEN]** are deliberate decisions to take, not bugs.

This document is the source of truth for what we're building and why. Coding and art agents should treat it as the brief; if something here conflicts with the existing code or with the UI Style Guide, this doc wins — but flag the conflict before changing things at scale.

---

## 1. Vision & Pillars

**One-line pitch.** A pocket-sized helicopter combat sandbox: fly, fight, ferry. Each level is a 90-second sortie where you destroy an enemy base, rescue wounded, and deploy ground forces under live fire.

**Heritage.** Rescue Raiders (Apple II, 1984) for the loop; Choplifter (1982) for the rescue tension; Boom Beach for the art language; Sky Force Reloaded for the campaign cadence; Royal Match for the polish ceiling.

**Positioning.** There is no modern F2P side-scrolling helicopter combat game on mobile. The closest cousins are Gunship Battle (2014, still updated — 3D mission-based) and Sky Force Reloaded (vertical shmup). The Choplifter / Rescue Raiders / Armor Alley lineage is empty. We are not breaking into a crowded niche — we are reviving a dormant one with current production values. That's both an opportunity (no incumbent to dethrone) and a risk (no audience pre-trained for the verbs); the FTUE has to be unusually generous because we cannot assume genre literacy.

**Three design pillars.** Every feature decision should pass at least one of these. Features that hit all three are the keepers.

1. **"One more sortie."** Sessions are 60–180 seconds with a clean win/lose beat. The player should always be 90 seconds away from a satisfying ending.
2. **Skill over taps.** Bullets can miss. Troops can lose. The player who reads the field beats the player who spams. Upgrades amplify skill, they don't substitute for it.
3. **Strategic loadout.** Choosing what to bring matters as much as how you fly. RPS counters, ammo budget, troop slots — every level rewards a thoughtful pre-mission decision.

**Anti-pillars** (what this is not).

- Not a PvP game at launch. Single-player campaign first; PvP/social is roadmap.
- Not a tower defence. Player is always the helicopter — never a base-painter.
- Not a gacha. No randomised heroes, no pulls, no banner FOMO.
- Not idle. Active play required; offline rewards are minimal.

---

## 2. Player Journey

The journey is the spine the rest of the doc hangs off. Decisions that contradict this should be revisited.

### First session (target: 8 minutes)

1. **Cold open** — black screen, title card stamps in, single-tap to start. No login wall.
2. **FTUE L1–L3** — three guided levels, no failure, ~90 seconds each. Player learns flight, fire, deploy.
3. **Rewards reveal** — first chest opens. Gold tally appears. Currency icons on HUD.
4. **FTUE L4–L6** — RPS, AA defence, full mission. Live mechanics, low risk.
5. **World map reveal** — region 1 unlocks. Player sees the next 6 levels and the path forward.
6. **Soft IAP prompt** — Starter Pack offer surfaces at end of session 1 (not before). One-time, 72-hour timer.

### First week (target: D7 retention 28%)

- Player clears Region 1, hits Region 2 boss within 2–3 sessions.
- First difficulty wall around Region 2 mid — the upgrade economy starts mattering here.
- Daily login chain established. Battle pass season tile becomes visible day 2.
- First **lives** consumption happens — see §9.
- First **rewarded ad** opportunity (revive after fail) on day 1–2.

### First month (target: D30 retention 12%)

- Player completes Regions 1–4 (out of 8 at launch). Star-grinding starts for ungated upgrades.
- Battle pass progression becomes a daily anchor.
- Player has made at least one IAP decision (yes or no) by D14.
- LTE (limited-time event) introduces a guest map/modifier.

---

## 3. Onboarding & FTUE

### Principles

- **No fail states during FTUE.** Player cannot die in levels 1–4.
- **One new mechanic per level.** Don't compound until the previous beat is rehearsed.
- **Total FTUE length under 5 minutes.** Industry has moved hard in this direction — Archero 2 ships a 28-second core tutorial. Long forced tutorials in 2025 collapse D1. We're more generous than Archero because our verbs are uncommon, but the ceiling is five minutes.
- **No "skip" button** until L5 (the first real-stakes level). The cost of forcing FTUE is ~3% drop-off; the cost of letting players skip is a population that never learns the deploy system. Genre-literate players will tolerate 3–4 min if the pace is brisk.
- **Pointer + tooltip + narrative line.** Each new input gets all three. Tooltip auto-dismisses after the action is performed.
- **Narrator voice** — a Commander-radio personality (think Boom Beach Lt. Hammerman energy). One-line briefs, no walls of text.

### Level-by-level breakdown

Five levels, ~4 minutes total. Each compresses two beats from the original outline.

| # | Title | New mechanics | Win condition | Time-to-clear |
|---|---|---|---|---|
| 1 | "Take Flight" | Joystick + FIRE | Fly to marker, destroy 2 static targets en route | ~45s |
| 2 | "Touch Down" | Landing + PICK | Pick up 1 wounded soldier and return to base | ~50s |
| 3 | "Boots on the Ground" | Deploy + RPS preview | Deploy 1 bazooka, beat 1 enemy tank | ~60s |
| 4 | "Air Defence" | Missile + AA battery | Use missile to destroy 1 AA emplacement, then a small enemy base | ~75s |
| 5 | "Operation Beachhead" | (consolidation, first stakes) | Destroy enemy base — first real level with full economy on | ~90s |

**FTUE-only safety nets:** infinite ammo, no resource cost to deploy, heli regenerates HP between waves. Lives system **off** until level 6+. These all turn off at L5 silently. The player notices the constraint just as they're ready for it.

**First IAP prompt:** surfaces after the player's first defeat **or** end of L5, whichever lands first. Never during FTUE proper. Anchor: ~77% of players who'll ever spend do so within 14 days; the contextual window after first failure is the highest-converting moment.

### Tutorial UI elements (art agents)

- **Pointer:** large cyan glove/finger sprite with bob animation. Anchored to button or world point.
- **Tooltip card:** translucent navy panel, 280×80 px on tablet, with 1–2 lines of body copy + Commander portrait corner-crop.
- **Mission brief overlay:** full-screen between-level card with map crop, objective text, OK button. Should match Boom Beach pre-battle screen energy.

---

## 4. Main Menu & Meta-Game

### Screen inventory

The meta-game lives across these screens. Each gets its own brief in §12.

1. **Title / loading** — logo, "Tap to begin", build version watermark bottom-left.
2. **World map** — primary hub. Regions visible, current region highlighted, level pins, player pin.
3. **Level brief** — pre-mission card: terrain, enemy composition, par time, star objectives, "Deploy" button.
4. **Loadout** — heli card, weapon/missile slots, troop slots, upgrade buttons. (See §7.)
5. **Shop** — IAP packs, gold-buys-stars-buys-upgrades chain, daily deals.
6. **Battle pass** — track view, free/premium toggle, claim buttons, progress bar.
7. **Leaderboard** — global / friends tabs, weekly reset countdown.
8. **Settings** — audio, language, account, support, restore purchases, credits.
9. **Daily reward** — appears as overlay on first launch each day before the world map renders.

### World map layout

- Single horizontal scrolling map (left to right is progression direction — mirrors the in-game scrolling direction).
- 8 regions at launch. Each region is a visually distinct biome chunk on the map (see §5).
- Within a region: 12 numbered pins + 1 boss pin = 13 levels.
- Player avatar (mini-helicopter sprite) sits on most recently completed level pin.
- Completed levels show 1/2/3 stars under the pin.
- Locked regions are visible but shrouded (think Royal Match dimmed islands).

### Top HUD (persistent across meta-game)

- Top-left: player avatar + level (XP-based rank, see §7).
- Top-centre: gold balance, star/gem balance, lives balance (with refill timer when not full).
- Top-right: settings cog, daily chest icon (pulsing if claimable), mailbox icon.

### Bottom HUD

- Centre: large **PLAY** button when on world map (drops you into the next level).
- Left: battle pass entry (with progress bar segment visible).
- Right: shop entry (with red dot when a new deal is available).

---

## 5. Level Structure

### Regions

**Launch:** 5 regions. **Post-launch:** regions 6–8 ship as content drops in months 3, 5, and 8. This matches industry norms — Sky Force Reloaded launched with 13 stages, Major Mayhem 2 with 50 levels, Iron Marines with 21 missions. Launching with 60 high-quality levels beats launching with 100 thin ones, and gates the art bill at something achievable.

| # | Region | Theme | New enemy unit | New hazard | New player unlock | Launch? |
|---|---|---|---|---|---|---|
| 1 | **Coral Coast** | Tropical beach (current art) | — (baseline only) | — | Infantry, Bazooka | Yes |
| 2 | **Saharan Front** | Desert outpost, dunes | Mortar emplacement | Sandstorms (vis reduction) | Tank | Yes |
| 3 | **Alpine Pass** | Snow peaks, ravines | Sniper nest | Crosswind | Heli rocket pod | Yes |
| 4 | **Iron Harbour** | Industrial port, cranes | Patrol boat | Oil slicks | Engineer troop | Yes |
| 5 | **Steel City** | Urban warzone, towers | Rooftop SAM | Skyscraper occlusion | Drone reinforcement | Yes |
| 6 | **Jade Delta** | Jungle river, mangroves | Camo'd ambush troop | Foliage | Medic troop | Drop M3 |
| 7 | **Black Reef** | Volcanic island, lava | Walker/mech | Lava jets | Heavy gunship variant | Drop M5 |
| 8 | **Frozen Vault** | Arctic finale, ice shelves | Boss heli (rival ace) | Whiteout sections | Endgame loadout | Drop M8 |

**Levels per region: 12 (10 standard + 2 sub-boss/boss).** Region rhythm: levels 1–4 introduce mechanics gently, levels 5–9 ramp difficulty, level 10 is a mid-boss skirmish, levels 11 is a high-difficulty grind level, level 12 is the region boss.

At launch: 5 × 12 = **60 levels.** Roughly 15 hours of first-clear play, ~30–40 hours including 3-starring. Post-launch each content drop adds another 12 levels.

### Level template

Every level slots into this structure. Coding agents: this should be the data shape.

```
Level {
  id: "r2_l07"
  region: "saharan_front"
  index_in_region: 7         // 1..12, or 13 for boss
  par_time_seconds: 90       // 2-star threshold
  par_damage_pct: 30         // 3-star = take less than this much heli damage
  enemy_spawn_table: [...]   // see §6
  hazards: ["sandstorm"]
  terrain_seed: 4717         // deterministic procgen for trees/rocks/etc.
  base_left:  { hp: 1000, ...}
  base_right: { hp: 1000, scale_by_region: true, ...}
  crate_slots: [...]
  intro_brief: "..."         // 1 line of Commander dialogue
  win: "destroy_enemy_base"
  loss: "heli_destroyed" | "player_base_destroyed"
}
```

### Star system

Three stars per level, awarded on **orthogonal** criteria — not stacking-severity. Stacking severity ("clear, then clear faster, then clear without damage") punishes early grinders and concentrates 3-star play among only the best. Orthogonal criteria give every play style a path to mastery and encourages multiple replays with different strategies. Sky Force Reloaded uses this model and is the proof.

The three star criteria for every level:

- **Star A — Victory:** destroy the enemy base. Default win condition.
- **Star B — Rescue:** extract every wounded soldier on the map before the level ends. There are always 2–4 wounded per level.
- **Star C — Discipline:** complete the level without losing any deployed unit (or with zero deployed units lost; depends on level type).

A skilled flier focused on aggression gets Star A. A careful pilot who plays the pickup game gets Stars A+B. A loadout strategist who reads RPS and protects troops gets all three. Most importantly: the player chooses which 2-star path they want on a re-run, which makes replay feel like new content, not chore.

Stars contribute to a region's overall progress meter, which unlocks chests at 25/50/75/100% (one-time rewards per region). 3-starring all 60 launch levels = 180 stars total. Region access also gates on star totals (see §7).

### Boss levels

Every 13th level. Bosses are:
- Tankier than regular bases (3× HP).
- Defended by a fixed enemy composition (no random spawn).
- Have one signature mechanic per boss (e.g. mortar barrage, armoured train, shielded SAM ring).
- Worth disproportionately more gold + a guaranteed star-pack reward on first clear.

---

## 6. Combat & Balancing

### Unit roster (player and enemy)

| Unit | Role | Speed | HP | DPS | Range | Strong vs | Weak vs |
|---|---|---|---|---|---|---|---|
| Infantry | Cheap line filler | 1.2 | 60 | 8 | 90 | Engineer | Tank, Mortar |
| Bazooka | Anti-armour | 0.9 | 50 | 18 (vs armour) | 140 | Tank, AA | Infantry |
| Tank | Armoured push | 0.6 | 240 | 14 | 110 | Infantry | Bazooka |
| Engineer (R4+) | Repairs friendly | 1.0 | 70 | 4 | 60 | — | Tank, Infantry |
| Medic (R6+) | Heals nearby allies | 1.0 | 50 | 0 | 50 (heal) | — | Anything direct |
| Drone (R5+) | Air recon, light strike | 2.0 | 40 | 6 | 100 | Stationary targets | AA, Sniper |

**RPS triangle** (primary). Infantry < Tank < Bazooka < Infantry. Modifiers: 1.5× damage when type advantage applies, 0.5× when disadvantaged.

### Enemy-only units

| Unit | Role | Notes |
|---|---|---|
| Mortar emplacement | Indirect fire | Stationary. Lobs shells in an arc — bypasses cover. |
| Sniper nest | Long-range pin | High damage, slow rate of fire. Cannot move. |
| AA battery | Anti-heli | Already in game. Immune to heli bullets. |
| Patrol boat | Coastal harassment | Mobile, fires shells. Region 4+. |
| Rooftop SAM | Heli-deny zone | Locks on. Player must break LOS or use missile. |
| Camo'd ambush | Pop-up squad | Hidden until heli or friendly passes within X. |
| Walker/mech | Heavy elite | Slow, lots of HP, area-effect attack. |
| Boss ace | Final region | Hostile helicopter — first time the player faces a peer. |

### Difficulty scaling

A clean formula beats hand-tuning when content is this volume. Coding agents — keep this in `data/level_scaling.json` or similar.

```
enemy_hp_mult       = 1 + 0.06 * (regionIndex - 1) + 0.015 * levelIndex
enemy_dmg_mult      = 1 + 0.05 * (regionIndex - 1) + 0.012 * levelIndex
enemy_spawn_rate    = base_rate * (1 + 0.04 * regionIndex)
enemy_base_hp_mult  = 1 + 0.18 * (regionIndex - 1) + 0.04 * levelIndex
```

This gives a region-1 level-1 enemy a 1.0× baseline; a region-8 boss enemy is ~2.5× HP, ~2× damage. Steep but survivable with upgrades.

### Enemy spawn cadence

Default: enemy base spawns 1 troop every 8 seconds, drawing from a region-specific composition table.

```
region_2_composition = {
  infantry: 0.55, bazooka: 0.25, tank: 0.15, mortar: 0.05
}
```

Spawns weight toward player's weakness if a clear pattern emerges (e.g. if player only deploys infantry, enemy spawns more bazookas). This is the **dynamic difficulty adjustment (DDA)** layer — subtle, off by default for the first three levels of any region, then on.

### Helicopter combat

- **Bullets:** straight, finite ammo, reload-on-empty. Already implemented.
- **Missiles:** lock-on for ground targets, dumbfire for moving. 2-pack purchase per level by default.
- **Rocket pods (R3+):** unguided burst. Counts as a single resource pool, separate from missiles.
- **Health regen:** none in-mission. Heal between levels or via medi crate.

---

## 7. Progression Paths

The upgrade economy is the **retention spine.** It must give the player a goal three sessions ahead at any point in the journey. Numbers below are starting positions — expect to tune in playtest.

### Helicopter (the hero unit)

Four upgrade tracks, each with 10 tiers. All tiers are gold-purchasable; tiers 7–10 of each track gate behind a region clear.

| Track | What it does | Tier-1 cost | Tier-10 cost | Region gate |
|---|---|---|---|---|
| **Hull** | +HP, +crash resistance | 200 g | 18,000 g | T7 needs R3 cleared |
| **Mini-gun** | +DPS, +fire rate | 200 g | 18,000 g | T7 needs R3 |
| **Missile rack** | +ammo cap, +damage | 400 g | 24,000 g | T7 needs R4 |
| **Avionics** | +speed, +turn rate, +cargo slots | 300 g | 22,000 g | T7 needs R5 |

Cost curve: `cost(tier) = 200 * (1.55 ^ (tier - 1))` rounded to a clean number.

### Troops

Each troop type has 10 levels. Same exponential cost curve, smaller base.

| Tier | Infantry HP/DPS | Bazooka HP/DPS | Tank HP/DPS |
|---|---|---|---|
| 1 | 60 / 8 | 50 / 18 | 240 / 14 |
| 5 | 96 / 13 | 80 / 28 | 380 / 22 |
| 10 | 165 / 22 | 140 / 48 | 660 / 38 |

A maxed unit is roughly 2.5× as effective as tier 1.

### XP and rank

Player has an XP track (separate from gold). Earned per level cleared. Rank gates **unlocks**, not stats:

- Rank 5: Engineer troop unlocks (and Region 4 access).
- Rank 12: Drone troop unlocks (and Region 5 access).
- Rank 18: Medic troop unlocks (and Region 6 access).
- Rank 30: Endgame loadout (and Region 8 access).

Stars (the in-level reward) also gate region access:

- R2: clear R1 boss + 8 stars.
- R3: clear R2 boss + 22 stars.
- R4: clear R3 boss + 42 stars.
- R5: clear R4 boss + 70 stars.

Two gates means a player can lean into either grinding or progressing, but not skip either entirely.

---

## 8. Economy

### Currencies

| Currency | Earned how | Spent on |
|---|---|---|
| **Gold** | Level clears, daily quests, ad watches, IAP | Heli & troop upgrades, level retries (low cost), missile packs |
| **Stars** (hard) | IAP, rare battle pass tiers, weekly leaderboard | Lives refill, upgrade speedups, exclusive cosmetics, premium battle pass |
| **XP** | Level clears (cannot buy) | Rank progression only |
| **Lives** | Refill timer, IAP, ad watches | Retry on failed level (not first attempt) |

### Sources and sinks

Sources (designed total per day for an active player):
- 6 level clears × 80 g avg = 480 g
- 3 daily quests × 50 g = 150 g
- 2 ad watches × 30 g = 60 g
- **Total daily gold income: ~690 g** for an active free player.

Sinks (typical):
- One upgrade per day at the player's current tier: 500–2,000 g depending on rank.
- Missile pack for one tough level: 100 g.

The intended pace is "one meaningful upgrade per 1–2 sessions" early game, slowing to "one upgrade per week" by mid-game. Cliff is intentional — that's where the battle pass and the Operator's Club subscription bridge the gap.

### Anti-economy rules

- Never sell direct stat boosts for stars. Stars buy time (speedup) or scarcity (lives), not raw power. Pay-to-win is a brand killer.
- Cosmetics are star-only, never gold. Stars need a meaningful spend that isn't gated by mid-game grind.

---

## 9. Monetisation

### Lives system **[OPEN — see Open Questions]**

Proposed model: **lives only deplete on a failed level.** First attempt at any level is free, *and so is every win.* You only burn a life when you fail. This is the modern best-practice variant — Royal Match, Candy Crush Saga, and Toon Blast all moved off "lose a life on every attempt" because charging on wins crushes session length without meaningful ARPDAU benefit.

- Max lives: **5** (raised to **7** while a premium battle pass is active — see §9 Battle Pass).
- Refill rate: **1 life per 30 minutes** (full refill in 2h 30m). Matches Royal Match, Candy Crush Saga, Toon Blast.
- Star refill cost: **75 stars** for a full top-up at launch (calibrate after soft launch).
- Ad refill: **1 free life per day** via rewarded ad.
- **Lives system off** until L6 — first 5 levels (FTUE) cannot consume lives.

Rationale: action games punish forced friction. Match-3 lives work because each session is exhausted in 30 seconds; an action level is 90s+ and the player's emotional investment makes "you have no lives left" feel arbitrary. Failure-as-cost preserves the urgency without taxing curious play. This is industry-aligned now — even the puzzle market has moved here.

**Alternative to pressure-test in playtest:** lives deplete on retry only (not first fail). Even gentler. Worth a controlled test post-launch.

### IAP catalogue

Standard mobile tiers, dual-priced for stars (hard currency) where applicable.

| SKU | Price (USD) | Stars | Notes |
|---|---|---|---|
| Star Pack — Recon | $0.99 | 80 | Entry tier |
| Star Pack — Squad | $4.99 | 480 | Best-converter; surface in starter pack slot |
| Star Pack — Battalion | $9.99 | 1,100 | "Best value" badge |
| Star Pack — Division | $19.99 | 2,400 | |
| Star Pack — Army | $49.99 | 6,500 | |
| Star Pack — Strategic | $99.99 | 14,000 | Whale tier |

Conversion math: 1 star ≈ $0.0083 at the $4.99 tier. Lives refill (50 stars) ≈ $0.42.

### Starter Pack (one-shot, surfaces after FTUE complete)

- $4.99. 72-hour countdown after first surfaced. Cannot be re-bought.
- Contents: 600 stars + 3,000 gold + +1 cargo slot heli upgrade + a cosmetic heli skin.
- Headline value: "5× normal star value."

This is the single highest-leverage IAP in mobile design. Get the value right, the conversion comes.

### Battle Pass — "Operator's Brief"

30-day seasons, 50 tiers, two tracks (free / premium). Modelled on the Royal Match Royal Pass which is the current best-in-class for casual-action audiences.

- **Free track:** ~30% of the rewards, all gold + minor cosmetics.
- **Premium track:** ~70% of rewards, including a season-exclusive heli skin, **1,200 stars** across the season (premium pass returns more than its purchase price in stars to engaged players — the Royal Pass trick), gold, daily login bonuses.
- **Premium pass price:** **$9.99 or 1,000 stars.** This is the dominant casual-action price point in 2024-25 ($9.99 across CoD Mobile premium, Royal Match local pricing average, action mobile baseline).
- **Premium pass utility hook:** while pass is active, lives cap rises 5 → 7. This is the Royal Pass trick — utility, not just rewards. Players who buy keep buying.

Pace: a daily-engaged player should complete ~tier 35 organically; tiers 36–50 require event participation or modest spend. The "miss-out" of free-track rewards is the conversion lever, not the premium-track exclusives. The +2 lives cap is the *retention* lever — that's what makes the pass feel like ongoing utility, not a one-time skin.

### Subscription — "Operator's Club" (post-launch, month 3+)

$9.99/month for:
- 2× daily login chest value
- +20% gold from level clears
- +1 daily ad-refill slot
- Member-only weekly cosmetic drop

Subscriptions outperform big IAP packs in LTV when stickiness is real. Hold for month 3 once we have D30 data.

### Rewarded ads

- **Continue after fail.** Most valuable placement. Counts as the retry, doesn't consume a life. Cap: 1 per level per session.
- **Double rewards.** Offered at end-of-level screen. Doubles gold + XP. Cap: unlimited (this is the volume placement).
- **Daily login bonus boost.** Watch ad to triple today's chest. Cap: 1 per day.
- **Free life.** 1 per day.

Target ad load: 3–4 impressions per active session. ECPM target $20+ (genre baseline).

---

## 10. Retention Systems

These are the meta-loops that pull the player back tomorrow.

### Daily login chain

7-day rotating reward. Day 7 is meaningfully bigger than days 1–6. Missing a day breaks the chain. After day 7 it resets — no escalating long-streak rewards (those punish players who already pay).

### Daily quests

3 quests, refresh every 24h. Examples:
- "Clear 3 levels." → 50 g
- "Use 5 bazooka deployments." → 50 g
- "Destroy an AA battery with a missile." → 50 g

Encourages varied play.

### Weekly tournament

Every Monday 09:00 UTC, a single region opens as a "weekly hot zone." Best 5-clear average time appears on a global leaderboard. Top 1,000 players get star rewards. Resets Sunday 21:00 UTC, then back to Monday.

### Limited-Time Events (LTEs)

Every 14 days. Each LTE is:
- 7 days long.
- Themed (e.g. "Operation Blackout" — night map, modified physics).
- A 15-level mini-campaign with unique boss.
- One exclusive cosmetic + meaningful gold/star pool.

LTEs are also the primary route for re-engagement push notifications.

### Push notifications

- Lives full (mute-able). Default on.
- Daily login chest available (next-morning).
- Weekly tournament starting.
- LTE starting / ending soon.

Three pushes per week is the safe ceiling. Beyond that, opt-out rates spike.

---

## 11. Social & Leaderboards

### Phase 1 (launch)

- **Global leaderboard.** Weekly hot-zone results (see §10).
- **Friend leaderboard.** Pulled from Game Center / Play Games. Just shows D-rank standings for all-time progress.
- **Friend invites.** Share a code, both players get 50 stars on the invitee's first level clear.
- **Profile card.** Avatar, rank, heli skin, stars earned, friend count.

### Phase 2 (post-launch)

- **Squads (clans).** 30-player groups. Squad chat, squad weekly goals (collectively clear 200 levels for a chest), squad leaderboard within global.
- **Squad raid.** A timed co-op event where the squad's combined damage chips down a giant base. Multi-day, big rewards.

Phase 2 is roadmap, not launch. Building it is a 6–8 week task that we should only commit to if D7 retention is hitting target.

---

## 12. Art & Audio Briefs (for art agents)

This section is the actionable handoff. For each screen/asset bucket, the art agent should:
1. Read the brief here.
2. Consult `UI_STYLE_GUIDE.md` for visual rules (palette, type, panel grammar).
3. Produce a mock or sprite set in the style anchored to Boom Beach / Royal Match references.

### Region art (eight biomes)

Each region needs:
- 1 parallax background (3 layers: far mountains/sky, mid terrain, foreground beach/ground).
- 4 hero scenery sprites (signature tree / rock / building / wreck).
- 2 base art variants (player blue, enemy red, theme-skinned).
- 1 unique hazard particle (sandstorm, snow, lava jet, etc.).
- 1 region "icon" for the world map.

Region 1 (Coral Coast) is done. Region 2–8 = 7 packs of ~10 sprites each. Estimate 4–6 weeks of art at 1 dedicated artist.

### Screens still to design

| Screen | Priority | Owner |
|---|---|---|
| Title / loading | P0 | art |
| FTUE pointer + tooltip | P0 | art + code |
| Mission brief overlay | P0 | art |
| World map | P0 | art |
| Loadout | P1 | art |
| Shop (IAP pack tiles) | P1 | art |
| Battle pass track view | P1 | art |
| Leaderboard | P2 | art |
| Squad screens | Phase 2 | — |

### New icon set needed (beyond current HUD)

- Engineer troop icon
- Medic troop icon
- Drone troop icon
- Rocket pod icon
- Star (currency) icon
- Lives heart icon
- Battle pass crest
- Squad/clan crest (Phase 2)

All to render in the cyan duotone idiom already established for HUD icons.

### Audio brief (separate effort)

- Commander VO: 40–60 one-line clips covering FTUE briefs, win/loss stings, mid-mission shouts. Adult male, British, dry. Reference: Boom Beach Sergeant.
- Music: 4 region themes, layered (calm/combat). Reference: Sky Force Reloaded OST tone.
- SFX: bullet variants, missile launch, base destruction, troop voices per faction.

---

## 13. Open Questions

These are decisions to take, not bugs. Sequencing matters: lock §13.1–13.3 before art commits to regions 5+; the rest can stay open through alpha.

### 13.1 Lives — every attempt or retry only?

Proposed: retries only (§9). Alternative: every attempt. Best resolved by an A/B test in soft launch; preserve the option in code.

### 13.2 PvP roadmap?

Single-player at launch. If D30 retention hits 12%+ and D90 hits 4%+, a real-time async PvP mode (think Royal Match's PvP add) is worth the build. Don't start engineering it before those numbers land.

### 13.3 Helicopter customisation — skins or chassis variants?

Skins (cosmetic only) are safer. Chassis variants (different base stats) introduces gacha-adjacent issues and complicates balance. Start with skins. Revisit chassis variants only if monetisation needs a deeper sink at month 6+.

### 13.4 Co-op?

Not in scope for launch or first content drop. Squad raid (§11) is the closest analogue without the technical cost of synchronous co-op.

### 13.5 Endgame loop?

What does a 200-hour player do? Currently unanswered. Likely a "Prestige" rank reset with cosmetic-only rewards. Need a stronger answer by month 6 of live ops.

### 13.6 Storefront positioning?

Casual action under "Arcade"? Strategy adjacent? Affects featuring conversation with the platforms. Decide before public soft launch.

---

## 14. Reference Games

Each entry: what we steal, what we don't.

- **Rescue Raiders (1984)** — the core verbs: fly, fight, ferry. The asymmetric ground war. We keep the verbs and the bidirectional map. We modernise everything else.
- **Choplifter (1982)** — the rescue tension and the side-scrolling discipline. We keep "every flight matters" — short, dense missions, no idle drifting.
- **Sky Force Reloaded** — campaign cadence (chapter × difficulty grid), star/medal grind, post-mission reward choreography. Closest peer for content structure.
- **Major Mayhem / Major Mayhem 2** — 60-second-mission discipline. We aim shorter than Sky Force, longer than Major Mayhem; ~90s is the sweet spot.
- **Royal Match** — meta-game polish, hearts UX, daily reward choreography, world-map shrouding. Our polish ceiling.
- **Boom Beach** — art direction (the lock we already chose), base aesthetics, scenery density, particle vocabulary.
- **Archero** — D1/D7 retention design, FTUE pacing (we are tighter), rewarded-ad placement. Their lives system is a counter-example: aggressive, frequently complained about; we are gentler.
- **Clash Royale** — RPS unit design discipline. Our RPS is simpler (3 types not 100) but the principle is the same: clear strong-vs-weak, never strict dominance.
- **Iron Marines** — single-screen RTS combat we don't want to be. Useful to understand where the player overload threshold sits when too many units are on-screen.
- **Brawl Stars** — short-session/social blend, profile/progress UX. Roadmap reference if PvP unlocks.

---

## Document conventions

- **[OPEN]** = decision to take.
- **(R4+)** = unlocks at Region 4 or later.
- **g** = gold (soft currency).
- **stars** = hard currency (premium).
- All times in seconds unless noted.
- All numbers in this draft are starting positions for tuning, not final values. Anything in a numbered table should be considered "version 0" — expect to retune in soft launch.

---

## Appendix: Research basis

Numbers in this draft were calibrated against current (2024-25) top-grossing games in adjacent genres. The most load-bearing references:

- **Lives system** (§9): Royal Match, Candy Crush Saga, Toon Blast all use 5 lives / 30-min refill / lose-on-fail-only. Industry has converged here in the last 18 months.
- **FTUE length** (§3): Archero 2 ships a 28-second core tutorial; industry rule is "no IAP gate before mechanics are understood." 77% of eventual spenders convert within 14 days — the early window matters, but premature spending prompts kill conversion.
- **Level count at launch** (§5): Sky Force Reloaded (13 stages × 4 difficulties), Major Mayhem 2 (50+ levels, boss every 10), Iron Marines (21 missions, 3 worlds), Archero (50 stages per chapter, boss every 10). 60 launch levels across 5 regions is the median for an action campaign by a small team.
- **3-star orthogonal criteria** (§5): Sky Force Reloaded's 4-medal system (kill 70%, kill 100%, rescue all, no damage) is the lineage. Orthogonal beats stacking-severity for replay value.
- **Battle pass economics** (§9): Royal Match Royal Pass (30 days, 80 rewards, 30 free / 50 premium, ~$11-14 local) is the casual-action benchmark. CoD Mobile premium at $4.99 / premium-plus at $9.99 sets the action-game band. Industry standard: 30-day, 50-tier, ~$9.99 premium.
- **Starter pack economics** (§9): Deconstructor of Fun 2024 industry survey — 59% of starter packs price under $5; 74% of starter-pack buyers make a second IAP within 30 days. $4.99 is the dominant entry tier.
- **Niche positioning** (§1): no modern F2P side-scrolling helicopter game on mobile in the last 3 years. Closest cousins are Gunship Battle (3D, 2014) and Sky Force Reloaded (vertical shmup). The Choplifter/Rescue Raiders lineage is empty space.

Full source list lives in the project chat history; key references include Royal Match Fandom Wiki, Game Makers analyses of Royal Match's $219 Battle Pass, Deconstructor of Fun on starter pack pricing, Game World Observer on Archero 2's tutorial, Sky Force Reloaded Fandom Wiki, and platform documentation for Iron Marines and Major Mayhem 2.

---

**End of v0.1.**
