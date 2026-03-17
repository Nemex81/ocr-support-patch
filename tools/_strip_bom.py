"""Strip UTF-8 BOM from specified GUI files."""
import os, sys

GUI_DIR = r'c:\Users\nemex\OneDrive\Documenti\GitHub\ocr-support-patch\ocr_support_compatibility_pach\gui'

FILES = [
    'window_culture.gui',
    'window_military.gui',
    'window_faith.gui',
    'window_inventory.gui',
]

BOM = b'\xef\xbb\xbf'

for name in FILES:
    path = os.path.join(GUI_DIR, name)
    with open(path, 'rb') as f:
        data = f.read()
    if data[:3] == BOM:
        with open(path, 'wb') as f:
            f.write(data[3:])
        print(f'STRIPPED: {name} ({len(data)} -> {len(data)-3} bytes)')
    else:
        print(f'NO-BOM:  {name} ({len(data)} bytes)')

# Verify
print('\n--- VERIFICA ---')
for name in FILES:
    path = os.path.join(GUI_DIR, name)
    with open(path, 'rb') as f:
        head = f.read(3)
    has_bom = head == BOM
    size = os.path.getsize(path)
    status = 'ERRORE: BOM ancora presente!' if has_bom else 'OK: senza BOM'
    print(f'{name}: {status} ({size} bytes)')
