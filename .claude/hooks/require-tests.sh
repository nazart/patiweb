#!/usr/bin/env bash
# Hook PreToolUse (Bash) de Claude Code: antes de cualquier `git commit`, corre la
# suite completa (`npm test`). Si falla, bloquea el commit (exit 2) y le devuelve a
# Claude el final del log para que corrija antes de reintentar.
set -uo pipefail
cmd=$(jq -r '.tool_input.command // ""')
if ! grep -Eq '(^|[;&|[:space:]])git([[:space:]]+-[^[:space:]]+)*[[:space:]]+commit([[:space:]]|$)' <<<"$cmd"; then
  exit 0
fi
cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}" || exit 0
log=$(mktemp)
if npm test >"$log" 2>&1; then
  rm -f "$log"
  exit 0
fi
{
  echo "Commit bloqueado: la suite de pruebas obligatoria (npm test) falló. Corrige y vuelve a intentar."
  echo "--- últimas líneas ---"
  tail -40 "$log"
} >&2
rm -f "$log"
exit 2
