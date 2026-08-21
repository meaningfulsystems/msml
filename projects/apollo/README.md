# Apollo (in progress)

Public NASA **Apollo 11 / Block II** instance on the generic Saturn V + CSM + LM stack. Civil / historical architecture only — no classified or biomedical detail.

Namespace `Apollo`. File stem `apollo`. Layout is `projects/apollo/` (not `examples/`).

The research brief is still incoming. This is a defensible skeleton so the stack, context, mission phases, GNC, CSM flows, and landing sequence can be refined when more detail arrives.

**Where 11 is atypical (notes only — not full examples):**

- Apollo 7 — no LM
- Apollo 8 / 10 — no lunar landing
- Apollo 13 — abort, not a completed landing

Do not stand up those missions as separate projects.

| View | File | Story |
| --- | --- | --- |
| Packages | `apollo-pkg` | LaunchVehicle, Spacecraft, CrewECLSS, GNC, Ground, Comms, Mission |
| BDD | `apollo-bdd` | Saturn V + CSM + LM + LES + SLA; instance and atypical notes |
| Context IBD | `apollo-ctx` | Vehicle / crew / MCC / RTCC / MSFN / Moon / Earth; uplink, downlink, backup voice |
| Internal IBD | `apollo-ibd` | Saturn stack joints (adjacent only; lines never through boxes) |
| STM | `apollo-stm` | Launch → TLI → LOI → Landing → Ascent → TEI → Entry + abort |
| Activity | `apollo-act` | Same phases as a start-to-entry flow |
| Sequence | `apollo-seq` | Landing: MCC → MSFN → USB → LGC / crew → descent |
| Requirements | `apollo-req` | Crew safety, landing, comms continuity, LES, ECLSS, guidance |
| GNC IBD | `apollo-gnc` | Crew–DSKY–AGC–IMU–Optics + LGC–AGS (P00–P67-class) |
| CSM IBD | `apollo-csm` | Electrical, propellant, RF, cabin atmosphere, telemetry |

Parts in the model include S-IC, S-II, S-IVB, IU, CSM (CM, SM), LM (descent, ascent), LES, SLA, crew, ECLSS, AGC, LGC, AGS, IMU, DSKY, optics, MCC, RTCC, MSFN, USB, backup voice, fuel cells, and ground computers.
