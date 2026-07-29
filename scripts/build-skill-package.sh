#!/usr/bin/env bash
set -Eeuo pipefail

readonly PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ "$#" -ne 1 ]]; then
    echo "Usage: $0 <new-output-directory>" >&2
    exit 2
fi

readonly OUTPUT_DIR="$1"

if [[ -e "$OUTPUT_DIR" ]]; then
    echo "Refusing to overwrite existing output: $OUTPUT_DIR" >&2
    exit 2
fi

cleanup_failed_build() {
    readonly exit_status="$?"
    if [[ "$exit_status" -ne 0 && -d "$OUTPUT_DIR" ]]; then
        rm -rf -- "$OUTPUT_DIR"
    fi
    exit "$exit_status"
}
trap cleanup_failed_build EXIT

mkdir -p "$OUTPUT_DIR"
cp "$PROJECT_DIR/SKILL.md" "$OUTPUT_DIR/SKILL.md"
cp "$PROJECT_DIR/LICENSE" "$OUTPUT_DIR/LICENSE"
cp "$PROJECT_DIR/NOTICE.md" "$OUTPUT_DIR/NOTICE.md"
cp -R "$PROJECT_DIR/agents" "$OUTPUT_DIR/agents"
cp -R "$PROJECT_DIR/references" "$OUTPUT_DIR/references"

if find "$OUTPUT_DIR" -type f \( -name '*.py' -o -name '*.pyc' -o -name '*.sh' \) \
    -print -quit | grep -q .; then
    echo "Runtime package unexpectedly contains executable maintenance code." >&2
    exit 1
fi

if find "$OUTPUT_DIR" -type l -print -quit | grep -q .; then
    echo "Runtime package unexpectedly contains a symbolic link." >&2
    exit 1
fi

trap - EXIT
echo "Built runtime Skill package: $OUTPUT_DIR"
