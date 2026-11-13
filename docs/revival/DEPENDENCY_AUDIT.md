# Dependency & Environment Audit Report

**Project Name:** Eel (Python-Eel)  
**Investigating Agent:** The Dependency & Environment Detective (Agent 3)  
**Date:** November 2026  
**Target Environment:** Cross-platform (Linux, macOS, Windows), Python 3.9 – 3.13  

---

## 1. Technical Environment Baseline

### 1.1 Python Runtime
- **Repository Baseline:** Specified `python_requires='>=3.7'` in `setup.py`, with classifiers only for Python 3.7 and 3.8. Both Python 3.7 and 3.8 have reached official End-of-Life (EOL).
- **Modern Target:** Python 3.9, 3.10, 3.11, 3.12, 3.13.

### 1.2 Package & Build Systems
- **Repository Baseline:**
  - `setup.py` using legacy setuptools without `pyproject.toml`.
  - Unmanaged requirements files (`requirements.txt`, `requirements-test.txt`, `requirements-meta.txt`) with conflicting constraints.
  - No deterministic lockfile.
  - Tox 3 configuration (`tox.ini`) relying on deprecated plugins (`tox-pyenv`, `tox-gh-actions`).
- **Modern Recommendation:**
  - Modern `pyproject.toml` adhering to PEP 517/518/621 specifications.
  - Support standard packaging tools (`pip`, `uv`, `build`, `hatchling` / `setuptools`).
  - Streamlined GitHub Actions matrix testing against Ubuntu, Windows, and macOS on modern Python versions.

---

## 2. Dependency Audit Matrix

| Package Name | Baseline Version | Recommended Version | Status | Justification / Impact |
|---|---|---|---|---|
| `gevent` | `gevent` (unpinned in reqs, pulled 22.10.1) | `>=24.2.1` | **Upgrade (Critical)** | Older gevent builds fail on modern Cython 3 (`undeclared name not builtin: long`). Modern gevent provides wheels for Python 3.10–3.13. |
| `greenlet` | `>=1.0.0,<2.0.0` | `>=3.0.0` | **Upgrade (Critical)** | `greenlet<2.0.0` is incompatible with Python 3.11+. The pin broke all installs on modern Python. |
| `future` | Listed in `setup.py` | *Remove* | **Remove (Critical)** | Obsolete Python 2/3 compatibility package. Unused in Python 3.7+. |
| `bottle` | `<1.0.0` | `>=0.12.25,<1.0.0` | **Retain / Update** | Core WSGI micro-framework. Maintain stable <1.0.0 bounds. |
| `bottle-websocket` | `<1.0.0` | `>=0.2.9,<1.0.0` | **Retain / Audit** | Provides WebSocket integration for Bottle. Compatible with gevent-websocket. |
| `gevent-websocket` | `<1.0.0` | `>=0.10.1,<1.0.0` | **Retain** | WebSocket handler for Gevent WSGI server. |
| `pyparsing` | `>=3.0.0,<4.0.0` | `>=3.1.0,<4.0.0` | **Retain / Update** | Used for parsing `eel.expose()` calls in frontend code. |
| `typing-extensions` | `>=4.3.0` | `>=4.8.0` | **Retain / Update** | Backport typing features across supported Python versions. |
| `importlib_resources` | `>=1.3` | `>=5.0.0` | **Retain / Conditional** | Backport for reading package data assets (`eel.js`). In Python 3.9+, standard library `importlib.resources` can be used directly with fallback. |
| `jinja2` | `>=2.10` (extra) | `>=3.1.0` | **Upgrade** | Templating engine for HTML views. Jinja2 3.x has security fixes and modern Python support. |
| `selenium` | `>=4.0.0,<5.0.0` | `>=4.20.0` | **Upgrade** | E2E browser automation for tests. Selenium 4.20+ includes native Selenium Manager, removing flaky third-party driver downloads. |
| `pytest` | `>=7.0.0,<8.0.0` | `>=8.0.0` | **Upgrade** | Modern test runner. |
| `pytest-timeout` | `>=2.0.0,<3.0.0` | `>=2.3.0` | **Retain / Update** | Prevents hanging tests when web server subprocesses run. |
| `mypy` | `>=1.0.0,<2.0.0` | `>=1.10.0` | **Upgrade** | Static type analysis. |
| `pyinstaller` | unpinned | `>=6.0.0` | **Upgrade** | Distributable packaging tool for desktop apps. |

---

## 3. Dependency Conflict Resolution

### The Greenlet / Cython / Gevent Deadlock:
1. **The Conflict:**
   - In `requirements.txt`: `greenlet>=1.0.0,<2.0.0`
   - Pip/uv attempted to find a `gevent` release compatible with `greenlet < 2.0.0`, selecting `gevent==22.10.1`.
   - On Python 3.10+, building `gevent==22.10.1` from source invoked Cython 3.
   - Cython 3 failed compiling `src/gevent/libev/corecext.pyx` due to `long` being removed.
2. **The Resolution:**
   - Upgrade `greenlet>=3.0.0` and `gevent>=24.0.0`.
   - Pre-compiled wheels exist for modern architectures (x86_64, aarch64/arm64) across Linux, macOS, and Windows.
   - Installation completes cleanly without Cython compilation failures.

---

## 4. Environment Requirements for Verification

- **Node.js / NPM (Optional for examples):** Examples 07 (CreateReactApp) and 09 (Electron) have frontend assets. The core Eel library itself has zero Node.js dependencies.
- **System Web Browsers:** Google Chrome, Chromium, Microsoft Edge, or system default browser.
- **Port Availability:** Dynamic port binding (`port=0`) or default port 8000.
