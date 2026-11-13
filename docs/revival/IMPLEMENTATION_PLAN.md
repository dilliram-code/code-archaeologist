# Modernization & Revival Implementation Plan

**Project:** Python-Eel (Eel)  
**Branch:** `revive/eel-20261113`  
**Chief Architect:** Agent 1  
**Lead Developers:** Code Repair Engineer (Agent 4), Security Researcher (Agent 5), Modernization/DevOps Engineer (Agent 7), QA Engineer (Agent 6)  
**Date:** November 2026  

---

## 1. Project Objectives & Architectural Vision

Eel is a lightweight bridge enabling desktop Python applications to render HTML/CSS/JS user interfaces and call Python functions from JavaScript (and vice-versa) via WebSockets.

The mission is to transform this abandoned repository into a modern, secure, cross-platform, well-tested, PEP 517/621-compliant library compatible with Python 3.9 through 3.13, while strictly preserving its intuitive zero-boilerplate public API (`eel.init()`, `eel.start()`, `@eel.expose()`).

---

## 2. Priority Breakdown & Work Packages

### Priority A: Critical (Application Functionality, Build & Startup)
- [x] **Task A.1 (Dependency Unblock):** Resolve greenlet/gevent Cython compilation deadlock by upgrading to modern `greenlet>=3.0.0` and `gevent>=24.2.1`.
- [x] **Task A.2 (Legacy Removal):** Remove `future` from `setup.py` / dependencies.
- [ ] **Task A.3 (Modern Packaging):** Introduce PEP 517/621 `pyproject.toml` with modern metadata, dependencies, optional extras (`jinja2`), build system, and scripts.
- [ ] **Task A.4 (Package Resources Migration):** Fix `eel/__main__.py` which still references deprecated `pkg_resources`. Migrate to `importlib.resources`.
- [ ] **Task A.5 (Python Anti-Pattern Fix):** Fix mutable default arguments in `eel.start()` (`cmdline_args`, `geometry`).
- [ ] **Task A.6 (Cross-Platform Browser Expansion):**
  - Update `eel/chrome.py` and `eel/edge.py` to discover Chromium-based browsers (Google Chrome, Microsoft Edge, Brave Browser, Chromium) across macOS, Linux, and Windows.
  - Fix `eel/edge.py`'s `find_path()` to return `Optional[str]` instead of `bool`.
  - Fix Windows-specific registry lookups and imports in `eel/chrome.py` so static type checks and non-Windows runtimes do not fail.

### Priority B: Important (Security, Reliability, Architecture & Quality)
- [ ] **Task B.1 (Security Hardening — Code Execution):**
  - Replace vulnerable `exec()` string formatting in `_mock_js_function` and `_import_js_function` with safe dynamic attribute binding (`setattr` on module / dynamic class dispatcher).
  - Validate JS exposed function names against valid identifier patterns to prevent injection.
- [ ] **Task B.2 (Security Hardening — Subprocess Execution):**
  - Remove `shell=True` in `eel/edge.py` and `eel/msIE.py` to eliminate command injection vulnerabilities.
- [ ] **Task B.3 (Frontend Client Cleanup):**
  - Remove leftover `debugger;` statement from `eel/eel.js` error handling.
  - Ensure strict JSON serialization safety.
- [ ] **Task B.4 (Static Type Checking):**
  - Fix all 7 MyPy errors under `mypy --strict eel`.
  - Ensure PEP 561 compliance (`py.typed`).
- [ ] **Task B.5 (Test Suite Repair & Expansion):**
  - Fix `test_init()` in `tests/unit/test_eel.py` where `.sort()` returned `None`, allowing tests to pass vacuously.
  - Add comprehensive unit tests for WebSocket message processing, JSON-RPC responses, exception handling, and browser discovery.
  - Modernize pytest configuration with `pytest.ini` / `pyproject.toml`.

### Priority C: Optional / Polish (DevOps, CI/CD, Documentation & Maintainer Experience)
- [ ] **Task C.1 (Modern CI/CD):**
  - Create modern GitHub Actions workflow (`.github/workflows/revival-ci.yml`) testing Linux, macOS, and Windows on Python 3.9, 3.10, 3.11, 3.12, and 3.13.
- [ ] **Task C.2 (Containerization):**
  - Provide a clean, reproducible `Dockerfile` and `docker-compose.yml` demonstrating headless Eel execution / web service mode.
- [ ] **Task C.3 (Open Source Documentation):**
  - Overhaul `README.md` with modern quickstart, badges, architecture diagrams, and accurate browser support.
  - Create `CONTRIBUTING.md`, `SECURITY.md`, and update `CHANGELOG.md`.
  - Provide complete technical audit and verification reports in `docs/revival/`.

---

## 3. Completion Criteria

1. `pip install -e .` succeeds in clean environments on Python 3.9–3.13 without warnings or compilation failures.
2. `mypy --strict eel` passes with 0 errors.
3. Unit and integration tests execute and pass cleanly with real assertions.
4. An Eel application starts and performs bidirectional RPC between Python and JavaScript.
5. All security risks (command injection, arbitrary exec, debugger statements) are eliminated.

