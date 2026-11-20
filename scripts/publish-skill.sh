#!/usr/bin/env bash
set -Eeuo pipefail

readonly PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly SOURCE_SHA="$(git -C "$PROJECT_DIR" rev-parse HEAD)"
readonly TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/line-docs-skill-publish.XXXXXX")"
readonly PACKAGE_DIR="$TEMP_ROOT/package"
readonly WORKTREE_DIR="$TEMP_ROOT/worktree"

cleanup() {
    if [[ -e "$WORKTREE_DIR/.git" ]]; then
        git -C "$PROJECT_DIR" worktree remove --force "$WORKTREE_DIR" || true
    fi
    rm -rf -- "$TEMP_ROOT"
}
trap cleanup EXIT

"$PROJECT_DIR/scripts/build-skill-package.sh" "$PACKAGE_DIR"

if git -C "$PROJECT_DIR" ls-remote --exit-code --heads origin skill \
    >/dev/null 2>&1; then
    git -C "$PROJECT_DIR" fetch origin skill
    published_subject=$(git -C "$PROJECT_DIR" log -1 --format=%s FETCH_HEAD)
    if [[ "$published_subject" =~ ^chore:\ publish\ runtime\ skill\ from\ ([0-9a-f]{40})$ ]]; then
        published_source="${BASH_REMATCH[1]}"
        if [[ "$published_source" != "$SOURCE_SHA" ]] &&
            git -C "$PROJECT_DIR" cat-file -e "${published_source}^{commit}" 2>/dev/null &&
            git -C "$PROJECT_DIR" merge-base --is-ancestor "$SOURCE_SHA" "$published_source"; then
            echo "Runtime Skill branch already contains a newer maintenance snapshot."
            exit 0
        fi
    fi
    git -C "$PROJECT_DIR" worktree add \
        --detach "$WORKTREE_DIR" FETCH_HEAD
else
    git -C "$PROJECT_DIR" worktree add --detach "$WORKTREE_DIR" "$SOURCE_SHA"
    git -C "$WORKTREE_DIR" switch --orphan skill
fi

git -C "$WORKTREE_DIR" rm -rf --ignore-unmatch .
git -C "$WORKTREE_DIR" clean -fdx
cp -R "$PACKAGE_DIR/." "$WORKTREE_DIR/"
git -C "$WORKTREE_DIR" add -A

if git -C "$WORKTREE_DIR" diff --cached --quiet; then
    echo "Runtime Skill branch is already current."
    exit 0
fi

git -C "$WORKTREE_DIR" config user.name "github-actions[bot]"
git -C "$WORKTREE_DIR" config \
    user.email "41898282+github-actions[bot]@users.noreply.github.com"
git -C "$WORKTREE_DIR" commit \
    -m "chore: publish runtime skill from ${SOURCE_SHA}"
git -C "$WORKTREE_DIR" push origin HEAD:skill
