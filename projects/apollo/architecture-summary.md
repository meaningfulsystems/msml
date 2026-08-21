# Apollo Architecture Summary

Apollo is a full lunar-orbit-rendezvous example: Saturn V, Block II CSM, LM-5, crew, and the ground network for Apollo 11 (AS-506). Read it as a system-of-systems model. Numbers are from NASA primary sources; a few values (including an official CSM lunar Δv table) are intentionally left unmarked.

Namespace `Apollo`. File stem `apollo`. Civil / historical NASA architecture only. Apollo 7, 8, 10, and 13 appear as notes, not as separate projects (7 had no LM; 8 and 10 did not land; 13 aborted).

## Parts

The launch vehicle is Saturn V: S-IC, S-II, S-IVB, and the Instrument Unit, with F-1 engines on the first stage and separate J-2 engines on S-II and S-IVB.

The spacecraft is a Block II CSM (CM and SM) plus LM-5. The CM side keeps AGC_CM, the IMU, two DSKY units, EMS, SPS, RCS, and ECLSS. The LM keeps descent and ascent stages, AGC_LM with one DSKY, AGS (AEA + ASA + DEDA), DPS, APS, and the landing radars. The IU keeps LVDC, ST-124, and the flight control computer.

Crew is three parts: CDR, CMP, and LMP. The ground network is MCC-H, GSFC, MSFN, KSC LC-39, Recovery, and RSO/AFETR.

## Key numbers

These values are already on the model (A11 Press Kit p.109 tank loads and launch masses unless noted). Do not invent replacements.

| Item | Value |
| --- | --- |
| S-IC | 7,653,854 lbf / 5,022,674 lb fueled |
| S-II | 1,059,171 lb |
| S-IVB | 260,523 lb |
| IU | 4,306 lb |
| CM | 12,250 lb |
| SM | 51,243 lb |
| DPS | 18,100 lb |
| APS | 5,214 lb |
| RCS | SM/LM 100 lbf · CM 93 lbf |
| AGC ropes | Comanche 055 / Luminary 1A |
| AEA | 4096 × 18-bit words |

Cite **both** SPS figures: 20,500 lbf (PK) vs 21,500 lbf vac (TN D-7375). Cite **both** DPS figures: 9,870 / 1,050–6,300 lbf (PK) vs 10,500 lbf and 10:1 (TN D-7143). USB RF stays as sourced on the model. VHF is 296.8 / 259.7 MHz (CSM–LM–EVA) and 243.0 MHz recovery beacon.

Left unmarked on purpose: official CSM lunar Δv, CSM-107 SPS loaded lb, and loaded SM/CM RCS propellant mass.

## Mission STM

countdown → boost → earthOrbit → TLI → dockEject → translunar → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery.

`dockEject` is its own state. Do not draw TLI → translunar or dockEject → LOI, and do not put translunar before dockEject.

## Views in this folder

Every rendered figure that is actually here:

`apollo-pkg.png`, `apollo-bdd.png`, `apollo-ctx.png`, `apollo-ibd.png`, `apollo-stm.png`, `apollo-abort.png`, `apollo-act.png`, `apollo-seq.png`, `apollo-req.png`, `apollo-sat-bdd.png`, `apollo-sat-ibd.png`, `apollo-csm-bdd.png`, `apollo-csm.png`, `apollo-lm-bdd.png`, `apollo-lm.png`, `apollo-gnc-pkg.png`, `apollo-cmc-stm.png`, `apollo-lgc-stm.png`, `apollo-gnd-bdd.png`, `apollo-gnd.png`, `apollo-crew.png`, `apollo-usb.png`, `apollo-cmd.png`, `apollo-eclss.png`, `apollo-eclss-par.png`, `apollo-eps.png`, `apollo-ags-bdd.png`, `apollo-dock.png`, `apollo-rcs.png`.

| View | File |
| --- | --- |
| Packages | `apollo-pkg.png` |
| BDD | `apollo-bdd.png` |
| Context IBD | `apollo-ctx.png` |
| Stack IBD | `apollo-ibd.png` |
| Mission STM | `apollo-stm.png` |
| Abort STM | `apollo-abort.png` |
| Activity | `apollo-act.png` |
| Sequence | `apollo-seq.png` |
| Requirements | `apollo-req.png` |
| Saturn V | `apollo-sat-bdd.png` · `apollo-sat-ibd.png` |
| CSM | `apollo-csm-bdd.png` · `apollo-csm.png` |
| LM | `apollo-lm-bdd.png` · `apollo-lm.png` |
| GNC | `apollo-gnc-pkg.png` · `apollo-cmc-stm.png` · `apollo-lgc-stm.png` |
| Ground and crew | `apollo-gnd-bdd.png` · `apollo-gnd.png` · `apollo-crew.png` |
| Comms | `apollo-usb.png` · `apollo-cmd.png` |
| ECLSS | `apollo-eclss.png` · `apollo-eclss-par.png` |
| Electrical | `apollo-eps.png` |
| AGS | `apollo-ags-bdd.png` |
| Docking | `apollo-dock.png` |
| RCS | `apollo-rcs.png` |

Longer captions live in [README.md](README.md).

![Apollo mission STM](apollo-stm.png)

![Apollo block definitions](apollo-bdd.png)

![Apollo vehicle stack](apollo-ibd.png)

![Apollo context](apollo-ctx.png)

![Apollo CSM](apollo-csm.png)

![Apollo LM](apollo-lm.png)

![Apollo ground](apollo-gnd.png)

## Validate and render

```bash
msml-validate-all projects/apollo --strict
msml-render-all projects/apollo
```
