# Apollo (in progress)

Public NASA **Apollo 11-class** system model. Civil / historical architecture only — no classified or biomedical detail.

Namespace `Apollo`. File stem `apollo`. Layout is `projects/apollo/` (not `examples/`).

The research brief is still incoming. This is a defensible skeleton so the stack, context, mission phases, and landing sequence can be refined when more detail arrives.

| View | File | Story |
| --- | --- | --- |
| Packages | `apollo-pkg` | LaunchVehicle, Spacecraft, CrewECLSS, GNC, Ground, Comms, Mission |
| BDD | `apollo-bdd` | Saturn V + CSM + LM + LES + SLA |
| Context IBD | `apollo-ctx` | Vehicle / crew / MCC / MSFN / Moon / Earth |
| Internal IBD | `apollo-ibd` | Saturn stack joints (adjacent only; lines never through boxes) |
| STM | `apollo-stm` | Launch → TLI → LOI → Landing → Ascent → TEI → Entry |
| Activity | `apollo-act` | Same phases as a start-to-entry flow |
| Sequence | `apollo-seq` | Landing: MCC → MSFN → USB → LGC / crew → descent |
| Requirements | `apollo-req` | Crew safety, landing, comms continuity, LES, ECLSS, guidance |

Parts in the model include S-IC, S-II, S-IVB, IU, CSM (CM, SM), LM (descent, ascent), LES, SLA, crew, AGC, LGC, AGS, IMU, DSKY, MCC, MSFN, USB, and ground computers.