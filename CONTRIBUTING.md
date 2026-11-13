# Contributing to Eel

Thank you for contributing to Eel! Eel is an open-source, community-driven project dedicated to keeping desktop HTML/JS GUI application development in Python lightweight, simple, and accessible.

## Development Setup

1. Clone the repository and create an isolated virtual environment:
   ```bash
   git checkout -b feature/my-feature
   ./scripts/setup_dev.sh
   ```
   Or manually:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .[jinja2,test,all]
   ```

2. Run the test suite:
   ```bash
   ./scripts/run_tests.sh
   ```

## Code Quality Standards

Before submitting a Pull Request, ensure that:
1. All static type checks pass strictly:
   ```bash
   mypy --strict eel
   ```
2. All unit and integration tests pass cleanly:
   ```bash
   pytest tests/unit tests/integration/test_server_e2e.py -v
   ```
3. New features or bug fixes include corresponding test cases under `tests/`.

## Architecture Principles
- **Minimal Boilerplate:** Preserve the 3-line startup simplicity of Eel.
- **Security by Default:** Never use dynamic code execution (`exec`, `eval`) or unescaped subprocess commands (`shell=True`).
- **Standardized Packaging:** All dependencies and metadata must remain PEP 517/621 compliant in `pyproject.toml`.

