# Changelog

All notable changes to this repository are documented in this file.

## 2026-07-29 — Runtime distribution correction

This section supersedes the same-day installer model described below.

### Corrected

- Split the repository into two responsibilities: `main` is maintainer source,
  while the generated `skill` branch is the only end-user installation target.
- Removed `install-skill.sh`. Users now clone or update the `skill` branch with
  Git and never execute repository Python or maintenance scripts.
- Added an allowlist-based runtime package builder. Published Skills contain
  only `SKILL.md`, `agents/`, `references/`, `LICENSE`, and `NOTICE.md`.
- Added contract coverage proving the package excludes Python, shell scripts,
  tests, workflows, evals, maintainer docs, README files, and changelog.
- Added automated `skill` branch publication after validated `main` pushes and
  after the daily documentation synchronization workflow. This is necessary
  because pushes made by one GitHub Actions workflow do not start another
  workflow automatically.
- Updated both READMEs and `SKILL.md` so human and LLM instructions never ask an
  installed Skill to find or run maintainer code.
- Updated the maintenance specification to document the source/distribution
  boundary and the zero-Python end-user requirement.

### Verification

- The current suite contains 11 deterministic tests after removing obsolete
  local-installer tests and adding the runtime package contract.
- The release is complete only after `main` CI succeeds and the generated
  `skill` branch is confirmed to contain the runtime allowlist.

## 2026-07-29

### Added

- Added `references/SYNC_MANIFEST.json` with the exact upstream repository,
  commit SHA, source subfolder, language, source-document count, and snapshot
  synchronization time.
- Added deterministic repository validation for generated indexes, manifest
  integrity, source-document coverage, Skill metadata, documentation claims,
  executable maintenance scripts, and immutable GitHub Action references.
- Added 15 local unit and integration tests covering index generation, atomic
  synchronization, stale-file removal, failure preservation, provenance,
  no-op timestamps, fresh installation, fast-forward updates, and rejection of
  dirty, divergent, unrelated, or non-Git targets.
- Added eight prompt-based routing contract evaluations for webhook signatures,
  LIFF browser context, LINE Login PKCE, rich menus, channel access tokens,
  Messaging API rate limits, LINE Mini App configuration, and Official Account
  Manager scope.
- Added a pull-request/push validation workflow and Codex UI metadata in
  `agents/openai.yaml`.
- Added `NOTICE.md` to identify the upstream source and separate the repository's
  AGPL-licensed material from synchronized documentation governed by LY
  Corporation terms.
- Added a committed maintenance hardening specification with executable
  acceptance criteria.

### Changed

- Rebuilt documentation synchronization around a validated staging snapshot.
  The destination is replaced only after clone, copy, index generation,
  provenance generation, and validation all succeed.
- Changed synchronization from overlay copying to an exact mirror so documents
  removed upstream are removed locally.
- Preserved the previous snapshot when any synchronization step fails.
- Preserved the existing `synced_at` value when the upstream commit is unchanged
  to avoid empty daily commits.
- Reworked `install-skill.sh` into a functional installer/updater. Missing
  targets are cloned; existing checkouts are updated only through a clean,
  matching, `main` fast-forward.
- Removed hidden per-use `git pull` behavior from `SKILL.md`. Installed snapshots
  now update only through an explicit user or host action.
- Reorganized `SKILL.md` around scope, freshness, external-content safety,
  minimal-context lookup, task routing, diagnostics, response structure, and
  verifiable completion criteria.
- Updated both READMEs to describe Git checkout and copied-snapshot behavior
  accurately, remove the stale fixed document-count claim, and clarify that the
  repository covers English LINE Developers content rather than the complete
  Official Account Manager help center.
- Changed large-reference guidance to search headings and load only relevant
  sections instead of loading the entire index or API reference.

### Security

- Pinned every GitHub Action to an immutable full commit SHA.
- Removed the third-party auto-commit Action and replaced it with explicit Git
  commands after snapshot validation.
- Restricted default workflow permissions to read-only and granted write access
  only to the scheduled synchronization job.
- Added workflow timeouts and concurrency controls.
- Added explicit instructions to treat synchronized Markdown as external data,
  not agent instructions, and to protect access tokens, channel secrets, user
  data, and local credentials.
- Added strict shell failure handling, validated paths, staging isolation, dirty
  checkout protection, remote-origin validation, and fast-forward-only updates.

### Verification

- Synchronized the official `docs/en` snapshot at upstream commit
  `c7dfdeafc6fd3dbbf573bad8a0f76303be52e552`.
- Verified the Skill with the Codex Skill Creator validator.
- Verified the generated index and snapshot manifest against all synchronized
  source documents.
- Verified the test suite and routing contracts on macOS with Python 3.14; CI
  repeats the checks on Ubuntu with Python 3.12.
