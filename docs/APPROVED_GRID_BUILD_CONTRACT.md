# Rebel Tech World — Approved Rebel Grid Build Contract

Owner approval, October 27, 2026: “THATS THE IDEA! Build exactly that but make it work … take your time and go one by one making sure everything works.”

## Meaning of the approval

The two generated concept images are the visual target, NOT screenshots of an existing playable park. Preserve their architectural language, RT identity, red/blue lighting, dark material palette, coaster-heavy skyline and dense custom district design. Do not reproduce impossible track intersections, unreadable generated lettering, blocked guest routes or physically incompatible ride mechanisms merely because they appear in concept art. Function takes precedence over a literal pixel match.

Authoritative conversation artifacts, SHA-256 verified in the working container:
- `rebel_tech_neon_coaster_kingdom.png`: `3a1f6e4e810f0304019eed7ebd5d0bb78f2d118e96480b6cf1ce5bf23d8e1739`
- `rebel_tech_theme_park_at_dusk.png`: `264a9e7b8b4f68f848bbfb3e123c49ba4600294a7ed9a0348d24f184eca0a6bb`

These identifiers record approval; they do not claim the images are already on Raven or in this repository. Existing uncommitted master-plan, branding and modeling work on Raven must be preserved and reconciled, not overwritten.

## Non-negotiable visual requirements

Glossy-black/obsidian and navy architecture; electric blue and signal-red circuit lighting; white and gray contrast. Original RT monogram/circle/orbit marks from the owner's uploads, not arbitrary text-font substitutes. Use high-contrast white/red/blue variants appropriate to each background. Do not distort logo geometry.

No exposed grass in completed guest districts: use broad dark paving, metal decking, dark terrain or custom scenery surfaces. Native walkable paths must remain under guest routes; scenery floors alone do not establish navigation. Screen distant non-editable terrain rather than promising to replace it.

Every visible station, queue hall, shop, restroom, service building and utility enclosure needs an original Rebel Tech exterior. The functional core may use PC2's native ride/shop/toilet systems; “all custom” describes the finished architecture, not a claim to replace the simulation engine. No unaltered Viking, mythology, tropical or generic shop blueprint counts as final work.

Main architecture families: server-rack towers; angular launch portals; orbit-ring canopies; red/blue cable conduits; white task lighting; dark plazas with restrained RT floor medallions. Preserve room for service access, queues and sightlines. Use repeatable modules and measure frame rate before expanding lighting density.

## Required coaster experiences — none marked built by this document

Names from the artwork are aliases, not grounds to overwrite established ride names. Select and test an actual supported ride model before committing its footprint.

| Requirement | Concept-art alias | Acceptance distinction |
| --- | --- | --- |
| Strata launch/top hat with rollback inspiration | Quantum Ascent | Tall supported launch/top-hat; a TT2-style multi-direction sequence needs a compatible swing-launch model. Record achieved height and sequence, not aspirational statistics. |
| Giga speed/airtime coaster | Hyperdrive Giga | Tall lift/drop and sweeping sustained-speed layout, separately identified from the compact existing Overclock prototype. |
| Genuine stand-up coaster | Uprising | Actual standing train; do not call a seated train stand-up. Keep a Maverick-inspired seated multi-launch design as a separate requirement/interpretation. |
| Inverted coaster | Null Inversion | Riders beneath the rails; check hanging-train envelope and support/building clearance. |
| Flying coaster | Skyward Flight | Actual prone flying posture and supported transitions, not simply inverted seating. |
| Launch shuttle returning backward | Echo Protocol | Correct forward/reverse sequence and safe station return. Verify whether the selected model uses LIM, LSM or another supported launch; label accurately. |
| Lie-on-your-back experience | Horizon | Verify an actual supported supine/fly-to-lie mechanism; retain as unresolved if unavailable rather than silently substituting seated trains. |
| 4D rotating-seat coaster | Chroma Spiral | Distinguish controlled X2-style seat rotation from free spinning/swinging. Test the selected system and clearly identify its actual behavior. |
| Fast motorcycle-style launch | Velocity Forge | Verify available train/model/DLC. Bike-and-sidecar is not an exact TRON lightcycle riding posture. No purchase without owner authorization. |

The current local master plan already uses alternate names; preserve its work and reconcile aliases before renaming anything. Optional extra coasters come AFTER the first functional district, not before.

## Construction order

1. Back up the current named park. One controller owns the live game at a time. Respect any active short-lived control lease; no competing mouse/keyboard inputs.
2. Repair ONE existing attraction: main guest path → dedicated queue → actual ride gate; actual exit gate → normal guest path → main circulation. Existing gate-placement checkmarks are not proof of a connected queue or exit.
3. Observe guests approach, queue, board, complete the ride and leave. Verify at least three complete guest cycles. Testing mode alone and an OPEN label are insufficient.
4. Connect food, drink, restrooms and staff access. Keep any incomplete ride or pool closed. Resolve navigation errors, not just hide notifications.
5. Build its custom RT shell, hardscape and lighting; repeat clearance and navigation tests after adding scenery.
6. Save a NEW checkpoint, make a byte-identical D: backup, reload the save in-game and repeat the guest-route check.
7. Only then begin the next attraction/section. Reserve flagship coaster footprints without bulk-placing disconnected rides.

## Acceptance gates per attraction or district

- Entrance is reachable from the park entrance over native guest paths.
- Queue actually terminates at the correct gate and never crosses/merges incorrectly.
- Exit reconnects to normal circulation without a dead end or accidental queue route.
- Ride is open and observed guests board and exit through at least three complete cycles.
- Nearby essential services are reachable and operate under the declared sandbox settings.
- Train, supports, scenery, queue and exits have clearances checked in motion.
- Save/reload passes for the exact checkpoint being accepted.
- RT custom architecture, readable signs, requested colors and covered grass are verified from guest viewpoints.
- Performance is reviewed at the chosen settings, recording the observed result rather than asserting a guaranteed frame rate.

Power, breakdown and other sandbox options must be recorded explicitly. Disabled electricity is not a built electrical network; a closed pool is not an operational waterpark. No setting may substitute for connected guest paths.

## Evidence and status discipline

Use `scripts/park_quality.py` to preserve a stable checkpoint and audit evidence completeness. It does not parse the proprietary park format, watch the game or independently certify connectivity. Each PASS must have a reviewer, timestamp, observation note and hashed evidence file. Hash verification proves the copied bytes match, not that the park works. Missing/failed gates return NOT_READY; do not relabel them COMPLETE.

Progress terms: PROPOSED → PLACED → CONNECTED → GUEST_TESTED → THEMED → RELOADED_AND_ACCEPTED. Report each separately. Work occurs during actual tool sessions; do not imply an unattended year-long build continues between messages. Close PC2 normally when no active session needs it, without interrupting another controller or discarding unsaved work.

## Verified external implementation note

Frontier's Sorcery Pack listing describes OUTAMAX LSM Raid with quick switches/swing launches and OUTAMAX Bike and Sidecar with LSM launch. This confirms advertised mechanisms, not ownership or compatibility with a particular custom layout. Source: https://store.steampowered.com/app/3902620/ (checked October 27, 2026). Cedar Point's official Maverick description documents two launches and a 95-degree first drop; do not confuse that low-level multi-launch inspiration with the separate stand-up request. Source: https://www.sixflags.com/cedarpoint/attractions/maverick .
