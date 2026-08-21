# Humanity Optimization System Architecture Summary

Civilization-scale decision-support concept. Namespace `HOS`. File stem `hos`. The model is a socio-technical loop: observe, model futures, screen ethics, evaluate interventions, brief human decision makers.

Longer prose lives in [Humanity_Optimization_System_Brief.md](Humanity_Optimization_System_Brief.md) and [Humanity_Optimization_Operational_Concept.md](Humanity_Optimization_Operational_Concept.md).

## Parts

HumanityOptimizationSystem with DecisionBriefingInterface, DecisionMakers, EarthBiosphere, EthicalConstraintGuard, EvidenceRepository, FutureGenerations, Governance System, and Humanity.

## Key numbers

HOS is a concept model. Do not invent quantitative performance claims that are not on `hos-model.msml`.

## Views

| View | File | Story |
| --- | --- | --- |
| Context BDD | `hos-context` | System in its environment |
| Context IBD | `hos-context-ibd` | External exchanges |
| Activity | `hos-operating-loop` | Observe → model → evaluate → brief |
| Sequence | `hos-decision-support-sequence` | Decision-support exchange |

![HOS context](hos-context-ibd.png)

## Validate and render

```bash
msml-validate-all projects/humanity-optimization --strict
msml-render-all projects/humanity-optimization
```
