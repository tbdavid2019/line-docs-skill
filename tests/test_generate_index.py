from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.generate_index import extract_title, generate_index


class GenerateIndexTests(unittest.TestCase):
    def test_extract_title_prefers_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            document = Path(temporary_directory) / "page.md"
            document.write_text(
                "---\ntitle: Frontmatter title\n---\n# Heading title\n",
                encoding="utf-8",
            )

            self.assertEqual(extract_title(document), "Frontmatter title")

    def test_generate_index_is_deterministic_and_excludes_generated_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            references = Path(temporary_directory)
            topic = references / "docs" / "messaging-api"
            topic.mkdir(parents=True)
            (topic / "overview.md").write_text("# Overview\n", encoding="utf-8")
            (references / "INDEX.md").write_text("old index", encoding="utf-8")
            (references / "SYNC_MANIFEST.json").write_text("{}", encoding="utf-8")

            first = generate_index(references)
            second = generate_index(references)

            self.assertEqual(first, second)
            self.assertIn(
                "[Overview](docs/messaging-api/overview.md)",
                first,
            )
            self.assertNotIn("INDEX.md", first)
            self.assertNotIn("SYNC_MANIFEST.json", first)

    def test_extract_title_reports_unreadable_documents(self) -> None:
        missing_document = Path("/definitely/missing/line-docs-page.md")

        with self.assertRaises(OSError):
            extract_title(missing_document)


if __name__ == "__main__":
    unittest.main()
