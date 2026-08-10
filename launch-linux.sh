#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
GUI_SCRIPT="$SCRIPT_DIR/codex56-control-center.py"

if [[ ! -f "$GUI_SCRIPT" ]]; then
  echo "[ERROR] GUI script was not found: $GUI_SCRIPT" >&2
  exit 1
fi

PYTHON_CMD=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && \
     "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
    PYTHON_CMD="$candidate"
    break
  fi
done

if [[ -z "$PYTHON_CMD" ]]; then
  echo "[ERROR] Python 3.10 or newer is required." >&2
  exit 1
fi

if ! "$PYTHON_CMD" -c 'import tkinter' >/dev/null 2>&1; then
  echo "[ERROR] Tkinter is required (for example, install python3-tk)." >&2
  exit 1
fi

echo "[Environment]"
"$PYTHON_CMD" --version
echo "[Starting] $GUI_SCRIPT"
cd "$SCRIPT_DIR"
exec "$PYTHON_CMD" "$GUI_SCRIPT"
