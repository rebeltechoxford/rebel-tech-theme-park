# Rebel Tech World — Phased Park Build

**Active game:** Planet Coaster 2 on Raven. **Current run-state:** game CLOSED at the owner's request. Do not relaunch until interactive work is needed. All large work products go on D:.

## Design rules
- Brand: navy, red, brushed steel, white and cyan data-line accents; CONNECTING. INSTALLING. SOLVING.
- Playability before complexity: every ride needs access, power, guests and save/reload proof.
- Original geometry only by default; third-party Sketchfab assets need an appropriate license and attribution.
- Treat the PC1 TMT ZIP and .pcugc files as legacy; standalone Blender/GLB candidates are **not** yet installed into PC2.
- PC2 normal blueprints and Workshop use Frontier's built-in systems; optional community converter use is a separate security/compatibility decision.
- Raven's GTX 1060 6GB / 16GB RAM is limited relative to ambitions for a giant park: use benchmark checkpoints, not a giant initial mass-import.
- Source and scripts in GitHub, checkpoints in local ignored D: backups, statuses and decisions in Notion.

## Current plan — district order
1. **The Core / Gate:** keep the central 8m guest boulevard and T-junction. Add lighting, branded pylons, entrance plaza, restroom and basic services. Existing modular Gateway sign is an OFFLINE model candidate.
2. **Power Grid / first operational ride:** power the existing 360 Power, fix queue geometry, and verify guest boarding.
3. **Overclock:** functional launched coaster, optimized layout and careful pathing.
4. **Clanka Labs:** robot-factory scenery and a family ride.
5. **Cyber City:** arcade, drop ride, and smaller food/shops; connect utilities.
6. **Signal Gardens:** quieter family area with foliage, shade and facilities.
7. **Cooling Loop:** PC2's pools, flumes and lazy river with a dedicated water treatment system and lifeguards.

## Deliverables by stage
| Stage | Stop condition |
| --- | --- |
| 0 — already complete | PC2 installed; vanilla sandbox saved/reloaded; three separated game save checkpoints; entrance path and first flat ride placed; safe desktop controller |
| 1 — next interactive | 360 Power powered, queue connected, open; D: verified backup |
| 2 — offline/current | Expand original modular entrance scenery kit in Blender; GLB round-trip and asset-manifest checks; no PC2 mod installation |
| 3 — optional | Evaluate PC2 custom converter provenance/version/security/rights; only test one model if user accepts mod dependency |
| 4 — in-game | Build first finished themed plaza, shops, toilets, power distribution and lighting; park operational checkpoint |
| 5+ | Other districts, coasters, waterpark and measured simulation performance |

## Park-wide quality gates
- Each asset has a license/author record, a reproducible source script, triangle/material/size counts and a GLB or .blend offline validation.
- Each game save is a named in-game checkpoint and an independently hashed copy on D:. Never overwrite a known-good checkpoint.
- Each active ride must have paths, queue, exit, power, staff if needed and observed guests.
- Every session closes PC2 normally when the owner requests it; do not leave the game consuming GPU/RAM unnecessarily.
- No Trello board unless complexity increases substantially.

## Restore point paths
- Repository: `D:\RebelTechWorld\rebel-tech-theme-park`
- Original sandbox: `build\backups\pc2\2026-10-27-initial-sandbox`
- Entrance path: `build\backups\pc2\2026-10-27-entrance-01`
- Built-in 360 Power: `build\backups\pc2\2026-10-27-ride-test-02`

Do not put actual .park2 files, private game-account identifiers or account tokens in public GitHub.
