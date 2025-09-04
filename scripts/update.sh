#!/usr/bin/env bash
set -euo pipefail

# Lightweight helper to (1) run tests & generate coverage badge, (2) refresh CHANGELOG.md via git-cliff.
# Mirrors the logic of the local pre-push hooks, but in one manual script.

echo "[1/2] Coverage + badge"
uv run coverage erase || true
uv run coverage run -m pytest -q
uv run coverage combine || true
uv run coverage xml -o coverage.xml || true
uv run coverage report

# Badge (write inside assets/ like repo layout). Fallback to python -m if entry point differs.
badge_out="assets/coverage.svg"
mkdir -p assets
if uvx genbadge --help >/dev/null 2>&1; then
  uvx genbadge coverage -i coverage.xml -o "$badge_out"
else
  uvx genbadge coverage -i coverage.xml -o "$badge_out" || true
fi
echo "   -> Badge at $badge_out"

echo "[2/2] CHANGELOG"
uvx git-cliff -o CHANGELOG.md

# Optional quick commit if user passed --commit (or -c) and repo is clean except for our outputs.
if [[ ${1:-} =~ ^(--commit|-c)$ ]]; then
  git add CHANGELOG.md "$badge_out" || true
  git commit -m "chore: update coverage badge & changelog" || echo "(Nothing new to commit)"
fi

echo "Done." 