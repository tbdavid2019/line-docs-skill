#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


GENERATED_FILENAMES = {"INDEX.md"}
SKIPPED_DIRECTORIES = {"assets", "images", "img", "static"}


def extract_title(file_path: str | Path) -> str:
    """Extract a useful title from frontmatter, the first H1, or the filename."""
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")

    frontmatter_match = re.search(
        r"^---\s*\n(.*?)\n---\s*\n",
        content,
        re.DOTALL,
    )
    if frontmatter_match:
        for line in frontmatter_match.group(1).splitlines():
            key, separator, value = line.partition(":")
            if separator and key.strip() == "title":
                title = value.strip().strip("\"'")
                if title:
                    return title

    h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()

    if path.name.lower() == "index.md":
        parent_name = path.parent.name
        if parent_name and parent_name != "references":
            return _humanize(parent_name)
        return "Overview"

    return _humanize(path.stem)


def _humanize(value: str) -> str:
    return value.replace("-", " ").replace("_", " ").capitalize()


def _category_name(relative_directory: Path) -> str:
    if relative_directory == Path("."):
        return "General"
    return " > ".join(_humanize(part).title() for part in relative_directory.parts)


def generate_index(root_dir: str | Path) -> str:
    """Return a deterministic Markdown index for all source documents."""
    root_path = Path(root_dir).resolve()
    categories: dict[str, list[str]] = {}

    for current_root, directories, filenames in os.walk(root_path):
        directories[:] = sorted(
            directory
            for directory in directories
            if not directory.startswith(".")
            and directory not in SKIPPED_DIRECTORIES
        )
        markdown_files = sorted(
            filename
            for filename in filenames
            if filename.endswith(".md")
            and filename not in GENERATED_FILENAMES
        )
        if not markdown_files:
            continue

        current_path = Path(current_root)
        category = _category_name(current_path.relative_to(root_path))
        entries: list[str] = []
        for filename in markdown_files:
            full_path = current_path / filename
            title = extract_title(full_path)
            link_path = full_path.relative_to(root_path).as_posix()
            entries.append(f"- [{title}]({link_path})")
        categories.setdefault(category, []).extend(entries)

    lines = [
        "# LINE Developers Documentation Index",
        "",
        (
            "This is a comprehensive index of the synchronized LINE Developers "
            "documentation, organized by category."
        ),
        "",
    ]

    for category in sorted(
        categories,
        key=lambda value: (value != "General", value.lower()),
    ):
        lines.append(f"## {category}")
        lines.extend(categories[category])
        lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    default_root = project_root / "references"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output = (args.output or root / "INDEX.md").resolve()
    if not root.is_dir():
        raise SystemExit(f"Reference directory does not exist: {root}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generate_index(root), encoding="utf-8")
    print(f"Generated {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
