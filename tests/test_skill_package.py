from __future__ import annotations

import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.support import commit_all, init_git_repository, run


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = REPOSITORY_ROOT / "scripts" / "build-skill-package.sh"
EXPECTED_TOP_LEVEL = {
    "SKILL.md",
    "agents",
    "references",
    "LICENSE",
    "NOTICE.md",
}


class SkillPackageTests(unittest.TestCase):
    def test_build_contains_only_runtime_skill_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            package_root = Path(temporary_directory) / "line-docs-skill"
            result = subprocess.run(
                ["bash", str(BUILD_SCRIPT), str(package_root)],
                cwd=REPOSITORY_ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(
                {path.name for path in package_root.iterdir()},
                EXPECTED_TOP_LEVEL,
            )
            self.assertTrue((package_root / "agents" / "openai.yaml").is_file())
            self.assertTrue(
                (
                    package_root
                    / "references"
                    / "SYNC_MANIFEST.json"
                ).is_file()
            )

            packaged_files = [
                path.relative_to(package_root).as_posix()
                for path in package_root.rglob("*")
                if path.is_file()
            ]
            self.assertFalse(
                any(path.endswith((".py", ".pyc", ".sh")) for path in packaged_files)
            )
            self.assertFalse(
                {"scripts", "tests", "docs", "evals", ".github"}
                & {path.parts[0] for path in package_root.rglob("*")}
            )

    def test_publish_creates_and_idempotently_updates_runtime_branch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repository = root / "maintenance"
            remote = root / "remote.git"
            init_git_repository(repository)

            for directory in ("scripts", "agents", "references"):
                (repository / directory).mkdir()
            for filename in ("SKILL.md", "LICENSE", "NOTICE.md"):
                shutil.copy2(REPOSITORY_ROOT / filename, repository / filename)
            shutil.copy2(
                REPOSITORY_ROOT / "agents" / "openai.yaml",
                repository / "agents" / "openai.yaml",
            )
            for filename in ("INDEX.md", "SYNC_MANIFEST.json"):
                shutil.copy2(
                    REPOSITORY_ROOT / "references" / filename,
                    repository / "references" / filename,
                )
            for filename in (
                "build-skill-package.sh",
                "publish-skill.sh",
            ):
                shutil.copy2(
                    REPOSITORY_ROOT / "scripts" / filename,
                    repository / "scripts" / filename,
                )

            commit_all(repository, "add maintenance source")
            run("git", "init", "--bare", str(remote), cwd=root)
            run("git", "remote", "add", "origin", str(remote), cwd=repository)
            run("git", "push", "-u", "origin", "main", cwd=repository)

            first_publish = run(
                "bash",
                "scripts/publish-skill.sh",
                cwd=repository,
                check=False,
            )
            self.assertEqual(
                first_publish.returncode,
                0,
                first_publish.stdout + first_publish.stderr,
            )

            published_files = set(
                run(
                    "git",
                    "--git-dir",
                    str(remote),
                    "ls-tree",
                    "-r",
                    "--name-only",
                    "skill",
                    cwd=root,
                ).stdout.splitlines()
            )
            self.assertEqual(
                published_files,
                {
                    "LICENSE",
                    "NOTICE.md",
                    "SKILL.md",
                    "agents/openai.yaml",
                    "references/INDEX.md",
                    "references/SYNC_MANIFEST.json",
                },
            )

            second_publish = run(
                "bash",
                "scripts/publish-skill.sh",
                cwd=repository,
                check=False,
            )
            self.assertEqual(
                second_publish.returncode,
                0,
                second_publish.stdout + second_publish.stderr,
            )
            self.assertIn(
                "Runtime Skill branch is already current.",
                second_publish.stdout,
            )


if __name__ == "__main__":
    unittest.main()
