# A‑Level Revision Planner — Research & Build Plan

**Prepared:** July 2026 · **Target learner:** Year 12 → Year 13 student, three A‑levels
**Goal:** minimum **AAA** for a chosen university course.
**Key dates:** Mock exams **Oct 2026** and **Feb 2027** · Final A‑levels **May–June 2027**.

**Subjects & boards**
- **Politics** — AQA (7152)
- **History** — AQA (7042): Russia depth + a Wars‑of‑the‑Roses‑era breadth study + Civil Rights NEA (coursework)
- **Business** — Edexcel/Pearson (9BS0)

---

## 1. Context — the problem we're solving

The student knows the content is coming but struggles to **organise himself**: what to revise, at what depth, in what order, and how to convert knowledge into **exam marks**. The evidence is unambiguous that the highest‑leverage activities for an A grade are (a) **spaced retrieval practice**, (b) **timed past‑paper practice self‑marked against the real mark schemes**, and (c) **exam technique drilled separately from content**. Passive re‑reading and highlighting are the weakest use of time.

So the app is **not** a notes/flashcard toy. It is a **planner + practice engine**: it breaks each spec into a topic map, generates a **daily plan** that ramps toward the three milestones, pushes **exam‑style questions continually**, and gives fast **feedback on essays against board mark schemes** — always flagged as an unofficial approximation.

---

## 2. Research findings (grounding the content — verified July 2026)

> Sourcing note: AQA/Pearson PDF hosts block automated download from this environment, so figures below come from indexed spec/mark‑scheme content cross‑checked across sources. Items marked **⚠ VERIFY** should be confirmed against a current past paper/spec PDF before the content is hard‑coded. None of this blocks the build — the content model is fully editable.

### 2.1 AQA Politics (7152) — 3 papers, each 2h, **77 marks, 33.3%**
| Paper | Title | Content |
|---|---|---|
| 1 | Government & Politics of the **UK** | Constitution, Parliament, PM & executive, judiciary/branches, devolution; democracy & participation, parties, electoral systems, voting & media, pressure groups |
| 2 | Government & Politics of the **USA** + comparative | US constitution/federalism, Congress, presidency, Supreme Court & civil rights, participation; **comparative** via rational / cultural / structural theory |
| 3 | **Political Ideas** | Core (compulsory): Liberalism, Conservatism, Socialism + **one** non‑core (Anarchism/Ecologism/Feminism/Multiculturalism/Nationalism) — ideas **and named thinkers** |

- **Question types:** `9‑mark "explain and analyse"` (AO1 6 / AO2 3, no evaluation) · `25‑mark extract/source` (Papers 1 & 2) · `25‑mark essay` "Analyse and evaluate the view that…" (**AO1 5 / AO2 10 / AO3 10**).
- **AOs:** AO1 knowledge · AO2 analysis · AO3 evaluation. Roughly **two‑thirds of marks are AO2+AO3** — analysis & evaluation win the grade.
- **Top band (Level 5, 21–25):** balanced, confidently developed analysis; sustained evaluation *throughout*; well‑substantiated judgement signposted early; precise current examples; genuine comparison (P2) / accurate thinkers (P3). Technique = **PEAL/PEEJE**, every paragraph returns to the question.
- ⚠ VERIFY: exact AO split of the *extract* question; Paper 3 essay‑choice structure.

### 2.2 AQA History (7042) — Comp1 40% · Comp2 40% · NEA 20%; overall **AO1 60 / AO2 20 / AO3 20**
- **⚠ IMPORTANT — which Component 1?** The true *Wars of the Roses* option is **2B (a Component 2 depth study)** — which **cannot** be taken alongside **Russia 2N (also Component 2)**. So the student almost certainly sits **Component 1 = 1C "The Tudors: England, 1485–1603"**, which opens with Henry VII ending the Wars of the Roses at Bosworth (1485). **Please confirm which he actually sits — it changes Component 1 entirely.** (Plan below assumes 1C Tudors.)
- **Component 1 — 1C Tudors** (2h30, 80 marks): Section A = one 30‑mark **interpretations** question on 3 historian extracts (**AO3**); Section B = two of three **25‑mark essays** (**AO1**), each spanning ≥20 years. Part One 1485–1547 (Henry VII, Henry VIII), Part Two 1547–1603 (Edward, Mary, Elizabeth).
- **Component 2 — 2N Russia 1917–1953** (2h30, 80 marks): Section A = one 30‑mark **primary‑source value** question on 3 sources (**AO2**); Section B = two of three **25‑mark essays** (**AO1**). Part One 1917–1929 (revolutions, Civil War, War Communism, NEP, Lenin's death); Part Two ~1929–1953 (collectivisation, Five‑Year Plans, Terror/purges, WWII, High Stalinism).
- **Component 3 — NEA / Civil Rights** (40 marks, tests AO1+AO2+AO3): **3,500–4,500 words**, spanning **~100 years**, evaluating **≥3 primary sources** and **differing historical interpretations**, own investigation, internally marked + AQA moderated.
- **Top bands (Level 5):** essays = fully analytical, balanced, well‑substantiated judgement; interpretations = understand all 3 extracts + strong context; sources = content **and** provenance evaluated for **value**.

### 2.3 Edexcel Business (9BS0) — 3 papers, each 2h, **100 marks, 33.3%**
| Paper | Title | Themes |
|---|---|---|
| 1 | Marketing, people & global businesses | **Themes 1 & 4** |
| 2 | Business activities, decisions & strategy | **Themes 2 & 3** |
| 3 | Investigating business in a competitive environment | **All four (synoptic)**, applied to a **pre‑released research context** |

- **Themes:** 1 Marketing & people · 2 Managing business activities · 3 Business decisions & strategy · 4 Global business.
- **Paper 3 pre‑release for Summer 2026:** confectionery/chocolate & sugar industry. (A new context will be published for **Summer 2027** — the app must let us swap it in.) ⚠ VERIFY the 2027 context when AQA/Pearson release it.
- **Question types:** short **calculations** (ratios, investment appraisal/NPV, break‑even, decision trees — "show working"); analysis 8–10 marks; **evaluation essays 12 & 20 marks** (each section ends in a 20‑marker). ⚠ VERIFY whether 9BS0 A‑level has any MCQs (evidence says **no** — that's a GCSE feature); confirm per‑question tariffs against Summer 2024/25 papers.
- **AOs:** AO1 knowledge (~20–22%) · AO2 application to context (~22–24%) · AO3 analysis (~28–30%) · AO4 evaluation/judgement (~26–28%). High‑tariff essays are **AO3+AO4‑dominated**.
- **Top band (L4, 17–20):** sustained application to the specific business; balanced developed analysis (**fewer, fully‑developed** chains beat many shallow ones); supported judgement adding fresh reasoning, justified via **MOPS = Market / Objectives / Product / Situation** and short‑ vs long‑term. **≥10% of qualification marks are quantitative.**

### 2.4 Revision science → how the engine should schedule (evidence‑based)
- **Combine spacing + retrieval into one engine.** Expanding intervals (~1‑3‑7‑14‑30‑60 days, doubling, capped at the exam), every study session **ends in a retrieval quiz**, missed items **resurface sooner** (Leitner/SM‑2‑style). Anchor the **final review 1–2 days before each exam** and count back — so topics are first learned ≥~30–45 days before the exam that assesses them.
- **Interleave** topics/question types within sessions; don't block one topic for hours.
- **Stage past papers:** untimed while learning → timed single questions/sections → **full timed papers** near mocks/finals. After every paper, **self‑mark against the scheme** and log where marks were lost.
- **Diagnose lost marks by cause** — content gap vs misread question vs timing vs weak structure vs slip — and route content gaps to the spacing queue, technique errors to separate **technique drills**.
- **Sustainable load, quality over quantity:** ~**3–4 focused hours** on school days, ~**4–6h** in holidays/peak, in short 25–50‑min blocks with breaks and rest days. **Consistency beats marathons.** Ramp: now→Oct (first‑pass learning + start reviews) → post‑Oct→Feb (fix weaknesses, more timed practice) → Feb→May/June (peak: full timed papers, heavy interleaved retrieval, final spaced reviews).
- Each mock is a **checkpoint that re‑weights the schedule** toward weak topics.

### 2.5 Essay auto‑marking (levels‑of‑response) design
- Schemes are **best‑fit / holistic**, split into levels with descriptors tied to AOs, plus **indicative content that is illustrative, not a checklist**. Marker process: read whole → place level bottom‑up → fine‑tune within level.
- **LLM rubric that mirrors this:** feed the model the **real level descriptors + AO weights for that exact question type**; instruct read‑holistically → place level → pick a mark in range → justify. Treat indicative content as illustrative (don't reward keyword‑stuffing). Output = **(a) level, (b) mark in range, (c) AO‑by‑AO feedback, (d) 2–3 concrete fixes**. Keep the prompt **lean** (minimal criteria‑focused rubrics beat baroque "you are a senior examiner" prompts). Optionally average a few runs for stability.
- **Always** label output as an **unofficial approximation — not a predicted/official grade**; encourage cross‑checking with the teacher and real mark scheme. LLM marking is prompt‑sensitive, varies run‑to‑run, and is weakest on surface accuracy.

---

## 3. App concept

A single **installable PWA** (add to home screen, works offline) that he opens daily. It answers three questions instantly: **"What do I do today?"**, **"How am I doing per topic/paper?"**, and **"Was this essay any good and how do I improve it?"**

Design principles: **daily‑first** (today's plan is the home screen), **practice‑centric** (every topic links to questions), **honest feedback**, **low friction** (2‑minute daily logging), **his data stays on his device**.

---

## 4. Architecture (reuses this repo's proven pattern)

The existing `beach‑raiders` app is a **dependency‑free PWA**: one `index.html`, a `manifest.json`, a service worker (`sw.js`) with network‑first HTML / cache‑first assets, and a JSON data file (`balance.json`) kept always‑fresh. **We mirror this exactly** — no framework, no build step, instantly deployable as a static site.

```
revision/                     # new folder in this repo (keeps the game untouched)
  index.html                  # app shell + all UI/logic (vanilla JS, modular <script> sections)
  manifest.json               # PWA metadata (name "Revision Planner", standalone, portrait)
  sw.js                       # offline shell cache (adapted from the game's sw.js)
  data/
    politics.json             # spec map: papers → topics → subtopics, question types
    history.json
    business.json
    rubrics.json              # per‑question‑type mark‑scheme levels + AO weights (for marking)
  assets/                     # icons
```

- **Storage:** `localStorage` for settings/schedule state; **IndexedDB** for the larger stuff (essay history, per‑topic practice log, question bank). All on‑device.
- **Content as data, not code:** every spec/topic/question/rubric lives in editable JSON so we can fix the ⚠ VERIFY items and swap the 2027 Business pre‑release without touching logic.
- **Essay marking needs an LLM.** No backend exists, so the pragmatic v1 is **bring‑your‑own Anthropic API key**, stored **only** in `localStorage` on his device, calling the API directly (using the latest Claude model). It's private, cheap per‑essay, and needs no server. `.gitignore` already blocks `*.key`/secrets. *(Decision flagged in §8 — a tiny hosted proxy is the alternative if you'd rather not manage a key.)*

---

## 5. Feature set

**A. Spec breakdown (the "map")** — each subject → papers → topics → subtopics, each tagged with paper, AOs, question types, and a **confidence RAG rating** he sets/updates. Visual progress per paper.

**B. Daily plan (home screen)** — generated each day from the scheduling engine (§6): a short, mixed, interleaved list — e.g. *"Russia: retrieval quiz on War Communism (10 min) · Business: one 12‑mark evaluation, untimed (20 min) · Politics: review Liberalism thinkers (10 min)."* Tick items off; ~2‑min logging.

**C. Practice & past papers** — a **question bank** (seed it from the specs + real past‑paper questions he adds), staged **untimed → timed → full paper** with a built‑in timer. After each: log mark vs scheme and **tag lost marks by cause**.

**D. Exam‑technique drills** — separate track: essay‑planning against the mark scheme, timing‑per‑mark, command‑word interpretation, structure templates (PEAL for Politics, MOPS judgement for Business, source‑provenance for History).

**E. Essay auto‑marking** — paste an answer + pick subject/question type → returns **level, mark‑in‑range, AO‑by‑AO feedback, 2–3 concrete fixes**, saved to a history so he can see improvement. Prominent "unofficial approximation" banner.

**F. Progress & milestone view** — countdowns to Oct mocks / Feb mocks / May–June finals; per‑paper readiness; weakest topics surfaced; mocks logged as checkpoints that **re‑weight** the plan.

**G. NEA tracker** — the Civil Rights coursework as its own checklist (question framing, ~100‑year span, ≥3 primary sources, historian interpretations, draft/redraft, word count 3,500–4,500) with internal deadlines.

---

## 6. Scheduling engine (the core logic)

1. **Topic inventory** per subject with `confidence` (0–5), `lastReviewed`, `examDate` (paper's exam), `weight` (exam importance).
2. **Spaced queue:** next‑review date via expanding intervals; low confidence & recently‑wrong items shorten the interval; final review pinned 1–2 days pre‑exam.
3. **Daily builder:** given today's date + a **capacity** (school‑day vs holiday hours, editable), pick a **mixed, interleaved** set across the three subjects, balancing due reviews, weak topics, and staged past‑paper practice — respecting per‑block lengths and break rests.
4. **Milestone ramp:** phase weights shift the mix from *learning* (now→Oct) → *timed practice* (Oct→Feb) → *full papers + final review* (Feb→June).
5. **Mock re‑weighting:** entering mock results per topic bumps weak areas up the queue.
6. **Adherence:** light streak/consistency signal (motivation without gamifying into pressure).

---

## 7. Build phases (proposed order; each phase is usable on its own)

- **Phase 0 — Scaffold:** `revision/` PWA shell, manifest, service worker, storage layer, navigation. *Installable, offline.*
- **Phase 1 — Spec maps & progress:** author the three `*.json` spec maps (with ⚠ VERIFY notes inline), RAG confidence UI, per‑paper progress. *He can see the whole course broken down.*
- **Phase 2 — Scheduling engine & daily plan:** the §6 engine + home‑screen daily plan + capacity settings + milestone countdowns. *The core "what do I do today".*
- **Phase 3 — Practice & technique:** question bank, timer, staged practice, lost‑mark tagging, technique drills. *Continuous exam‑style practice.*
- **Phase 4 — Essay auto‑marking:** `rubrics.json`, marking UI, LLM integration (BYO key), essay history. *Feedback loop on technique.*
- **Phase 5 — NEA tracker & polish:** coursework checklist, mock‑result re‑weighting, refinements from his real use.

I'd suggest we build **Phase 0–2 first** (a genuinely useful daily planner) so he can start using it within days, then layer practice and marking on top.

---

## 8. Open decisions (need your call before/at build)

1. **History Component 1** — confirm **1C The Tudors (1485–1603)** vs an actual Wars‑of‑the‑Roses depth option. Changes the whole History breadth map. *(Default: 1C Tudors.)*
2. **Essay marking backend** — **(a) bring‑your‑own Anthropic API key** stored on his device (recommended: private, no server, ~pennies per essay) **vs (b)** a small hosted proxy we run **vs (c)** ship without marking in v1 and add later.
3. **Where to host** — the game is a static PWA; we can deploy `revision/` the same way (e.g. GitHub Pages / any static host) so he installs it on his phone. Confirm the host.
4. **Question bank seeding** — I'll seed spec‑derived questions, but real past‑paper questions/mark schemes give the best practice. Can he/you supply his past‑paper PDFs to load in?

---

## 9. Verification (how we'll confirm it works)

- **Install test:** loads offline after first visit; installs to iOS/Android home screen (mirrors the game's PWA behaviour).
- **Engine test:** seed topics with known dates → confirm the daily plan spaces reviews on the expanding intervals, interleaves subjects, respects capacity, and pins final reviews pre‑exam; simulate crossing Oct/Feb milestones to see the mix ramp.
- **Marking test:** paste a known mid‑level exemplar for each board/question type → confirm the returned level/AO feedback is sensible and the "unofficial" banner shows.
- **Content check:** walk each spec map past the ⚠ VERIFY list against a current past paper before relying on it.
- **Daily‑use trial:** he uses Phase 0–2 for a week; we tune capacity, block lengths, and topic weights from real adherence.
```
