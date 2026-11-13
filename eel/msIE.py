from __future__ import annotations
import os
import platform
import subprocess as sps
import sys
from typing import List, Optional
from eel.types import OptionsDictT

name: str = 'MSIE'


def run(_path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    """Launch legacy Edge in IE compatibility mode on Windows."""
    if not start_urls:
        return
    url = start_urls[0]
    startfile = getattr(os, 'startfile', None)
    if callable(startfile):
        startfile(f'microsoft-edge:{url}')
    else:
        sps.Popen(['cmd', '/c', 'start', f'microsoft-edge:{url}'],
                  stdout=sys.stdout, stderr=sys.stderr, stdin=sps.PIPE)


def find_path() -> Optional[str]:
    if platform.system() == 'Windows':
        return 'microsoft-edge'
    return None
