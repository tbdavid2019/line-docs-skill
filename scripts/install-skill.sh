#!/usr/bin/env bash
set -Eeuo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SOURCE_CHECKOUT="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly REPO_URL="${LINE_DOCS_SKILL_REPO_URL:-https://github.com/tbdavid2019/line-docs-skill.git}"
readonly TARGET_DIR="${1:-$SOURCE_CHECKOUT}"

normalize_repository_url() {
    local value="${1%/}"
    value="${value%.git}"
    printf '%s\n' "$value"
}

validate_checkout() {
    local checkout="$1"
    if [[ ! -d "$checkout/.git" ]]; then
        echo "Target is not a Git checkout: $checkout" >&2
        return 1
    fi
    if [[ ! -f "$checkout/SKILL.md" ]]; then
        echo "Target does not contain SKILL.md: $checkout" >&2
        return 1
    fi
}

if [[ -e "$TARGET_DIR" ]]; then
    validate_checkout "$TARGET_DIR"

    if [[ -n "$(git -C "$TARGET_DIR" status --porcelain)" ]]; then
        echo "Refusing to update a dirty checkout: $TARGET_DIR" >&2
        exit 1
    fi

    readonly CURRENT_ORIGIN="$(git -C "$TARGET_DIR" remote get-url origin)"
    if [[ "$(normalize_repository_url "$CURRENT_ORIGIN")" != \
        "$(normalize_repository_url "$REPO_URL")" ]]; then
        echo "Target origin does not match the LINE docs skill repository." >&2
        echo "Expected: $REPO_URL" >&2
        echo "Actual:   $CURRENT_ORIGIN" >&2
        exit 1
    fi

    readonly CURRENT_BRANCH="$(git -C "$TARGET_DIR" branch --show-current)"
    if [[ "$CURRENT_BRANCH" != "main" ]]; then
        echo "Refusing to update non-main branch: $CURRENT_BRANCH" >&2
        exit 1
    fi

    git -C "$TARGET_DIR" fetch origin main
    if ! git -C "$TARGET_DIR" merge-base --is-ancestor HEAD origin/main; then
        echo "Checkout has local or divergent commits; fast-forward refused." >&2
        exit 1
    fi
    git -C "$TARGET_DIR" merge --ff-only origin/main
    echo "Updated LINE docs skill in $TARGET_DIR"
else
    mkdir -p "$(dirname "$TARGET_DIR")"
    git clone --branch main --single-branch "$REPO_URL" "$TARGET_DIR"
    validate_checkout "$TARGET_DIR"
    echo "Installed LINE docs skill in $TARGET_DIR"
fi

if [[ -f "$TARGET_DIR/scripts/validate_repository.py" ]]; then
    python3 "$TARGET_DIR/scripts/validate_repository.py"
fi

echo "Skill ready: $TARGET_DIR/SKILL.md"
