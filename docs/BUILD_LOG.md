# Rebel Tech World — Build Log

## 2026-10-27 — Planning & starter pipeline
- **Owner authorization:** set up Planet Coaster 1 project on Raven, use D: for working files, download trustworthy dependencies, coordinate GitHub/Notion; Sketchfab account available later.
- **Confirmed:** \`rebeltechoxford/rebel-tech-theme-park\` created, initial README committed; Notion hub exists.
- **Blocker:** Raven appears OFFLINE through the authorized Desktop Commander device list; no remote disk inspection or software installation has been performed.
- **Research:** Frontier's Thememaker's Toolkit accepts FBX + PNG textures + icon ZIP and returns \`.pcugc\`; requires six LODs and per-asset limits (see docs/TMT_PIPELINE.md).
- **Prepared:** agent rules, import runbook, read-only Windows preflight, initial Blender source prototype (still to be validated).
- **Next:** reconnect Raven; inspect C:/D:, locate Blender/Planet Coaster; run preflight and try a Blender build of the first test sign.
- **Evidence to capture:** Blender version, source export manifest, Toolkit build status, in-game screenshot, save/reload result. Don't upload private paths or account details.

## 2026-10-27 — Raven connected, first procedural scenery exported
- **Verified online:** Raven (Windows 11 Pro), C: 22.6 GiB free, D: 316.7 GiB free; Planet Coaster 1 on D:, Blender 4.5.3 LTS and Git available.
- **Created workspace:** `D:\RebelTechWorld\rebel-tech-theme-park`, cloned from GitHub.
- **Implemented:** `blender/create_gateway.py` procedural Rebel Tech World Gateway sign using original geometry, navy/red/white/steel/cyan materials and six LOD meshes.
- **Execution evidence:** Blender produced `ASSET_BUILD_SUCCESS` after fixing an FBX export selection bug. LOD triangle counts: 6520, 5432, 5332, 108, 48, 36. FBX, .blend source, PNG textures, icon, preview and ZIP are in ignored `build/` on D:.
- **NOT YET VERIFIED:** Frontier Toolkit conversion, in-game placement, appearance, save/reload. Steam sign-in may require user interaction.
- **Next:** visually inspect preview, validate the upload ZIP with the official Toolkit, and import .pcugc into Planet Coaster. Keep generated binaries and local paths out of public Git.

## 2026-10-27 — Offline export acceptance checks completed
- **Validation:** Blender 4.5.3 LTS clean-scene FBX round-trip passed using `blender/validate_gateway.py`, including 6 correctly named LOD meshes, progressively decreasing triangle counts (6520 / 5432 / 5332 / 108 / 48 / 36), five named materials, valid UV layers, and dimensions **7.55 × 0.86 × 5.54 meters**.
- **Packaging:** The Thememaker's Toolkit candidate ZIP passed local integrity and root-file checks. ZIP size **614,931 bytes**. Exported using Raven's existing Blender installation, with no extra software installation.
- **Preview:** `docs/images/gateway-v0.1.jpg` committed to GitHub as a visual prototype. Render is not an in-game screenshot.
- **Constraints:** Only Blender 2.79 is explicitly on Frontier's historical tested-version list. Blender 4.5 export has NOT yet been accepted/rejected by Frontier's conversion service.
- **Blocked acceptance test:** Owner-authorized Steam sign-in on Frontier's website, upload ZIP + preview, download compiled `.pcugc`, move to Planet Coaster TMT folder, place in-game and save/reload.

## 2026-10-27 — Repeatability and game-control preparation
- **Build repeatability:** `scripts/build_gateway.ps1` was executed on Raven and successfully regenerated the Blender source, FBX, textures, Toolkit upload ZIP, preview, and OFFLINE validation report from a clean background Blender session.
- **Local automation environment:** isolated Python virtual environment at `D:\RebelTechWorld\.venv`; installed `mss 10.2.0` to enable window-only screenshot testing without using C: for project packages.
- **Read-only GUI probe:** `scripts/game_window_probe.py` tested and reported `GAME_NOT_RUNNING`, consistent with Planet Coaster not being launched yet. No screenshots, clicks, gameplay or GUI construction were executed.
- **Owner handoff:** `scripts/open_toolkit_upload.ps1` launched the official Frontier website and the local ZIP/preview folder on Raven. Steam sign-in/online conversion is still outstanding.
- **Disk check after setup:** C: 22.51 GiB free; D: 316.68 GiB free.
- **Next:** complete Toolkit conversion and in-game save/reload test, then investigate supervised automation after the game is running.

## 2026-10-27 — Owner pivots to Planet Coaster 2
- **Decision:** owner is purchasing Planet Coaster 2 and has ended the PC1-specific import plan. Preserve PC1 prototype geometry as reusable source, but stop PC1 Toolkit conversion.
- **Raven status:** still online; no PC2 folder found in checked common Steam locations yet (installation may be underway). No PC2 game, sandbox park or custom scenery has been tested.
- **PC2 capabilities:** built-in coasters, scenery, parks and waterpark rides; Frontier Workshop supports in-game shared blueprints. Add proposed **Cooling Loop** water district.
- **Custom models:** third-party **KMods Converter** claims support for Blender/FBX/GLB to PC2 scenery packs, dependent on ACSE/ForgeUtils. Installer is unsigned; no such mod has been installed or trusted automatically.
- **Document updates:** README.md and AGENTS.md updated for PC2. New docs/PC2_PIPELINE.md describes vanilla-first plan and optional mod risk gate. PC1 docs/TMT_PIPELINE.md archived conceptually without deleting it.
- **Next:** confirm PC2 is installed on Raven, test a vanilla sandbox save and load, then adapt original gateway into a single-object Blender/GLB source candidate. Only consider mod installation after a safety/compatibility check.

## 2026-10-27 — PC2 Gateway GLB source candidate exported on Raven
- **New generator:** blender/prepare_pc2_gateway.py extracts just the original highest-detail Gateway mesh (not 6 duplicated LOD objects), reloads/packs source PNGs, and exports an embedded GLB and cleaned .blend under ignored build/pc2/ on D:.
- **Validation:** PC2_GATEWAY_EXPORT_PASS in Blender 4.5.3 LTS after independent clean-scene GLB import. Exactly one mesh, 6,520 triangles, UVs, five materials; bounds 7.55 × 0.86 × 5.54m. GLB 265,936 bytes.
- **Troubleshooting:** Blender images load lazily on reopen, so source textures were explicitly reloaded and pixel arrays touched before packing. That fixed the initial unsuccessful validation runs.
- **Not yet accomplished:** PC2 actual game launch, KMods/ACSE/ForgeUtils mod installation, converted scenery, park save, or in-game screenshot. Model import and workshop sharing are unverified.
- **Next:** confirm game installation when purchase/download is complete; test unmodified sandbox save/reload before considering a modded scenery test.

## 2026-10-27 — PC2 install status and performance baseline
- **Steam state when checked:** D:\SteamLibrary\steamapps\common\Planet Coaster 2 directory was created; Steam appmanifest_2688950.acf exists but the game folder contained no EXE/data files yet.
- **Reported by Steam manifest at inspection:** BytesToDownload ~13,900,636,080; BytesDownloaded 0; game installation is **not yet complete**. Do not attempt game launch until Steam finishes.
- **Raven hardware:** Intel Core i7-9700K (8 cores), NVIDIA GeForce GTX 1060 6GB, ~16GB RAM. PC2's official listed minimum includes a GTX 1060 (6GB VRAM) and 16GB RAM, so benchmark actual performance before planning excessive scenery counts, park complexity or water-simulation loads.
- **Next:** wait for actual Steam install completion; then perform vanilla startup/sandbox/save/reload test before enabling any third-party mods.
