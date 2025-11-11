#!/bin/bash

# Wrapper script for building Check Document from Obsidian
# Can be triggered via Commander plugin or terminal

set -e

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "🔨 Building Check Document..."
echo "📍 Project root: $PROJECT_ROOT"
echo ""

# Run the Python script with AI analysis by default
if command -v python3 &> /dev/null; then
    python3 "$SCRIPT_DIR/build_check_document.py" --ai-analysis
    EXIT_CODE=$?
else
    echo "❌ Error: python3 not found"
    exit 1
fi

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Check Document successfully built!"
    echo "📄 File: content/0. Управление/0.5. Проверочный документ.md"
else
    echo ""
    echo "❌ Build failed with exit code $EXIT_CODE"
    exit $EXIT_CODE
fi
