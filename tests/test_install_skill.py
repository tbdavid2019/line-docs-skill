from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from tests.support import commit_all, init_git_repository, run


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = REPOSITORY_ROOT / "scripts" / "install-skill.sh"


class InstallSkillTests(unittest.TestCase):
    def create_source_repository(self, root: Path) -> Path:
        source = root / "source"
        init_git_repository(source)
        (source / "SKILL.md").write_text(
            "---\nname: line-docs-skill\ndescription: Test skill.\n---\n",
            encoding="utf-8",
        )
        commit_all(source, "initial skill")
        return source

    def installer_environment(self, source: Path) -> dict[str, str]:
        environment = os.environ.copy()
        environment["LINE_DOCS_SKILL_REPO_URL"] = str(source)
        return environment

    def test_installs_missing_target_as_git_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = self.create_source_repository(root)
            target = root / "installed"

            result = run(
                "bash",
                str(INSTALL_SCRIPT),
                str(target),
                cwd=REPOSITORY_ROOT,
                check=False,
                env=self.installer_environment(source),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / ".git").is_dir())
            self.assertTrue((target / "SKILL.md").is_file())

    def test_updates_clean_checkout_with_matching_origin(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = self.create_source_repository(root)
            target = root / "installed"
            environment = self.installer_environment(source)
            run(
                "bash",
                str(INSTALL_SCRIPT),
                str(target),
                cwd=REPOSITORY_ROOT,
                env=environment,
            )

            (source / "version.txt").write_text("v2\n", encoding="utf-8")
            latest_commit = commit_all(source, "update skill")
            result = run(
                "bash",
                str(INSTALL_SCRIPT),
                str(target),
                cwd=REPOSITORY_ROOT,
                check=False,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            installed_commit = run(
                "git",
                "rev-parse",
                "HEAD",
                cwd=target,
            ).stdout.strip()
            self.assertEqual(installed_commit, latest_commit)

    def test_rejects_dirty_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = self.create_source_repository(root)
            target = root / "installed"
            environment = self.installer_environment(source)
            run(
                "bash",
                str(INSTALL_SCRIPT),
                str(target),
                cwd=REPOSITORY_ROOT,
                env=environment,
            )
            (target / "SKILL.md").write_text("dirty\n", encoding="utf-8")

            result = run(
                "bash",
                str(INSTALL_SCRIPT),
                str(target),
                cwd=REPOSITORY_ROOT,
                check=False,
                env=environment,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(
                (target / "SKILL.md").read_text(encoding="utf-8"),
                "dirty\n",
            )

    def test_rejects_existing_non_git_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = self.create_source_repository(root)
            target = root / "installed"
            target.mkdir()
            marker = target / "keep.txt"
            marker.write_text("keep\n", encoding="utf-8")

            result = run(
                "bash",
                str(INSTALL_SCRIPT),
                str(target),
                cwd=REPOSITORY_ROOT,
                check=False,
                env=self.installer_environment(source),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep\n")


if __name__ == "__main__":
    unittest.main()
