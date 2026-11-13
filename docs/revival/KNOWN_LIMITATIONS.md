# Known Limitations & Design Boundaries

**Project:** Python-Eel (Eel)  
**Date:** November 2026  
**Documenting Agent:** Chief Architect (Agent 1)  

---

## 1. Architectural Boundaries

Eel is explicitly designed for lightweight, offline, Electron-like utility desktop applications and developer dashboards. It is not intended to replace full-scale native GUI toolkits (Qt, wxWidgets) or complex web application servers.

Key architectural boundaries to keep in mind:

1. **Gevent Cooperative Concurrency:**
   Eel runs on Gevent. Any long-running blocking CPU-intensive calculations performed on the main thread will starve the Gevent event loop and prevent WebSocket messages from being processed. Applications should offload heavy CPU work to background greenlets (`eel.spawn`) or worker threads/processes.

2. **Single-User / Localhost Assumptions:**
   Eel was architected primarily for single-user local applications. While `all_interfaces=True` permits listening on `0.0.0.0`, Eel contains no built-in session isolation, per-socket user authentication, or cryptographic authorization between different browser tabs. If deployed over a public network, it should sit behind an authenticating reverse proxy with TLS.

3. **Browser App Mode Support:**
   Eel launches Chrome, Edge, Chromium, and Brave in `--app` mode (frameless browser window looking like a desktop application). Browsers such as Mozilla Firefox and Safari do not support an equivalent `--app` command-line switch; for those browsers, Eel opens a standard browser tab.

4. **PyInstaller Binary Bundling:**
   While `python -m eel` or `eel-pack` automates PyInstaller configuration, packaging desktop apps for cross-platform distribution requires building on each target operating system (Windows for `.exe`, macOS for `.app`/`.dmg`, Linux for AppImage/binary).

5. **Legacy Internet Explorer Mode:**
   The `msie` mode is maintained solely for legacy backwards-compatibility via Microsoft Edge's IE compatibility redirect on Windows. Internet Explorer 11 itself has been retired by Microsoft.

