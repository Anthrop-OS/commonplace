#!/usr/bin/env bash
# Create an isolated git worktree for a new task. Run this BEFORE editing
# anything when starting a task. The main clone holds a single HEAD shared
# across all processes — concurrent agent sessions that each `git checkout -b`
# clobber each other.
#
# Usage:
#   ./scripts/new-task.sh ops/<branch-name> [--force]
#
# Effect:
#   1. fetch origin/main
#   2. abort with a structured hint if any PR (any state) already uses this
#      branch name as head ref. `--force` demotes the abort to a WARNING.
#   3. create ../<repo>-wt/<branch-tail>/ as a worktree on a new branch
#      off origin/main
#   4. run scripts/bootstrap.sh inside the worktree (idempotent)
#   5. run the in-flight search (open PRs/issues for this task's keywords)
#      BY CONSTRUCTION — the funnel T1 step, not advisory text you may skip.
#
# Cleanup after PR merges:
#   git worktree remove ../<repo>-wt/<branch-tail>
#   git worktree prune
#
# Adapted from homelab-s5oyt03iv9/homelab-ops scripts/new-task.sh.

set -euo pipefail

force=0
branch=""
while [ $# -gt 0 ]; do
  case "$1" in
    --force) force=1 ;;
    -h|--help)
      echo "usage: $0 ops/<branch-name> [--force]" >&2
      exit 0
      ;;
    --) shift; branch="${1:-}"; break ;;
    -*)
      echo "error: unknown flag: $1" >&2
      echo "usage: $0 ops/<branch-name> [--force]" >&2
      exit 2
      ;;
    *)
      if [ -z "$branch" ]; then
        branch="$1"
      else
        echo "error: unexpected extra positional arg: $1" >&2
        exit 2
      fi
      ;;
  esac
  shift
done

if [ -z "$branch" ]; then
  echo "usage: $0 ops/<branch-name> [--force]" >&2
  exit 2
fi

case "$branch" in
  main|master|origin/main|origin/master)
    echo "error: refusing to create worktree directly on $branch" >&2
    exit 2
    ;;
esac

repo_root="$(git rev-parse --show-toplevel)"
repo_name="$(basename "$repo_root")"
parent="$(dirname "$repo_root")"
tail="${branch##*/}"
wt_dir="${parent}/${repo_name}-wt/${tail}"

# --- PR-slug collision detection -------------------------------------------
# Search PRs whose head ref matches this branch name (any state). If any
# match, abort with a structured hint so the operator can contribute to the
# existing PR, rebrand, or override with --force.
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  collision_json="$(gh pr list --head "$branch" --state all \
    --json number,title,state,headRefName,url 2>/dev/null || echo '[]')"
  collision_count="$(printf '%s' "$collision_json" | jq 'length' 2>/dev/null || echo 0)"
  if [ "${collision_count:-0}" -gt 0 ]; then
    if [ "$force" -eq 1 ]; then
      label="WARNING"
    else
      label="ERROR"
    fi
    {
      echo
      echo "${label}: branch slug \"$branch\" collides with existing PR(s):"
      printf '%s' "$collision_json" | jq -r \
        '.[] | "  #\(.number)  \(.title)  (state: \(.state), branch: \(.headRefName))\n        \(.url)"'
      echo "HINT: another session may have already claimed this work. Options:"
      echo "        1. Contribute to the existing PR (gh pr checkout <NNN>)"
      echo "        2. Rebrand your branch: ./scripts/new-task.sh ops/<different-slug>"
      echo "        3. If the existing PR is stale, ack with the operator and pass --force."
      echo
    } >&2
    if [ "$force" -ne 1 ]; then
      exit 2
    fi
    echo "→ --force passed; proceeding despite collision." >&2
  fi
else
  echo "!! gh unavailable/unauthenticated — collision check SKIPPED." >&2
  echo "!! Verify manually before continuing:" >&2
  echo "     gh pr list --head \"$branch\" --state all" >&2
fi

if [ -e "$wt_dir" ]; then
  echo "error: $wt_dir already exists" >&2
  echo "       use a different branch name or \`git worktree remove $wt_dir\` first" >&2
  exit 1
fi

git -C "$repo_root" fetch origin main
git -C "$repo_root" worktree add -b "$branch" "$wt_dir" origin/main

if [ -x "${wt_dir}/scripts/bootstrap.sh" ]; then
  ( cd "$wt_dir" && ./scripts/bootstrap.sh )
fi

# --- in-flight search (funnel T1 foundational) -----------------------------
# The wrapper performs the search; you read the result. Cheap pre-flight as
# structure, not voluntary prose.
kw="$(printf '%s' "$tail" | tr '-_' '  ' | tr -s ' ')"
echo
echo "── in-flight search (keywords: ${kw}) ──"
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  echo "open PRs:"
  gh pr list --state open --search "$kw" \
    --json number,title --jq '.[] | "  #\(.number) \(.title)"' 2>/dev/null \
    || echo "  (search failed — run manually: gh pr list --search \"$kw\")"
  echo "open issues:"
  gh issue list --state open --search "$kw" \
    --json number,title --jq '.[] | "  #\(.number) \(.title)"' 2>/dev/null \
    || echo "  (search failed — run manually: gh issue list --search \"$kw\")"
  echo "→ If any of the above already covers this task, STOP and coordinate"
  echo "  on that issue/PR instead of duplicating work."
else
  echo "!! gh unavailable/unauthenticated — T1 search NOT satisfied."
  echo "!! You MUST run before authoring:"
  echo "     gh pr list --state open --search \"$kw\""
  echo "     gh issue list --state open --search \"$kw\""
fi

cat <<EOF

ok: worktree ready
  path:   $wt_dir
  branch: $branch (off origin/main)

next:
  cd $wt_dir
EOF
