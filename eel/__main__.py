from __future__ import annotations
import os
import sys
from argparse import ArgumentParser, Namespace
from typing import List

try:
    from importlib.resources import files, as_file
except ImportError:
    from importlib_resources import files, as_file  # type: ignore[no-redef]


def get_eel_js_path() -> str:
    """Safely resolve the file path to eel.js for PyInstaller packaging."""
    ref = files('eel') / 'eel.js'
    # Use as_file to support both extracted directories and zipped distributions
    with as_file(ref) as file_path:
        return str(file_path)


def main() -> None:
    import PyInstaller.__main__ as pyi

    parser: ArgumentParser = ArgumentParser(description="""
Eel is a little Python library for making simple Electron-like offline HTML/JS GUI apps,
 with full access to Python capabilities and libraries.
""")
    parser.add_argument(
        "main_script",
        type=str,
        help="Main python file to run app from"
    )
    parser.add_argument(
        "web_folder",
        type=str,
        help="Folder including all web files including file as html, css, ico, etc."
    )
    args: Namespace
    unknown_args: List[str]
    args, unknown_args = parser.parse_known_args()
    main_script: str = args.main_script
    web_folder: str = args.web_folder

    print("Building executable with main script '%s' and web folder '%s'...\n" %
          (main_script, web_folder))

    eel_js_file: str = get_eel_js_path()
    js_file_arg: str = '%s%seel' % (eel_js_file, os.pathsep)
    web_folder_arg: str = '%s%s%s' % (web_folder, os.pathsep, web_folder)

    needed_args: List[str] = ['--hidden-import', 'bottle_websocket',
                              '--add-data', js_file_arg, '--add-data', web_folder_arg]
    full_args: List[str] = [main_script] + needed_args + unknown_args
    print('Running:\npyinstaller', ' '.join(full_args), '\n')

    pyi.run(full_args)


if __name__ == '__main__':
    main()
