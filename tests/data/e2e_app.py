import os
import sys
import eel

# Ensure root web directory is resolved properly
base_dir = os.path.dirname(os.path.abspath(__file__))
web_dir = os.path.join(base_dir, 'init_test')
eel.init(web_dir)


@eel.expose('e2e_add')
def add(a: int, b: int) -> int:
    return a + b


@eel.expose('e2e_greet')
def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    eel.start('sample.html', mode=False, port=port, block=True, host='127.0.0.1')
