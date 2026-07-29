from __future__ import annotations

import tempfile
import subprocess
import unittest
from pathlib import Path

from scripts.validate_repository import validate_repository


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_repository_validator_passes(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/validate_repository.py"],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_skill_routing_evaluations_pass(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/run_skill_evals.py"],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_manifest_is_reported_without_crashing(self) -> None:
        for invalid_manifest in ("not-json\n", "[]\n"):
            with self.subTest(invalid_manifest=invalid_manifest):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    project_root = Path(temporary_directory)
                    references = project_root / "references"
                    references.mkdir()
                    (references / "INDEX.md").write_text(
                        "# LINE Developers Documentation Index\n\n"
                        "This is a comprehensive index of the synchronized "
                        "LINE Developers documentation, organized by "
                        "category.\n",
                        encoding="utf-8",
                    )
                    (references / "SYNC_MANIFEST.json").write_text(
                        invalid_manifest,
                        encoding="utf-8",
                    )

                    errors = validate_repository(project_root)

                    self.assertTrue(
                        any(
                            "Invalid sync manifest" in error
                            for error in errors
                        )
                    )


if __name__ == "__main__":
    unittest.main()
