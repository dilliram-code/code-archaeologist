import os
import eel
import pytest
from tests.utils import TEST_DATA_DIR

# Directory for testing eel.__init__
INIT_DIR = TEST_DATA_DIR / 'init_test'


@pytest.mark.parametrize('js_code, expected_matches', [
    ('eel.expose(w,"say_hello_js")', ['say_hello_js']),
    ('eel.expose(function(e){console.log(e)},"show_log_alt")', ['show_log_alt']),
    (' \t\nwindow.eel.expose((function show_log(e) {console.log(e)}), "show_log")\n', ['show_log']),
    ((INIT_DIR / 'minified.js').read_text(), ['say_hello_js', 'show_log_alt', 'show_log']),
    ((INIT_DIR / 'sample.html').read_text(), ['say_hello_js']),
    ((INIT_DIR / 'App.tsx').read_text(), ['say_hello_js', 'show_log']),
    ((INIT_DIR / 'hello.html').read_text(), ['say_hello_js', 'js_random']),
])
def test_exposed_js_functions(js_code, expected_matches):
    """Test the PyParsing grammar against several specific test cases."""
    matches = eel._parse_exposed_js_calls(js_code)
    assert matches == expected_matches, f'Expected {expected_matches} (found: {matches}) in: {js_code}'


def test_init():
    """Test eel.init() against a test directory and ensure that all JS functions are in the global _js_functions."""
    eel.init(path=str(INIT_DIR))
    expected = sorted(['show_log', 'js_random', 'show_log_alt', 'say_hello_js'])
    actual = sorted(eel._js_functions)
    assert actual == expected, f'Expected {expected} (found: {actual}) in {INIT_DIR}'


def test_expose_decorator():
    """Test exposing functions with and without custom names."""
    @eel.expose
    def py_test_func(a, b):
        return a + b

    assert 'py_test_func' in eel._exposed_functions
    assert eel._exposed_functions['py_test_func'](2, 3) == 5

    @eel.expose('custom_exposed_name')
    def another_func():
        return "custom_val"

    assert 'custom_exposed_name' in eel._exposed_functions
    assert eel._exposed_functions['custom_exposed_name']() == "custom_val"


def test_malicious_js_identifier_rejected():
    """Security test: Ensure invalid or malicious JS identifiers cannot inject arbitrary code."""
    malicious_names = [
        "__import__('os').system('echo hacked')",
        "foo; bar()",
        "123invalid",
        "hello-world",
        "def foo(): pass",
    ]
    for bad_name in malicious_names:
        eel._mock_js_function(bad_name)
        assert bad_name not in globals(), f"Malicious identifier '{bad_name}' was improperly bound!"
        eel._import_js_function(bad_name)
        assert bad_name not in globals(), f"Malicious identifier '{bad_name}' was improperly imported!"


def test_process_message_rpc_call():
    """Test WebSocket message processing for Python function calls."""
    @eel.expose('test_add')
    def add_nums(x, y):
        return x + y

    sent_messages = []

    class MockWebSocket:
        def send(self, msg):
            sent_messages.append(msg)

    ws = MockWebSocket()
    message = {
        'call': 12345,
        'name': 'test_add',
        'args': [10, 25]
    }
    eel._process_message(message, ws)

    assert len(sent_messages) == 1
    import json
    data = json.loads(sent_messages[0])
    assert data['return'] == 12345
    assert data['status'] == 'ok'
    assert data['value'] == 35


def test_process_message_rpc_error():
    """Test WebSocket message processing when exposed function raises an exception."""
    @eel.expose('test_fail')
    def fail_func():
        raise ValueError("Simulated failure")

    sent_messages = []

    class MockWebSocket:
        def send(self, msg):
            sent_messages.append(msg)

    ws = MockWebSocket()
    message = {
        'call': 999,
        'name': 'test_fail',
        'args': []
    }
    eel._process_message(message, ws)

    assert len(sent_messages) == 1
    import json
    data = json.loads(sent_messages[0])
    assert data['return'] == 999
    assert data['status'] == 'error'
    assert "ValueError" in data['error']['errorText']


def test_browser_discovery():
    """Test browser discovery modules."""
    import eel.chrome as chm
    import eel.edge as edge
    import eel.electron as ele
    import eel.msIE as msie

    # Verify every browser module defines required interface
    for mod in [chm, edge, ele, msie]:
        assert hasattr(mod, 'name')
        assert hasattr(mod, 'run')
        assert hasattr(mod, 'find_path')
        assert callable(mod.find_path)


def test_build_urls():
    """Test URL building logic."""
    import eel.browsers as brw
    options = {'host': '127.0.0.1', 'port': 8080}
    urls = brw._build_urls(['main.html', {'scheme': 'http', 'host': 'localhost', 'port': 9000, 'path': 'page.html'}], options)
    assert urls[0] == 'http://127.0.0.1:8080/main.html'
    assert urls[1] == 'http://localhost:9000/page.html'
