#!/usr/bin/env bash
set -euo pipefail
mkdir -p v1
python3 scripts/sync-canvas.py
git config user.name "saferill"
git config user.email "saferill@users.noreply.github.com"
if ! git diff --quiet v1/; then
  git add v1/
  git commit -m "chore(canvas): auto-update background video catalog"
  git push origin main
else
  echo "No canvas updates."
fi
