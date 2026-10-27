# Planet Coaster 2 — Asset, Gameplay & Mod Compatibility

**Status: October 27, 2026. PC2 installed and vanilla construction / save-reload tested, but now CLEANLY CLOSED at owner's request. Three original Blender entrance kit GLBs plus Gateway source exist; no custom-model import or mods have been tested.**

## Stage 1 — Official in-game construction
Start with a vanilla Planet Coaster 2 sandbox park and use built-in scenery, path, coaster, pool and waterslide construction tools. The official **Frontier Workshop** supports sharing PC2 blueprints and parks, including cross-platform content. Source: https://www.planetcoaster.com/en-US/help-center

### Acceptance
- Verify game installation on Raven. Use D: for build materials and check installation destination.
- Launch PC2, create a tiny sandbox entrance with paths/facilities and save the park.
- Quit and reopen the saved park; confirm clean operation without mods.

## Stage 2 — Custom original model exports (Blender)
The existing procedural **Rebel Tech Gateway** was generated in Blender 4.5.3. It has several LOD meshes for the **old PC1** toolkit. The .blend geometry can be reused, but PC1's Toolkit ZIP and .pcugc are not a PC2 custom-scenery format.

Suggested preparation: load the original generated Blender .blend, keep only the highest-detail visible gateway mesh, pack textures, check dimensions and origin, then export a standalone GLB or FBX and preserve a cleaned .blend. This is an offline export candidate, NOT evidence of a game import.

## Current original asset sources

- [Three-piece original entrance kit, GLB files and build guide](../assets/pc2/entrance-kit-v0.1/README.md)
- [Kit preview](images/pc2-entrance-kit-v0.1.png)
- [Procedural generator](../blender/build_entrance_kit.py)
- [Legacy repurposed Gateway](../blender/prepare_pc2_gateway.py)

Blender 4.5.3 LTS successfully exported the RT Fiber Pylon (1,496 triangles), RT Data Core (3,232), and RT Wayfinding Sign (1,996). Each survived an independent Blender GLB round-trip with materials/UVs intact, but actual in-game appearance, emissive effects, collision and distribution are **unverified**.

## Stage 3 — OPTIONAL, unofficial model import
A community tool **KMods Converter** advertises conversion of FBX, OBJ, DAE, GLB/glTF and BLEND files to PC2 scenery packs. Its current Nexus description advertises **version 3.1**, although other metadata may still show 3.0; version and checksums must be confirmed before use. Conversion relies on community mods **ACSE** and **ForgeUtils**, even when the utility includes its own conversion engine. No third-party installer has been downloaded or executed for this project.

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

**Risk note:** Original GLB asset files and preview images are safe, portable source artifacts; that alone does not make the KMods EXE safe or guarantee PC2 mod compatibility. The game remains closed during offline work.

## Historical PC1 material
The original Thememaker's Toolkit instructions remain under docs/TMT_PIPELINE.md for archival reference only. They should not be followed for PC2.

## Licensing and ownership
Use original procedural meshes by default. User has a Sketchfab account, but any individual marketplace model needs a license check and proper attribution if applicable; purchase/download/authentication remain user-controlled.