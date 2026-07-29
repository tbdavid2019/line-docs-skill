#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path


def count_documents(references_root: Path) -> int:
    return sum(
        1
        for path in references_root.rglob("*.md")
        if path.name != "INDEX.md"
    )


def build_manifest(
    references_root: Path,
    *,
    source_url: str,
    source_subfolder: str,
    upstream_commit: str,
    synced_at: str,
    language: str,
) -> dict[str, str | int]:
    return {
        "schema_version": 1,
        "source_url": source_url,
        "source_subfolder": source_subfolder,
        "upstream_commit": upstream_commit,
        "synced_at": synced_at,
        "language": language,
        "document_count": count_documents(references_root),
    }


def reusable_synced_at(
    previous_manifest_path: Path | None,
    manifest: dict[str, str | int],
    fallback: str,
) -> str:
    if not previous_manifest_path or not previous_manifest_path.is_file():
        return fallback
    try:
        previous = json.loads(
            previous_manifest_path.read_text(encoding="utf-8")
        )
        previous_timestamp = str(previous["synced_at"])
        datetime.fromisoformat(previous_timestamp.replace("Z", "+00:00"))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return fallback

    identity_fields = (
        "source_url",
        "source_subfolder",
        "upstream_commit",
        "language",
    )
    if all(previous.get(field) == manifest[field] for field in identity_fields):
        return previous_timestamp
    return fallback


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write provenance metadata for a synchronized snapshot."
    )
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--source-subfolder", required=True)
    parser.add_argument("--upstream-commit", required=True)
    parser.add_argument("--synced-at", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--previous-manifest", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_manifest(
        args.root,
        source_url=args.source_url,
        source_subfolder=args.source_subfolder,
        upstream_commit=args.upstream_commit,
        synced_at=args.synced_at,
        language=args.language,
    )
    manifest["synced_at"] = reusable_synced_at(
        args.previous_manifest,
        manifest,
        args.synced_at,
    )
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
