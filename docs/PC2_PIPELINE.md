# Planet Coaster 2 — Asset, Gameplay & Mod Compatibility

**Status: planning/compatibility review, October 27, 2026. PC2 has not yet been launched on Raven.**

## Stage 1 — Official in-game construction
Start with a vanilla Planet Coaster 2 sandbox park and use built-in scenery, path, coaster, pool and waterslide construction tools. The official **Frontier Workshop** supports sharing PC2 blueprints and parks, including cross-platform content. Source: https://www.planetcoaster.com/en-US/help-center

### Acceptance
- Verify game installation on Raven. Use D: for build materials and check installation destination.
- Launch PC2, create a tiny sandbox entrance with paths/facilities and save the park.
- Quit and reopen the saved park; confirm clean operation without mods.

## Stage 2 — Custom original model exports (Blender)
The existing procedural **Rebel Tech Gateway** was generated in Blender 4.5.3. It has several LOD meshes for the **old PC1** toolkit. The .blend geometry can be reused, but PC1's Toolkit ZIP and .pcugc are not a PC2 custom-scenery format.

Suggested preparation: load the original generated Blender .blend, keep only the highest-detail visible gateway mesh, pack textures, check dimensions and origin, then export a standalone GLB or FBX and preserve a cleaned .blend. This is an offline export candidate, NOT evidence of a game import.

## Stage 3 — OPTIONAL, unofficial model import
A community tool **KMods Converter** claims to convert FBX, OBJ, DAE, GLB/glTF and BLEND files to scenery packs for Planet Coaster 2. Its Nexus listing was updated October 2026. It requires separate community mods **ACSE** and **ForgeUtils**.

Project/vendor references:
- KMods Converter: https://www.nexusmods.com/planetcoaster2/mods/59
- ForgeUtils: https://www.nexusmods.com/planetcoaster2/mods/18
- ForgeUtils repository: https://github.com/Distantz/ForgeUtils

**Third-party compatibility and security caveats:**
- KMods Converter, ACSE and ForgeUtils are not Frontier-supported components. Do not equate Nexus' virus-scan label with a complete security audit.
- The KMods listing notes its app may be unsigned and trigger SmartScreen. Do not blindly bypass or suppress protective prompts.
- Confirm the exact installed game version, current tool/mod versions, provenance and independent experiences before deciding to install.
- Back up PC2 saves; only modify installs after risk assessment and owner awareness.
- Converter features, output appearance, and workshop compatibility are not verified on Raven.
- Mods may become incompatible with patches or prevent other users from loading shared custom-scenery blueprints, especially cross-platform.

### Optional proof of concept
After PC2 is proven to work without mods, import **one** original gateway model in a test park, check orientation/UVs/materials/scale, save/restart/reload and record screenshots. Failures should not endanger the vanilla park.

## Historical PC1 material
The original Thememaker's Toolkit instructions remain under docs/TMT_PIPELINE.md for archival reference only. They should not be followed for PC2.

## Licensing and ownership
Use original procedural meshes by default. User has a Sketchfab account, but any individual marketplace model needs a license check and proper attribution if applicable; purchase/download/authentication remain user-controlled.