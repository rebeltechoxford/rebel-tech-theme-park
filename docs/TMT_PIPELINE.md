# Planet Coaster 1 — Thememaker's Toolkit Pipeline

**Status:** research verified from Frontier documentation, local implementation untested (Raven offline 2026-10-27).

## Authoritative references
- https://thememakers-toolkit.planetcoaster.com/user-guide
- https://thememakers-toolkit.planetcoaster.com/user-guide/user-guide
- https://thememakers-toolkit.planetcoaster.com/user-guide/materials
- https://thememakers-toolkit.planetcoaster.com/user-guide/exporting
- https://thememakers-toolkit.planetcoaster.com/user-guide/error-descriptions
- https://thememakers-toolkit.planetcoaster.com/user-guide/3d-software

## Asset requirements
- Static item must contain appropriately named render meshes _L0 ... _L5 (6 LOD meshes); triangle count should reduce with each step.
- Maximum 8m x 8m x 8m model bounds; highest-detail _L0 max 8,000 triangles.
- Maximum eight unique materials; use base-colour PNG maps named after the material, e.g. RTNavy_BC.png.
- Base texture resolution at most 2048 x 2048; keep texture budget low; use dimensions divisible by four.
- FBX Y-forward, Z-up and static export with animation disabled. Apply scale and rotation prior to export.
- ZIP must contain .fbx, .png textures and an icon.png at its root. A separate preview image is uploaded alongside the ZIP.
- Supported/tested authoring software stated in legacy Frontier guide: Blender 2.79. Later Blender versions may work, but must be validated with an actual conversion.
- Toolkit can create scenery, NOT new ride mechanics, original roller coasters, or game-engine lighting effects.

## Conversion steps
1. Generate Blender source and FBX + PNG textures using assets you own (see experimental blender/create_rt_world_sign.py).
2. Review dimensions, UVs, naming, geometry/triangle counts, textures, and license/attribution.
3. Make ZIP with the FBX, PNG texture maps, and icon.png. Keep preview.png outside ZIP.
4. Sign in with the owner's Steam account at https://thememakers-toolkit.planetcoaster.com/ .
5. Choose Create New Item, upload ZIP and preview, fill in description/category/settings, wait for Frontier conversion to finish.
6. Download the generated .pcugc if conversion succeeds. Record any Toolkit errors rather than guessing.
7. Install the .pcugc into the user's Documents\Frontier Developments\Planet Coaster\TMT folder (the path is normally on C: even if source assets are on D:).
8. Start Planet Coaster 1, locate Toolkit Items/scenery category, place the item in a test sandbox park.
9. Save, exit and reload; verify shape, scale, materials, reflections, shadows, rotations, and file footprint.

## Pitfalls
- "Missing Render Level": verify _L0 through _L5 nodes were exported.
- "High Poly Count": reduce the _L0 mesh below 8,000 triangles.
- "LODOrderBad": progressively reduce triangle counts.
- "ugcNoIcon" / "ugcNo.fbx": ZIP must have icon.png and .fbx at root.
- "TooManyMaterials": use 8 or fewer materials.
- "TextureSizeInvalid": use PNG dimensions that are multiples of four.
- "ModelTooBig": ensure all axes stay within 8m.

## Distribution
Publish source scripts and documentation only. Do not push downloaded .pcugc files, user game saves, copyrighted third-party models, Steam auth materials, or local machine inventory into this public repository by default.
