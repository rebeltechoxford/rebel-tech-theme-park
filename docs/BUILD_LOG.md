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

## 2026-10-27 — Planet Coaster 2 installed and launched
- **Steam evidence:** `D:\SteamLibrary\steamapps\common\Planet Coaster 2\PlanetCoaster2.exe` exists (317,260,288 bytes). Steam app manifest for app 2688950 reports StateFlags=4 and BytesDownloaded=13,900,636,080/13,900,636,080.
- **Launch:** sent official Steam URI `steam://rungameid/2688950` and verified `PlanetCoaster2` PID 50632 started with a responsive, visible 1920×1080 window.
- **GUI probe:** reused the existing read-only window probe locally with PC2 executable name. Result `GAME_WINDOW_FOUND`, foreground=false. No mouse/keyboard game inputs were sent, no screenshots of game content were captured, and no park save/reload was verified.
- **Next:** get PC2 foreground in an interactive session, capture/review the game state, create vanilla sandbox park, and save/reopen it. Avoid third-party mods until the baseline is proven.

## 2026-10-27 — Build session 003: PC2 sandbox creation, GUI control, actual paths and flat ride
- **Raven control:** developed and committed `scripts/pc2_desktop_control.py` (GitHub commit `04e204a`): foreground-checked, exact-process-verified WinAPI mouse and keyboard operations, click/move/scroll, game screenshot, and constrained text input. Ran these controls against PC2's live 1920×1080 window. Original game briefly closed before automation began, then relaunched through Steam and remained responsive.
- **Vanilla park:** created **Rebel Tech World** in Planet Coaster 2 Sandbox, tropical biome, default sandbox preset/unlimited funds. Confirmed active simulation and initial guests.
- **Baseline:** saved `Rebel Tech World-6DD535CD.park2` (~4.44 MB). Opened game Load Park menu and successfully reloaded that saved park. Copied and SHA-256-verified an unchanged backup in ignored `build/backups/pc2/2026-10-27-initial-sandbox/` on D:.
- **Entrance path:** placed an 8-meter-wide straight guest path from park spawn, observed guests walking on it, extended the central avenue and made a left/right transverse T-junction. No scenery, water attractions, or custom Blender asset was imported.
- **Checkpoint 1:** saved `Rebel Tech World - Entrance 01` (~4.46 MB) before extending the T-junction; backed up and hash-verified on D: under `build/backups/pc2/2026-10-27-entrance-01/`.
- **First ride:** placed a built-in **Planet Coaster 360 Power** flat ride beside the main path as an experimental attraction. The game shows **CLOSED / This ride isn't accessible / Connect Entrance to Path**; entrance and exit placement indicators show completed but a working queue connection is NOT complete. Attempts to join a straight queue directly to the avenue returned **Paths cannot cross**. Do not call the ride operational.
- **Checkpoint 2:** saved `Rebel Tech World - Ride Test 02` (~4.44 MB) with extended avenue/T-junction and flat ride; backed up and SHA-256-verified on D: under `build/backups/pc2/2026-10-27-ride-test-02/`. Three distinct game save checkpoints now exist in PC2 Saves, without overwriting each other.
- **Next:** build a short queue segment from the ride entrance and connect cleanly to the guest path (try 2-segment path / curve builder and avoid path intersection crossing), connect exit to guest path, supply power, open/test the ride. Then incrementally landscape and add facilities. Validate game save/reload of newer checkpoints before publishing blueprints or installing optional third-party modding tools.
- **Scope/safety:** No third-party custom model converter or ACSE/ForgeUtils mod installed; original D: Blender model retained; game binary/save file not committed publicly.


## 2026-10-27 — Game closed; offline entrance kit and queue repair plan
- **Owner instructions:** Keep project moving but **close Planet Coaster 2 until needed**. Followed the normal in-game Exit to Main Menu flow and clicked Quit, then verified no PlanetCoaster2 process was running. All three saved park checkpoints remained present and unchanged, including the SHA-verified D: backups.
- **Queue/access research:** PC2 uses orange **queue paths** from ride entrances to normal guest paths and standard paths for ride exits. Build a short straight queue from the entrance before bending; end it at the edge of the guest avenue rather than crossing it. Recent community reports confirm sharp bends, queue overlap and node editing can be tricky. Official Frontier/Xbox notes confirm powered generators and connected distributors are required for rides.
- **New instructions:** [Ride & Utilities Runbook](RIDE_AND_UTILITIES_RUNBOOK.md), [Build Phases](BUILD_PHASES.md). These are OFFLINE plans; 360 Power remains CLOSED, path connection still unverified, and power remains 0/36.
- **New Blender source:** `blender/build_entrance_kit.py` procedurally generated three original modular pieces while PC2 stayed closed.
  - RT Fiber Pylon: 1,496 triangles, 1.90 × 1.15 × 5.71 m, six materials, 83,368-byte GLB.
  - RT Data Core landmark: 3,232 triangles, 3.984 × 4.60 × 5.235 m, five materials, 224,892-byte GLB.
  - RT Wayfinding Sign: 1,996 triangles, 4.58 × 0.316 × 3.14 m, five materials, 99,020-byte GLB.
- **Validation:** Blender 4.5.3 LTS generated a combined source .blend, three independent GLBs, rendered preview and JSON manifest. Each GLB was successfully re-imported with matching triangles, UVs and material counts (Blender-only round trip).
- **Published:** [Blender preview](https://github.com/rebeltechoxford/rebel-tech-theme-park/blob/main/docs/images/pc2-entrance-kit-v0.1.png) and the [exact three original GLBs](https://github.com/rebeltechoxford/rebel-tech-theme-park/tree/main/assets/pc2/entrance-kit-v0.1) committed to GitHub so other authorized agents can access them. Compared GitHub binary object hashes against Raven's `git hash-object` outputs; all three matched. Source generator committed; local build artifacts also retained on D:.
- **Safety:** No mods or unofficial KMods Converter downloaded/installed; no PC2 executables/save binaries/Steam data uploaded. Original park game save files remain private and versioned locally.
- **Next interactive session:** Open the latest Ride Test 02 checkpoint only when actual game work is appropriate. Fix 360 Power entrance queue, normal exit path and power network; confirm guests ride it and save as a distinct Ride Operational 03 checkpoint before themed scenery placement.

## 2026-10-27 — Rebel Grid branding revision and original van kit
- **Owner specification:** dark TRON-like technology city, red/blue/white with actual blue instead of cyan; no visible grass; pure-white streetlights; original RT logos throughout; three matching mobile-workshop vans; custom branded shops/restrooms/restaurants; additional advanced coaster types and Mombasa theme music.
- **Current authoritative plan:** docs/REBEL_GRID_MASTERPLAN.md. Candidate roster includes ROOT ACCESS 420 strata, GIGABIT FORCE giga, ZERO-DAY seated Maverick-style launcher, UPRISING true stand-up, BLACK ICE inverted, PHANTOM PACKET flying, MOUSE.EXE single-car mouse, LIGHTCYCLE PROTOCOL bike, KERNEL PANIC X 4D, STACK OVERFLOW multiverse, DEADLOCK tilt and PACKET RACE dueling launch. These are concepts/targets, not new in-game rides.
- **Correction:** Maverick is seated; a true stand-up is a separate requirement. Advanced track mechanisms are model-specific, not universally mixable. Sorcery Pack LSM Raid / Bike and Sidecar are DLC-dependent; ownership is not inferred from installed package files and no purchase was made.
- **Original artwork verified:** RT circle and detailed Oxford hero image are byte-identical to owner uploads, retrieved from the owner's deployed website and checked against known Git blob hashes. Sources/provenance are in assets/branding/grid-v1.
- **Native media staged:** scripts/stage_grid_media.ps1 produced seven custom dark signs plus two original images and copied all nine into the existing PC2 UserMedia directory. Every copy has a SHA-256 match. Custom billboard image assignment / saved placement remains unverified.
- **Offline models built:** blender/build_rebel_grid_kit.py created an original high-roof branded workshop van (5,728 triangles), pure-white lamp (444), 12m paving module (72), and six branded facility shells (482 each). All nine GLBs passed fresh-scene Blender 4.5.3 re-import validation. A preview and packed .blend remain on D:. The preview uses three instances of one van mesh; no custom vans have been placed in PC2.
- **Quality check:** fixed missing preview-world setup, adjusted the shell signs to keep the entry opening clear, widened the preview to show every item, reran all nine round-trip tests successfully. These remain first-pass prototypes, not a finished exact van replica or functional game buildings.
- **Desktop coordination:** another supervised session holds the PC2 GUI lease for path repair. This session stopped GUI input rather than bypassing the lock. A TV Screen 4m experiment may have added an unassigned screen to the Hotdog Squad group before the lease; no custom image or save of that experiment is claimed. Handoff recorded under ignored build/coordination.
- **Park evidence:** observed the existing District Spine checkpoint as the latest .park2 save at initial preflight (4,427,909 bytes). No new operational ride result or completed no-grass makeover was verified in this branding session. The end-of-day UI observed earlier still reported zero average rides per guest; OPEN labels are not a boarding test.
- **Music:** likely Hans Zimmer's Mombasa from Inception. No matching file in PC2 UserAudio, no music downloaded/purchased, no DRM bypass, no public audio redistribution. Needs an authorized local recording.
- **Next:** integrate native logo billboards in a coordinated game session; replace grass/tropical scenery district-by-district with dark surfaces and white lighting; fit native facilities into custom shells; verify guest access and complete flagship rides one at a time.

## 2026-10-27 — Work resume: actual save inventory and verified preservation
- Read latest Notion first and inspected Raven via Desktop Commander. Latest actual saved checkpoint remains RT Grid 360 Access 10 (4,610,796 bytes); later live Teacups edits are potentially unsaved per handoff.
- Created a fresh non-overwriting D: snapshot of all ten existing park saves and independently matched every SHA-256; private manifest retained with backups.
- Active coaster-queues-20261027-C lease respected: no GUI inputs, game reset/load/close, controller bypass or edits to other sessions' dirty files. Safe handoff requested locally. Monitor capture showed ChatGPT foreground; no current game-view claim made.
- No new construction or guest tests claimed. See docs/checkpoints/2026-10-27-work-resume-preflight.md for verified evidence and next acceptance step.


## 2026-10-27 � Work: actual 360 exit repair, separately saved
- Acquired explicitly released control lease; preserved live park as Work Preserve 11 and hash-verified D: copy.
- Placed normal 5m route at actual lower 360 exit attachment. Specific exit warning disappeared; screenshot committed. Live pre-repair summary showed 252 lifetime guests, but no three-cycle test claimed.
- Teacups connector attempts did not clear its exit warning. Sky Watcher/Overclock access and ride staffing remain open. No new coasters, long queues or completed themed district claimed.
- Saved RT Grid Exit Repair 12 (4,615,056 bytes); independent D: copy SHA256 matched. Reload remains untested. Normal game quit initiated before offline handoff. See docs/checkpoints/2026-10-27-work-exit-repair.md.

## 2026-10-27 � Dream-board visual inspection and native access audit
- Both Notion dream-board image uploads were visually inspected; reference copies retained locally. Approved masterplan roster and every-building-custom standard remain binding.
- Reloaded Exit Repair 12 successfully; 360 exit warning remained absent. Added public 5m cross-connection and cleaned failed Teacups connector pieces. Teacups exit remains unresolved; no new coaster or long queue claimed.
- Saved Access Audit 13 and verified independent D: backup SHA256 eac2dda45b2ddd36261bbc474a239564d942c246506a6d50a5dcd3f5629a126a. See docs/checkpoints/2026-10-27-dream-board-continuation.md. Current control/attachment reliability prevents efficient further building; avoid repeated guesses against owner credit budget.

## 2026-10-27 � Work Mode grid import trial
Four original models converted into native pack; incomplete ACSE dependency blocked runtime. Launch crashed before menu; new mod folders moved out of ovldata, preserved on D:. No ground/path/skyline placement claimed. See docs/GRID_BASE_IMPORT_TRIAL.md. Existing blank and old saves preserved.



## 2026-10-27 - THE GRID biome v1 (Claude session) and fresh Rebel Tech Grid park
- Owner reset: all old parks deleted, fresh start. Old KMods/ForgeUtils mods removed; ovldata now holds ACSE 0.729 plus our own Mod_KMods_rebel_tech_tron_grid (Tron tiles from blender/build_tron_grid.py).
- Shutdown crash (PlanetCoaster2.exe+0x14AEE62) was bisected to ACSE alone. Saves and reloads are unaffected. A 442 m asset crashes at startup (0xFDEAD); 96 m loads fine.
- Built a custom Grid biome with OpenNaja cobra-tools (scripts/pc2_grid_biome.py). It overrides the Temperate biome in place, with originals backed up under build/backups/pc2/temperate-*-original:
  - Temperate.ovl: every terrain paint layer is repainted as Tron grid (black + RT blue #244CFF; red, white, navy and solid brushes as accents). Grass and flower detail is made transparent; macro tint and detail normals are neutralised.
  - TemperateWorld.ovl: the skirt heightmap is flattened and all 64,324 skirt trees are removed.
  - TerrainSkirts/TemperateSandbox.bakedHeightMap: replaced with a flat v0 bake at park level. Rewriting the shipped v2 bake crashed the game (0xFDEAD), which was recovered immediately.
- New sandbox "Rebel Tech Grid" (Creative, Temperate = THE GRID): starter trees bulk-deleted, wind/rain/storms/snow off, sun fixed at 12:00 am. Saved as Rebel Tech Grid-D813563F.park2; D: copy SHA-256 74c2f650...e4d1 matched. The reload was verified in-game: night grid, no hills or trees.
- Known limits: terrain has no emissive channel, so the lines read as a lit blue grid rather than true bloom. A few dark terrain mounds and edge trees remain. A Steam "verify files" or game update will restore the stock biome; re-run scripts/pc2_grid_biome.py all (cobra-venv Python, game closed) to reapply it. The restore step undoes it.

## 2026-10-27 - THE GRID look pass: glow, skyline, hidden coaches (Claude session)
- scripts/pc2_grid_look.py (new): teal Tron colour grade (GameTemperate LUT), stronger cyan bloom, +1.1 EV exposure, teal sky/haze/fog in GameMain/Main.ovl; guest coaches shrunk to 1% so arriving buses are invisible. Originals backed up whole-folder to build/backups/pc2/grid-look-original; "restore" puts them back.
- Biome terrain lines are now neon cyan (#00E5FF) with a gaussian halo and white-hot core, thicker for distance.
- ForgeUtils restored from build/backups/pc2/removed-mods-20261027: our pack registers its scenery through it, so the Tron pieces were never in the browser before. Game launches and loads fine with it.
- New pieces in the Rebel Tech pack (blender/build_tron_skyline.py): RT Grid Tower, RT Grid Skyline A/B, RT Grid Glow Floor (lines-only emissive floor). PC2 scenery scales up to 1000%.
- Park: edge trees inside the boundary deleted; tower placed at 500% on the far edge, two skyline walls at 400% on the side edges, glow floor at 500% in front. Lighting fixed at 6 pm (emissive pieces bloom; terrain alone cannot emit). Saved and backed up to build/backups/pc2/rebel-tech-grid-20261027-2145 (hash matched).
- Not done: terrain mounds and red paint patches inside the boundary; trees beyond the boundary on the remaining edges are only partly hidden. Quitting still triggers the known ACSE shutdown crash; close crash_reporter before relaunching.

## 2026-10-28 - Grid city, entry portal, red coaster, nature hidden (Claude session)
- blender/build_tron_skyline.py rebuilt with detailed buildings (chamfered piers, glass curtain walls, fins, stepped crowns, antennas) plus RT Grid Spire and RT Grid Portal (vortex ring between two pillars carrying the Rebel Tech Grid logo on both faces; logo cropped from the owner's reference into build/references). Textures from blender/make_city_textures.py. All added to the Rebel Tech pack (build/tron-grid/make_pack.py).
- Portal placed at 300% on the open side of the park between the skyline walls. Spires did not place (to retry).
- scripts/pc2_hide_nature.py (new): template trees/ferns/bramble/flowers made fully transparent and rocks Grid black, so nature outside the boundary disappears too. Backups in build/backups/pc2/hide-nature-original. Model shrinking failed on trees (wind vertex data), so this works through materials.
- scripts/pc2_grid_biome.py: every terrain paint layer is now the same cyan grid (template red/blue patches gone) and terrain detail scatter models are shrunk to 1%. Mounds inside the boundary flattened with Flatten to Foundation.
- scripts/pc2_glow_cars.py (new): channel-1 emissive enabled on all 53 coaster car types; no visible glow in game yet. Backups in build/backups/pc2/glow-cars-original.
- Coaster test: Twisted Arc placed, all track and car colours set to RT red (#E10616), Sci-Fi music. Rails use an extrusion shader with no emissive input, so rails cannot glow; lighting fixed at 4 pm so red reads while neon edges still show.
- Saved; backup build/backups/pc2/rebel-tech-grid-20261028-final (hash matched).

## 2026-10-28 - Gloss-black grid fix, dream-board city, test coaster removed (Claude session)
- Biome: every terrain layer is the cyan grid (auto-paint had wiped it with a black layer); bump/height maps neutralised for gloss black; roughness 55.
- City rebuilt in dream-board style (armored towers, red/blue neon, RT badges, shopfronts, RT ring monument); same object ids so placed pieces updated. New rt-badge.png texture from assets/branding.
- Test coaster Twisted Arc and its 103-piece scenery group deleted. Saved 05:47; backup build/backups/pc2/rebel-tech-grid-20261028-city (hash matched). Handoff written to the Notion project hub.
- Not done: more city blocks in the remaining edge gaps (camera navigation was too costly); outer-boundary terrain ridges.
