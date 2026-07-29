#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def evaluate_contract(
    project_root: Path,
    cases: list[dict[str, object]],
) -> list[str]:
    errors: list[str] = []
    skill_text = (project_root / "SKILL.md").read_text(encoding="utf-8")
    normalized_skill = " ".join(skill_text.casefold().split())
    seen_ids: set[str] = set()

    for case in cases:
        case_id = str(case.get("id", "")).strip()
        prompt = str(case.get("prompt", "")).strip()
        if not case_id:
            errors.append("Routing case has no id")
            continue
        if case_id in seen_ids:
            errors.append(f"{case_id}: duplicate id")
        seen_ids.add(case_id)
        if not prompt:
            errors.append(f"{case_id}: prompt must not be empty")

        required_docs = case.get("required_docs", [])
        required_phrases = case.get("required_skill_phrases", [])
        if not isinstance(required_docs, list) or not isinstance(
            required_phrases,
            list,
        ):
            errors.append(f"{case_id}: requirements must be lists")
            continue

        for document in required_docs:
            relative_path = str(document)
            if not (project_root / relative_path).is_file():
                errors.append(f"{case_id}: missing document {relative_path}")
            if relative_path not in skill_text:
                errors.append(
                    f"{case_id}: SKILL.md does not route to {relative_path}"
                )

        for phrase in required_phrases:
            value = str(phrase)
            normalized_phrase = " ".join(value.casefold().split())
            if normalized_phrase not in normalized_skill:
                errors.append(
                    f"{case_id}: SKILL.md is missing required phrase {value!r}"
                )

    return errors


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    cases_path = project_root / "evals" / "routing_cases.json"
    try:
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: Unable to load routing cases: {error}")
        return 1
    if not isinstance(cases, list):
        print("ERROR: Routing cases must be a JSON array")
        return 1

    errors = evaluate_contract(project_root, cases)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Skill routing evaluations passed: {len(cases)} cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
