#!/usr/bin/env bash
# Blocks dangerous Bash commands before Claude executes them.
set -euo pipefail

CMD="${CLAUDE_TOOL_INPUT:-}"

BLOCKED_PATTERNS=(
  "rm -rf"
  "git push --force"
  "git push -f "
  "DROP TABLE"
  "DROP DATABASE"
  "TRUNCATE TABLE"
  "\.env"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$CMD" | grep -qi "$pattern"; then
    echo "BLOCKED: Dangerous command pattern detected: '$pattern'" >&2
    exit 2
  fi
done

exit 0
