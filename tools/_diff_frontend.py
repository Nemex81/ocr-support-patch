import sys

p = open(r'c:\Users\nemex\OneDrive\Documenti\GitHub\ocr-support-patch\ocr_support_compatibility_pach\gui\frontend_main.gui', encoding='utf-8').readlines()
o = open(r'c:\Users\nemex\OneDrive\Documenti\GitHub\CK3-OCR\OCR-Support\gui\frontend_main.gui', encoding='utf-8').readlines()

print(f'Patch={len(p)} righe, OCR={len(o)} righe')

diffs = []
for i, (a, b) in enumerate(zip(p, o)):
    if a != b:
        diffs.append((i+1, a.rstrip(), b.rstrip()))

if len(p) != len(o):
    print('ATTENZIONE: lunghezze diverse!')

print(f'Differenze trovate: {len(diffs)}')
for ln, a, b in diffs:
    print(f'--- Riga {ln} ---')
    print(f'  PATCH: {a!r}')
    print(f'  OCR:   {b!r}')

# Verifica bilanciamento parentesi graffe
text_p = ''.join(p)
open_p = text_p.count('{')
close_p = text_p.count('}')
print(f'\nBilanciamento graffe nella PATCH: {{ = {open_p}, }} = {close_p}, differenza = {open_p - close_p}')

# Controlla window blocks
import re
windows = re.findall(r'^\s*window\s*=\s*\{', text_p, re.MULTILINE)
print(f'Blocchi "window = {{" trovati nella patch: {len(windows)}')

# Verifica root widget
first_line = p[0].strip()
print(f'Widget radice: {first_line[:60]}')
