#!/usr/bin/env bash
set -e

echo "=== Initializing Python Development Environment ==="
if command -v uv >/dev/null 2>&1; then
    uv venv .venv
    source .venv/bin/activate
    uv pip install -e .[jinja2,test,all]
else
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .[jinja2,test,all]
fi

echo "=== Development Environment Ready! ==="

