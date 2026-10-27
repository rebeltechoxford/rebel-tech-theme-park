# Rebel Tech World — Shared Agent Instructions
> **OWNER REVISION: THE REBEL GRID (2026-10-27).** The latest owner brief supersedes earlier tropical, grassy and cyan art direction: charcoal/navy grid city; RED #E10616, BLUE #244CFF, PURE WHITE #FFFFFF streetlights; no visible grass inside completed themed areas; original RT branding, custom facility shells and three matching workshop vans. Read [the current master plan](docs/REBEL_GRID_MASTERPLAN.md) and [validated offline asset kit](assets/pc2/rebel-grid-v1/README.md). Native billboard images are staged, but assigned in-game logos, custom vans and the new flagship coaster lineup are NOT verified complete. Respect active desktop coordination leases and preserve other agents' uncommitted work.

**ACTIVE GAME TARGET: Planet Coaster 2** (owner pivoted October 27, 2026). Review README.md, docs/PC2_PIPELINE.md and docs/BUILD_LOG.md before doing work.

## Mandatory custom-building requirement

Read [docs/CUSTOM_BUILDING_STANDARD.md](docs/CUSTOM_BUILDING_STANDARD.md) before any theming. Every visible building, station, queue hall, toilet, staff/utility and pool facility needs an original RT architectural composition. A recolored stock prefab, identical box with a different sign, or offline GLB render is not a finished building. Retain supported functional cores and native construction pieces, but replace or fully conceal default visible themed shells without obstructing real paths/doors/ride clearance. Use exact supplied logo artwork with appropriate red/navy/white contrast. Source-image inventory: [docs/RT_REFERENCE_MANIFEST.json](docs/RT_REFERENCE_MANIFEST.json). **Path, queue, exit and staff repairs stay first; prove guest arrival, boarding and return before expansion, and retest after theming.** Generated park concepts are never evidence of in-game completion.

## Raven and workspace
- Authorized PC: Raven, Windows 11 Pro; Desktop Commander when connected.
- Clone and build directory on D: drive: D:\RebelTechWorld\rebel-tech-theme-park.
- Blender 4.5.3 LTS was inspected and used successfully; Planet Coaster 1 is installed but is no longer our target.
- PC2 is installed; an original tropical sandbox park with working 8m guest boulevard and T-junction plus a CLOSED flat ride was built and saved in three separate checkpoints. Vanilla save/reload was verified.
- **Current request:** The game was cleanly QUIT on Raven. Keep PC2 **CLOSED** for offline research, scripts, documentation and Blender builds. Relaunch only when an actual in-game construction/validation task needs it.
- An original three-piece entrance scenery kit is published in `assets/pc2/entrance-kit-v0.1/`, Blender/GLB-tested OFFLINE but **not** imported into PC2.
- Preserve the existing gateway .blend, source code, and preview on D:; no deletion or destructive migration.

## PC2-specific approach
1. First confirm Planet Coaster 2 installation on Raven and launch a vanilla sandbox park.
2. Use the game's own creation tools and Frontier Workshop for official park/blueprint sharing.
3. PC1's Thememaker's Toolkit, ZIP packaging and .pcugc files are **legacy only**. Do not submit those to PC2.
4. Optional third-party KMods Converter claims BLEND/FBX/GLB-to-PC2 scenery support, using ACSE + ForgeUtils. Vet download provenance, compatibility, licensing, unsigned installer security, restore point/save backups before enabling. No silent mods installs.
5. For reuse, export just one gateway object with textures and sensible origin/scale. Six PC1 LOD meshes must not turn into six independent PC2 scenery objects.
6. Prove model renders and functions in the actual game before scaling to full districts.
7. Add the Cooling Loop water park district using PC2 pool/slide systems.

## Agent collaboration
- Use GitHub for source, scripts and reviewable commits; Notion for overall status and decisions. No Trello board unless later warranted.
- For every task, update docs/BUILD_LOG.md with date, author, changes, test evidence, blocker and next safe action.
- Mark concepts PROPOSED, generated assets EXPORTED, installed objects TESTED-IN-GAME, and only verified builds COMPLETE.
- Claude and Grokbot do not automatically have control of Raven or access to this GitHub repo; verify permissions.
- Do not publish machine-private details, credentials, Steam data, game binaries, proprietary saves or unlicensed Sketchfab models.
- Avoid undocumented game-save modifications, bypassing OS security warnings, or destructive installs.

## Current acceptance state
- COMPLETE: PC2 installed and launched; sandbox park saved/reloaded; guests use the entrance avenue; three independent game save checkpoints preserved and backed up on D:.
- COMPLETE, Blender-only: Gateway GLB and three entrance kit GLBs roundtrip-validated as original scenery model candidates.
- OPEN BLOCKER: built-in 360 Power flat ride CLOSED, missing connected queue and power (0/36); UI showed `Paths cannot cross`. Refer to [docs/RIDE_AND_UTILITIES_RUNBOOK.md](docs/RIDE_AND_UTILITIES_RUNBOOK.md) before the next game session.
- NOT ATTEMPTED: KMods/ACSE/ForgeUtils installation, PC2 custom model import or a completed powered ride. Do not claim completion without evidence.
- NEXT interactive milestone: functional ride with guests boarding, followed by a new named in-game save and a D: SHA-verified backup.

Project hub: https://app.notion.com/p/4066b61e436e8102931fe868f8ac2ee3?pvs=204
PC1 legacy notes: docs/TMT_PIPELINE.md