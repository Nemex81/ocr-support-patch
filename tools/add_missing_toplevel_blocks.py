"""
add_missing_toplevel_blocks.py
Estrae blocchi top-level mancanti da OCR upstream e li aggiunge ai wrapper della patch.
Uso: python tools/add_missing_toplevel_blocks.py
"""
import os
import sys

def find_block_end(lines, start_idx):
    """Trova la riga di chiusura di un blocco Jomini partendo da start_idx."""
    depth = 0
    for i in range(start_idx, len(lines)):
        depth += lines[i].count('{') - lines[i].count('}')
        if depth <= 0 and i > start_idx:
            return i
    return len(lines) - 1

def extract_top_block(lines, start_idx):
    """Estrae il testo completo di un blocco top-level."""
    end_idx = find_block_end(lines, start_idx)
    return lines[start_idx:end_idx + 1], end_idx

def block_already_present(patch_text, names):
    """Verifica che nessuno dei nomi sia già presente nel file wrapper."""
    return any(n in patch_text for n in names)

def add_block_to_file(patch_path, block_lines, block_label):
    """Aggiunge un blocco alla fine del file wrapper."""
    with open(patch_path, encoding='utf-8') as f:
        content = f.read()
    # Rimuovi eventuale trailing newline multipla e aggiungi il blocco
    content = content.rstrip('\n') + '\n\n' + ''.join(block_lines) + '\n'
    with open(patch_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  AGGIUNTO: {block_label} -> {os.path.basename(patch_path)}')

def main():
    ocr_base = '../CK3-OCR/OCR-Support/gui/'
    patch_base = 'ocr_support_compatibility_pach/gui/'

    # (file_ocr, riga_1based_inizio, check_name, file_patch, label)
    tasks = [
        ('window_army.gui',       4533, 'army_reorganization_window',   'window_army.gui',         'army_reorganization_window'),
        ('window_army.gui',       5095, 'attach_to_army_window',        'window_army.gui',         'attach_to_army_window'),
        ('window_county_view.gui',3763, 'holding_tracks_view',          'window_county_view.gui',  'holding_tracks_view'),
        ('window_county_view.gui',4558, 'holding_type_selection_view',  'window_county_view.gui',  'holding_type_selection_view'),
        ('window_council.gui',    441,  'potential_task_location_window','window_council.gui',      'potential_task_location_window'),
        ('interaction_menu_window.gui', 2, 'window_ocr',                'interaction_menu_window.gui', 'window_ocr'),
    ]

    # Carica le linee dei file OCR (cache per evitare riletture)
    ocr_cache = {}

    for ocr_fname, start_1based, check_name, patch_fname, label in tasks:
        ocr_path = ocr_base + ocr_fname
        patch_path = patch_base + patch_fname

        if not os.path.exists(ocr_path):
            print(f'ERRORE: file OCR mancante {ocr_path}')
            continue

        # Verifica che il blocco non sia già presente nella patch
        with open(patch_path, encoding='utf-8') as f:
            patch_text = f.read()
        if check_name in patch_text:
            print(f'  SKIP (gia presente): {label} in {patch_fname}')
            continue

        # Carica OCR upstream
        if ocr_fname not in ocr_cache:
            with open(ocr_path, encoding='utf-8') as f:
                ocr_cache[ocr_fname] = f.readlines()
        ocr_lines = ocr_cache[ocr_fname]

        start_idx = start_1based - 1
        if start_idx >= len(ocr_lines):
            print(f'ERRORE: riga {start_1based} fuori range in {ocr_fname} ({len(ocr_lines)} righe)')
            continue

        # Cerca all'indietro la riga con '{' se necessario (per catturare 'window = {' prima del 'name')
        actual_start = start_idx
        if '{' not in ocr_lines[start_idx]:
            for k in range(start_idx - 1, max(0, start_idx - 5), -1):
                if '{' in ocr_lines[k]:
                    actual_start = k
                    break

        block_lines, end_idx = extract_top_block(ocr_lines, actual_start)
        print(f'  Estratto: {label} da {ocr_fname} L{actual_start+1}-L{end_idx+1} ({len(block_lines)} righe)')

        # Verifica bilanciamento del blocco estratto
        block_text = ''.join(block_lines)
        opens = block_text.count('{')
        closes = block_text.count('}')
        if opens != closes:
            print(f'  ATTENZIONE: bilanciamento non OK ({opens} vs {closes}) per {label}')

        add_block_to_file(patch_path, block_lines, label)

    # Verifica bilanciamento finale dei file modificati
    print('\n=== Verifica bilanciamento finale ===')
    modified = set(t[3] for t in tasks)
    for fname in modified:
        text = open(patch_base + fname, encoding='utf-8').read()
        bal = text.count('{') - text.count('}')
        status = 'OK' if bal == 0 else f'ERRORE ({bal})'
        print(f'  {fname}: {status}')

if __name__ == '__main__':
    main()
