#!/usr/bin/env bash
# Pre-flight check for commonplace agent sessions.
#
# Run BEFORE any git operation. Classifies the current cwd into one of four
# modes and prints a next-step suggestion. Exits non-zero in the one case
# that should halt work (main clone drifted onto a feature branch — likely
# owned by another active session).
#
# Detection is by remote identity + worktree dir shape, NOT by an absolute
# clone path, so it works regardless of where the repo is checked out.
#
# Modes:
#   main_clone_clean    commonplace main clone, on `main`
#   main_clone_drifted  commonplace main clone, HEAD != main
#   inside_worktree     inside a ../commonplace-wt/* worktree
#   unrelated           not a commonplace repo or worktree
#
# Exit codes:
#   0  proceed (clean / inside_worktree / unrelated)
#   1  HALT — main_clone_drifted; do NOT operate, do NOT reset HEAD
#
# Adapted from homelab-s5oyt03iv9/homelab-ops scripts/preflight.sh.

# Must run past failing git probes to report a mode + exit code
# deliberately, so `set -e` is intentionally omitted.
set -uo pipefail

cwd_real="$(pwd -P)"
mode="unrelated"
branch=""
worktree_root=""

if git rev-parse --git-dir >/dev/null 2>&1; then
  branch="$(git symbolic-ref --short HEAD 2>/dev/null || echo "DETACHED")"
  worktree_root="$(git rev-parse --show-toplevel)"
  worktree_real="$(cd "$worktree_root" && pwd -P)"
  origin_url="$(git config --get remote.origin.url 2>/dev/null || true)"

  is_commonplace=0
  case "$origin_url" in
    *Anthrop-OS/commonplace|*Anthrop-OS/commonplace.git) is_commonplace=1 ;;
  esac

  parent_name="$(basename "$(dirname "$worktree_real")")"
  base_name="$(basename "$worktree_real")"

  if [ "$is_commonplace" -eq 1 ]; then
    if [ "$parent_name" = "commonplace-wt" ]; then
      mode="inside_worktree"
    elif [ "$base_name" = "commonplace" ]; then
      if [ "$branch" = "main" ]; then
        mode="main_clone_clean"
      else
        mode="main_clone_drifted"
      fi
    fi
  fi
fi

printf 'mode:           %s\n' "$mode"
printf 'cwd:            %s\n' "$cwd_real"
printf 'worktree_root:  %s\n' "$worktree_root"
printf 'branch:         %s\n' "$branch"

case "$mode" in
  main_clone_clean)
    cat <<'EOF'

next:
  - Read-only ops (browse, gh issue list, git log) are fine here.
  - For any write/commit work, isolate via worktree first:
      ./scripts/new-task.sh ops/<branch>
      cd ../commonplace-wt/<branch-tail>
EOF
    exit 0
    ;;
  main_clone_drifted)
    cat <<'EOF'

HALT:
  - DO NOT operate here. Another session may still own this HEAD.
  - DO NOT `git checkout main` — you risk clobbering an in-progress task.
  - For your own task, create a worktree off origin/main (it works
    independent of the main clone's drift):
      ./scripts/new-task.sh ops/<branch>
      cd ../commonplace-wt/<branch-tail>
EOF
    exit 1
    ;;
  inside_worktree)
    cat <<EOF

next:
  - Proceed with task work. cwd is isolated; the main clone is unaffected.
  - After your PR merges, clean up from the main clone:
      git worktree remove ${worktree_root}
EOF
    exit 0
    ;;
  unrelated)
    cat <<'EOF'

next:
  - Not inside a commonplace repo or worktree. This script's guidance does
    not apply; proceed with whatever the original task requires.
EOF
    exit 0
    ;;
esac
