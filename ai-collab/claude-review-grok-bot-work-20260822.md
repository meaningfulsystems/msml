# Review: Cursor/Grok bot work, `58538ca..0e5921d`

**Date:** 2026-08-22
**Reviewer:** Claude (Anthropic)
**Under review:** 93 commits merged to `main` via PR #1 (`cursor/sysml1-coverage-render-qa-0594`) and PR #2 (`cursor/apollo-estimate-simulations-b828`)
**Author of the work:** `Cursor Agent <cursoragent@cursor.com>` — 92 of the 93 commits
**Range:** `58538ca` (Update license holder, 2026-05-18) → `0e5921d` (2026-08-22), 167 files changed, +45,409 / −598

> Naming note: no commit in this repository is signed by Grok. The bot work in this range is authored entirely by Cursor Agent; this review treats that as the "grok bot work" the branch name refers to. If a separate Grok-authored contribution exists elsewhere, it is not in this range.

> Folder note: `ai-collab/README.md` declares this folder historical and closed to *new agent instructions*. This file is a review, not agent instruction — the living agent path remains `AGENTS.md` plus `skills/`.

---

## Verification performed

All three checks from `AGENTS.md` were run against `0e5921d` on macOS 15 / Python 3 / Pillow 12.0.0:

| Check | Result |
|---|---|
| `python3 -m unittest` | **64 tests, 0 failures** |
| `msml-validate-all projects --strict` | **0 errors, 0 warnings** |
| `msml-render-all projects` | **64 succeeded, 0 failed** |

Inventory: 5 `.msml` models, 64 `.msmd` views, 64 PNGs. Every project directory holds exactly one model file — the model/view split the Grok proposal in `grok-feedback.md` asked for is now actually enforced across all five projects, not just the hero.

---

## What the bot got right

### 1. The v1 model/view architecture is real, not aspirational

`grok-feedback-decisions.md` accepted the `.msml` / `.msmd` split as a direction. This range finishes it. Five projects, one model each, 64 views referencing them, and a strict validator that passes clean. The concern Grok raised in May — "semantic drift, no enforceable single source of truth" — is answered by working tooling rather than by convention.

### 2. Test coverage is unusually strong for generated work

858 assertions across seven test files:

| File | Assertions |
|---|---|
| `test_apollo_example.py` | 411 |
| `test_e_bike_example.py` | 136 |
| `test_package.py` | 130 |
| `test_apollo_simulations.py` | 78 |
| `test_appliance_twins.py` | 60 |
| `test_adoption_pack.py` | 32 |
| `test_ibd_no_line_through_box.py` | 11 |

This matters more than the raw count suggests. The Apollo and e-bike locks in `AGENTS.md` are prose — the kind of instruction an agent silently drifts from three sessions later. Binding them to 547 assertions converts them into something that fails loudly. `1aaf1bd` ("Fix Apollo test: build relationship map for structure locks") shows the bot repairing that binding rather than deleting the failing assertion, which is the correct instinct.

### 3. The epistemic guardrails on Apollo are the best work in the range

`projects/apollo/simulations/` could easily have become a machine for laundering invented numbers into a NASA-branded model. It does the opposite, and does it deliberately:

- Every printed result is a range or a sensitivity, labeled `ESTIMATE`, never a single mission number.
- Values the model marks `UNKNOWN` (specific impulse, CSM-107 SPS loaded lb, loaded SM/CM RCS propellant) stay as **parameters** — the scripts refuse to fill them.
- The README states plainly: "Simulation output is not a NASA fact," with an explicit "do not promote estimates" section forbidding copying output into a *shall*.
- Press Kit tank rows stay flagged `UNRECONCILED` rather than being forced into a closed mass budget.

`c023b66` and `8530c05` show the bot holding this line under pressure — adding the scripts *without* filling the unmarked blanks. For a model whose whole credibility rests on being citable, this restraint is the single most valuable behaviour in the range.

### 4. Honest scoping of the weakest project

`projects/humanity-optimization/` is demoted in its own summary to a "concept sketch, not a design baseline," with an explicit instruction that it be scored as a sketch. HOS was the part Grok praised most in May; downgrading it is the less flattering and more correct call.

### 5. Conflicting sources cited as conflicting

SPS thrust is carried as both 20,500 lbf (Press Kit) and 21,500 lbf vac (TN D-7375) rather than silently averaged or picked. Same for DPS. Planned-vs-flown GET is kept as three distinct labels for TLI. This is the right handling of a contested number, and it survived several rewrite passes (`fa814d8`, `eb73f37`, `505781a`).

---

## Defects found

### D-1 — The test suite overwrites 64 committed PNGs (confirmed)

**`tests/test_package.py:82-83`**

```python
def test_render_all_projects(self):
    self.assertEqual(render_all(ROOT / "projects"), 0)
```

`render_all` writes PNGs next to each view — into the working tree. Running `python3 -m unittest` therefore rewrites all 64 committed PNGs as a side effect. Verified on a clean checkout of `0e5921d`: after one test run, `git status` reported **64 of 64 PNGs modified, 0 non-PNG changes**.

The output is not byte-identical to what is committed:

| | md5 | bytes |
|---|---|---|
| Committed `apollo-bdd.png` | `191f3e63…` | 16,768 |
| Rendered here | `c0757500…` | 15,795 |

Two consecutive runs on this machine produced identical md5s, so the renderer is deterministic *per environment*. The divergence is environmental: `src/msml/render.py:29-33` resolves fonts by first hit in a fixed list — `/Library/Fonts/Arial.ttf`, then the macOS Supplemental path, then DejaVu, then Liberation. A Linux CI box lands on DejaVu; this Mac lands on Arial Supplemental; glyph metrics differ, so every box and line shifts.

Why this bites: `AGENTS.md` instructs every agent to run the test suite. Each one dirties 64 binary files, and the natural next move — `git add -A` — commits a font-driven re-render as if it were a diagram change. The ~1KB delta is invisible in review.

**Fix:** render into a temp directory in tests (`render_all(tmpdir)` or a `dest` parameter), leaving `msml-render-all projects` as the one explicit command that writes into the repo. If committed PNGs are meant to be reproducible artifacts, the font stack has to be pinned or bundled — first-hit-wins across four OS paths cannot produce stable bytes.

### D-2 — Binary churn is being written into history

287 PNG blob writes across only 65 distinct paths in these 93 commits; `.git` is already 15 MB for a project whose source is JSON and Markdown. The bot's "Apply X" / "Render X" commit pairing (`a60658b`+`d4f6bf4`, `ad50ce9`+`1dc1013`, and ~20 more) means every semantic edit ships a second commit of re-rendered binaries.

The pairing itself is good practice — it keeps meaning changes reviewable apart from pixels. The cost is that PNGs are versioned artifacts of a non-reproducible renderer (see D-1), so the repo accumulates weight that no one can diff. Worth deciding explicitly: either PNGs are build output (drop them from git, render in CI) or they are deliverables (pin the renderer so the bytes mean something). Right now they are treated as both.

### D-3 — Decision flip-flopping in the commit log

Four consecutive commits argue with themselves about one directory name:

```
512264c Lock starter path to template/new-project (singular)
a84ad68 Lock starter path to templates/new-project (plural)
f0375e0 Use template/new-project for the starter
0726162 Publish starter at templates/new-project and lock ElectricBike meaning
```

Singular → plural → singular → plural, each labeled "lock." The final state (`templates/`) is correct and matches `AGENTS.md`, so nothing is broken. But "lock" in this repo is a strong word — it appears throughout `AGENTS.md` to mean a decision that must not drift — and spending it four times on a reversal devalues it. A locked decision that changes twice was never locked; it was a draft.

---

## Observations, not defects

- **`AGENTS.md` is carrying a lot.** 74 lines, 10.5 KB, ~22 bullet locks spanning EN 15194 clauses, Apollo hardware serials, GET timings, and state-machine sequencing. It is dense but it is *test-bound*, which is what makes it survivable. The risk is that the prose and the assertions are two sources of the same truth and can disagree; `6e48c9c` ("Drop leftover 2200 kcal figure from AGENTS.md") is exactly that disagreement being cleaned up after the fact. Consider generating the lock list from the test names, or at minimum adding a test that the numbers quoted in `AGENTS.md` appear in the model.
- **The SysML2d twinning worked.** Repeated commits sync names and layout rules against specific SysML2d commits (`c081214` against `6aeab93`, `2f801e9` against `e0e45b2`). Cross-repo consistency by explicit commit reference is a sound pattern.
- **`projects/apollo/simulations/__pycache__/` exists locally** but is correctly untracked — `.gitignore` covers it, and `git ls-files` confirms only the nine source files are tracked.

---

## Verdict

The engineering is sound and the discipline around sourcing is better than most human-authored technical documentation. All three prescribed checks pass clean, the model/view architecture Grok proposed in May is fully realized, and the Apollo work refuses to invent facts under conditions where inventing them would have been easy and invisible.

**D-1 should be fixed before the next agent session**, because it silently corrupts the working tree for every contributor who follows `AGENTS.md`. D-2 deserves an explicit decision. D-3 is process hygiene.

Nothing here needs reverting.
