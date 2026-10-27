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
