#!/usr/bin/env bash
set -euo pipefail

# This script runs formatting and linting tools using configuration
# located in the `format_configs` directory.

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HERE/format_configs"
CONFIG_SH="$CONFIG_DIR/config.sh"

if [ ! -d "$CONFIG_DIR" ]; then
  echo "format_configs directory not found at $CONFIG_DIR" >&2
  exit 1
fi

if [ -f "$CONFIG_SH" ]; then
  # shellcheck disable=SC1090
  source "$CONFIG_SH"
else
  echo "Config file $CONFIG_SH not found. Create it to customize tool args." >&2
  exit 1
fi

# If script is called with arguments, treat them as tool names to run.
if [ "$#" -gt 0 ]; then
  TO_RUN=("$@")
else
  TO_RUN=("${FORMAT_TOOLS[@]}")
fi

for tool in "${TO_RUN[@]}"; do
  case "$tool" in
    black)
      echo "==> Running: black $BLACK_ARGS"
      black $BLACK_ARGS
      ;;
    isort)
      echo "==> Running: isort $ISORT_ARGS"
      isort $ISORT_ARGS
      ;;
    pylint)
      echo "==> Running: pylint $PYLINT_ARGS"
      pylint $PYLINT_ARGS
      ;;
    mypy)
      echo "==> Running: mypy $MYPY_ARGS"
      mypy $MYPY_ARGS
      ;;
    *)
      echo "Unknown tool: $tool" >&2
      exit 2
      ;;
  esac
done

echo "Formatting and linting completed."
