# Grid base import trial — 2026-10-27

Owner scope: blank park only; white square grid covers ground, blue guest squares, red queue squares, dark original metropolis. No rides or layout.

## Actual result
- Original models EXPORTED: white-grid-ground (48m square), guest-blue, queue-red, dark-metropolis (32 towers). Source: blender/build_grid_metropolis.py plus build_blank_grid_surfaces.py.
- KMods Converter 3.1.0 author-linked portable distribution reviewed; included distribution hashes matched. Unsigned executables. Defender remained enabled. No SmartScreen bypass.
- Converted all four into Mod_KMods_rebel_tech_grid_base. Converter reported native_reload_passed but runtime_validation not_tested and game_ready false.
- Pack installed on disk, NOT placed or verified in game.
- Official ForgeUtils v2.7.0 downloaded from Distantz/ForgeUtils GitHub release, reviewed README and scanned with Defender, then installed for trial.
- ACSE PC2 unavailable without Nexus login: Raven browser signed out, author page says Log in to download. GitHub releases inspected were not a verified PC2 distribution; none substituted.
- Launch with incomplete dependency set CRASHED before menu. No park was loaded. Both newly added folders moved OUT of ovldata into build/import-review/disabled-after-launch-test. Vanilla relaunch started.
- Independent D: pack backup build/backups/pc2/rebel-grid-base-pack verified with zero SHA256 mismatches.

## Current boundaries
These are scenery panels, not terrain paints or registered path materials. Native path recolouring is a separate task. Ground cover, skyline placement and blue/red path defaults are NOT COMPLETE. Blank save remains preserved. No rides added.

## Next safe action
Obtain PC2 ACSE from the official Nexus page after owner signs in, review/scan package, restore isolated mod folders, prove vanilla and modded launches, then place one tile at correct height and verify before covering the sandbox. Do not activate incomplete mods again.

Official sources: https://www.nexusmods.com/planetcoaster2/mods/59 ; https://www.nexusmods.com/planetcoaster2/mods/1 ; https://github.com/Distantz/ForgeUtils
