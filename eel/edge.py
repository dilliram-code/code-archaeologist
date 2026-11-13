from __future__ import annotations
import os
import subprocess as sps
import sys
from shutil import which
from typing import List, Optional, Any
from eel.types import OptionsDictT

name: str = 'Edge'


def run(path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    if not isinstance(options.get('cmdline_args'), list):
        raise TypeError("'cmdline_args' option must be of type List[str]")
    cmdline_args: List[str] = options['cmdline_args']

    for url in start_urls:
        if options.get('app_mode', True):
            cmd = [path, f'--app={url}'] + cmdline_args
        else:
            cmd = [path, '--new-window'] + cmdline_args + [url]

        sps.Popen(cmd, stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)


def find_path() -> Optional[str]:
    if sys.platform in ['win32', 'win64']:
        return _find_edge_win()
    elif sys.platform == 'darwin':
        return _find_edge_mac()
    elif sys.platform.startswith('linux'):
        return _find_edge_linux()
    return None


def _find_edge_mac() -> Optional[str]:
    default_dir = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
    if os.path.isfile(default_dir):
        return default_dir
    return None


def _find_edge_linux() -> Optional[str]:
    for name in ['microsoft-edge', 'microsoft-edge-stable', 'msedge']:
        path = which(name)
        if path is not None:
            return path
    return None


def _find_edge_win() -> Optional[str]:
    try:
        import winreg as reg
    except ImportError:
        return None

    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe'
    edge_path: Optional[str] = None

    reg_hives: List[Any] = [
        getattr(reg, 'HKEY_CURRENT_USER', None),
        getattr(reg, 'HKEY_LOCAL_MACHINE', None),
    ]

    for install_type in reg_hives:
        if install_type is None:
            continue
        try:
            open_key = getattr(reg, 'OpenKey', None)
            key_read = getattr(reg, 'KEY_READ', 0)
            query_value = getattr(reg, 'QueryValue', None)
            if not open_key or not query_value:
                continue

            reg_key = open_key(install_type, reg_path, 0, key_read)
            edge_path = query_value(reg_key, None)
            reg_key.Close()
            if edge_path and os.path.isfile(edge_path):
                return edge_path
        except OSError:
            edge_path = None

    for env_var in ['PROGRAMFILES(X86)', 'PROGRAMFILES', 'LOCALAPPDATA']:
        base = os.environ.get(env_var)
        if base:
            candidate = os.path.join(base, r'Microsoft\Edge\Application\msedge.exe')
            if os.path.isfile(candidate):
                return candidate

    return which('msedge')
