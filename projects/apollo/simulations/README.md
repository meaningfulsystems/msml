# Apollo simulations (estimates only)

These Python scripts are **educational**. They help a student see how a missing number moves when an input changes. They are **not** sources.

**Simulation output is not a NASA fact.**

## Do not promote estimates

- Never copy a printed number into `architecture-summary.md` as a requirement or a filled blank.
- Never turn an estimate into a *shall*.
- Never fill the teaching-note blanks from these scripts: official CSM lunar change-in-velocity table, CSM-107 Service Propulsion System (SPS) loaded mass, loaded Service Module / Command Module Reaction Control System (RCS) propellant.
- If a line is labeled `ESTIMATE`, treat it as homework, not as a citation.

The architecture notes stay unmarked on those values on purpose.

## What they use

Scripts read numbers that are already on `../apollo-model.msml` (Apollo 11 Press Kit p.109 masses and tank loads, Press Kit RCS thrust, both SPS thrust citations, LM RCS 604 lb, Block II SPS oxidizer-to-fuel ratio 1.6). Those Press Kit tank rows stay **UNRECONCILED**: they are not a closed mass budget.

If the model leaves a value **UNKNOWN** — specific impulse, CSM-107 SPS loaded pounds, SM/CM RCS loaded pounds, SLA mass, SA-507 or SP-4029 tank/mass figures — the script keeps it as a **parameter**. It does not invent an Apollo number and it does not invent a citation.

Every printed result is a **range** or a sensitivity, never a single “true” mission number. Every printed result is labeled `ESTIMATE`.

## Scripts

1. `estimate_delta_v.py` — rocket-equation change in velocity from published wet/dry masses. Specific impulse is a parameter (not on the model).
2. `estimate_sps_load.py` — how SPS change in velocity and burn time move if you supply a load. CSM-107 SPS loaded pounds stay UNKNOWN unless you pass them.
3. `estimate_rcs.py` — LM RCS 604 lb is sourced; SM/CM loads are parameters.
4. `estimate_stack_mass.py` — adds Press Kit rows and compares them to the published ignition and first-motion masses. They do not close. Optional SA-507 / SP-4029 columns are parameters; the script will not force sources to agree.

`run_all.py` runs the four scripts with no extra arguments (sourced inputs only; unknowns stay parameters).

## How to run

From the repository root:

```bash
python3 projects/apollo/simulations/run_all.py
python3 projects/apollo/simulations/estimate_delta_v.py --isp-s 260 --isp-s 305
python3 projects/apollo/simulations/estimate_sps_load.py --sps-load-lb 20000 --sps-load-lb 40000 --isp-s 300 --isp-s 314
python3 projects/apollo/simulations/estimate_rcs.py --sm-load-lb 1000 --cm-load-lb 200 --isp-s 280
python3 projects/apollo/simulations/estimate_stack_mass.py
```

`--isp-s` values you type are **parameters**, not Apollo specific-impulse citations.

`g0 = 32.174 ft/s²` is standard gravity (the usual English-unit convention for specific impulse). It is not an Apollo measurement.

## Why the rocket equation

A trajectory integration would need gravity loss, steering, atmosphere, and many masses the model does not have. Those would be invented numbers. Rocket-equation sensitivity is enough to show a range from the published masses and from the parameters you choose to leave open.
