#!/bin/bash

# Configuration
REPO_URL="https://github.com/line/line-developers-docs-source.git"
SOURCE_SUBFOLDER="docs/en"
DEST_FOLDER="references"
TEMP_REPO=".tmp_repo"

echo "🦞 LINE Documentation Sync Engine"
echo "────────────────────────────────"

# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Function to clean up temp repo
cleanup() {
    if [ -d "$TEMP_REPO" ]; then
        echo "🧹 Cleaning up temporary repository..."
        rm -rf "$TEMP_REPO"
    fi
}

# Trap exit to cleanup
trap cleanup EXIT

# Clear destination folder first (optional, but ensures clean state)
# mkdir -p "$DEST_FOLDER"
# rm -rf "$DEST_FOLDER"/*

echo "📡 Cloning upstream repository (sparse-checkout)..."
mkdir -p "$TEMP_REPO"
cd "$TEMP_REPO"

git init
git remote add origin "$REPO_URL"
git config core.sparseCheckout true

# Specify the subfolder to pull
echo "$SOURCE_SUBFOLDER/*" >> .git/info/sparse-checkout

# Pull the documentation
git pull --depth 1 origin main

# Check if the folder exists
if [ ! -d "$SOURCE_SUBFOLDER" ]; then
    echo "❌ Error: Could not find $SOURCE_SUBFOLDER in the upstream repository."
    exit 1
fi

echo "📂 Syncing files to $DEST_FOLDER..."
# Move back to project root
cd ..

# Copy files from temp repo to references
# We flatten the docs/en structure into the references folder
mkdir -p "$DEST_FOLDER"
cp -R "$TEMP_REPO/$SOURCE_SUBFOLDER/"* "$DEST_FOLDER/"

# Summary
FILE_COUNT=$(find "$DEST_FOLDER" -name "*.md" | wc -l)
echo "✅ Sync complete! $FILE_COUNT markdown files synced."

# Generate index
echo "🗂️ Generating documentation index..."
python3 scripts/generate_index.py

echo "💡 Tip: Run this script whenever you want to update the documentation."
