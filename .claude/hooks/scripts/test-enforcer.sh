#!/usr/bin/env bash
# Runs pytest when Claude stops. Warns on failure — never blocks the session.
set -euo pipefail

TESTS_DIR="tests"

if [[ ! -d "$TESTS_DIR" ]]; then
  exit 0
fi

if ! pytest -x --tb=short -q 2>/dev/null; then
  echo "WARNING: Tests are failing. Run 'pytest -xvs' to investigate." >&2
fi

exit 0
