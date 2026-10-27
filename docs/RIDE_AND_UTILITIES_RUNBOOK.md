# Rebel Tech World — PC2 Ride Access & Power Runbook
**Verified state:** October 27, 2026; game was cleanly exited after build session 003. This guide is an untested repair plan, not proof of repair.

## Snapshot: what is actually built
- Open latest park save **Rebel Tech World - Ride Test 02** (not the original baseline or Entrance 01).
- Entrance is a working ~8-meter-wide guest path leading from the tropical spawn buses to a T-junction.
- A built-in **360 Power** flat ride is placed on the *right-hand side* of the main boulevard.
- Ride panel displayed: "CLOSED", "This ride isn't accessible", "Place Entrance" ✓, "Place Exit" ✓, **"Connect Entrance to Path" ✗**, and **Power Used 0/36**.
- Several straight orange queue attempts displayed "Paths cannot cross". No functioning queue and no powered, open attraction has been observed.
- A safe rollback copy of the unmodified base park and saved entrance path exists on D:; the ride test itself is also backed up.
- The owner requested PC2 **remain closed** until it is actually needed. Do not relaunch for documentation or asset export tasks.

## Queue repair (next interactive game session)
1. Launch PC2 only after the next explicit construction task and load **Ride Test 02**.
2. Confirm the ride remains closed; enter its "Connect Entrance to Path" action to activate **queue path**, not standard guest path.
3. Start AT the ride's entrance marker (orange queue segment), draw a **short straight segment away from the gate first** before attempting a right-angle turn. Recent PC2 community reports note immediate tight turns can accidentally detach queue paths.
4. Continue with a gentle curve or one additional short segment toward the main boulevard. **End the queue at the edge of the regular guest path** where the snap/connection indicator turns valid; do not draw a queue *across* a regular path or across itself.
5. If red "Paths cannot cross" occurs, do NOT commit more bad geometry. Back out of the tool, examine the nodes, use edit-path / edit-point mode or remove only the invalid queue stub, then retry with a wider angle and more space. Screenshots at each attempt, labeled with success or failure, are useful.
6. Place a **normal guest path** from the ride's exit gate to the boulevard. Do not use orange queue path for the exit.
7. Return to the ride's summary/checklist and verify both connection statuses, then resolve electrical power before attempting to open. The Exit ✓ icon alone means a gate exists, not necessarily that a walkable path is complete.

## Electrical power
1. In **Facilities → Utilities**, place a standard generator or solar generator at a safe back-of-house site and a **Power Distributor** within the attraction's coverage area.
2. Use the game's power-cable construction tool/underground heatmap to connect **Generator → Distributor**, and verify the distributor can supply the ride. Proximity by itself does not guarantee the equipment is connected.
3. The placed **360 Power** ride reports a requirement of **36 power units** in the blueprint catalog. Ensure the power system is sufficiently supplied, not just physically nearby.
4. If the game displays no electricity available, check heatmap coverage and cable continuity. If workers/maintenance are missing, add those as indicated by the ride's current operational checklist.
5. Open only when the game's ride panel says access and power are valid. Observe guests entering the queue, boarding, and leaving; do not infer operation from a visually complete build.

## Milestone acceptance
- [ ] Ride entrance queue visibly connects to main guest path, no "Paths cannot cross".
- [ ] Ride exit links to guest path.
- [ ] Generator and distributor network supplies power to 360 Power.
- [ ] Ride reports OPEN and actually boards, operates and unloads guests.
- [ ] Save a distinct **Rebel Tech World - Ride Operational 03** checkpoint using in-game Save As.
- [ ] Copy its .park2 file to ignored build/backups/pc2 on D: and verify a SHA-256 match.
- [ ] Record screenshot/evidence, actual power requirements and exact errors in docs/BUILD_LOG.md. Do not commit game saves.

## References
- Frontier's official guide confirms rides require generators and connected distributors: https://www.planetcoaster.com/en-US/news/2024-09-25/deep-dive-mastering-management
- Xbox/Frontier overview explains regular guest paths, queues and power management: https://news.xbox.com/en-us/2024/11/06/planet-coaster-2-tips/
- Community discussion of queue detachment with sharp bends: https://www.reddit.com/r/PlanetCoaster2/comments/1vut52d/why_does_this_happen_every_time_i_create/
- Community path-edit technique for "Paths cannot cross": https://www.reddit.com/r/PlanetCoaster/comments/1uax44k/paths_cannot_cross/
- Community report of cable installation under Utilities and underground view: https://steamcommunity.com/app/2688950/discussions/0/595141926473186251/
