# Rebel Tech Theme Park

**Rebel Tech World** is a community creative project to design and build a playable, technology-themed amusement park in **Planet Coaster 1** on the Windows PC **Raven**.

> Status: planning / repository initialized. No game build, custom asset import, or automation test has been completed yet.

## Vision

An immersive technology-themed park inspired by Rebel Tech Oxford's **CONNECTING. INSTALLING. SOLVING.** identity: deep navy, red, white, illuminated circuits, robotics, networks, and server-room architecture. The goal is an actual playable park, not just renders, with working rides, paths, queues, shops, facilities, lighting, and scenery.

### Proposed districts

| District | Concept | Potential signature attraction |
| --- | --- | --- |
| **The Core** | Main gate, central promenade, towering data-center landmark | Server Crash coaster |
| **Overclock District** | CPUs, performance computing, neon cooling systems | The Overclock launched coaster |
| **Clanka Labs** | Robotics and automated factories | Fetchin' Clanka: Factory Escape dark ride |
| **Cyber City** | Gaming, terminals, arcades, digital infrastructure | Kernel Panic drop tower |
| **Power Grid** | Industrial power, electrical systems, kinetic energy | Energy-themed thrill attractions |
| **Signal Gardens** | Quieter landscaping and network-themed paths | Family rides and scenic areas |

Names, layout, and ride details are proposals subject to gameplay testing.

## Target environment

- **Game:** Planet Coaster 1 for Windows, sandbox mode.
- **Host PC:** Raven; verify actual hardware and installations before proceeding.
- **Workspace:** `D:\RebelTechWorld` to reduce use of C:; check capacity before setup. Game/system caches and saves may still occupy C:.
- **3D authoring:** Existing Blender installation, version and compatibility to be verified.
- **Custom scenery:** Planet Coaster's official Thememaker's Toolkit; validate its currently supported export/import workflow before automating.
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

- [ ] Connect to Raven with permission and inspect C:/D: available space, Planet Coaster, Blender, and build prerequisites.
- [ ] Create the local `D:\RebelTechWorld` workspace and Git clone.
- [ ] Confirm Thememaker's Toolkit process and create a test scenery object in Blender.
- [ ] Import the object into Planet Coaster; capture evidence of success.
- [ ] Test reproducible UI automation for a small entrance plaza.
- [ ] Save, close, reopen, and validate the first playable checkpoint.
- [ ] Create a measured construction roadmap for all districts.

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

Directories and files beyond this README are planned, not present yet.

## Agent collaboration

**ChatGPT, Claude, and Grokbot** may contribute via normal GitHub workflows when independently connected and granted access. Do not assume that another agent sees local changes or can access this repository automatically.

For every work session, document:
- What changed, by whom, and which commit or branch contains it.
- Screenshots, imports, tests, or save/reload evidence, as applicable.
- Outstanding blockers, relevant versions, and the next safe action.

**Preferred workflow:** create a focused branch for substantial changes, commit source and docs, request review, and merge after validation. The repository and Notion hub should tell the same story.

## Getting started

When Raven is available, the owner can say: **"ok I'm on my pc"** to resume the setup and validation workflow. Check authorized access before operating the machine or installing anything.

---
Rebel Tech Oxford — **CONNECTING. INSTALLING. SOLVING.**

This is an independent fan-made creative project, not affiliated with or endorsed by Frontier Developments or Planet Coaster.
