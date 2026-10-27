# Rebel Tech World — Original Entrance Kit v0.1

**Target:** Planet Coaster 2 on Raven. These files are **original Blender-generated model candidates**, not yet converted to playable Planet Coaster 2 scenery. No PC2 mod, converter or game installation was changed.

## Models

| Asset | Dimensions in meters | Triangles | Materials | Use |
| --- | --- | ---: | ---: | --- |
| [RT Fiber Pylon](rt_fiber_pylon.glb) | 1.90 × 1.15 × 5.71 | 1,496 | 6 | Place mirrored copies at the boulevard entry, server-rack-inspired LED/signage pylons |
| [RT Data Core](rt_data_core.glb) | 3.984 × 4.60 × 5.235 | 3,232 | 5 | Future signature central plaza sculpture with cyan circuit rings |
| [RT Wayfinding Sign](rt_wayfinding_sign.glb) | 4.58 × 0.316 × 3.14 | 1,996 | 5 | Directional sign for The Core and Clanka Labs, suitable near the T-junction |

[View the Blender concept preview](../../../docs/images/pc2-entrance-kit-v0.1.png).

All three were exported as *single-object GLBs* with materials and UVs. Each passed a separate GLB import and triangle/material check in Blender 4.5.3 LTS on Raven. The SHA of every GitHub binary was compared with Git's hash-object output for the original file on Raven, establishing byte-identical uploads.

## Reproduce from source

Run this after cloning the repository to Raven's D: drive and with Blender installed:

```powershell
& "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --background --python blender\build_entrance_kit.py
```

Source: [blender/build_entrance_kit.py](../../../blender/build_entrance_kit.py)

The command regenerates the local .blend, GLBs, preview and validation manifest under `build/pc2/entrance_kit/`. The entire `build/` directory is ignored by Git. These published GLBs and the preview are explicitly approved project originals, not exports of Frontier game assets.

## Integration requirements still outstanding

1. Keep PC2 closed until an actual interactive build or test requires launching it.
2. Confirm whether an acceptable PC2 custom scenery importer is available and compatible with the installed game. One *unofficial* option is KMods Converter using ACSE and ForgeUtils. Do not install unsigned third-party software automatically or disable protections.
3. If custom import is approved, test **one** small prop in a disposable test park, then verify correct size/materials, load after restart, and public Workshop limitations.
4. Avoid placing a visual sculpture in any active guest path; test in-game clipping/collision behavior.
5. Retain the vanilla park saves and independent backups on D:.

**No in-game appearance, dynamic lighting or collision behavior is guaranteed by the Blender-only tests.**
