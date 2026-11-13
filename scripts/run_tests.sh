#!/usr/bin/env bash
set -e

echo "=== Running Strict Type Checks (MyPy) ==="
.venv/bin/mypy --strict eel

echo "=== Running Unit & Integration Tests (Pytest) ==="
PYTHONPATH=. .venv/bin/pytest tests/unit tests/integration/test_server_e2e.py -v

echo "=== All Tests and Checks Passed Successfully! ==="

