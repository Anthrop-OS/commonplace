#!/usr/bin/env bash
# adr-verify.sh — single source of truth for ADR-corpus invariants.
#
# Invokers (all run the SAME assertions):
#   - adr-pr-check workflow        : default mode (pending files allowed)
#   - adr-assign Action            : --no-pending (post-assignment, fail-closed)
#
# Exit 0 = corpus conformant. Exit 1 = at least one invariant violated
# (all violations are printed; the script does not stop at the first).
#
# Pure repo-state checker: no git, no network. Reference-rewrite
# correctness is asserted by the assign Action's own post-rewrite grep,
# deliberately NOT here (uuid persists as a permanent alias, so a stray
# uuid mention is not by itself a violation).
#
# Portable to bash 3.2 (macOS): no associative arrays, no mapfile.
#
# Adapted from homelab-s5oyt03iv9/homelab-ops tools/adr-verify.sh.

set -euo pipefail

DECISIONS_DIR="${ADR_DECISIONS_DIR:-decisions}"
no_pending=0
[ "${1:-}" = "--no-pending" ] && no_pending=1

fail=0
err() { printf 'FAIL: %s\n' "$1" >&2; fail=1; }

fm() {  # fm <file> <key> -> value of first `key: value` in frontmatter
  awk -v k="$2" '
    NR==1 && $0=="---" { inf=1; next }
    inf && $0=="---"   { exit }
    inf {
      line=$0; sub(/^[ \t]+/,"",line)
      if (line ~ "^" k ":") { sub("^" k ":[ \t]*","",line); print line; exit }
    }' "$1"
}

shopt -s nullglob
numbered=( "$DECISIONS_DIR"/adr-[0-9][0-9][0-9][0-9]-*.md )
pending=(  "$DECISIONS_DIR"/adr-pending-*.md )
shopt -u nullglob

ids=""      # newline list of "NNNN<TAB>basename"
uuids=""    # newline list of "uuid<TAB>basename" (numbered + pending)

# --- numbered ADRs ---
for f in ${numbered[@]+"${numbered[@]}"}; do
  base="$(basename "$f")"
  fn_seq="$(printf '%s' "$base" | sed -n 's/^adr-\([0-9]\{4\}\)-.*/\1/p')"
  [ -n "$fn_seq" ] || { err "$base: filename not adr-NNNN-<slug>.md"; continue; }

  id="$(fm "$f" id)"
  uuid="$(fm "$f" uuid)"

  [ "$id" = "$fn_seq" ] || err "$base: frontmatter id='$id' != filename seq '$fn_seq'"
  printf '%s' "$uuid" | grep -qE '^[0-9a-f]{8}$' \
    || err "$base: uuid='$uuid' not 8 lowercase hex"

  # body H1 must read "# ADR-<id> — ...". The assign Action rewrites filename +
  # frontmatter id on merge; this asserts the H1 was normalized too, so a
  # numbered ADR can't ship half-numbered ("# ADR-pending (uuid)").
  h1="$(grep -m1 '^# ADR' "$f" || true)"
  h1num="$(printf '%s' "$h1" | sed -n 's/^# ADR-\([0-9A-Za-z]*\).*/\1/p')"
  if [ -z "$h1" ]; then
    err "$base: no '# ADR-<id>' H1 title line"
  elif [ "$h1num" != "$fn_seq" ]; then
    err "$base: body H1 number != frontmatter id '$fn_seq' (H1: ${h1:-<none>})"
  fi

  ids="$ids$fn_seq	$base
"
  [ -n "$uuid" ] && uuids="$uuids$uuid	$base
"
done

# --- pending ADRs ---
if [ "$no_pending" -eq 1 ] && [ "${#pending[@]}" -gt 0 ]; then
  for f in ${pending[@]+"${pending[@]}"}; do err "$(basename "$f"): adr-pending-* must not exist in this context (--no-pending)"; done
fi
for f in ${pending[@]+"${pending[@]}"}; do
  base="$(basename "$f")"
  name_uuid="$(printf '%s' "$base" | sed -n 's/^adr-pending-\([0-9a-f]\{8\}\)-.*/\1/p')"
  [ -n "$name_uuid" ] || { err "$base: not adr-pending-<8hex>-<slug>.md"; continue; }

  id="$(fm "$f" id)"
  uuid="$(fm "$f" uuid)"
  [ "$id" = "pending" ] || err "$base: pending file must have 'id: pending' (got '$id')"
  [ "$uuid" = "$name_uuid" ] || err "$base: frontmatter uuid='$uuid' != filename uuid '$name_uuid'"

  [ -n "$uuid" ] && uuids="$uuids$uuid	$base
"
done

# --- duplicate id ---
dup_id="$(printf '%s' "$ids" | sed '/^$/d' | cut -f1 | sort | uniq -d)"
if [ -n "$dup_id" ]; then
  for d in $dup_id; do
    err "duplicate id $d: $(printf '%s' "$ids" | awk -F'\t' -v k="$d" '$1==k{printf "%s ",$2}')"
  done
fi

# --- duplicate uuid (across numbered + pending) ---
dup_uuid="$(printf '%s' "$uuids" | sed '/^$/d' | cut -f1 | sort | uniq -d)"
if [ -n "$dup_uuid" ]; then
  for d in $dup_uuid; do
    err "duplicate uuid $d: $(printf '%s' "$uuids" | awk -F'\t' -v k="$d" '$1==k{printf "%s ",$2}')"
  done
fi

# --- contiguity: numbered ids must be exactly 1..N ---
sorted_ids="$(printf '%s' "$ids" | sed '/^$/d' | cut -f1 | sort -n)"
if [ -n "$sorted_ids" ]; then
  expect=1
  for n in $sorted_ids; do
    dec=$((10#$n))
    if [ "$dec" -ne "$expect" ]; then
      err "id sequence not contiguous: expected $(printf '%04d' "$expect"), got $n"
    fi
    expect=$((expect+1))
  done
fi

if [ "$fail" -eq 0 ]; then
  echo "adr-verify: OK (${#numbered[@]} numbered, ${#pending[@]} pending)"
fi
exit "$fail"
