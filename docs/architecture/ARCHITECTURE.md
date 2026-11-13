# Eel Architecture Documentation

## 1. System Overview

Eel bridges Python and web technologies by hosting a local WSGI server running on Bottle and Gevent-WebSocket, opening a local browser instance in App Mode, and facilitating bidirectional Remote Procedure Calls (RPC) over a persistent WebSocket connection.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Browser as Client Browser (Chrome / Edge / Brave)
    participant WS as WebSocket Bridge (/eel)
    participant Bottle as Bottle WSGI Server
    participant Python as Python Backend (@eel.expose)

    User->>Python: eel.init('web') & eel.start('main.html')
    Python->>Bottle: Start local WSGI server (port 8000 or dynamic)
    Python->>Browser: Launch browser with --app=http://localhost:8000/main.html
    Browser->>Bottle: HTTP GET /main.html & /eel.js
    Bottle-->>Browser: Serve HTML & dynamic eel.js (exposed functions payload)
    Browser->>WS: Open WebSocket connection ws://localhost:8000/eel?page=main.html
    WS-->>Browser: Connection established

    Note over Browser, Python: Bidirectional RPC Communication
    Browser->>WS: {"call": 1, "name": "py_func", "args": [42]}
    WS->>Python: Invoke registered @eel.expose function
    Python-->>WS: Return result
    WS-->>Browser: {"return": 1, "status": "ok", "value": "Processed"}

    Python->>WS: eel.js_func("hello")
    WS-->>Browser: {"call": 2, "name": "js_func", "args": ["hello"]}
    Browser-->>WS: {"return": 2, "status": "ok", "value": "Ack"}
    WS-->>Python: Return result to Python
```

---

## 2. Component Design

### 2.1 Python Core (`eel/__init__.py`)
- **`init(path, allowed_extensions, ...)`:**
  Scans the directory of static assets for JavaScript calls to `eel.expose()`. Binds proxy functions dynamically to module globals without `exec()`.
- **`start(*start_urls, mode, host, port, ...)`:**
  Sets up Bottle HTTP routing, binds WebSocket endpoint, resolves browser path, launches the browser process, and starts the Gevent server loop.
- **`expose(name_or_function)`:**
  Decorator registering Python functions in `_exposed_functions` dictionary for WebSocket invocation.
- **`_process_message(message, ws)`:**
  Dispatches incoming WebSocket JSON payloads, executing Python functions or resolving return value callbacks for JavaScript calls.

### 2.2 Frontend Bridge (`eel/eel.js`)
- Injected on the web page, initializing `window.eel`.
- Provides `eel.expose(func, name)` in JavaScript.
- Connects WebSocket on DOMContentLoaded.
- Translates `await eel.py_function(args)()` into promises resolved when Python sends back the return message.

### 2.3 Browser Launchers (`eel/browsers.py`)
- Abstract interface delegating to browser-specific modules:
  - `eel.chrome`: Google Chrome, Chromium, Brave Browser
  - `eel.edge`: Microsoft Edge (Chromium-based)
  - `eel.electron`: Electron standalone binaries
  - `eel.msIE`: Legacy Edge IE compatibility redirect

