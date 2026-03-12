import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import gui_validator as v
from pathlib import Path

righe = Path('ocr_support_compatibility_pach/gui/window_army.gui').read_text(encoding='utf-8').splitlines(keepends=True)
bv = v._trova_blocchi_modalita(righe, 'vanilla')
bo = v._trova_blocchi_modalita(righe, 'ocr')
print(f'Blocchi vanilla trovati ({len(bv)}):')
for b in bv:
    print(f'  righe {b[0]}-{b[1]}')
print(f'Riga 5292 in vanilla? {v._linea_in_range(5292, bv)}')
print(f'Riga 5524 in vanilla? {v._linea_in_range(5524, bv)}')
print(f'Riga 5292 in ocr?     {v._linea_in_range(5292, bo)}')
print(f'Riga 5524 in ocr?     {v._linea_in_range(5524, bo)}')
