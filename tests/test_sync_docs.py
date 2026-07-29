from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from tests.support import commit_all, init_git_repository, run


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SYNC_SCRIPT = REPOSITORY_ROOT / "scripts" / "sync-docs.sh"


class SyncDocsTests(unittest.TestCase):
    def create_upstream_repository(self, root: Path) -> tuple[Path, str]:
        upstream = root / "upstream"
        init_git_repository(upstream)
        docs = upstream / "docs" / "en" / "docs" / "messaging-api"
        docs.mkdir(parents=True)
        (docs / "overview.md").write_text(
            "# Messaging API overview\n",
            encoding="utf-8",
        )
        commit = commit_all(upstream, "add upstream docs")
        return upstream, commit

    def sync_environment(
        self,
        upstream: Path,
        destination: Path,
    ) -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(
            {
                "LINE_DOCS_REPO_URL": str(upstream),
                "LINE_DOCS_SOURCE_SUBFOLDER": "docs/en",
                "LINE_DOCS_DEST_DIR": str(destination),
                "LINE_DOCS_SYNCED_AT": "2026-07-29T00:00:00Z",
            }
        )
        return environment

    def test_replaces_destination_exactly_and_writes_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            upstream, upstream_commit = self.create_upstream_repository(root)
            destination = root / "references"
            destination.mkdir()
            (destination / "stale.md").write_text("stale\n", encoding="utf-8")

            result = run(
                "bash",
                str(SYNC_SCRIPT),
                cwd=REPOSITORY_ROOT,
                check=False,
                env=self.sync_environment(upstream, destination),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((destination / "stale.md").exists())
            self.assertTrue(
                (
                    destination
                    / "docs"
                    / "messaging-api"
                    / "overview.md"
                ).is_file()
            )
            self.assertTrue((destination / "INDEX.md").is_file())
            manifest = json.loads(
                (destination / "SYNC_MANIFEST.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["upstream_commit"], upstream_commit)
            self.assertEqual(manifest["synced_at"], "2026-07-29T00:00:00Z")
            self.assertEqual(manifest["document_count"], 1)
            self.assertEqual(manifest["language"], "en")

    def test_failed_clone_preserves_existing_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            destination = root / "references"
            destination.mkdir()
            marker = destination / "existing.md"
            marker.write_text("existing\n", encoding="utf-8")
            missing_upstream = root / "missing-upstream"

            result = run(
                "bash",
                str(SYNC_SCRIPT),
                cwd=REPOSITORY_ROOT,
                check=False,
                env=self.sync_environment(missing_upstream, destination),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(marker.read_text(encoding="utf-8"), "existing\n")


if __name__ == "__main__":
    unittest.main()
