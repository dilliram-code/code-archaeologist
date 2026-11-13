import json
import urllib.request
import websocket
import pytest
import eel
from tests.utils import TEST_DATA_DIR

INIT_DIR = TEST_DATA_DIR / 'init_test'


def test_eel_http_and_websocket_e2e():
    """End-to-end test of the Eel Bottle HTTP server and WebSocket RPC."""
    eel.init(str(INIT_DIR))

    @eel.expose('e2e_multiply')
    def multiply(a: int, b: int) -> int:
        return a * b

    @eel.expose('e2e_echo')
    def echo(msg: str) -> str:
        return f"Echo: {msg}"

    # Start Eel in non-blocking mode with mode=False (no browser window) on dynamic port
    eel.start(
        'sample.html',
        mode=False,
        port=0,
        block=False,
        host='127.0.0.1',
    )

    # Yield control to gevent event loop so Bottle WSGI server can bind and listen
    eel.sleep(0.5)
    actual_port = eel._start_args['port']
    assert actual_port > 0, f"Expected valid assigned port, got {actual_port}"

    base_url = f"http://127.0.0.1:{actual_port}"

    # 1. Test HTTP GET /eel.js
    req = urllib.request.Request(f"{base_url}/eel.js")
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        content_type = response.headers.get('Content-Type')
        assert 'javascript' in content_type
        body = response.read().decode('utf-8')
        assert 'eel = {' in body
        assert 'e2e_multiply' in body
        assert 'e2e_echo' in body

    # 2. Test HTTP GET static asset (/sample.html)
    with urllib.request.urlopen(f"{base_url}/sample.html") as response:
        assert response.status == 200
        html = response.read().decode('utf-8')
        assert 'eel.expose(say_hello_js)' in html

    # 3. Test WebSocket JSON-RPC connection
    ws_url = f"ws://127.0.0.1:{actual_port}/eel?page=sample.html"
    ws = websocket.create_connection(ws_url, timeout=5)

    try:
        # Client sends RPC call to Python: e2e_multiply(6, 7)
        call_msg = {
            'call': 101,
            'name': 'e2e_multiply',
            'args': [6, 7]
        }
        ws.send(json.dumps(call_msg))
        raw_reply = ws.recv()
        reply = json.loads(raw_reply)

        assert reply['return'] == 101
        assert reply['status'] == 'ok'
        assert reply['value'] == 42

        # Client sends RPC call to Python: e2e_echo("Antigravity")
        call_echo = {
            'call': 102,
            'name': 'e2e_echo',
            'args': ["Antigravity"]
        }
        ws.send(json.dumps(call_echo))
        raw_echo_reply = ws.recv()
        echo_reply = json.loads(raw_echo_reply)

        assert echo_reply['return'] == 102
        assert echo_reply['status'] == 'ok'
        assert echo_reply['value'] == "Echo: Antigravity"

    finally:
        ws.close()
