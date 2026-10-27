"""Offline checkpoint backup and evidence gate for Rebel Tech World.

Does not launch/control PC2, parse proprietary saves, or certify path connectivity.
It validates saved evidence records; visual/guest tests must be performed in-game.
Python 3.10+, standard library only. All backup destinations are user-selected.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GATES = (
    "entrance_reachable", "queue_connected", "exit_connected", "ride_open",
    "guests_boarded", "guests_exited", "services_reachable", "clearances_checked",
    "save_reloaded", "custom_rt_theme", "no_exposed_grass", "performance_reviewed",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def contained(root: Path, value: Any) -> Path:
    """Resolve a manifest-relative file, rejecting traversal and outside symlinks."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("File reference must be a nonempty relative path")
    relative = Path(value)
    # Reject both Windows and Unix absolute forms on either host OS.
    if relative.is_absolute() or ":" in value or "\\" in value or ".." in relative.parts:
        raise ValueError(f"Unsafe file reference: {value!r}")
    result = (root.resolve() / relative).resolve()
    if not result.is_relative_to(root.resolve()) or not result.is_file():
        raise ValueError(f"Missing or outside-root file: {value!r}")
    return result


def snapshot(source: Path, destination_root: Path) -> dict[str, Any]:
    """Copy one stable existing .park2 to a new directory; never overwrite a save."""
    source = source.resolve(strict=True)
    if source.suffix.lower() != ".park2" or not source.is_file():
        raise ValueError("Select an existing .park2 save, not an autosave or directory")
    if source.stat().st_size == 0:
        raise ValueError("Save is empty or still being written; no snapshot made")
    destination_root.mkdir(parents=True, exist_ok=True)
    before = source.stat()
    original_hash = digest(source)
    temporary = Path(tempfile.mkdtemp(prefix=".pending-", dir=destination_root))
    try:
        copy = temporary / source.name
        shutil.copy2(source, copy)
        copied_hash = digest(copy)
        after = source.stat()
        final_source_hash = digest(source)
        if ((before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns)
                or original_hash != copied_hash or original_hash != final_source_hash):
            raise ValueError("Save changed during backup; discarded incomplete snapshot")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        folder = destination_root / (stamp + "-" + uuid.uuid4().hex[:12])
        record = {
            "schema_version": 1, "created_utc": datetime.now(timezone.utc).isoformat(),
            "save_file": source.name, "bytes": copy.stat().st_size,
            "sha256": copied_hash, "copy_integrity": "verified",
            "in_game_reload_verified": False,
            "note": "Byte-identical backup only; does not prove the park is functional.",
        }
        (temporary / "checkpoint.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        # Unique destination: rename fails rather than overwrite another snapshot.
        temporary.rename(folder)
        return {**record, "backup_directory": str(folder)}
    except BaseException:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


def audit(document: dict[str, Any], root: Path) -> dict[str, Any]:
    """Check evidence completeness and hashes. This is not a visual game test."""
    issues: list[str] = []
    if document.get("schema_version") != 1:
        issues.append("schema_version must be 1")
    if not isinstance(document.get("area"), str) or not document.get("area", "").strip():
        issues.append("area must identify the attraction or district")
    checkpoint = document.get("checkpoint")
    if not isinstance(checkpoint, dict):
        issues.append("checkpoint record missing")
        checkpoint = {}
    expected = checkpoint.get("sha256")
    try:
        save = contained(root, checkpoint.get("file"))
        if save.suffix.lower() != ".park2" or save.stat().st_size == 0:
            issues.append("checkpoint is not a nonempty .park2 save")
        if not isinstance(expected, str) or len(expected) != 64 or digest(save) != expected.lower():
            issues.append("checkpoint SHA-256 missing or mismatched")
    except (ValueError, OSError) as exc:
        issues.append(f"checkpoint: {exc}")
    cycles = document.get("complete_guest_cycles")
    if type(cycles) is not int or cycles < 3:
        issues.append("At least three observed guest boarding/ride/exit cycles required")
    gates = document.get("gates")
    if not isinstance(gates, dict):
        issues.append("gates must be an object")
        gates = {}
    for name in GATES:
        entry = gates.get(name)
        if not isinstance(entry, dict) or entry.get("status") != "pass":
            issues.append(f"{name}: not passed")
            continue
        if entry.get("reviewed") is not True:
            issues.append(f"{name}: needs an explicit human/agent visual review")
        if not isinstance(entry.get("note"), str) or not entry.get("note", "").strip():
            issues.append(f"{name}: observation note missing")
        try:
            when = datetime.fromisoformat(entry.get("observed_at", ""))
            if when.tzinfo is None:
                raise ValueError("timezone required")
            if when > datetime.now(timezone.utc):
                raise ValueError("future observation")
        except (ValueError, TypeError):
            issues.append(f"{name}: valid non-future observation timestamp required")
        evidence = entry.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            issues.append(f"{name}: supporting evidence files missing")
            continue
        for item in evidence:
            try:
                if not isinstance(item, dict):
                    raise ValueError("evidence entry must be an object")
                file = contained(root, item.get("file"))
                if file.stat().st_size == 0 or digest(file) != str(item.get("sha256", "")).lower():
                    raise ValueError("evidence empty or SHA-256 mismatch")
            except (ValueError, OSError) as exc:
                issues.append(f"{name}: {exc}")
    return {
        "area": document.get("area"),
        "result": "EVIDENCE_COMPLETE" if not issues else "NOT_READY",
        "automatically_verified_in_game": False,
        "issues": issues,
        "note": "Evidence completeness is not independent proof that observations are correct.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    backup = commands.add_parser("snapshot", help="Back up a stable .park2 without overwriting")
    backup.add_argument("source", type=Path)
    backup.add_argument("destination", type=Path)
    check = commands.add_parser("audit", help="Read-only check of recorded evidence")
    check.add_argument("manifest", type=Path)
    check.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "snapshot":
            result = snapshot(args.source, args.destination)
            code = 0
        else:
            document = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
            if not isinstance(document, dict):
                raise ValueError("Manifest must be a JSON object")
            result = audit(document, args.root)
            code = 0 if result["result"] == "EVIDENCE_COMPLETE" else 2
        print(json.dumps(result, indent=2))
        return code
    except (OSError, ValueError) as exc:
        print(json.dumps({"result": "ERROR", "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
