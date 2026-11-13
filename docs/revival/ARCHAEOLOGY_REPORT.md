# Archaeological Analysis Report: Python-Eel (Eel)

**Project Name:** Eel (Python-Eel)  
**Original Repository:** `https://github.com/python-eel/Eel.git`  
**Target Revival Branch:** `revive/eel-20261113`  
**Date of Investigation:** November 2026  
**Investigating Agent:** The Code Archaeologist (Agent 2) & Chief Architect (Agent 1)  

---

## 1. Executive Summary

Eel is a popular, lightweight Python library created in 2017 by Chris Knott (and later maintained under the `python-eel` GitHub organization by Samuel H. Williams and contributors) designed to build Electron-like desktop GUI applications using web technologies (HTML, CSS, JavaScript) backed by a Python server. Unlike heavyweight frameworks such as Electron (Node.js/Chromium) or CEFPython (Chromium Embedded Framework), Eel achieves GUI capabilities by combining:
1. A local WSGI web server running on **Bottle** and **Gevent-WebSocket**.
2. A lightweight bi-directional JSON-RPC bridge over WebSockets.
3. Automated launching of system browsers (Google Chrome / Chromium in `--app` mode, Microsoft Edge, or system default).
4. Code-level RPC decorators (`@eel.expose` in Python and `eel.expose()` in JavaScript) enabling seamless function calls across language boundaries.

In June 2025, the project was officially declared **unmaintained** by its primary maintainer (`b161f13 - Add unmaintained warning to readme.`), leaving critical technical debt, obsolete packaging, dependency conflicts, unpinned build environments, and latent security issues.

---

## 2. Historical Timeline & Evolution

| Period / Commit | Milestone / Event | Impact |
|---|---|---|
| **2017** | Initial creation by Chris Knott | Introduced the core concept: Bottle + gevent-websocket + Chrome app mode. |
| **2018–2020** | Expansion & Organization | Moved to `python-eel` organization. Added callbacks, promise support, Electron launcher, Jinja2 templating. |
| **v0.12 – v0.16** | Cross-platform refinements | Added Edge support, multi-window geometry, PyInstaller integration, dynamic port binding. |
| **v0.18.0 (2024)** | Migration to Python >= 3.7 (`7c3f6ad`) | Added initial type annotations, dropped Python 2 syntax, added `typing_extensions` and `types.py`. |
| **v0.18.1 – v0.18.2 (June 2025)** | Maintenance releases (`0ede901`, `07c0ec7`) | Fixed missing dependencies, switched from deprecated `pkg_resources` to `importlib.resources`. |
| **June 16–22, 2025** | Unmaintained warning (`b161f13`, `e779b24`) | Maintainer added caution banner to README stating no further updates planned. Project abandoned. |

---

## 3. Original Architecture & Codebase Map

```text
Eel (Repository)
│
├── eel/                                 # Core Python Package
│   ├── __init__.py                      # Main entrypoint: expose, init, start, show, sleep, spawn, WebSocket handler
│   ├── eel.js                           # Frontend client library injecting the `window.eel` bridge
│   ├── browsers.py                      # Browser launcher abstraction (Chrome, Edge, Electron, system default)
│   ├── chrome.py                        # Chrome/Chromium launcher & finder across OS platforms
│   ├── edge.py                          # Microsoft Edge launcher
│   ├── electron.py                      # Electron subprocess runner
│   ├── msIE.py                          # Deprecated Internet Explorer launcher
│   ├── types.py                         # Type aliases and typing stubs
│   └── py.typed                         # PEP 561 typing marker
│
├── examples/                            # Official demonstration applications
│   ├── 01 - hello_world/                # Basic bidirectional call demo
│   ├── 02 - callbacks/                  # Asynchronous callback demo
│   ├── 03 - sync_callbacks/             # Synchronous return value demo
│   ├── 04 - file_access/                # Native OS file system access demo
│   ├── 05 - input/                      # Form input handling demo
│   ├── 06 - jinja_templates/            # Server-side templating with Jinja2
│   ├── 07 - CreateReactApp/             # React SPA integration
│   ├── 08 - disable_cache/              # Cache-control demonstration
│   ├── 09 - Eelectron-quick-start/      # Electron integration demo
│   └── 10 - custom_app_routes/          # Custom Bottle route extension
│
├── tests/                               # Test suite
│   ├── unit/test_eel.py                 # PyParsing regex tests and init tests
│   ├── integration/test_examples.py     # Selenium-based end-to-end example tests
│   ├── conftest.py                      # Selenium WebDriver fixtures
│   └── utils.py                         # Test harness and server lifecycle helpers
│
├── .github/workflows/                   # CI/CD configurations
│   ├── test.yml                         # Outdated tox CI matrix
│   └── main.yml                         # PyPI publish workflow
│
├── setup.py                             # Legacy setuptools packaging
├── requirements.txt                     # Pinned runtime dependencies
├── requirements-test.txt                # Pinned test dependencies
└── tox.ini                              # Legacy tox configuration
```

---

## 4. Why the Project Stalled: Root Cause Analysis

1. **Obsolete & Rigid Dependency Pinning:**
   - `requirements.txt` pinned `greenlet>=1.0.0,<2.0.0`. On modern Python (3.11, 3.12, 3.13), greenlet < 2.0.0 does not compile. This forced resolvers to fetch ancient `gevent==22.10.1`, which fails Cython compilation with `undeclared name not builtin: long` because modern Cython 3 dropped Python 2 built-in types.
   - `setup.py` retained `future` in `install_requires`, an obsolete Python 2/3 compatibility package that has not been needed since Python 2 support was dropped.
2. **Brittle Packaging & Build Infrastructure:**
   - Relies on legacy `setup.py` without a `pyproject.toml` (PEP 517/518/621).
   - Tox configuration (`tox.ini`) relied on deprecated `tox-pyenv` and `tox-gh-actions` (v2), incompatible with modern Tox 4+.
3. **Flawed and Ineffective Testing:**
   - In `tests/unit/test_eel.py`, `test_init()` executed:
     ```python
     result = eel._js_functions.sort()
     functions = ['show_log', 'js_random', 'show_log_alt', 'say_hello_js'].sort()
     assert result == functions
     ```
     Because Python's `list.sort()` sorts in-place and returns `None`, `result` was `None` and `functions` was `None`. The test passed unconditionally regardless of whether `_js_functions` contained the expected values!
   - Integration tests depend on Selenium 4 with an obsolete WebDriverManager pattern (`webdriver_manager.chrome.ChromeDriverManager().install()`), which frequently fails on modern Chrome with new driver endpoints.
4. **Security Vulnerabilities:**
   - In `eel/__init__.py`, `_mock_js_function` and `_import_js_function` use `exec()` with string formatting:
     ```python
     exec('%s = lambda *args: _mock_call("%s", args)' % (f, f), globals())
     ```
     PyParsing regex extracts identifiers from parsed JS files, but invalid or hostile JS function names can lead to arbitrary code execution during Python initialization.
   - Production JS artifact: In `eel/eel.js` (line 138), a `debugger;` statement was left in the production error handler.
5. **Python Anti-Patterns & Code Quality:**
   - Mutable default arguments in `eel.start()`:
     `cmdline_args: List[str] = ['--disable-http-cache']` and `geometry: Dict[str, Tuple[int, int]] = {}`. In Python, mutable default arguments retain state across multiple calls.
   - In `eel/msIE.py`, `find_path()` returns `bool`, violating the return type contract `Optional[str]` expected by `eel.browsers`.

---

## 5. Preservation vs. Modernization Strategy

### What Must Be Preserved (Core Identity):
- **Zero-Boilerplate API:** Keep `eel.init()`, `eel.start()`, and `@eel.expose`. Developers love Eel because 3 lines of code create a desktop app.
- **Frontend Agnosticism:** Allow plain HTML, Vue, React, Svelte, or Jinja templates without requiring custom build steps.
- **Bi-directional Asynchronous RPC:** Preserve seamless calls from Python to JS (`eel.js_func()()`) and JS to Python (`await eel.py_func()()`).

### What Must Be Modernized:
- Modern packaging (`pyproject.toml` with `hatchling` or modern `setuptools`).
- Modern runtime compatibility (Python 3.9 through 3.13).
- Upgrade `gevent` and `greenlet` to modern versions with clean binary wheels across macOS, Linux, and Windows.
- Eliminate `future` and obsolete dependencies.
- Remove arbitrary `exec()` in favor of dynamic attribute assignment (`setattr` / `__getattr__`).
- Fix tests and assertions so they actually verify functionality.
- Provide modern Docker and CI/CD workflows.
