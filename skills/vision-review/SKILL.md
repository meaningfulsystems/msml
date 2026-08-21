---
name: vision-review
description: Inspect every rendered PNG with vision before commit. Use after msml-render or msml-render-all, and before a public or PR screenshot lands.
---

# Vision-review MSML figures

Open each PNG with a vision-capable read. Do not trust coordinates alone. The Friday bar is publication quality: a reader must understand the system from the picture, and the picture must look good enough to announce.

## When to use

- After `msml-render` or `msml-render-all`.
- Before committing PNGs or updating a PR that embeds screenshots.

## Hard rule (via SysML2d)

**Connections never pass over boxes.** A connector, association, transition, or control flow must not cut through a block, part, state, use-case oval, or requirement box.

Hop-overs are only for **line-on-line** crossings. If two lines must cross, that is allowed; if a line crosses a box, reroute the waypoints.

IBD is the highest visual priority. Ports must not sit under connectors.

## Also fail the review for

- Overlapping labels (transition names on state borders, «include» on an oval).
- Leftover canvas (large empty band after the last node or last message).
- Low contrast (gray-on-gray text, thin light lines on a light fill).
- Unreadable STM pairs (Off↔Standby drawn as a tight double arrow). Keep two separate paths. E-bike `resetFault` must read Fault→Off.
- Cramped compartments (property text clipped by the box).
- Merged meaning on one line (command and charge sharing one inbound connector).
- Context mistakes on the e-bike: only rider / charger / ElectricBike / road. Wheel Torque is not an actor.
- Requirement trees that hang Range / Assist Limit / Charge Safety off Ride Safety, or hang Display / Structural off Range / Assist Limit.

## How to review

1. List every `.msmd` you touched and confirm a matching `.png` exists and is non-empty.
2. Read each PNG with vision. For each figure, answer: what system story does this picture tell, and what is ugly?
3. Fix the `.msmd` (sometimes the `.msml` name/display_name). Re-render that file.
4. Re-inspect the changed PNGs. Repeat until the hard rule holds.
5. Then commit the PNGs with the source.

## E-bike meaning locks (do not “fix” these away)

- Ride «include» Adjust Assist (ride includes adjust). Rider on Ride + Adjust; Charger on Charge only — never Charger on Adjust Assist.
- Requirements are siblings under the bike. Walk and 250 W stay siblings; do not hang them under Assist Limit.
- STM `resetFault` is Fault→Off. Standby —powerOff→ Off. Charging from Off only (EPAC choice on a note or do-behavior; state name is `charging`). No Standby→Charging. IBD has no rider/charger/road; charge is charger → bms → pack.
- INT/BDD call the motor Rear Geared Hub, not Hub Motor.

## Sibling note

SysML2d reviews SVG; MSML reviews PNG. The visual bar is the same. The files are not interchangeable.