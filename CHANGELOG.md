# Change log

### 0.19.0 (Revival Release - November 2026)

* **Packaging:** Complete PEP 517/518/621 modernization with `pyproject.toml`.
* **Runtime Support:** Full compatibility with Python 3.9, 3.10, 3.11, 3.12, and 3.13. Removed deprecated Python 2 `future` package.
* **Dependency Unblock:** Upgraded to `greenlet>=3.0.0` and `gevent>=24.2.1`, resolving Cython 3 build failures and modern wheel compatibility.
* **Security Hardening:**
  * Replaced arbitrary `exec()` string evaluation in `_mock_js_function` and `_import_js_function` with strict identifier validation and safe `globals()` binding.
  * Eliminated command injection risks by removing `shell=True` in browser execution commands.
  * Removed debug artifact (`debugger;`) from production `eel.js`.
* **Browser Expansion:**
  * Modernized Edge support across macOS, Linux, and Windows, returning valid executable paths.
  * Added discovery for Chromium and Brave Browser in addition to Google Chrome.
* **Quality & Verification:**
  * Fixed bug in `test_init` where `.sort()` returned `None`, allowing tests to pass vacuously.
  * Added live end-to-end integration test (`tests/integration/test_server_e2e.py`) verifying real HTTP asset serving and WebSocket RPC.
  * Achieved 100% clean strict static typing with MyPy (`mypy --strict eel`).
* **DevOps:** Added Dockerfile, docker-compose.yml, multi-OS GitHub Actions workflow, and developer setup scripts.

### 0.18.2

* Switch from using `pkg_resources` to `importlib.resources`: https://github.com/python-eel/Eel/pull/766

### 0.18.1

* Fix: Include `typing_extensions` in install requirements.

### 0.18.0
* Added support for MS Internet Explorer in #744.
* Added supported for app_mode in the Edge browser in #744.
* Improved type annotations in #683.

### 0.17.0
* Adds support for Python 3.11 and Python 3.12

### v0.16.0
* Drop support for Python versions below 3.7

### v0.15.3
* Comprehensive type hints implement by @thatfloflo in https://github.com/python-eel/Eel/pull/577.

### v0.15.2
* Adds `register_eel_routes` to handle applying Eel routes to non-Bottle custom app instances.

### v0.15.1
* Bump bottle dependency from 0.12.13 to 0.12.20 to address the critical CVE-2022-31799 and moderate CVE-2020-28473.

### v0.15.0
* Add `shutdown_delay` as a `start()` function parameter ([#529](https://github.com/python-eel/Eel/pull/529))

### v0.14.0
* Change JS function name parsing to use PyParsing rather than regex, courtesy @KyleKing.

### v0.13.2
* Add `default_path` start arg to define a default file to retrieve when hitting the root URL.

### v0.13.1
* Shut down the Eel server less aggressively when websockets get closed (#337)

## v0.13.0
* Drop support for Python versions below 3.6
* Add `jinja2` as an extra for pip installation, e.g. `pip install eel[jinja2]`.
* Bump dependencies in examples to dismiss github security notices. We probably want to set up a policy to ignore example dependencies as they shouldn't be considered a source of vulnerabilities.
* Disable edge on non-Windows platforms until we implement proper support.

### v0.12.4
* Return greenlet task from `spawn()` ([#300](https://github.com/samuelhwilliams/Eel/pull/300))
