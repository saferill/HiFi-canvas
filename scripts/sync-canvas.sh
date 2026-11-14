#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 scripts/sync-canvas.py

# `git status --porcelain` also catches a brand-new (untracked) catalog file,
# which `git diff` alone would miss.
if [ -z "$(git status --porcelain -- v1/)" ]; then
  echo "No canvas updates."
  exit 0
fi

BRANCH="${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}"

git config user.name "saferill"
git config user.email "saferill@users.noreply.github.com"
git add v1/
git commit -m "chore(canvas): auto-update background video catalog"

# Someone may have pushed (e.g. a merged PR) while this job was running.
for attempt in 1 2 3; do
  if git push origin "HEAD:${BRANCH}"; then
    exit 0
  fi
  echo "Push rejected (attempt ${attempt}), rebasing on origin/${BRANCH}..."
  git pull --rebase origin "${BRANCH}"
done

echo "Could not push canvas update after 3 attempts." >&2
exit 1
