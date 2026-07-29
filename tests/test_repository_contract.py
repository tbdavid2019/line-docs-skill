from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate_repository import validate_repository


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MANDATORY_UPDATE_COMMAND = (
    "git -C <skill-directory> pull --ff-only origin skill"
)


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

    def test_ai_agent_contract_requires_refresh_before_use(self) -> None:
        for readme_name in ("README.md", "README_TW.md"):
            with self.subTest(readme=readme_name):
                readme = (REPOSITORY_ROOT / readme_name).read_text(
                    encoding="utf-8"
                )
                self.assertIn("AI Agent Installation Contract", readme)
                self.assertIn(MANDATORY_UPDATE_COMMAND, readme)
                self.assertIn("references/SYNC_MANIFEST.json", readme)
                self.assertIn("references/INDEX.md", readme)

        skill = (REPOSITORY_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Before every LINE documentation task", skill)
        self.assertIn(MANDATORY_UPDATE_COMMAND, skill)
        self.assertIn("If the pull fails", skill)
        self.assertNotIn(
            "Do not run `git pull` or mutate the installed Skill",
            skill,
        )

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
