#!/usr/bin/env python3
"""
repair_missing_types.py — Ripara i wrapper della patch aggiungendo i blocchi
types e template mancanti dai file OCR upstream e vanilla.

Principio: quando la nostra patch sovrascrive un file OCR, TUTTI i blocchi
top-level (types, template) presenti nel file OCR devono essere inclusi,
altrimenti le definizioni di tipo vanno perse e il gioco crasha.

Uso:
    python tools/repair_missing_types.py --dry-run     # mostra cosa farebbe
    python tools/repair_missing_types.py               # applica le modifiche
"""

import sys
import re
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import OCR_GUI, VANILLA_GUI, PATCH_GUI


# ---------------------------------------------------------------------------
# Parsing — blocchi top-level
# ---------------------------------------------------------------------------

def find_block_end(lines, start):
    """Trova la fine di un blocco { } partendo dalla riga start."""
    depth = 0
    entered = False
    for i in range(start, len(lines)):
        if lines[i].lstrip().startswith("#"):
            continue
        depth += lines[i].count("{") - lines[i].count("}")
        if depth > 0:
            entered = True
        if entered and depth == 0:
            return i
    raise ValueError(f"Blocco alla riga {start + 1} non chiuso")


def extract_top_level_blocks(lines):
    """
    Estrae tutti i blocchi top-level non-window da un file .gui.
    Restituisce lista di dict: {kind, name, start, end, text}
    kind: 'types_block' | 'template' | 'type'
    """
    re_types_block = re.compile(r'^\s*types\s+(\w+)')
    re_template = re.compile(r'^\s*template\s+(\w+)')
    re_type = re.compile(r'^\s*type\s+(\w+)\s*=')
    re_window = re.compile(r'^\s*window\s*=\s*\{')
    re_local_template = re.compile(r'^\s*local_template\s+(\w+)')

    results = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        # Skip window blocks
        if re_window.match(line):
            end = find_block_end(lines, i)
            i = end + 1
            continue

        m = re_types_block.match(line)
        if m:
            end = find_block_end(lines, i)
            text = "".join(lines[i:end + 1])
            results.append({"kind": "types_block", "name": m.group(1),
                            "start": i, "end": end, "text": text})
            i = end + 1
            continue

        m = re_template.match(line)
        if m:
            end = find_block_end(lines, i)
            text = "".join(lines[i:end + 1])
            results.append({"kind": "template", "name": m.group(1),
                            "start": i, "end": end, "text": text})
            i = end + 1
            continue

        m = re_local_template.match(line)
        if m:
            end = find_block_end(lines, i)
            text = "".join(lines[i:end + 1])
            results.append({"kind": "local_template", "name": m.group(1),
                            "start": i, "end": end, "text": text})
            i = end + 1
            continue

        m = re_type.match(line)
        if m:
            end = find_block_end(lines, i)
            text = "".join(lines[i:end + 1])
            results.append({"kind": "type", "name": m.group(1),
                            "start": i, "end": end, "text": text})
            i = end + 1
            continue

        i += 1

    return results


def count_blocks_by_name(lines):
    """Restituisce dict di {(kind, name): count} per i blocchi già presenti."""
    blocks = extract_top_level_blocks(lines)
    counts = {}
    for b in blocks:
        key = (b["kind"], b["name"])
        counts[key] = counts.get(key, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Riparazione
# ---------------------------------------------------------------------------

def repair_file(patch_file, ocr_file, vanilla_file, dry_run=False):
    """
    Aggiunge i blocchi types/template mancanti al file della patch.
    Strategia:
    1. Includi tutti i blocchi dall'OCR upstream (il nostro override rimpiazza OCR)
       In Jomini, blocchi con lo stesso nome sono legali (vengono mergiati),
       quindi rispettiamo le occorrenze multiple.
    2. Includi blocchi vanilla con nome diverso da quelli OCR (servono al container vanilla)
    3. Non duplicare blocchi già presenti nella patch
    """
    patch_lines = open(patch_file, encoding="utf-8-sig").readlines()
    existing_counts = count_blocks_by_name(patch_lines)

    blocks_to_add = []
    ocr_block_counts = {}

    # 1. Blocchi da OCR upstream — rispetta occorrenze multiple
    if ocr_file.exists():
        ocr_lines = open(ocr_file, encoding="utf-8-sig").readlines()
        ocr_blocks = extract_top_level_blocks(ocr_lines)
        for b in ocr_blocks:
            key = (b["kind"], b["name"])
            ocr_block_counts[key] = ocr_block_counts.get(key, 0) + 1
            already_have = existing_counts.get(key, 0)
            needed = ocr_block_counts[key]
            # PROTEZIONE DUPLICATI: aggiunge solo se il numero di occorrenze
            # nel file patch e' inferiore a quelle previste da OCR upstream.
            # Se il blocco e' gia' presente con il conteggio corretto, si salta.
            if needed > already_have:
                blocks_to_add.append(b)
                existing_counts[key] = existing_counts.get(key, 0) + 1
            else:
                # Blocco gia' presente con il numero atteso di occorrenze — skip
                pass

    # 2. Blocchi vanilla che OCR non include (nome diverso)
    if vanilla_file.exists():
        van_lines = open(vanilla_file, encoding="utf-8-sig").readlines()
        van_blocks = extract_top_level_blocks(van_lines)
        for b in van_blocks:
            key = (b["kind"], b["name"])
            if key not in existing_counts and key not in ocr_block_counts:
                blocks_to_add.append(b)
                existing_counts[key] = 1

    if not blocks_to_add:
        return 0

    # Prepara il testo da inserire
    insert_text = ""
    for b in blocks_to_add:
        insert_text += b["text"]
        if not b["text"].endswith("\n"):
            insert_text += "\n"
        insert_text += "\n"

    # Trova dove inserire: prima del primo "window = {"
    insert_pos = 0
    for i, line in enumerate(patch_lines):
        if re.match(r'^\s*window\s*=\s*\{', line):
            insert_pos = i
            break

    # Se ci sono commenti di header prima della window, inserisci dopo quelli
    # ma prima della window
    new_content = "".join(patch_lines[:insert_pos]) + insert_text + "".join(patch_lines[insert_pos:])

    if dry_run:
        block_names = [f"  {b['kind']}:{b['name']}" for b in blocks_to_add]
        print(f"  [DRY-RUN] Aggiungerei {len(blocks_to_add)} blocchi:")
        for name in block_names:
            print(f"    {name}")
    else:
        with open(patch_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  SCRITTO — {len(blocks_to_add)} blocchi aggiunti")
        # Sanity check post-scrittura: verifica duplicati nel file appena scritto
        written_lines = open(patch_file, encoding="utf-8").readlines()
        written_counts = count_blocks_by_name(written_lines)
        duplicates = {k: v for k, v in written_counts.items() if v > 1}
        if duplicates:
            print(f"  ATTENZIONE: duplicati rilevati nella versione scritta: {duplicates}")

    return len(blocks_to_add)


def main():
    parser = argparse.ArgumentParser(description="Ripara blocchi types/template mancanti nei wrapper")
    parser.add_argument("--dry-run", action="store_true", help="Mostra cosa farebbe senza scrivere")
    parser.add_argument("--file", help="Ripara un solo file (nome senza path, es. window_army.gui)")
    args = parser.parse_args()

    patch_dir = PATCH_GUI
    if not patch_dir.exists():
        print(f"[ERRORE] Directory patch non trovata: {patch_dir}")
        sys.exit(1)

    files = sorted(patch_dir.glob("*.gui"))
    if args.file:
        files = [f for f in files if f.name == args.file]
        if not files:
            print(f"[ERRORE] File non trovato: {args.file}")
            sys.exit(1)

    total_added = 0
    total_files_fixed = 0

    for patch_file in files:
        ocr_file = OCR_GUI / patch_file.name
        vanilla_file = VANILLA_GUI / patch_file.name

        if not ocr_file.exists() and not vanilla_file.exists():
            continue

        print(f"\n--- {patch_file.name} ---")
        count = repair_file(patch_file, ocr_file, vanilla_file, args.dry_run)
        if count > 0:
            total_added += count
            total_files_fixed += 1

    print(f"\n{'=' * 60}")
    print(f"Totale: {total_added} blocchi aggiunti a {total_files_fixed} file")
    if args.dry_run:
        print("[DRY-RUN] Nessun file modificato. Riesegui senza --dry-run per applicare.")


if __name__ == "__main__":
    main()
