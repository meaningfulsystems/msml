# Humanity Optimization System — Architecture / System Design

Civilization-scale decision-support concept. Namespace `HOS`. File stem `hos`. This note is the design argument for the model in this folder, not a catalog of pictures.

Longer prose lives in [Humanity_Optimization_System_Brief.md](Humanity_Optimization_System_Brief.md) and [Humanity_Optimization_Operational_Concept.md](Humanity_Optimization_Operational_Concept.md). This file follows the same section structure as the other examples. It does **not** invent biomedical or human-body claims, performance scores, or population statistics that are not on `hos-model.msml`.

## 1. Purpose / context

HOS is a socio-technical loop: observe the world, hold evidence and models, generate possible futures, screen interventions against ethical constraints, evaluate portfolios, and brief human decision makers.

The system does not replace human judgment. The mission on the model is `CivilizationDecisionSupport` with `agencyConstraint: HumanAgencyPreservation` and `objectiveSet: PluralHumanAndEcologicalGoals`. The goal is better human decisions about coupled Earth-scale questions (resources, biosphere, technology, governance, future generations) — not automated control of people or bodies.

## 2. System boundary and actors

**Inside HOS:** HumanityOptimizationSystem, EvidenceRepository, Evidence and Models, ScenarioModel, InterventionEvaluator, EthicalConstraintGuard, DecisionBriefingInterface.

**Outside (context):** Humanity, DecisionMakers, EarthBiosphere, FutureGenerations, TechnologyResources, Governance System.

Context connectors:

- EarthBiosphere `conditions` → HOS `worldSignals` (conditions and warning signals)
- FutureGenerations `protectedInterest` → HOS `futureInterest`
- Humanity `needsValues` → HOS `valuesIn` (needs, values, lived experience)
- TechnologyResources `pathways` ↔ HOS `pathwayQuery` (pathways, resources, constraints)
- HOS `briefOut` → DecisionMakers `decisionBrief`

Governance System appears as a context block. It is not wired as a port on the context IBD.

There are no use-case or actor definitions on this model. Decision makers are a block, not a SysML actor.

## 3. Requirements

This MSML HOS model has **no requirement definitions**. There are no requirement ids or shall-statements on `hos-model.msml`.

Design properties that *are* on the model (qualitative, not numeric targets):

- HumanityOptimizationSystem: mission, agency constraint, plural objective set
- EthicalConstraintGuard: `constraints: AgencyTransparencyJusticeRule`, `protectedInterests: StakeholderInterest`
- DecisionBriefingInterface: `brief: DecisionBrief`, `explanation: TraceableRationale`
- EvidenceRepository: observations and assumptions
- ScenarioModel: possible futures and a confidence range
- InterventionEvaluator: portfolios and multi-objective gain

Do not invent mortality, physiology, or clinical performance requirements.

## 4. Structure and interfaces

HOS is composed of the evidence, scenario, evaluator, ethics, and briefing parts listed above. Ports on the system boundary are `worldSignals`, `futureInterest`, `valuesIn`, `pathwayQuery`, and `briefOut`.

The operating loop (activity) is observe → model futures → screen ethics → evaluate interventions → brief. The sequence view is a decision-support exchange, not a command-and-control uplink.

## 5. States and modes

None. There is no state machine on `hos-model.msml`. Modes such as “crisis” or “steady stewardship” are not defined and are not invented here.

## 6. Allocations (req → part)

None. Until requirements exist, there is nothing to allocate to EvidenceRepository, EthicalConstraintGuard, or DecisionBriefingInterface.

Intended responsibility (not formal `allocate` edges): evidence stays in the repository; futures stay in ScenarioModel; portfolio comparison stays in InterventionEvaluator; hard constraints stay in EthicalConstraintGuard; the only output to people is a traceable brief.

## 7. Sourced numbers

None. HOS is a concept model. Do not invent quantitative performance claims, population figures, or biomedical rates.

## 8. Open risks / TBD

- No requirements, so agency preservation and justice rules are properties, not testable shalls.
- No STM, so degraded or contested-governance modes are unspecified.
- Governance System is on the BDD and not connected on the context IBD.
- EthicalConstraintGuard has no interface into the evaluator on the IBD — screening is visible on the activity, not as a port.
- Scope is decision support. Medical, physiological, and individual-body modeling are out of scope.

## 9. Views in this folder

`hos-context.png`, `hos-context-ibd.png`, `hos-operating-loop.png`, `hos-decision-support-sequence.png`.

![HOS context](hos-context-ibd.png)

```bash
msml-validate-all projects/humanity-optimization --strict
msml-render-all projects/humanity-optimization
```
