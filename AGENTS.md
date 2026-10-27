# Rebel Tech World — Shared Agent Instructions

**ACTIVE GAME TARGET: Planet Coaster 2** (owner pivoted October 27, 2026). Review README.md, docs/PC2_PIPELINE.md and docs/BUILD_LOG.md before doing work.

## Raven and workspace
- Authorized PC: Raven, Windows 11 Pro; Desktop Commander when connected.
- Clone and build directory on D: drive: D:\RebelTechWorld\rebel-tech-theme-park.
- Blender 4.5.3 LTS was inspected and used successfully; Planet Coaster 1 is installed but is no longer our target.
- Planet Coaster 2 purchase/install was still underway at last check; do not claim PC2 has run or any custom assets work in-game until tested.
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

## First acceptance test
- PC2 installed and running.
- A minimal vanilla park opens, saves and reloads.
- Gateway source adapted and exported as one standalone object.
- Third-party converter vetted before optional installation.
- Model appears in-game with correct orientation, scale, textures, and saves/reloads if approved.

Project hub: https://app.notion.com/p/4066b61e436e8102931fe868f8ac2ee3?pvs=204
PC1 legacy notes: docs/TMT_PIPELINE.md