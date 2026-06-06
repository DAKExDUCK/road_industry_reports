#!/usr/bin/env bash
# Shell configuration sourced by `format.sh`.
# Edit these variables to change tool args and default order.

# Arguments passed to `black`
BLACK_ARGS="."

# Arguments passed to `isort`
ISORT_ARGS="."

# Arguments passed to `pylint`
PYLINT_ARGS="--recursive=y ."

# Arguments passed to `mypy`
MYPY_ARGS="."

# Default order of tools to run (space-separated)
FORMAT_TOOLS=(black isort pylint mypy)
