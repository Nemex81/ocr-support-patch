import os
gui = r'c:\Users\nemex\OneDrive\Documenti\GitHub\ocr-support-patch\ocr_support_compatibility_pach\gui'
for name in ['window_culture.gui','window_military.gui','window_faith.gui','window_inventory.gui']:
    path = os.path.join(gui, name)
    with open(path,'rb') as f: head = f.read(3)
    bom = head == b'\xef\xbb\xbf'
    size = os.path.getsize(path)
    print(f'{name}: BOM={bom}, Size={size}')
