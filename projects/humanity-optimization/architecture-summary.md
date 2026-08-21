# Humanity Optimization System — Concept Sketch

This folder is an MSML **concept sketch**, not a design baseline. Namespace `HOS`. File stem `hos`. Red Team should score it as a sketch, not as architecture.

Civilization-scale language lives as aspiration in [Humanity_Optimization_System_Brief.md](Humanity_Optimization_System_Brief.md). The operational picture is [Humanity_Optimization_Operational_Concept.md](Humanity_Optimization_Operational_Concept.md). This file keeps the original nine section headings as a sketch frame. The twin examples (toaster, blender, e-bike, Apollo) use MagicGrid walkthrough headings. It does **not** invent biomedical or human-body claims, performance scores, population statistics, or shall-statements that are not on `hos-model.msml`.

## 1. Purpose / context

The model shows a socio-technical loop: observe, hold evidence, generate possible futures, screen against named constraint properties, evaluate portfolios, and emit a brief.

Properties on `HumanityOptimizationSystem` are `mission: CivilizationDecisionSupport`, `agencyConstraint: HumanAgencyPreservation`, and `objectiveSet: PluralHumanAndEcologicalGoals`. Those are labels on a sketch, not a certified mission.

## 2. System boundary and actors

**Inside the sketch:** HumanityOptimizationSystem, EvidenceRepository, Evidence and Models, ScenarioModel, InterventionEvaluator, EthicalConstraintGuard, DecisionBriefingInterface.

**Outside (context):** Humanity, DecisionMakers, EarthBiosphere, FutureGenerations, TechnologyResources, Governance System.

Context connectors on the model:

- EarthBiosphere `conditions` → HOS `worldSignals`
- FutureGenerations `protectedInterest` → HOS `futureInterest`
- Humanity `needsValues` → HOS `valuesIn`
- TechnologyResources `pathways` ↔ HOS `pathwayQuery`
- HOS `briefOut` → DecisionMakers `decisionBrief`

Governance System appears as a context block. It is not wired as a port on the context IBD.

There are no use-case or actor definitions. Decision makers are a block, not a SysML actor.

## 3. Requirements

This MSML HOS model has **no requirement definitions**. There are no requirement ids and no shall-statements on `hos-model.msml`.

Do **not** invent shalls for “humans decide” or for ethics fail-closed. Those phrases are not requirements here.

Properties that *are* on the model (qualitative labels only):

- HumanityOptimizationSystem: mission, agency constraint, plural objective set
- EthicalConstraintGuard: `constraints: AgencyTransparencyJusticeRule`, `protectedInterests: StakeholderInterest`
- DecisionBriefingInterface: `brief: DecisionBrief`, `explanation: TraceableRationale`
- EvidenceRepository: observations and assumptions
- ScenarioModel: possible futures and a confidence range
- InterventionEvaluator: portfolios and multi-objective gain

## 4. Structure and interfaces

HOS is composed of the evidence, scenario, evaluator, ethics, and briefing parts listed above. Ports on the system boundary are `worldSignals`, `futureInterest`, `valuesIn`, `pathwayQuery`, and `briefOut`.

The activity view is observe → model futures → screen ethics → evaluate interventions → brief. The sequence view is a decision-support exchange.

## 5. States and modes

None. There is no state machine on `hos-model.msml`.

## 6. Allocations (req → part)

None. There are no requirements to allocate.

## 7. Sourced numbers

None. Do not invent quantitative performance claims, population figures, or biomedical rates.

## 8. Open risks / TBD

- Sketch only — not a design baseline and not architecture to certify.
- No requirements, so agency and justice labels are not testable.
- No STM.
- Governance System is on the BDD and not connected on the context IBD.
- EthicalConstraintGuard has no IBD port into the evaluator; screening is an activity name only.
- Medical, physiological, and individual-body modeling are out of scope.

## 9. Views in this folder

`hos-context.png`, `hos-context-ibd.png`, `hos-operating-loop.png`, `hos-decision-support-sequence.png`.

![HOS context](hos-context-ibd.png)

```bash
msml-validate-all projects/humanity-optimization --strict
msml-render-all projects/humanity-optimization
```
