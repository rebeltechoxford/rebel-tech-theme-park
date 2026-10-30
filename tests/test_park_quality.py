"""Synthetic fixtures test the audit logic, never actual park functionality."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("park_quality", Path(__file__).resolve().parents[1] / "scripts" / "park_quality.py")
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)


class QualityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.save = self.root / "synthetic.park2"
        self.save.write_bytes(b"UNIT TEST FIXTURE - NOT A REAL PARK")
        self.evidence = self.root / "synthetic-observation.txt"
        self.evidence.write_text("UNIT TEST EVIDENCE - NOT A GAME OBSERVATION")
        record = {"status": "pass", "reviewed": True, "note": "synthetic test fixture",
                  "observed_at": "2026-01-01T00:00:00+00:00",
                  "evidence": [{"file": self.evidence.name, "sha256": q.digest(self.evidence)}]}
        self.document = {"schema_version": 1, "area": "SYNTHETIC TEST ONLY", "complete_guest_cycles": 3,
                         "checkpoint": {"file": self.save.name, "sha256": q.digest(self.save)},
                         "gates": {name: copy.deepcopy(record) for name in q.GATES}}

    def tearDown(self):
        self.tmp.cleanup()

    def test_complete_record_is_evidence_only(self):
        result = q.audit(self.document, self.root)
        self.assertEqual(result["result"], "EVIDENCE_COMPLETE")
        self.assertFalse(result["automatically_verified_in_game"])

    def test_empty_record_is_not_ready(self):
        self.assertEqual(q.audit({}, self.root)["result"], "NOT_READY")

    def test_failed_queue_blocks(self):
        self.document["gates"]["queue_connected"]["status"] = "fail"
        self.assertEqual(q.audit(self.document, self.root)["result"], "NOT_READY")

    def test_no_evidence_blocks(self):
        self.document["gates"]["guests_boarded"]["evidence"] = []
        self.assertEqual(q.audit(self.document, self.root)["result"], "NOT_READY")

    def test_changed_checkpoint_blocks(self):
        self.save.write_bytes(b"DIFFERENT BUILD")
        self.assertEqual(q.audit(self.document, self.root)["result"], "NOT_READY")

    def test_changed_evidence_blocks(self):
        self.evidence.write_text("changed")
        self.assertEqual(q.audit(self.document, self.root)["result"], "NOT_READY")

    def test_missing_visual_review_blocks(self):
        self.document["gates"]["exit_connected"]["reviewed"] = False
        self.assertEqual(q.audit(self.document, self.root)["result"], "NOT_READY")

    def test_insufficient_cycles_blocks(self):
        for value in (0, 2, True, "3"):
            self.document["complete_guest_cycles"] = value
            self.assertEqual(q.audit(self.document, self.root)["result"], "NOT_READY")

    def test_unsafe_paths_rejected(self):
        for value in ("../escape.txt", "/tmp/outside", "C:/private/file", "..\\escape", ""):
            with self.assertRaises(ValueError):
                q.contained(self.root, value)

    def test_snapshot_is_verified_and_does_not_overwrite(self):
        a = q.snapshot(self.save, self.root / "backups")
        b = q.snapshot(self.save, self.root / "backups")
        self.assertNotEqual(a["backup_directory"], b["backup_directory"])
        self.assertEqual(a["sha256"], q.digest(self.save))
        self.assertFalse(a["in_game_reload_verified"])

    def test_empty_save_rejected(self):
        self.save.write_bytes(b"")
        with self.assertRaises(ValueError):
            q.snapshot(self.save, self.root / "backups")

    def test_changing_save_rejected(self):
        real_copy = q.shutil.copy2
        def changing(src, dest):
            result = real_copy(src, dest)
            src.write_bytes(b"UPDATED WHILE COPYING")
            return result
        with patch.object(q.shutil, "copy2", changing):
            with self.assertRaises(ValueError):
                q.snapshot(self.save, self.root / "backups")
        self.assertEqual(list((self.root / "backups").iterdir()), [])

    def test_future_timestamp_rejected(self):
        self.document["gates"]["ride_open"]["observed_at"] = "2999-01-01T00:00:00+00:00"
        self.assertEqual(q.audit(self.document, self.root)["result"], "NOT_READY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
