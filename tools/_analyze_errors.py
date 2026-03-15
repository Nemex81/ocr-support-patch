#!/usr/bin/env python3

"""Analisi error.log del crash — classifica errori per sorgente."""
import re
import sys
from collections import Counter, defaultdict

log_path = sys.argv[1] if len(sys.argv) > 1 else r"c:\Users\nemex\OneDrive\Documenti\Paradox Interactive\Crusader Kings III\crashes\ck3_20260315_130032\logs\error.log"

lines = open(log_path, encoding='utf-8-sig', errors='replace').readlines()
print(f"Righe totali: {len(lines)}")

# Pattern per estrarre il file sorgente dall'errore
re_file = re.compile(r'file:\s*(gui/\S+\.gui)', re.IGNORECASE)
re_file2 = re.compile(r'in\s+(gui/\S+\.gui)', re.IGNORECASE)
re_file3 = re.compile(r"'([^']+\.gui)'")

# I nostri file nella patch
our_files = {
    'hud.gui', 'interaction_blackmail.gui', 'interaction_interfere_in_war_notification.gui',
    'interaction_menu_window.gui', 'window_activity.gui', 'window_activity_list.gui',
    'window_army.gui', 'window_character.gui', 'window_character_lifestyle.gui',
    'window_combat.gui', 'window_council.gui', 'window_county_view.gui',
    'window_court.gui', 'window_culture.gui', 'window_decisions.gui',
    'window_dynasty_house.gui', 'window_factions.gui', 'window_faith.gui',
    'window_intrigue.gui', 'window_inventory.gui', 'window_military.gui',
    'window_my_realm.gui'
}

# Classificazione
errors_by_file = Counter()
errors_by_source = Counter()  # 'our_patch' | 'ocr_upstream' | 'vanilla' | 'other' | 'unknown'
error_types = Counter()
our_patch_details = defaultdict(list)  # file -> [error messages]
sample_errors = defaultdict(list)  # file -> first 3 errors

# Pattern per _patch_vanilla
re_patch_vanilla = re.compile(r'_patch_vanilla', re.IGNORECASE)

for line in lines:
    line = line.strip()
    if not line:
        continue

    # Trova il file referenziato
    m = re_file.search(line) or re_file2.search(line) or re_file3.search(line)
    if m:
        filepath = m.group(1) if re_file.search(line) or re_file2.search(line) else m.group(1)
        filename = filepath.split('/')[-1] if '/' in filepath else filepath
        errors_by_file[filename] += 1

        # Classifica
        if re_patch_vanilla.search(line):
            errors_by_source['_patch_vanilla (orfani)'] += 1
        elif filename in our_files:
            errors_by_source['nostra_patch'] += 1
            if len(sample_errors[filename]) < 3:
                sample_errors[filename].append(line[:200])
        elif 'vanilla/' in filepath:
            errors_by_source['ocr_vanilla_dir'] += 1
        elif any(x in filepath for x in ['OCR', 'ocr', 'preload']):
            errors_by_source['ocr_upstream'] += 1
        else:
            errors_by_source['altro'] += 1
    else:
        errors_by_source['no_file_ref'] += 1

    # Tipo di errore
    if 'not a valid' in line.lower():
        error_types['not_a_valid_widget/type'] += 1
    elif 'scrollwidget' in line.lower():
        error_types['scrollwidget'] += 1
    elif 'could not find' in line.lower():
        error_types['could_not_find'] += 1
    elif 'not handled' in line.lower():
        error_types['not_handled'] += 1
    elif 'datatype' in line.lower() or 'data type' in line.lower():
        error_types['datatype'] += 1
    elif 'promote' in line.lower():
        error_types['promote'] += 1
    elif 'missing' in line.lower():
        error_types['missing'] += 1

print(f"\n=== ERRORI PER SORGENTE ===")
for source, count in sorted(errors_by_source.items(), key=lambda x: -x[1]):
    print(f"  {source}: {count}")

print(f"\n=== TIPI DI ERRORE (classificati) ===")
for etype, count in sorted(error_types.items(), key=lambda x: -x[1]):
    print(f"  {etype}: {count}")

print(f"\n=== TOP 25 FILE CON PIU' ERRORI ===")
for filename, count in errors_by_file.most_common(25):
    tag = " [NOSTRA]" if filename in our_files else ""
    tag = " [ORFANO]" if '_patch_vanilla' in filename else tag
    print(f"  {filename}: {count}{tag}")

print(f"\n=== ERRORI NOSTRA PATCH — DETTAGLIO PER FILE ===")
our_total = 0
for filename in sorted(our_files):
    c = errors_by_file.get(filename, 0)
    if c > 0:
        our_total += c
        print(f"  {filename}: {c}")
print(f"  --- TOTALE NOSTRA PATCH: {our_total}")

print(f"\n=== CAMPIONI ERRORI NOSTRA PATCH (primi 3 per file) ===")
for filename in sorted(sample_errors.keys()):
    print(f"\n  --- {filename} ---")
    for s in sample_errors[filename]:
        print(f"    {s}")
