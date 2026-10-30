# Park quality checks — evidence, not a simulator

Read [Approved Grid Build Contract](../APPROVED_GRID_BUILD_CONTRACT.md) first. `scripts/park_quality.py` never controls PC2, reads the live map, parses proprietary save internals, or automatically proves a path is connected. It provides non-overwriting backups and checks that a completion report has reviewed, hashed evidence for every required gate.

## Run tests

Python 3.10+; standard library only. No pip installation required.

```powershell
python -m unittest discover -s tests -v
```

All 13 synthetic unit tests passed on Raven on October 27, 2026, with zero failures/errors. They cover changed checkpoints, changed/missing evidence, failed queue gates, missing visual review, too few guest cycles, traversal paths, incomplete/changing saves and non-overwriting snapshots. These are code tests, NOT 13 successful rides or park simulation tests.

## Back up an actual game save

```powershell
python scripts/park_quality.py snapshot "<actual-save-path>.park2" "D:\RebelTechWorld\quality-audit-20261027\build\quality\snapshots"
```

Choose a named in-game save already written by PC2. The command checks source size/mtime and hashes before/after copying, then publishes a unique backup directory containing the .park2 and checkpoint.json. It never overwrites the original or an existing checkpoint. Empty or changing files fail. A successful copy explicitly records `in_game_reload_verified: false`; only an actual reload can change the evidence of that fact.

## Record an attraction's observations

Keep runtime evidence and park saves under ignored `build/`, never in the public repository. Use one JSON ledger per attraction/district and checkpoint. A ledger needs schema_version=1, area, checkpoint.file (relative to --root), checkpoint.sha256, complete_guest_cycles, and gates.

Required gates are listed in the module's GATES tuple. A passed gate requires status=pass, reviewed=true, a timezone-aware non-future observed_at timestamp, a nonempty observation note, and at least one evidence entry with file and sha256. Evidence paths are relative to --root; use forward slashes. Absolute paths, traversal, outside-root symlinks, missing files, empty files and mismatched hashes are rejected.

A starting ledger should set EVERY gate to unverified, reviewed=false, evidence=[], and complete_guest_cycles=0. Do not convert unknown state to PASS merely to make the command green. Record three observed complete boarding/ride/exit cycles, not three empty test runs.

```powershell
python scripts/park_quality.py audit build/quality/acceptance-live.json --root .
```

Exit 0 means EVIDENCE_COMPLETE, exit 2 means NOT_READY, exit 1 means invalid input or an I/O error. EVIDENCE_COMPLETE means the report is complete and its files match their hashes. It is NOT independent validation of the truth of the notes or screenshots. The actual in-game tests remain mandatory.

## Verified deployment in this session

The quality branch was cloned separately to `D:\RebelTechWorld\quality-audit-20261027` so the active game's source worktree and controller were not changed. An existing District Spine checkpoint (4,427,909 bytes) was copied to a new D: snapshot with matching SHA-256. A new unverified acceptance ledger was evaluated and correctly returned NOT_READY. No attraction was marked finished.

Live game control was reserved by another supervised path-repair session. This session did not send game inputs, take over its lease, close its game, overwrite its scripts, or merge into its worktree.
