#!/usr/bin/env python3
"""Classifica i CRITICO dal file val_out.txt."""
import re, sys

try:
    with open('val_out.txt', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
except FileNotFoundError:
    print("val_out.txt non trovato", file=sys.stderr)
    sys.exit(1)

critico = [l.strip() for l in lines if 'CRITICO' in l]
print(f'Totale CRITICO: {len(critico)}')
types = {}
rows = []
for l in critico:
    m = re.search(r'\|\s*(\d+)\s*\|', l)
    lnum = m.group(1) if m else '?'
    m2 = re.search(r'icon senza tooltip|button senza tooltip|button_icon senza|invertit|nessuna struttura', l)
    t = m2.group(0) if m2 else 'other'
    types[t] = types.get(t, 0) + 1
    rows.append(f'riga {lnum}: {t}')

for k, v in sorted(types.items(), key=lambda x: -x[1]):
    print(f'  {v}x  {k}')
print()
for r in rows:
    print(r)
