# Rebel Tech World — Planet Coaster 2

**Rebel Tech World** is a community creative project to design and build a playable, technology-themed amusement park in **Planet Coaster 2** on the Windows PC **Raven**.

> **Active project (2026-10-27): Planet Coaster 2.** The owner pivoted from PC1 during purchase. The earlier Blender gateway prototype is preserved, but was designed around the **PC1** Toolkit format; no model has been imported into PC2 and no playable PC2 save exists yet.

## Vision

An immersive technology-themed park inspired by Rebel Tech Oxford's **CONNECTING. INSTALLING. SOLVING.** identity: deep navy, red, white, illuminated circuits, robotics, networks, and server-room architecture. The goal is an actual playable park, not just renders, with working rides, paths, queues, shops, facilities, lighting, and scenery.

### First prototype: Rebel Tech World Gateway

![Blender render of the first Rebel Tech World Gateway scenery prototype](docs/images/gateway-v0.1.jpg)

*Original procedural Blender preview from the PC1 prototype. Its geometry and source assets can be adapted for PC2, but the old Toolkit ZIP is not a PC2 package. This is not an in-game screenshot.*

### Proposed districts

| District | Concept | Potential signature attraction |
| --- | --- | --- |
| **The Core** | Main gate, central promenade, towering data-center landmark | Server Crash coaster |
| **Overclock District** | CPUs, performance computing, neon cooling systems | The Overclock launched coaster |
| **Clanka Labs** | Robotics and automated factories | Fetchin' Clanka: Factory Escape dark ride |
| **Cyber City** | Gaming, terminals, arcades, digital infrastructure | Kernel Panic drop tower |
| **Power Grid** | Industrial power, electrical systems, kinetic energy | Energy-themed thrill attractions |
| **Signal Gardens** | Quieter landscaping and network-themed paths | Family rides and scenic areas |
| **Cooling Loop** | PC2 water park, pools, slides and liquid cooling theme | Cooling tower flumes and lazy river |

Names, layout, and ride details are proposals subject to gameplay testing.

## Target environment

- **Game:** **Planet Coaster 2** for Windows, sandbox mode. Purchase/install underway; not yet confirmed running on Raven.
- **Host PC:** Raven; Windows 11 Pro, inspected October 27, 2026.
- **Workspace:** `D:\RebelTechWorld` to reduce use of C:; check capacity before setup. Game/system caches and saves may still occupy C:.
- **3D authoring:** Blender 4.5.3 LTS confirmed. Preserve old gateway source and adapt a standalone model for PC2.
- **Official content sharing:** PC2 uses Frontier Workshop for built-in blueprints and parks. PC1's Thememaker's Toolkit and .pcugc pipeline are **legacy only**. For custom model imports, evaluate optional third-party KMods Converter with ACSE/ForgeUtils after version/security review and save backups; see [PC2 pipeline](docs/PC2_PIPELINE.md).
- **Automation:** Authorized local desktop controls and deterministic scripts where practical; screenshot-driven inspection and manual checkpoints.
- **Knowledge hub:** [Rebel Tech World — Notion project hub](https://app.notion.com/p/4066b61e436e8102931fe868f8ac2ee3?pvs=204).

## Project principles

1. **Playable first.** Favor working rides and safe guest navigation over impressive but nonfunctional mockups.
2. **Validate the pipeline.** Build and import one small custom scenery piece before designing dozens.
3. **Checkpoints and backups.** Save, reload, and verify incremental builds; don't alter undocumented proprietary save formats.
4. **Reproducible construction.** Keep source assets, scripts, documented dependencies, and build procedures under version control.
5. **Protect disk space.** Keep large temporary exports on D: when configurable; do not commit installed game files or Steam assets.
6. **Measured automation.** Prove mouse/keyboard control before assuming unattended construction is feasible.
7. **Evidence over claims.** Label designs as proposed, work as in-progress, and tests as passed only once verified.

## Initial milestones

- [x] Connect to Raven with permission and inspect C:/D: available space, Planet Coaster, Blender, and build prerequisites. (C: 22.6 GiB free; D: 316.7 GiB free.)
- [x] Create the local `D:\RebelTechWorld` workspace and Git clone.
- [x] Create original scenery in Blender; export and verify **PC1-format** FBX/ZIP offline (retained solely as reusable source).
- [ ] Install and launch **Planet Coaster 2** on Raven; save/reload a vanilla sandbox park.
- [ ] Produce one single-object Blender/GLB/FBX gateway asset appropriate for PC2.
- [ ] Review optional community KMods Converter / ACSE / ForgeUtils for security, game-version compatibility and backups; test custom scenery only if approved.
- [ ] Test reproducible UI automation for a small entrance plaza.
- [ ] Save, close, reopen, and validate the first playable checkpoint.
- [ ] Create a measured construction roadmap for all districts, including **Cooling Loop** waterpark.

## Planned repository structure

```text
rebel-tech-theme-park/
├── README.md
├── AGENTS.md             # Agent coordination and safety conventions
├── docs/                 # Architecture, runbooks, park layout, build log
├── scripts/              # Reproducible local automation / export helpers
├── blender/              # Editable original Blender source assets
├── assets/               # Original, license-safe asset inputs
└── .gitignore            # Local caches, saves, exports and secrets
```

The source Blender generator, offline validator, Windows preflight script, agent instructions, **PC2 pipeline**, PC1 legacy Toolkit runbook, and build log now exist. Further project folders are added as needed.

## Agent collaboration

**ChatGPT, Claude, and Grokbot** may contribute via normal GitHub workflows when independently connected and granted access. Do not assume that another agent sees local changes or can access this repository automatically.

For every work session, document:
- What changed, by whom, and which commit or branch contains it.
- Screenshots, imports, tests, or save/reload evidence, as applicable.
- Outstanding blockers, relevant versions, and the next safe action.

**Preferred workflow:** create a focused branch for substantial changes, commit source and docs, request review, and merge after validation. The repository and Notion hub should tell the same story.

## Important: PC1 legacy work

The prior `docs/TMT_PIPELINE.md` and scripts creating `.pcugc` upload ZIPs were made for PC1 and remain as historical/reference work. **Do not run a PC1 Toolkit conversion as part of the active PC2 setup.** The original Blender gateway geometry and preview remain useful.

## Getting started

When Raven is available, the owner can say: **"ok I'm on my pc"** to resume the setup and validation workflow. Check authorized access before operating the machine or installing anything.

---
Rebel Tech Oxford — **CONNECTING. INSTALLING. SOLVING.**

This is an independent fan-made creative project, not affiliated with or endorsed by Frontier Developments or Planet Coaster.
