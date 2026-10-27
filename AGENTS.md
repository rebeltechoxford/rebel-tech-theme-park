# Rebel Tech World — Agent Instructions

Read README.md and docs/TMT_PIPELINE.md before changing assets. Notion hub: https://app.notion.com/p/4066b61e436e8102931fe868f8ac2ee3?pvs=204

## Scope and current state
- Target: an original playable theme park in Planet Coaster 1, using Blender-authored scenery.
- Machine: Windows PC **Raven**; intended working directory D:\RebelTechWorld (inspect free space first).
- On 2026-10-27 the Remote Desktop Commander device **Raven** was offline. Do not claim local changes or tests until connectivity is confirmed.
- Initial README is committed. Blender/game/Toolkit integration has NOT been tested on Raven yet.

## Agents: ChatGPT, Claude, Grokbot
- Use short descriptive branches, small commits, and reviewable PRs; no automatic merges of untested changes.
- Never assume any other agent has access to this repo, machine, Notion, or a third-party account.
- Record each task in docs/BUILD_LOG.md: date, agent, changed files, evidence, blockers, next step.
- Mark speculative concepts PROPOSED and unexecuted code UNTESTED, not COMPLETE.
- Do not expose personal paths, usernames, browser cookies, Steam tokens, passwords, or device information publicly.
- Source assets must be original or have explicit compatible licenses; record attribution and source URLs.

## Build safety
1. Treat D: as the default source/build drive; do not relocate Windows profiles or Steam libraries without separate approval.
2. Run the read-only scripts/preflight.ps1 before creating or downloading anything on Raven.
3. Favor official Frontier Toolkit import, in-game construction, and normal save mechanisms. No binary patching or undocumented save editing.
4. Respect the game's license and service terms; don't implement unattended gameplay automation or service scraping unless permitted.
5. The Toolkit is a website, not an EXE installer; Steam sign-in and license acceptance remain owner-controlled.
6. Avoid installs or downloads from unverified sources. Never commit game files, installed applications, third-party models without rights, or generated save files.
7. Create a minimal scenery item and verify import before scaling to a full district.

## Acceptance gate for the first milestone
- Raven drive and tool versions observed.
- Blender model generator runs with no errors and an original .blend/.fbx is produced on D:.
- Thememaker's Toolkit accepts the ZIP and returns a .pcugc.
- The item appears in Planet Coaster; save, exit, reload, and screenshot evidence reviewed.
- No claim that in-game construction is autonomous until separately validated and allowed.
