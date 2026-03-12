from pathlib import Path
righe = Path('../CK3-OCR/OCR-Support/gui/window_army.gui').read_text(encoding='utf-8').splitlines()
for i, r in enumerate(righe):
    if 'army_reorganization_window' in r:
        print(f'Riga {i+1}: {r.strip()[:80]}')
        if i > 3300:
            break

# trova la fine di army_window OCR (primo window)
depth = 0
in_window = False
for i, r in enumerate(righe):
    if r.strip() == 'window = {':
        in_window = True
        depth = 1
        start = i+1
        continue
    if in_window:
        depth += r.count('{') - r.count('}')
        if depth <= 0:
            print(f'Fine primo window OCR: riga {i+1}')
            # mostra le 10 righe prima della fine
            for j in range(max(0, i-9), i+2):
                print(f'  {j+1}: {righe[j].strip()[:80]}')
            break
