# Frontline Extraction — Functional Implementation Spec
**Based on:** GAME_DESIGN.md v0.1  
**Status:** Draft for review  
**Constraint:** Single-file PWA, Canvas 2D, target 60fps on mid-tier Android (Snapdragon 600-series, 3GB RAM)

---

## 0. Guiding Principle

The GDD is a full production F2P game. This spec translates it into a **phased, buildable roadmap** for the existing single-HTML-file codebase. Each phase must ship playably on mobile before the next begins. Anything not listed is explicitly out of scope for this implementation pass.

---

## 1. Architecture Principles (Non-Negotiable)

### 1.1 Mobile Performance Budget
- **Frame budget:** 16ms at 60fps. Game logic must complete in ≤4ms; render in ≤12ms.
- **Draw calls:** Minimise `ctx.save()`/`ctx.restore()` — batch transforms. Current code does this acceptably.
- **No shadow/blur during gameplay.** `ctx.shadowBlur` is GPU-expensive on mobile. The existing code has 40+ `shadowBlur` assignments scattered through gameplay renderers (`drawSky`, `drawCloud`, `drawUnit`, `drawHelicopter`, HUD renderers, shop overlay). All must be audited. During active gameplay, remove or replace with a second slightly-larger filled shape (fake bloom). Restrict real `shadowBlur` to menu/overlay screens only.
- **Particle cap:** Hard cap of 80 simultaneous particles. Pool and reuse (see §7.1 for correct typed-array approach with color/type flags).
- **Unit cap:** Hard cap of 40 simultaneous units (player + enemy combined). Excess spawns are queued, not dropped.
- **Object pools:** Bullets, particles, and floating texts must come from pre-allocated pools. No `push()` that grows unbounded arrays in the hot path.
- **Touch button state updates:** `updateButtonFills` already runs in its own independent `requestAnimationFrame` chain. Throttle it within that chain using a frame counter — do NOT absorb it into the main `gameLoop`.
- **Offscreen background:** Pre-render the static background to a `document.createElement('canvas')` once per level load. Redraw only when cameraX changes by ≥1px (dirty flag). The cached layer covers: sky gradient, mountains, static ground, beach, rocks/flowers. **Excluded from cache (animated):** ocean waves (`drawOcean` reads `frameCount`), cloud sprites, birds. Cache must not include `ctx.shadowBlur` from `drawSky` sun glow — replace with a plain filled arc.
- **Gradient allocation GC risk:** `drawSky`, `drawGround`, and `drawOcean` together create ~50 gradient objects per frame (40 rocks × 1 radial gradient each + sky/ocean linear gradients). These trigger GC. The background cache eliminates most of them; the cache must cover the entire ground layer including rock gradients.
- **rAF throttling on idle screens:** On static states (`'menu'`, `'paused'`, `'levelcomplete'`, `'worldmap'`, `'levelbrief'`), throttle the main rAF to ~10fps by tracking `performance.now()` and skipping frames.
- **rAF pause on `document.hidden`:** Add `document.addEventListener('visibilitychange', ...)` to cancel rAF when hidden, resume when visible. Prevents battery drain and avoids accumulating `frameCount` during backgrounded sessions (which corrupts lives-refill timestamp logic).
- **State machine ctx safety:** Every new canvas screen draw function (`drawWorldMap`, `drawLevelBrief`, `drawStarScreen`, etc.) **must** begin with `ctx.save()` and end with `ctx.restore()`. Any leaked `shadowBlur`, `globalAlpha`, or `globalCompositeOperation` will corrupt gameplay rendering.
- **`localStorage` iOS PWA risk:** iOS standalone PWA `localStorage` can be wiped on storage pressure or after ~7 days. `writeSave` must wrap in try/catch and display a non-blocking warning toast if storage fails.

### 1.2 Single-File Constraint
All code stays in `index.html`. Supporting data lives in `balance.json` and a new `levels.json`. No npm, no build step.

### 1.3 Persistence
Use `localStorage` for all persistent state (gold, stars, XP, upgrade levels, lives, current level progress). Key: `fe_save_v1`. JSON-serialised. Written on every level complete + on `visibilitychange` (app backgrounded).

### 1.4 State Machine
The top-level `gameState` variable expands from the current 4 values to:

```
'menu'          → title screen
'worldmap'      → world map + level select
'levelbrief'    → pre-mission card overlay
'ftue_N'        → guided tutorial levels 1–5 (N = step index 0..4)
'playing'       → active gameplay
'paused'        → gameplay paused
'levelcomplete' → post-level star award screen
'shop'          → between-level upgrade shop (currently 'complete')
'gameover'      → defeat screen
'victory'       → campaign complete
```

**Transition table (critical — every existing `if (gameState !== 'playing') return` must be audited):**

| State | Runs `update()` | Runs `render()` | rAF rate |
|-------|----------------|-----------------|----------|
| `menu` | No | No (DOM screen) | Pause after 2s |
| `worldmap` | No | Yes (canvas) | 10fps |
| `levelbrief` | No | Yes (canvas overlay) | 10fps |
| `ftue_N` | Yes (FTUE logic) | Yes | 60fps |
| `playing` | Yes | Yes | 60fps |
| `paused` | No | Yes (static frame) | 10fps |
| `levelcomplete` | No | Yes (star anim only) | 60fps during anim, then 10fps |
| `shop` | No | Yes (canvas overlay) | 10fps |
| `gameover` | No | No (DOM screen) | Pause |
| `victory` | No | No (DOM screen) | Pause |

States that run `update()` must prevent enemy spawning when `levelState !== 'active'`; this is already guarded in the existing code.

---

## 2. Phase 1 — Core Campaign Loop (Implement First)

**Goal:** A complete, saveable campaign with star rewards, rescue mechanic, and 5 levels per region across 2 regions (24 playable levels). This makes the game feel like a real product, not a prototype.

### 2.1 Level Data Structure

Replace the current `BALANCE.levels.compositions` array with a `levels.json` file:

```json
{
  "regions": [
    {
      "id": "coral_coast",
      "name": "Coral Coast",
      "theme": "tropical",
      "unlockStars": 0,
      "levels": [
        {
          "id": "r1_l01",
          "name": "First Blood",
          "parTimeSec": 90,
          "parDamagePct": 30,
          "woundedCount": 2,
          "enemyComposition": { "infantry": 0.7, "bazooka": 0.3 },
          "spawnEveryFrames": 150,
          "baseHp": 400,
          "aaCount": 1,
          "briefText": "Enemy scouts have taken the beach. Clear them out.",
          "goldReward": 80,
          "xpReward": 20,
          "boss": null
        }
        // ... 11 more
      ]
    },
    {
      "id": "saharan_front",
      "name": "Saharan Front",
      "unlockStars": 8,
      "levels": [ /* ... */ ]
    }
  ]
}
```

**Region unlock check:** Before showing a region on the world map, check `totalStars >= region.unlockStars`. The current region is always accessible; locked regions show as dimmed pins.

**Load failure fallback:** `levels.json` must be embedded inline as a `const LEVELS_DATA` fallback (same pattern as `BALANCE`). If the fetch fails, the game falls back to the inline constant. At minimum, inline data for Regions 1–2 (24 levels). The `loadLevels()` async function fetches and deepMerges over the inline constant, identical to `loadBalance()`.

**Difficulty scaling** — apply formula from GDD §6 at load time, not at runtime:
```js
// Pre-compute scaled stats when loading level data
function scaleLevelStats(level, regionIndex, levelIndex) {
  const hpMult    = 1 + 0.06 * (regionIndex - 1) + 0.015 * levelIndex;
  const dmgMult   = 1 + 0.05 * (regionIndex - 1) + 0.012 * levelIndex;
  const baseHpMul = 1 + 0.18 * (regionIndex - 1) + 0.04  * levelIndex;
  return { hpMult, dmgMult, baseHpMul };
}
```

### 2.2 Wounded Soldier Rescue Mechanic

**Wounded soldiers** are stationary friendly units placed at fixed world-space positions at level start. They cannot move or fight. They are the Star B objective.

**Data shape:**
```js
let woundedSoldiers = [];
// Per wounded:
{ x, y: GROUND_Y - 11,  // ground level
  rescued: false,
  frameOffset: Math.random() * 100  // for idle bob animation
}
```

**Rendering:** Draw as infantry_blue sprites with `globalAlpha = 0.7`, slightly crouched (scale 0.85×). Draw a small pulsing red cross above them (drawn with canvas paths, no extra sprite asset).

**Pickup:** Same `helicopterPickup()` function. Add `wounded` unit type to the liftable check. When all wounded are delivered to the player base (heli drops over `playerBase.x ± 150` at low altitude), mark Star B as earned.

**Count per level:** Taken from `level.woundedCount` (2–4). Positions: evenly spread between x=600 and x=WORLD_WIDTH-600, avoiding base areas.

**FTUE safety net:** In FTUE levels (level global index ≤ 5), wounded soldiers cannot die (no enemy units target them).

### 2.3 Star Award System

Stars are evaluated at level end. Three checks:

| Star | ID | Condition |
|------|-----|-----------|
| A    | `victory`    | Enemy base destroyed (always true if level ended) |
| B    | `rescue`     | All wounded soldiers rescued before level ended |
| C    | `discipline` | No deployed player units were killed (or zero deployed) |

**Discipline tracking:** Add `playerUnitsLostThisLevel` counter. Increment when a player unit's HP reaches 0. Reset to 0 at level start.

**Star persist:** Stars per level stored in save: `save.stars["r1_l01"] = 2` (0–3). Total stars = sum of all values. Used for region unlock gates.

**Post-level screen (`levelcomplete` state):** Full-screen overlay drawn on canvas:
- Level name + "CLEARED" header
- 3 star slots animating in (empty → filled, staggered 400ms each)
- Gold earned + XP earned flying in (counter animation, 800ms)
- Two buttons: "RETRY" (re-run same level) and "CONTINUE" (advance to shop)
- Performance: this screen is static after animation completes — draw once, cache to offscreen canvas

**Star animation:** Use a frame counter; after `levelCompleteTimer > N`, fill star N. Stars use a canvas-drawn 5-point polygon (no extra sprite). Gold fill = `#ffc107`, empty = `rgba(255,255,255,0.2)`.

### 2.4 Economy & Persistence

**Gold (soft currency):**
- Earned: per-kill bounty (already exists), level clear reward, daily login.
- Spent: upgrades (existing), future: missile packs.
- Stored in `save.gold`.

**Stars / hard currency:** Not implemented in Phase 1. Stub the balance; display placeholder icon.

**XP and Rank:**
- Earned per level clear: `level.xpReward`.
- Rank thresholds: [0, 100, 250, 500, 900, 1500, 2300, 3500, 5000, 7500, 10000, 15000, 21000, 30000, ...] (18 ranks for Phase 1).
- Rank gates unit unlocks (see §2.5).
- Display: rank number + small bar on world map HUD.

**Lives:**
- Lives pool: 5 max. Refills 1 per 30 minutes real time (store `save.livesLastRefillTs`).
- Consumed only on defeat (not on first attempt per GDD §9). First attempt at any level is free.
- FTUE levels (index ≤ 5) never consume lives.
- Display as heart icons in world map HUD.
- **No lives gate in Phase 1** — implement the counter and display but always grant free retry. Gate enforcement in Phase 2.

### 2.5 World Map Screen

Drawn on the canvas (not DOM). The world map is the hub between `menu` and `levelbrief`.

**Layout:**
- Horizontal scrolling map (matches in-game scroll direction).
- Region 1 always unlocked; each subsequent region gates on star count.
- Each level = a circular pin. Connected by a path line.
- Pin states: locked (grey), available (gold pulse), completed-1star, completed-2star, completed-3star.
- Player helicopter sprite sits on the most recently completed level pin.

**Navigation:**
- Left/right drag or swipe to scroll between regions.
- Tap a pin to select → shows level name + star display → tap again to enter `levelbrief`.
- On desktop: arrow keys scroll, Enter selects.

**HUD strip (top of world map):**
- Left: rank badge + XP bar.
- Centre: gold icon + amount, lives hearts.
- Right: settings cog (stub).

**Performance:** The world map is not animated except for the pulsing available-level pin and the helicopter bob. Everything else is static after first draw. Cache static layer to offscreen canvas; only redraw when star counts change.

### 2.6 Level Brief Screen

Drawn on canvas as an overlay atop the world map.

**Content:**
- Level ID + region name.
- Difficulty indicator (1–3 skulls, derived from `regionIndex + levelIndex / 6`).
- Objective list (always: Destroy base. If `woundedCount > 0`: Rescue wounded. If level type === 'discipline': No losses).
- Star criteria shown as three greyed stars with labels.
- Gold reward estimate.
- "DEPLOY" button → transitions to `playing`.
- "BACK" button → returns to world map.

---

## 3. Phase 2 — FTUE Tutorial

Implement after Phase 1 is stable. The FTUE runs the `ftue_N` states.

### 3.1 FTUE Level Sequence

Five tutorial levels. Use hardcoded level data (not from `levels.json`) with FTUE safety nets active:
- Infinite ammo
- No CP cost to deploy
- Heli regenerates HP between waves (not in-mission)
- Lives system off
- No failure state

| Index | State key | New mechanic | Win |
|-------|-----------|-------------|-----|
| 0 | `ftue_0` | Joystick + FIRE | Reach marker, destroy 2 targets |
| 1 | `ftue_1` | Landing + PICK up wounded | Rescue 1 wounded to base |
| 2 | `ftue_2` | DEPLOY + RPS preview | Deploy 1 bazooka, beat 1 tank |
| 3 | `ftue_3` | Missile + AA | Missile-kill 1 AA, destroy small base |
| 4 | `ftue_4` | Consolidation | Full mechanics, first real stakes |

### 3.2 Tutorial UI Overlay (Canvas-drawn)
- **Pointer:** large animated arrow drawn in canvas at target button/location. Bob animation via sin(frameCount).
- **Tooltip card:** navy panel `rgba(10,22,40,0.92)`, 280×80px, drawn at fixed screen position. Auto-dismiss after the required input is performed.
- **Completion:** `ftue_N` → `ftue_N+1` when win condition met. After `ftue_4`, set `save.ftueComplete = true`, transition to world map.

### 3.3 FTUE Entry
- On first launch (`!save.ftueComplete`): skip title screen, go directly to `ftue_0`.
- On subsequent launches: skip FTUE entirely, go to world map.

---

## 4. Phase 3 — Additional Enemy Types

Implement after Phase 2. These expand the tactical variety of Regions 2+.

### 4.1 Mortar Emplacement
- Stationary. Placed at fixed world positions in region 2+ levels.
- Fires parabolic shells (arc trajectory using gravity). Shell `vy` starts negative, gravity pulls down.
- Targets the player base (not the helicopter) — forces player to destroy it quickly.
- Cannot be damaged by the helicopter minigun (same immunity as AA).
- Killed by ground troops or missiles.
- Data: `{ type: 'mortar', x, y, hp: 120, fireInterval: 300, team: 'enemy' }`.

### 4.2 Sniper Nest
- Stationary. High range (250px), high damage (45/shot), slow fire rate (every 180 frames).
- Targets player ground units (not heli). Forces RPS awareness.
- Can be killed by heli minigun (unlike AA/Mortar).

### 4.3 Camo'd Ambush Squad
- Spawned at fixed positions, `visible = false` until heli or friendly passes within 200px.
- When revealed: spawn 3 infantry from that position simultaneously.
- No special rendering until revealed.

---

## 5. Phase 4 — Dynamic Difficulty Adjustment (DDA)

Implement last, only if retention data warrants.

**Algorithm:**
- Track per-session: `playerDeployedTypes[]` — last 10 deployed unit types (ring buffer).
- If ≥ 60% of deployments are a single type, increase weight of that type's counter by 1.5× in the current level's composition table.
- **Renormalize** the resulting weights so they still sum to 1.0.
- Active from level 4+ in each region (matches GDD "off for first three levels").
- Store the weights as a multiplier overlay, not a mutation of the base composition.

```js
function adjustedSpawnWeights(baseComposition, playerDeployedTypes) {
  if (!playerDeployedTypes.length) return baseComposition;
  const counts = {};
  for (const t of playerDeployedTypes) counts[t] = (counts[t] || 0) + 1;
  const dominant = Object.entries(counts).sort((a, b) => b[1] - a[1])[0];
  if (!dominant || dominant[1] / playerDeployedTypes.length < 0.6) return baseComposition;
  const counter = { infantry: 'bazooka', bazooka: 'infantry', tank: 'bazooka' }[dominant[0]];
  if (!counter || !(counter in baseComposition)) return baseComposition;
  const adjusted = { ...baseComposition, [counter]: baseComposition[counter] * 1.5 };
  // Renormalize so values still sum to 1.0
  const total = Object.values(adjusted).reduce((a, b) => a + b, 0);
  for (const k of Object.keys(adjusted)) adjusted[k] /= total;
  return adjusted;
}
```

---

## 6. Features Explicitly Out of Scope

These features from the GDD are **not implemented** in this pass. Stub display elements only where the GDD requires them to appear:

| Feature | Reason deferred |
|---------|----------------|
| IAP / real payments | Requires app store, payment SDK. Stub gold/stars UI only. |
| Battle pass | Complex season management. Stub UI tile visible but greyed. |
| Leaderboards | Requires backend/Game Center. Stub button. |
| Social / squads | Phase 2 in GDD, architecture not warranted yet. |
| Rewarded ads | Ad SDK integration. Reserve placement slots. |
| Push notifications | Requires PWA permission flow. Add `<link rel="manifest">` push fields but no actual sends. |
| Regions 6–8 | GDD specifies these as content drops (months 3, 5, 8). |
| Engineer / Medic / Drone troops | Gated behind Rank 5+. Show in UI as locked. |
| Rocket pods | Region 3 unlock, not yet in scope. |
| Helicopter skins / cosmetics | No art assets yet. |
| Daily/weekly quests | Backend required for real-time reset. |
| LTE events | Deferred — requires content team output. |

---

## 7. Refactor & Performance Tasks (Do Alongside Phase 1)

These are not features but are required for Phase 1 to be performant.

### 7.1 Object Pools

The existing particle system stores heterogeneous particle types as plain objects with type flags (`isShockwave`, `isCasing`, `isDebris`, `isDust`) and a `color` string. A pure Float32Array pool cannot store these. Use a **hybrid pool**: Float32Array for physics fields, parallel Int8Array for type flags, separate color index:

```js
const MAX_PARTICLES = 80;
// Float32Array fields: x, y, vx, vy, life, maxLife, size, gravity (8 per particle)
const pPhysics  = new Float32Array(MAX_PARTICLES * 8);
// Int8Array flags: type (0=fire, 1=smoke, 2=casing, 3=shockwave, 4=debris, 5=dust)
const pType     = new Int8Array(MAX_PARTICLES);
// Color indices — map to a lookup array (avoids string allocation per particle)
const PARTICLE_COLORS = ['#ff9800','#ff5722','#ffeb3b','#9e9e9e','#795548','#ffffff'];
const pColorIdx = new Uint8Array(MAX_PARTICLES);
let particleCount = 0;

function spawnParticleFull(x, y, vx, vy, life, size, colorIdx, type = 0, gravity = 0.08) {
  if (particleCount >= MAX_PARTICLES) return;
  const b = particleCount * 8;
  pPhysics[b]=x; pPhysics[b+1]=y; pPhysics[b+2]=vx; pPhysics[b+3]=vy;
  pPhysics[b+4]=life; pPhysics[b+5]=life; pPhysics[b+6]=size; pPhysics[b+7]=gravity;
  pType[particleCount] = type;
  pColorIdx[particleCount] = colorIdx;
  particleCount++;
}

function updateAndDrawParticles() {
  let i = 0;
  while (i < particleCount) {
    const b = i * 8;
    pPhysics[b]   += pPhysics[b+2];
    pPhysics[b+1] += pPhysics[b+3];
    pPhysics[b+3] += pPhysics[b+7]; // vy += gravity
    pPhysics[b+4] -= 1;
    if (pPhysics[b+4] <= 0) {
      // Swap-remove with last
      const last = particleCount - 1;
      const lb = last * 8;
      pPhysics.copyWithin(b, lb, lb + 8);
      pType[i] = pType[last];
      pColorIdx[i] = pColorIdx[last];
      particleCount--;
    } else {
      // Draw
      const alpha = pPhysics[b+4] / pPhysics[b+5];
      ctx.globalAlpha = alpha;
      ctx.fillStyle = PARTICLE_COLORS[pColorIdx[i]];
      ctx.fillRect(pPhysics[b] - pPhysics[b+6]/2, pPhysics[b+1] - pPhysics[b+6]/2,
                   pPhysics[b+6], pPhysics[b+6]);
      i++;
    }
  }
  ctx.globalAlpha = 1;
}
```

Special particle types (casings: rotated rect; shockwaves: expanding ring) retain their own small plain-object arrays with a hard cap of 4 each — they are infrequent and complex to pool uniformly.

### 7.2 Background Caching

```js
let bgCanvas = null;
let bgCameraX = -1;

function ensureBgCanvas() {
  if (!bgCanvas) {
    bgCanvas = document.createElement('canvas');
    bgCanvas.width = W; bgCanvas.height = H;
  }
}

function drawCachedBackground() {
  ensureBgCanvas();
  if (Math.abs(cameraX - bgCameraX) >= 1) {
    const bctx = bgCanvas.getContext('2d');
    // ... draw sky, mountains, ground to bctx
    bgCameraX = cameraX;
  }
  ctx.drawImage(bgCanvas, 0, 0);
}
```

### 7.3 Remove `ctx.shadowBlur` from Hot Path

Audit all `drawUnit`, `drawHelicopter`, `drawBullets`, `updateParticles` render calls. Move any `shadowBlur` to offscreen pre-render or replace with a second slightly-larger filled shape (fake bloom).

### 7.4 Touch Button State Updates

`updateButtonFills` already runs in its own rAF chain (independent of `gameLoop`). Throttle it within that chain — do NOT merge it into `gameLoop`:

```js
let _btnFillSkip = 0;
function updateButtonFills() {
  if (++_btnFillSkip < 3) { requestAnimationFrame(updateButtonFills); return; }
  _btnFillSkip = 0;
  // ... existing fill logic ...
  requestAnimationFrame(updateButtonFills);
}
```

---

## 8. Save Format

```js
const DEFAULT_SAVE = {
  version: 1,
  gold: 30,
  stars: {},       // { "r1_l01": 2, ... }
  xp: 0,
  rank: 1,
  lives: 5,
  livesLastRefillTs: 0,
  upgrades: {},    // { "infantryDamage": 1, ... } — persistent across levels
  currentRegion: 0,
  currentLevel: 0, // index within region
  ftueComplete: false,
};

function loadSave() {
  try {
    const raw = JSON.parse(localStorage.getItem('fe_save_v1') || '{}');
    // Use deepMerge (existing utility) so sub-objects like stars/upgrades are
    // merged field-by-field rather than replaced wholesale by a shallow spread.
    const s = JSON.parse(JSON.stringify(DEFAULT_SAVE));
    deepMerge(s, raw);
    return s;
  } catch { return JSON.parse(JSON.stringify(DEFAULT_SAVE)); }
}
function writeSave(save) {
  try {
    localStorage.setItem('fe_save_v1', JSON.stringify(save));
  } catch (e) {
    // iOS PWA storage can be wiped; surface non-blocking warning
    showToast('⚠ Save failed — storage full?');
  }
}
```

Upgrades are now **persistent across levels** (not reset between levels as in the current code). The between-level shop unlocks deeper tiers rather than starting fresh each run.

---

## 9. Upgrade Economy (Persistent, Phase 1)

The current 3-tier upgrade system is replaced with the 10-tier system from GDD §7.

**Helicopter tracks (4):**

| ID | Effect per tier | Base cost |
|-----|----------------|-----------|
| `hull` | +HP | 200g |
| `minigun` | +DPS / fire rate | 200g |
| `missileRack` | +ammo cap, +damage | 400g |
| `avionics` | +speed, +cargo slots | 300g |

Cost curve: `cost(tier) = baseCost * (1.55 ^ (tier - 1))`, rounded to nearest 10.

**Unit tracks (3, 10 tiers each):**

| ID | Effect |
|-----|--------|
| `infantryStats` | HP and DPS per tier |
| `bazookaStats` | HP and DPS per tier |
| `tankStats` | HP and DPS per tier |

**Shop access:** The between-level shop now shows the 4 heli tracks + 3 unit tracks (7 cards total) using horizontal scroll on mobile. Cards show current tier / 10, cost of next tier.

**Region gate:** Tiers 7–10 of heli upgrades are greyed out until the appropriate region is cleared (see GDD §7 table).

---

## 10. Implementation Order

**Phase 1A** (lock save shape first — everything else reads from it):
1. **Refactor: object pools + background caching** (§7) — establishes performance baseline.
2. **Save/load system + persistent upgrade economy rewrite** (§8, §9) — lock `DEFAULT_SAVE` shape before any UI that reads it. Stub `playerDeployedTypes[]` array in `spawnPlayerUnit` here (needed by DDA later).
3. **Level data + wounded mechanic** (§2.1–2.2).

**Phase 1B**:
4. **Star award screen** (§2.3).
5. **Economy + XP + lives display** (§2.4).

**Phase 1C**:
6. **World map screen** (§2.5).
7. **Level brief screen** (§2.6).

**Phase 2**:
8. **FTUE** (§3).

**Phase 3+**:
9. **Additional enemy types** (§4).
10. **DDA** (§5).

---

## 11. Open Questions (Flagged for Designer)

1. **Upgrades persist across lives/retries?** Current spec says yes (persistent). GDD implies yes for campaign progression, but within-run vs across-runs wasn't explicit. **Decision needed before implementing §9.**
2. **Lives gate enforcement:** GDD says lives off until level 6+. With persistent levels, does "level 6" mean global level count or within-region? **Decision needed before implementing §2.4.**
3. **World map scroll direction:** GDD says "left to right is progression." Current game scroll is also left-to-right (player base on left, enemy on right). Confirmed consistent — no change needed.
4. **woundedCount = 0 levels:** Some early FTUE levels may have no wounded. Should Star B be automatically awarded or hidden? Recommend: hide Star B slot entirely when `woundedCount === 0`.
5. **Offline lives refill:** If user opens the game after 4 hours offline, they should receive 4 lives back (max 5). Cap refill at max. Timestamp-based calc — confirmed straightforward, no open question.
