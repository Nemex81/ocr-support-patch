#!/usr/bin/env python3
"""Test encoding of files."""
import sys

files = [
    '.github/resources/jomini_scope_whitelist.md',
    'ocr_support_compatibility_pach/gui/window_army.gui',
]
for path in files:
    try:
        with open(path, encoding='utf-8') as f:
            content = f.read()
        print(f'OK: {path} len={len(content)}')
    except Exception as e:
        print(f'ERROR: {path} => {e}')
