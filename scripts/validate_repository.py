#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

try:
    from .generate_index import generate_index
    from .write_sync_manifest import count_documents
except ImportError:
    from generate_index import generate_index
    from write_sync_manifest import count_documents


INDEX_LINK_PATTERN = re.compile(r"^- \[.*\]\(([^)]+\.md)\)$", re.MULTILINE)
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
UTC_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)
FRONTMATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
ACTION_REFERENCE_PATTERN = re.compile(
    r"^\s*uses:\s*[^@\s]+@([^\s#]+)",
    re.MULTILINE,
)
PINNED_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
OFFICIAL_SOURCE_URL = (
    "https://github.com/line/line-developers-docs-source.git"
)
MANDATORY_UPDATE_COMMAND = (
    "git -C <skill-directory> pull --ff-only origin skill"
)


def validate_references(references_root: Path) -> list[str]:
    errors: list[str] = []
    index_path = references_root / "INDEX.md"
    manifest_path = references_root / "SYNC_MANIFEST.json"

    if not index_path.is_file():
        errors.append(f"Missing generated index: {index_path}")
        return errors
    if not manifest_path.is_file():
        errors.append(f"Missing sync manifest: {manifest_path}")
        return errors

    current_index = index_path.read_text(encoding="utf-8")
    expected_index = generate_index(references_root)
    if current_index != expected_index:
        errors.append("references/INDEX.md is not up to date")

    indexed_paths = INDEX_LINK_PATTERN.findall(current_index)
    document_paths = sorted(
        path.relative_to(references_root).as_posix()
        for path in references_root.rglob("*.md")
        if path.name != "INDEX.md"
    )
    if sorted(indexed_paths) != document_paths:
        errors.append("INDEX.md entries do not exactly match source documents")
    for relative_path in indexed_paths:
        if relative_path.startswith("/") or ".." in Path(relative_path).parts:
            errors.append(f"Unsafe index path: {relative_path}")
        elif not (references_root / relative_path).is_file():
            errors.append(f"Broken index path: {relative_path}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"Invalid sync manifest: {error}")
        return errors
    if not isinstance(manifest, dict):
        errors.append("Invalid sync manifest: root value must be an object")
        return errors

    required_fields = {
        "schema_version",
        "source_url",
        "source_subfolder",
        "upstream_commit",
        "synced_at",
        "language",
        "document_count",
    }
    missing_fields = sorted(required_fields - manifest.keys())
    if missing_fields:
        errors.append(
            "Sync manifest is missing fields: " + ", ".join(missing_fields)
        )
        return errors

    if manifest["schema_version"] != 1:
        errors.append("Unsupported sync manifest schema_version")
    if not COMMIT_PATTERN.fullmatch(str(manifest["upstream_commit"])):
        errors.append("Sync manifest has an invalid upstream_commit")
    if not UTC_TIMESTAMP_PATTERN.fullmatch(str(manifest["synced_at"])):
        errors.append("Sync manifest has an invalid synced_at timestamp")
    if not str(manifest["source_url"]).strip():
        errors.append("Sync manifest source_url must not be empty")
    if not str(manifest["language"]).strip():
        errors.append("Sync manifest language must not be empty")
    if manifest["document_count"] != count_documents(references_root):
        errors.append("Sync manifest document_count is incorrect")

    return errors


def validate_repository(project_root: Path) -> list[str]:
    errors = validate_references(project_root / "references")
    required_files = (
        "SKILL.md",
        "README.md",
        "README_TW.md",
        "NOTICE.md",
        "CHANGELOG.md",
        "agents/openai.yaml",
        "evals/routing_cases.json",
        ".github/workflows/auto-sync.yml",
        ".github/workflows/validate.yml",
    )
    for relative_path in required_files:
        if not (project_root / relative_path).is_file():
            errors.append(f"Missing required repository file: {relative_path}")

    skill_path = project_root / "SKILL.md"
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        frontmatter_match = FRONTMATTER_PATTERN.match(skill_text)
        if not frontmatter_match:
            errors.append("SKILL.md has invalid YAML frontmatter boundaries")
        else:
            metadata: dict[str, str] = {}
            for line in frontmatter_match.group(1).splitlines():
                key, separator, value = line.partition(":")
                if separator:
                    metadata[key.strip()] = value.strip()
            if set(metadata) != {"name", "description"}:
                errors.append(
                    "SKILL.md frontmatter must contain only name and description"
                )
            if metadata.get("name") != "line-docs-skill":
                errors.append("SKILL.md has an unexpected skill name")
            description = metadata.get("description", "")
            if "Routes LINE Platform" not in description:
                errors.append("SKILL.md description must state what it provides")
            if "Use when" not in description:
                errors.append("SKILL.md description must include trigger contexts")
            if len(description) > 1024:
                errors.append("SKILL.md description exceeds 1024 characters")

        required_sections = (
            "## Scope Boundary",
            "## Freshness Boundary",
            "## Safety Boundary",
            "## Minimal-Context Lookup",
            "## Core Routing Map",
            "## Diagnostic Workflow",
            "## Response Contract",
            "## Verification",
        )
        for section in required_sections:
            if section not in skill_text:
                errors.append(f"SKILL.md is missing section: {section}")
        if len(skill_text.splitlines()) > 500:
            errors.append("SKILL.md exceeds the 500-line context budget")
        if "scripts/" in skill_text or ".py" in skill_text:
            errors.append(
                "SKILL.md must not direct installed Skills to maintenance code"
            )
        if "Before every LINE documentation task" not in skill_text:
            errors.append("SKILL.md does not require refresh before every task")
        if MANDATORY_UPDATE_COMMAND not in skill_text:
            errors.append("SKILL.md does not contain the mandatory pull command")
        if "If the pull fails" not in skill_text:
            errors.append("SKILL.md does not define pull failure behavior")

    manifest_path = project_root / "references" / "SYNC_MANIFEST.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            manifest = None
        if isinstance(manifest, dict):
            if manifest.get("source_url") != OFFICIAL_SOURCE_URL:
                errors.append(
                    "Repository manifest does not use the official source"
                )
            if manifest.get("source_subfolder") != "docs/en":
                errors.append("Repository manifest must track docs/en")
            if manifest.get("language") != "en":
                errors.append(
                    "Repository manifest must identify English content"
                )

    for readme_name in ("README.md", "README_TW.md"):
        readme_path = project_root / readme_name
        if not readme_path.is_file():
            continue
        readme = readme_path.read_text(encoding="utf-8")
        if re.search(r"\b\d{3,}\+\s+Markdown", readme, re.IGNORECASE):
            errors.append(f"{readme_name} contains a stale fixed document count")
        if "SYNC_MANIFEST.json" not in readme:
            errors.append(f"{readme_name} does not explain provenance metadata")
        if "NOTICE.md" not in readme:
            errors.append(f"{readme_name} does not link the licensing boundary")
        if "--branch skill --single-branch" not in readme:
            errors.append(
                f"{readme_name} must install from the runtime skill branch"
            )
        if "install-skill.sh" in readme:
            errors.append(
                f"{readme_name} still references the obsolete installer"
            )
        if "AI Agent Installation Contract" not in readme:
            errors.append(
                f"{readme_name} has no AI Agent Installation Contract"
            )
        if MANDATORY_UPDATE_COMMAND not in readme:
            errors.append(
                f"{readme_name} does not contain the mandatory pull command"
            )
        for runtime_file in (
            "references/SYNC_MANIFEST.json",
            "references/INDEX.md",
        ):
            if runtime_file not in readme:
                errors.append(
                    f"{readme_name} does not verify {runtime_file}"
                )

    for script_name in (
        "sync-docs.sh",
        "build-skill-package.sh",
        "publish-skill.sh",
    ):
        script_path = project_root / "scripts" / script_name
        if not os.access(script_path, os.X_OK):
            errors.append(f"Maintenance script is not executable: {script_name}")

    workflows_root = project_root / ".github" / "workflows"
    if workflows_root.is_dir():
        for workflow_path in workflows_root.glob("*.yml"):
            workflow = workflow_path.read_text(encoding="utf-8")
            for reference in ACTION_REFERENCE_PATTERN.findall(workflow):
                if not PINNED_COMMIT_PATTERN.fullmatch(reference):
                    errors.append(
                        f"{workflow_path.name} has an unpinned action: {reference}"
                    )
            if "timeout-minutes:" not in workflow:
                errors.append(f"{workflow_path.name} has no timeout")
            if "concurrency:" not in workflow:
                errors.append(f"{workflow_path.name} has no concurrency policy")

        for workflow_name in ("auto-sync.yml", "validate.yml"):
            workflow_path = workflows_root / workflow_name
            if workflow_path.is_file():
                workflow = workflow_path.read_text(encoding="utf-8")
                if "bash scripts/publish-skill.sh" not in workflow:
                    errors.append(
                        f"{workflow_name} does not publish the runtime branch"
                    )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate generated artifacts.")
    parser.add_argument(
        "--references-only",
        type=Path,
        help="Validate only a staged references directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.references_only:
        errors = validate_references(args.references_only.resolve())
    else:
        project_root = Path(__file__).resolve().parents[1]
        errors = validate_repository(project_root)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
