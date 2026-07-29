#!/usr/bin/env bash
set -Eeuo pipefail

readonly PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly REPO_URL="${LINE_DOCS_REPO_URL:-https://github.com/line/line-developers-docs-source.git}"
readonly SOURCE_SUBFOLDER="${LINE_DOCS_SOURCE_SUBFOLDER:-docs/en}"
readonly LANGUAGE="${LINE_DOCS_LANGUAGE:-${SOURCE_SUBFOLDER##*/}}"
readonly SYNCED_AT="${LINE_DOCS_SYNCED_AT:-$(date -u '+%Y-%m-%dT%H:%M:%SZ')}"

if [[ "${LINE_DOCS_DEST_DIR:-}" == /* ]]; then
    readonly DEST_DIR="$LINE_DOCS_DEST_DIR"
else
    readonly DEST_DIR="$PROJECT_DIR/${LINE_DOCS_DEST_DIR:-references}"
fi

case "$SOURCE_SUBFOLDER" in
    ""|/*|*".."*)
        echo "Invalid source subfolder: $SOURCE_SUBFOLDER" >&2
        exit 2
        ;;
esac

if [[ -z "$DEST_DIR" || "$DEST_DIR" == "/" ]]; then
    echo "Refusing unsafe destination: $DEST_DIR" >&2
    exit 2
fi

readonly DEST_PARENT="$(dirname "$DEST_DIR")"
mkdir -p "$DEST_PARENT"
readonly TEMP_DIR="$(mktemp -d "$DEST_PARENT/.line-docs-sync.XXXXXX")"
readonly UPSTREAM_DIR="$TEMP_DIR/upstream"
readonly STAGED_REFERENCES="$TEMP_DIR/references"
readonly PREVIOUS_REFERENCES="$TEMP_DIR/previous-references"

cleanup() {
    local exit_status=$?
    set +e
    if [[ -e "$PREVIOUS_REFERENCES" && ! -e "$DEST_DIR" ]]; then
        echo "Restoring previous snapshot after interrupted installation" >&2
        mv "$PREVIOUS_REFERENCES" "$DEST_DIR"
    fi
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
    return "$exit_status"
}
trap cleanup EXIT

echo "LINE documentation sync"
echo "Source: $REPO_URL ($SOURCE_SUBFOLDER)"
echo "Destination: $DEST_DIR"

git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$UPSTREAM_DIR"
git -C "$UPSTREAM_DIR" sparse-checkout set "$SOURCE_SUBFOLDER"

readonly SOURCE_DIR="$UPSTREAM_DIR/$SOURCE_SUBFOLDER"
if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Upstream subfolder not found: $SOURCE_SUBFOLDER" >&2
    exit 1
fi

mkdir -p "$STAGED_REFERENCES"
cp -R "$SOURCE_DIR/." "$STAGED_REFERENCES/"

readonly UPSTREAM_COMMIT="$(git -C "$UPSTREAM_DIR" rev-parse HEAD)"
python3 "$PROJECT_DIR/scripts/generate_index.py" \
    --root "$STAGED_REFERENCES" \
    --output "$STAGED_REFERENCES/INDEX.md"

manifest_arguments=(
    --root "$STAGED_REFERENCES"
    --output "$STAGED_REFERENCES/SYNC_MANIFEST.json"
    --source-url "$REPO_URL"
    --source-subfolder "$SOURCE_SUBFOLDER"
    --upstream-commit "$UPSTREAM_COMMIT"
    --synced-at "$SYNCED_AT"
    --language "$LANGUAGE"
)
if [[ -f "$DEST_DIR/SYNC_MANIFEST.json" ]]; then
    manifest_arguments+=(
        --previous-manifest "$DEST_DIR/SYNC_MANIFEST.json"
    )
fi
python3 "$PROJECT_DIR/scripts/write_sync_manifest.py" \
    "${manifest_arguments[@]}"
python3 "$PROJECT_DIR/scripts/validate_repository.py" \
    --references-only "$STAGED_REFERENCES"

if [[ -e "$DEST_DIR" ]]; then
    mv "$DEST_DIR" "$PREVIOUS_REFERENCES"
fi
if ! mv "$STAGED_REFERENCES" "$DEST_DIR"; then
    if [[ -e "$PREVIOUS_REFERENCES" && ! -e "$DEST_DIR" ]]; then
        mv "$PREVIOUS_REFERENCES" "$DEST_DIR"
    fi
    echo "Failed to install synchronized snapshot" >&2
    exit 1
fi

readonly DOCUMENT_COUNT="$(
    find "$DEST_DIR" -type f -name '*.md' ! -name 'INDEX.md' | wc -l | tr -d ' '
)"
echo "Sync complete: $DOCUMENT_COUNT source documents at $UPSTREAM_COMMIT"
