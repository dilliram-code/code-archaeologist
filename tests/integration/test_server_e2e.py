import json
import os
import subprocess
import sys
import time
import urllib.request
import websocket
import pytest
from tests.utils import TEST_DATA_DIR, get_process_listening_port


def test_eel_http_and_websocket_e2e():
    """End-to-end test of the Eel Bottle HTTP server and WebSocket RPC."""
    app_script = TEST_DATA_DIR / 'e2e_app.py'

    # Launch the Eel app subprocess on an auto-assigned port (port=0)
    proc = subprocess.Popen(
        [sys.executable, str(app_script), "0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(TEST_DATA_DIR)
    )

    try:
        # Wait up to 10 seconds for the subprocess to bind and listen
        port = None
        for _ in range(100):
            try:
                port = get_process_listening_port(proc)
                if port:
                    break
            except Exception:
                time.sleep(0.1)

        assert port is not None, "Eel server subprocess failed to start listening"
        base_url = f"http://127.0.0.1:{port}"

        # 1. Test HTTP GET /eel.js
        req = urllib.request.Request(f"{base_url}/eel.js")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200
            content_type = response.headers.get('Content-Type')
            assert 'javascript' in content_type
            body = response.read().decode('utf-8')
            assert 'eel = {' in body
            assert 'e2e_add' in body
            assert 'e2e_greet' in body

        # 2. Test HTTP GET static asset (/sample.html)
        with urllib.request.urlopen(f"{base_url}/sample.html", timeout=5) as response:
            assert response.status == 200
            html = response.read().decode('utf-8')
            assert 'eel.expose(say_hello_js)' in html

        # 3. Test WebSocket JSON-RPC connection
        ws_url = f"ws://127.0.0.1:{port}/eel?page=sample.html"
        ws = websocket.create_connection(ws_url, timeout=5)

        try:
            # Client sends RPC call: e2e_add(15, 27)
            call_msg = {
                'call': 101,
                'name': 'e2e_add',
                'args': [15, 27]
            }
            ws.send(json.dumps(call_msg))
            reply = json.loads(ws.recv())

            assert reply['return'] == 101
            assert reply['status'] == 'ok'
            assert reply['value'] == 42

            # Client sends RPC call: e2e_greet("Antigravity")
            call_greet = {
                'call': 102,
                'name': 'e2e_greet',
                'args': ["Antigravity"]
            }
            ws.send(json.dumps(call_greet))
            reply_greet = json.loads(ws.recv())

            assert reply_greet['return'] == 102
            assert reply_greet['status'] == 'ok'
            assert reply_greet['value'] == "Hello, Antigravity!"

        finally:
            ws.close()

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
