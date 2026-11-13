from __future__ import annotations
import sys
import os
import subprocess as sps
from shutil import which
from typing import List, Optional, Any
from eel.types import OptionsDictT

name: str = 'Google Chrome/Chromium'


def run(path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    if not isinstance(options['cmdline_args'], list):
        raise TypeError("'cmdline_args' option must be of type List[str]")
    if options['app_mode']:
        for url in start_urls:
            sps.Popen([path, '--app=%s' % url] +
                      options['cmdline_args'],
                      stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
    else:
        args: List[str] = options['cmdline_args'] + start_urls
        sps.Popen([path, '--new-window'] + args,
                  stdout=sps.PIPE, stderr=sys.stderr, stdin=sps.PIPE)


def find_path() -> Optional[str]:
    if sys.platform in ['win32', 'win64']:
        return _find_chrome_win()
    elif sys.platform == 'darwin':
        return _find_chrome_mac() or _find_chromium_mac() or _find_brave_mac()
    elif sys.platform.startswith('linux'):
        return _find_chrome_linux()
    else:
        return None


def _find_chrome_mac() -> Optional[str]:
    default_dir = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    if os.path.exists(default_dir):
        return default_dir
    # Use mdfind to locate Chrome in alternate locations and return the first one
    name = 'Google Chrome.app'
    try:
        alternate_dirs = [x for x in sps.check_output(["mdfind", name]).decode().split('\n') if x.endswith(name)]
        if alternate_dirs:
            candidate = alternate_dirs[0] + '/Contents/MacOS/Google Chrome'
            if os.path.isfile(candidate):
                return candidate
    except Exception:
        pass
    return None


def _find_chromium_mac() -> Optional[str]:
    default_dir = r'/Applications/Chromium.app/Contents/MacOS/Chromium'
    if os.path.exists(default_dir):
        return default_dir
    name = 'Chromium.app'
    try:
        alternate_dirs = [x for x in sps.check_output(["mdfind", name]).decode().split('\n') if x.endswith(name)]
        if alternate_dirs:
            candidate = alternate_dirs[0] + '/Contents/MacOS/Chromium'
            if os.path.isfile(candidate):
                return candidate
    except Exception:
        pass
    return None


def _find_brave_mac() -> Optional[str]:
    default_dir = r'/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    if os.path.exists(default_dir):
        return default_dir
    return None


def _find_chrome_linux() -> Optional[str]:
    chrome_names = [
        'chromium-browser',
        'chromium',
        'google-chrome',
        'google-chrome-stable',
        'brave-browser',
    ]

    for name in chrome_names:
        chrome = which(name)
        if chrome is not None:
            return chrome
    return None


def _find_chrome_win() -> Optional[str]:
    try:
        import winreg as reg
    except ImportError:
        return None

    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
    chrome_path: Optional[str] = None

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
            chrome_path = query_value(reg_key, None)
            reg_key.Close()
            if chrome_path and os.path.isfile(chrome_path):
                return chrome_path
        except OSError:
            chrome_path = None

    # Fallback paths on Windows
    for env_var in ['LOCALAPPDATA', 'PROGRAMFILES', 'PROGRAMFILES(X86)']:
        base = os.environ.get(env_var)
        if base:
            candidate = os.path.join(base, r'Google\Chrome\Application\chrome.exe')
            if os.path.isfile(candidate):
                return candidate

    return None
