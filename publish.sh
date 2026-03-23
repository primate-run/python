#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$(mktemp -d -t primate-publish-XXXXXX)"

cleanup() {
  rm -rf "$VENV"
}
trap cleanup EXIT

rm -rf "$ROOT/dist" "$ROOT/build" "$ROOT"/*.egg-info

python3 -m venv "$VENV"
source "$VENV/bin/activate"

python -m ensurepip --upgrade || true
python -m pip install --upgrade pip build twine

python -m build "$ROOT"
python -m twine upload "$ROOT"/dist/*
