#!/usr/bin/env bash
# Per-clone one-time setup. Idempotent.
# Run after `git clone` (or whenever .githooks/ changes).
#
# Adapted from homelab-s5oyt03iv9/homelab-ops scripts/bootstrap.sh.

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

git config core.hooksPath .githooks
chmod +x .githooks/* 2>/dev/null || true

echo "ok: core.hooksPath = $(git config core.hooksPath)"
echo "ok: hooks present  = $(ls .githooks | tr '\n' ' ')"
