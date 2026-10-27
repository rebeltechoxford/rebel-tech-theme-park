# THE REBEL GRID - Every Building Is Custom

Owner requirement, 2026-10-27: **"Theme every building too, no standard build in's all custom."**

This is a mandatory addition to REBEL_GRID_MASTERPLAN.md, not a claim that these buildings have been constructed. Path, queue, exit and staffing repairs retain first priority. The two generated park illustrations are concept references, NOT screenshots or evidence of game construction.

## What counts as custom

Every guest-visible building must have an original Rebel Tech architectural composition: massing, roofline, facade, doorway/counter surround, lighting, signage and guest-facing interior. This includes entrances, coaster stations, queue halls, food/drink counters, retail, restaurants, toilets, first aid, staff buildings, utilities and pool facilities. The rear and roof count wherever they can be seen from a queue, tower or coaster.

Native walls, roofs, structural pieces, functional facility cores and ride mechanisms may be used as components. A stock themed blueprint, a default kiosk with an RT sticker, or a recolored prefab does NOT meet the requirement. Do not promise new ride physics, seats or shop simulation that the installed game does not support.

Prefer native in-game piece-by-piece construction so custom exteriors do not depend on an unverified model importer. Existing Blender/GLB shells are design prototypes only. Six copies of the same prototype with different signs are not six finished custom buildings. Shared structural modules are encouraged for performance, but the visible compositions must differ.

## Mandatory visual language

- Glossy black/charcoal and deep navy dominate: #090B10 and #061A33. Use gloss selectively on panels, canopies and signs rather than claiming unsupported mirror reflections.
- Signal red #E10616 and saturated electric blue #244CFF provide architectural contrast. White #FFFFFF and graphite/gray provide trim and readable signage. Do not drift to cyan, orange, amber or warm-yellow primary lighting.
- Pure-white practical lighting makes paths, stairs, counters, entrances and exits readable. Red/blue edge strips accent architecture without hiding circulation.
- Angular portal frames, layered canopies, server-rack fins, organized cable channels, repeated panel joints and selected orbital motifs create one coherent RT district.
- The complete editable district must not expose ordinary grass. Use actual dark guest paths, paved plazas, metal decks, dark terrain and screened edges. Scenery slabs do not create a walkable path and must not conceal disconnected path nodes.
- No tropical/Viking/default-shop decorative shells in finished areas. Keep any temporary stock pieces clearly recorded as TEMPORARY and replace them without deleting their working facility core.

## Use the owner's real artwork

Preserve the RT silhouette, relative letter shapes, orbit layout and original aspect ratio. No typed R/T substitutes, guessed logo geometry or AI redraws as final branding. Do not stretch a square logo across a wide billboard. Frame or letterbox the artwork instead.

Approved reference roles from the seven images in the current owner message:
1. Server-room neon artwork: mood and large feature-display reference, not a tiny directional icon.
2. Metallic standalone RT: hero signage or large station panels.
3. Atomic RT on red: red district panels; navy/white contrast.
4. Atomic RT on navy: dark district panels; white/red contrast.
5. Atomic RT on white: light/gray panels; navy/red contrast.
6. Full Oxford Rebel Tech illustration/wordmark: main entrance, showroom or large feature wall.
7. Circular RT monogram: repeated gate, station, wayfinding and facility identity.

Artwork stays legible against its backdrop. Use the supplied contrast variants instead of putting dark navy lettering directly on black. Add a border or backing panel if necessary; keep the source originals unchanged.

The current Raven repository has byte-identical originals for references 6 and 7 under assets/branding/grid-v1. The other five originals remain provided in the conversation and are inventoried in docs/RT_REFERENCE_MANIFEST.json; do not claim they have all been staged on Raven or assigned to in-game screens. Generated concept images do not replace these brand originals.

## Architectural schedule - specified, not built

| Facility | Custom identity and geometry | Functional opening that must remain clear |
| --- | --- | --- |
| BOOT GATE / main entrance | Twin server towers, layered angular entry portals, large true RT emblem and white-lit threshold | Full entry/exit lanes and their connection to the rooted main boulevard |
| Coaster stations | A different silhouette per ride; bespoke train-hall roof, control booth facade, signage, platforms and exit gallery | Station entrance, exit, train movement envelope and verified loading area |
| Queue halls | Substantial multi-bay switchbacks inside cable-gallery or server-room architecture; visible entrance and sheltered sections | One continuous actual queue from public path to the correct ride entrance; no decorative fake queue |
| BYTE BITE / food | Stepped processor-style roof and separate lit counter portals | Each native food counter's approach, service space and connected guest path |
| OVERCLOCK CAFE / drinks | Slanted blade canopy, recessed facade, white menu lighting and blue trim | Counter, collection area and through circulation |
| REBOOT RESTROOMS | Twin offset privacy portals, readable white restroom signs, black/navy service facade | Native door/approach and guest route, not just a decorative doorway |
| CACHE & CARRY / retail | Display-window frontage and asymmetric framed roof; contrast RT panels | Shop entrance and customer standing space |
| CORE KITCHEN / dining | Circular or faceted orbital pavilion, tiered dark roof and red/blue accents | Working restaurant/food-court access and seating circulation; actual supported facility type recorded |
| PATCH BAY / aid and information | Crisp white/navy diagnostic facade with red framing | Aid/service door and staff access; keep service identity obvious |
| SERVICE MODE / staff | Custom industrial service-bay facade and screened mechanical yard | Staff building and maintenance access; no blocked working door |
| Cooling Loop facilities | Chiller-plant architecture, dark deck, white-lit changing/shower/entry portals | Real pool access, working changing/toilet routes and lifeguard access where required |
| Utilities / backstage | Dark transformer or server enclosures with economical vent/detail modules | Power/water/maintenance connections and service routes remain usable |

### Station personalities

These are architecture targets, not verification of the underlying ride model. The master plan and live catalogue verification decide ride mechanics.

- Strata/top-hat: tall launch-control tower and an open-ended acceleration hall. Structure remains outside the entire forward/reverse train envelope.
- Giga: long horizontal server-gallery station with a visible lift-tower sightline.
- Seated multi-launch: low angular tunnel complex with separately framed launch sections.
- Stand-up: vertical ribbed pavilion, distinct from the seated multi-launch ride.
- Inverted: elevated cable-tray canopy and protected lower queue, leaving hanging trains and riders clear.
- Flying: swept-wing canopy and generous fly-to-lie/train clearance.
- Shuttle launch: bidirectional tunnel with separate guest return route; no structure on the rollback path.
- Lie-back concept: low orbital vault with overhead light ribs, only after compatible seating is confirmed.
- 4D: segmented gimbal/ring architecture outside the full rotating-seat envelope. Controlled-rotation and free-spinning types must not be conflated.
- Bike launch: repeated red/blue portal sequence and a long dark canopy, with only supported seating and launch mechanics.

## Non-negotiable path and queue gate

Build and test circulation BEFORE dressing it. Do not place another attraction to avoid fixing the current one.

1. Identify the actual ride entrance and exit attachment nodes; visually overlapping a path is insufficient.
2. Preserve a rooted public route to the park entrance. Run a substantial, logical queue in its own reserved footprint. Give it room to turn without self-crossing or cutting the public boulevard.
3. Use a separate ordinary exit path returning guests to that public network. Queue and exit cannot silently swap roles.
4. Check staff availability, ride operation and current notifications without dismissing or disabling accessibility alerts.
5. Observe guests arriving, entering the queue, boarding, riding, unloading and leaving onto the public route. Record evidence for at least three complete dispatch cycles before marking the attraction accepted.
6. Save a distinct native checkpoint, verify its D: backup hash, then reload it. A cleared warning or an OPEN label alone is not completion.
7. Add custom architecture only after this gate passes. Re-run the circulation and save/reload checks after adding walls, supports, floor pieces and signage.

## Finished-building acceptance

A building is FINISHED_IN_GAME only when all of these are verified:
- Original RT composition is installed in the actual park; no exposed default themed facade, including visible sides/rear/roof.
- Correct exact logo, legible contrast, aspect ratio and correct palette; nighttime practical light is white.
- Real doors, counters, queue entries, ride exits, staff access and train clearances remain unobstructed.
- Guest/staff use was observed, not inferred from decoration or a green UI toggle.
- No unintended visible grass or floating paving inside the completed footprint.
- Native save/reload retains its architecture, image assignments and functionality.
- In-game evidence exists; an offline render is not substituted for it.

State labels: SPECIFIED / NATIVE_BUILD_IN_PROGRESS / VISUAL_CHECKED / ACCESS_RETESTED / SAVE_RELOAD_VERIFIED / FINISHED_IN_GAME. Existing offline shells remain OFFLINE_PROTOTYPE until actually constructed or imported and tested.

## Coordination and cost control

Use the freshest park save and handoff, not the older checkpoint names embedded in historical logs. Respect the desktop-control lease. Preserve other agents' modified scripts. Keep the game closed during documentation and offline preparation; launch only for an actual game operation. Do not create another render-only asset pipeline while the required path repair remains blocked.
