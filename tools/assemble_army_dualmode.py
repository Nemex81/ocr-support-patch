#!/usr/bin/env python3
"""
assemble_army_dualmode.py
Assembla window_army.gui con supporto dual-mode (OCR + vanilla).

Struttura output:
  - army_window: OCR vbox (da OCR upstream) + vanilla container (da vanilla CK3)
  - army_reorganization_window: OCR block + vanilla container
  - attach_to_army_window: OCR block + vanilla container

Uso:
    python tools/assemble_army_dualmode.py [--dry-run]
"""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import OCR_GUI, VANILLA_GUI, PATCH_GUI

OCR_FILE     = OCR_GUI / "window_army.gui"
VANILLA_FILE = VANILLA_GUI / "window_army.gui"
PATCH_FILE   = PATCH_GUI / "window_army.gui"

DRY_RUN = "--dry-run" in sys.argv


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def read_file(path: Path) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return f.readlines()


def find_window_end(lines: list[str], start: int) -> int:
    """
    Trova la riga di chiusura (}) del window block che inizia a 'start'.
    Ignora le righe che sono commenti puri (iniziano con # dopo whitespace opzionale)
    per evitare che codice commentato con { o } scompensi il conteggio.
    """
    depth = 0
    for i in range(start, len(lines)):
        stripped = lines[i].lstrip()
        if stripped.startswith("#"):
            continue  # riga commento: ignora braces
        depth += lines[i].count("{") - lines[i].count("}")
        if depth == 0:
            return i
    raise ValueError(f"Block starting at line {start+1} non chiuso correttamente")


def find_top_level_windows(lines: list[str]) -> list[tuple[int, int, str]]:
    """
    Restituisce lista di (start, end, name) per ogni window = { ... } top-level.
    """
    results = []
    i = 0
    while i < len(lines):
        stripped = lines[i].rstrip()
        if stripped == "window = {" or stripped.startswith("window = {"):
            end = find_window_end(lines, i)
            # Cerca il name nelle prime 5 righe del blocco
            name = "unknown"
            for j in range(i, min(i + 6, end)):
                if "name" in lines[j]:
                    parts = lines[j].split('"')
                    if len(parts) >= 2:
                        name = parts[1]
                        break
            results.append((i, end, name))
            i = end + 1
        else:
            i += 1
    return results


def find_block_end(lines: list[str], start: int) -> int:
    """
    Come find_window_end ma gestisce blocchi dove { e' sulla riga SUCCESSIVA
    rispetto alla riga iniziale (es. 'types ArmyWindow\n{').
    Attende di entrare nel blocco (depth > 0) prima di restituire depth == 0.
    """
    depth = 0
    entered = False
    for i in range(start, len(lines)):
        stripped = lines[i].lstrip()
        if stripped.startswith("#"):
            continue
        depth += lines[i].count("{") - lines[i].count("}")
        if depth > 0:
            entered = True
        if entered and depth == 0:
            return i
    raise ValueError(f"Block starting at line {start+1} non chiuso correttamente")


def find_type_block(lines: list[str], type_name: str, start_from: int = 0) -> tuple[int, int]:
    """
    Trova inizio e fine (inclusa) di 'type <type_name> = ...' nel file.
    Restituisce (-1, -1) se non trovato.
    """
    pattern = re.compile(r'^\s*type\s+' + re.escape(type_name) + r'\s*=')
    for i in range(start_from, len(lines)):
        if pattern.match(lines[i]):
            end = find_block_end(lines, i)
            return i, end
    return -1, -1


def find_template_block(lines: list[str], template_name: str, start_from: int = 0) -> tuple[int, int]:
    """
    Trova inizio e fine (inclusa) di 'template <template_name> { ... }' nel file.
    Usa match esatto del nome (non come prefisso) per evitare falsi positivi.
    Restituisce (-1, -1) se non trovato.
    """
    pattern = re.compile(r'^\s*template\s+' + re.escape(template_name) + r'\s*(\{\s*)?$')
    for i in range(start_from, len(lines)):
        if pattern.match(lines[i].rstrip()):
            end = find_block_end(lines, i)
            return i, end
    return -1, -1


def extract_inner_vbox_from_ocr_army_window(lines: list[str], start: int, end: int) -> tuple[int, int, int, int]:
    """
    Nell'army_window OCR, trova:
    - il blocco 'widget { size = {400 100%} }' (outer_start, outer_end)
    - l'inner 'widget { size = {800 100%} }' all'interno (inner_start, inner_end)
    Il vbox OCR e' il primo figlio dell'inner widget.
    Restituisce (outer_start, outer_end, inner_start, inner_end).
    """
    # Cerca il widget con size {400 100%}
    outer_start = outer_end = inner_start = inner_end = -1
    for i in range(start, end):
        line = lines[i].rstrip()
        if "size = { 400 100% }" in line or "size = {400 100%}" in line:
            # backtrack fino a widget = {
            for j in range(i, max(i-5, start-1), -1):
                if "widget" in lines[j] and "{" in lines[j]:
                    outer_start = j
                    outer_end = find_window_end(lines, j)
                    break
            if outer_start >= 0:
                break
        # Oppure: la riga e' solo widget = { subito seguita da size = {400...}
        if line.strip() == "widget = {" or line.strip() == "widget={":
            # controlla la prossima riga significativa
            for k in range(i+1, min(i+4, end)):
                if "400 100%" in lines[k] or "size = { 400" in lines[k]:
                    outer_start = i
                    outer_end = find_window_end(lines, i)
                    break
            if outer_start >= 0:
                break

    if outer_start < 0:
        raise ValueError("Outer widget {400 100%} non trovato nell'army_window OCR")

    # Dentro outer_start..outer_end, cerca widget con size {800 100%}
    for i in range(outer_start, outer_end):
        if "800 100%" in lines[i] or "size = { 800" in lines[i]:
            for j in range(i, max(i-5, outer_start-1), -1):
                if lines[j].strip() in ("widget = {", "widget={"):
                    inner_start = j
                    inner_end = find_window_end(lines, j)
                    break
            if inner_start >= 0:
                break
        if lines[i].strip() in ("widget = {", "widget={"):
            for k in range(i+1, min(i+4, outer_end)):
                if "800 100%" in lines[k] or "size = { 800" in lines[k]:
                    inner_start = i
                    inner_end = find_window_end(lines, i)
                    break
            if inner_start >= 0:
                break

    if inner_start < 0:
        raise ValueError("Inner widget {800 100%} non trovato nell'army_window OCR")

    return outer_start, outer_end, inner_start, inner_end


# ---------------------------------------------------------------------------
# Costruzione sezioni
# ---------------------------------------------------------------------------

TOGGLE_OCR_OFF = "[Not(GetVariableSystem.Exists('ocr'))]"
TOGGLE_OCR_ON  = "[GetVariableSystem.Exists('ocr')]"

VANILLA_CONTAINER_HEADER = """\
\twidget = {
\t\tname = "vanilla_army_container"
\t\tvisible = "[GetVariableSystem.Exists('ocr')]"
\t\tsize = { 785 350 }
\t\tparentanchor = bottom|left
\t\tallow_outside = yes

\t\t# ==============================================================
\t\t# CONTAINER VANILLA — copia fedele del CK3 originale 1.17.1
\t\t# variabile ocr PRESENTE = modalita' normo-vedente
\t\t# NON MODIFICARE MAI — identico al vanilla
\t\t# ==============================================================
"""

VANILLA_REORG_HEADER = """\
\twidget = {
\t\tname = "vanilla_reorg_container"
\t\tvisible = "[GetVariableSystem.Exists('ocr')]"

\t\t# ==============================================================
\t\t# CONTAINER VANILLA riorganizzazione — copia fedele CK3 1.17.1
\t\t# ==============================================================
"""

VANILLA_ATTACH_HEADER = """\
\twidget = {
\t\tname = "vanilla_attach_container"
\t\tvisible = "[GetVariableSystem.Exists('ocr')]"

\t\t# ==============================================================
\t\t# CONTAINER VANILLA aggancio — copia fedele CK3 1.17.1
\t\t# ==============================================================
"""

OCR_WRAPPER_OPEN = """\
\twidget = {
\t\tname = "ocr_{}_container"
\t\tvisible = "[Not(GetVariableSystem.Exists('ocr'))]"
\t\tsize = {{ 100% 100% }}

"""

OCR_WRAPPER_CLOSE = "\t}\n"
VANILLA_WRAPPER_CLOSE = "\t}\n"


def indent_lines(lines: list[str], extra_tabs: int = 1) -> list[str]:
    """Aggiunge 'extra_tabs' tabulazioni a ogni riga non vuota."""
    tab = "\t" * extra_tabs
    return [tab + line if line.strip() else line for line in lines]


def build_army_window(ocr_lines, vanilla_lines, ocr_win, vanilla_win) -> list[str]:
    """
    Costruisce il blocco army_window dual-mode.
    Strategia:
    - Mantieni tutto il contenuto OCR fino alla fine dell'inner widget {800 100%}
    - Inietta vanilla_army_container PRIMA della chiusura dell'inner widget
    """
    os_idx, oe_idx, ve_idx = ocr_win[0], ocr_win[1], vanilla_win[1]
    ov_idx = ocr_win[0]

    # Window header OCR fino a (escludendo) l'ultima riga di chiusura della finestra
    # La struttura e': window {...  widget{400} { widget{800} { vbox_ocr } } }
    # Vogliamo: window {...  widget{400} { widget{800} { vbox_ocr  vanilla_container } } }

    outer_s, outer_e, inner_s, inner_e = extract_inner_vbox_from_ocr_army_window(
        ocr_lines, os_idx, oe_idx
    )

    # Linee del window OCR: dal inizio al (incluso) inner_e - 1
    # poi inseriamo vanilla container
    # poi richiudiamo inner, outer e window

    # Quante '}' ci sono dopo inner_e fino a oe_idx?
    # = 1 per inner, 1 per outer, 1 per window
    closing_after_inner = ocr_lines[inner_e + 1 : oe_idx + 1]

    # Tutti il contenuto OCR dal window start fino alla riga PRIMA della } di chiusura del inner_widget
    ocr_up_to_inner_close = ocr_lines[os_idx : inner_e]  # esclude la } di chiusura inner

    # Vanilla inner content: tutto tranne prima e ultima riga (window = { ... })
    vanilla_inner = vanilla_lines[vanilla_win[0] + 1 : ve_idx]

    # Costruisci le righe del container vanilla armato
    vanilla_container = (
        [VANILLA_CONTAINER_HEADER]
        + indent_lines(vanilla_inner, extra_tabs=2)
        + ["\t}\n"]  # chiude vanilla_army_container
    )

    result = list(ocr_up_to_inner_close)
    # chiudi il vbox OCR con i suoi livelli: l'inner_e e' la } dell'inner widget
    # ma abbiamo escluso quella riga (inner_e), quindi aggiungiamo il vanilla container
    # prima della } dell'inner widget
    result += vanilla_container
    # ora riaggiungiamo la } dell'inner widget e le successive
    result += ocr_lines[inner_e : oe_idx + 1]  # include } inner, } outer
    result += ["\n"]  # blank line between windows

    return result


def build_sub_window_dual(ocr_lines, vanilla_lines, ocr_win, vanilla_win,
                          window_name: str, vanilla_header: str) -> list[str]:
    """
    Costruisce una sub-window dual-mode (reorg o attach).
    Struttura output:
    window = {
        name = "..."
        [attributi window-level OCR]
        [states da OCR]
        using = Window_Background_No_Edge (se presente in OCR)
        widget { name="ocr_X_container" visible=Not(ocr) size={100% 100%}
            [vbox content da OCR, senza il wrapper window]
        }
        widget { name="vanilla_X_container" visible=(ocr)
            [size/parentanchor vanilla + contenuto vanilla]
        }
    }
    """
    os_idx, oe_idx = ocr_win
    vs_idx, ve_idx = vanilla_win

    # OCR: tutto tranne prima riga (window = {) e ultima (})
    ocr_inner = ocr_lines[os_idx + 1 : oe_idx]

    # Vanilla: tutto tranne prima riga e ultima
    vanilla_inner = vanilla_lines[vs_idx + 1 : ve_idx]

    # Identifica fino a dove vanno gli attributi window-level OCR (prima del vbox/using/state)
    # Per semplicita': prendiamo tutto come OCR inner e lo avvolgiamo nel container OCR

    result = [f"window = {{\n"]
    result += [f"\tname = \"{window_name}\"\n"]

    # Attributi window-level (tutto tranne i vbox/widget principali del contenuto OCR)
    # Heuristica: prendi le righe PRIMA della prima vbox = { o widget = { che non sia state/using/etc
    # Per sicurezza: distingui "header" (state, using, layer, size, attachto, etc.)
    #              da "body" (il primo vbox = { o widget = { che e' il contenuto principale)
    header_lines = []
    body_start = len(ocr_inner)
    for i, line in enumerate(ocr_inner):
        stripped = line.strip()
        # Il "body" inizia al primo vbox/widget di contenuto (non state, attachto, using, layer, etc.)
        if (stripped.startswith("vbox = {") or stripped.startswith("vbox={")
                and not any(kw in line for kw in ("state", "attachto", "using", "layer"))):
            body_start = i
            break
        # hbox come diretto figlio del window = body
        if stripped.startswith("hbox = {") and i > 5:
            body_start = i
            break

    header_lines = ocr_inner[:body_start]
    body_lines   = ocr_inner[body_start:]

    # Window-level header (size, layer, state, attachto, using)
    result += header_lines

    # OCR container
    ocr_container_name = f"ocr_{window_name.replace('army_', '').replace('_window', '')}_container"
    result += ["\n"]
    result += [f"\t# ============================================================\n"]
    result += [f"\t# BLOCCO OCR — testo, screen reader ready\n"]
    result += [f"\t# variabile ocr ASSENTE = modalita' non vedente\n"]
    result += [f"\t# ============================================================\n"]
    result += [f"\twidget = {{\n"]
    result += [f"\t\tname = \"{ocr_container_name}\"\n"]
    result += [f"\t\tvisible = \"[Not(GetVariableSystem.Exists('ocr'))]\"\n"]
    result += [f"\t\tsize = {{ 100% 100% }}\n\n"]
    result += indent_lines(body_lines, extra_tabs=2)
    result += ["\t}\n"]

    # Vanilla container
    result += ["\n"]
    result += [f"\t# ============================================================\n"]
    result += [f"\t# BLOCCO VANILLA — copia fedele CK3 originale\n"]
    result += [f"\t# variabile ocr PRESENTE = modalita' normo-vedente\n"]
    result += [f"\t# ============================================================\n"]

    vanilla_container_name = f"vanilla_{window_name.replace('army_', '').replace('_window', '')}_container"
    result += [f"\twidget = {{\n"]
    result += [f"\t\tname = \"{vanilla_container_name}\"\n"]
    result += [f"\t\tvisible = \"[GetVariableSystem.Exists('ocr')]\"\n\n"]
    result += indent_lines(vanilla_inner, extra_tabs=2)
    result += ["\t}\n"]

    result += ["}\n"]
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== Assemblaggio window_army.gui — Dual Mode ===\n")

    print(f"Lettura OCR upstream:  {OCR_FILE}")
    ocr_lines = read_file(OCR_FILE)
    print(f"  {len(ocr_lines)} righe lette")

    print(f"Lettura vanilla CK3:   {VANILLA_FILE}")
    vanilla_lines = read_file(VANILLA_FILE)
    print(f"  {len(vanilla_lines)} righe lette")

    print("\nRilevamento window blocks...")
    ocr_windows = find_top_level_windows(ocr_lines)
    vanilla_windows = find_top_level_windows(vanilla_lines)

    print(f"\nOCR upstream windows ({len(ocr_windows)}):")
    for s, e, n in ocr_windows:
        print(f"  '{n}'  righe {s+1}–{e+1}")

    print(f"\nVanilla CK3 windows ({len(vanilla_windows)}):")
    for s, e, n in vanilla_windows:
        print(f"  '{n}'  righe {s+1}–{e+1}")

    # Verifica che ci siano almeno 3 windows in entrambi
    if len(ocr_windows) < 3 or len(vanilla_windows) < 3:
        print("\n[ERRORE] Numero di window blocks insufficiente nei file sorgente.")
        sys.exit(1)

    # Verifica nomi corrispondenti
    expected = ["army_window", "army_reorganization_window", "attach_to_army_window"]
    for i, name in enumerate(expected):
        ocr_name = ocr_windows[i][2]
        van_name = vanilla_windows[i][2]
        if name not in ocr_name or name not in van_name:
            print(f"\n[AVVERTENZA] Window {i}: OCR='{ocr_name}', vanilla='{van_name}' (atteso: '{name}')")

    print("\nAssemblaggio sezioni...")

    output = []

    # Header commento patch
    output.append("# window_army.gui — OCR Support Patch\n")
    output.append("# Dual Mode: OCR (screen reader) + Vanilla CK3 1.17.1\n")
    output.append("# Generato da: tools/assemble_army_dualmode.py\n")
    output.append("# NON modificare il container vanilla — identico al file originale Paradox.\n")
    output.append("\n")

    # --- 1. army_window ---
    print("\n[1/3] army_window...")
    try:
        army_section = build_army_window(
            ocr_lines, vanilla_lines,
            (ocr_windows[0][0], ocr_windows[0][1]),
            (vanilla_windows[0][0], vanilla_windows[0][1])
        )
        output += army_section
        print(f"  OK — {len(army_section)} righe")
    except Exception as e:
        print(f"  [ERRORE] {e}")
        import traceback; traceback.print_exc()
        sys.exit(1)

    # --- 2. army_reorganization_window ---
    print("\n[2/3] army_reorganization_window...")
    try:
        reorg_section = build_sub_window_dual(
            ocr_lines, vanilla_lines,
            (ocr_windows[1][0], ocr_windows[1][1]),
            (vanilla_windows[1][0], vanilla_windows[1][1]),
            "army_reorganization_window",
            VANILLA_REORG_HEADER
        )
        output += reorg_section
        output.append("\n")
        print(f"  OK — {len(reorg_section)} righe")
    except Exception as e:
        print(f"  [ERRORE] {e}")
        import traceback; traceback.print_exc()
        sys.exit(1)

    # --- 3. attach_to_army_window ---
    print("\n[3/3] attach_to_army_window...")
    # Trova le righe delle windows rimanenti (potrebbe includere template/types dopo)
    # Per vanilla: usa vanilla_windows[2] (potrebbe finire prima dei templates)
    # Per OCR: usa ocr_windows[2]
    try:
        attach_section = build_sub_window_dual(
            ocr_lines, vanilla_lines,
            (ocr_windows[2][0], ocr_windows[2][1]),
            (vanilla_windows[2][0], vanilla_windows[2][1]),
            "attach_to_army_window",
            VANILLA_ATTACH_HEADER
        )
        output += attach_section
        output.append("\n")
        print(f"  OK — {len(attach_section)} righe")
    except Exception as e:
        print(f"  [ERRORE] {e}")
        import traceback; traceback.print_exc()
        sys.exit(1)

    # --- Types/Templates: vanilla (base) + OCR FortTypes + OCR nuovi types + OCR templates ---
    print("\nAssemblaggio sezione types/template...")
    search_from = ocr_windows[-1][1] + 1  # riga dopo l'ultimo window OCR

    # 1. Vanilla types (usati sia dal container vanilla che dal container OCR)
    van_last_end = vanilla_windows[-1][1]
    if van_last_end + 1 < len(vanilla_lines):
        vanilla_types = vanilla_lines[van_last_end + 1:]
        non_empty = [l for l in vanilla_types if l.strip()]
        if non_empty:
            output.append("\n")
            output += vanilla_types
            print(f"  [1] Vanilla types: {len(vanilla_types)} righe")

    # 2. OCR FortTypes block (tra army_window e reorg_window nel file OCR)
    # Contiene: raid_target_item, hostile_fort_item, friendly_county_item
    ocr_main_end  = ocr_windows[0][1]
    ocr_reorg_start = ocr_windows[1][0]
    fort_types = ocr_lines[ocr_main_end + 1 : ocr_reorg_start]
    if any(l.strip() for l in fort_types):
        output += fort_types
        print(f"  [2] OCR FortTypes: {len(fort_types)} righe")

    # 3. Tipi OCR nuovi — NON presenti nel vanilla, necessari per la modalita' OCR
    # Vengono estratti singolarmente per evitare di includere i tipi vanilla duplicati
    # presenti nel blocco 'types ArmyWindow' del file OCR.
    NEW_OCR_TYPES = [
        "army_location",
        "button_holding_army",
        "button_province_army",
        "hbox_reorg_regiment_entry_core_ocr",
        "move_regiment",
        "forts_list",
        "resupply_item",
        "battle_button",
        "battles_categories",
        "button_army_adjacency",
        "button_raid_lists",
        "button_raid_county",
    ]
    ocr_new_type_lines: list[str] = []
    for type_name in NEW_OCR_TYPES:
        ts, te = find_type_block(ocr_lines, type_name, start_from=search_from)
        if ts < 0:
            print(f"  [AVVISO] Tipo OCR '{type_name}' non trovato dopo riga {search_from+1}")
            continue
        ocr_new_type_lines.extend(ocr_lines[ts : te + 1])
        ocr_new_type_lines.append("\n")
        print(f"    + {type_name}: righe {ts+1}-{te+1}")
    if ocr_new_type_lines:
        output.append("\ntypes OCRArmyNewTypes\n{\n")
        output += ocr_new_type_lines
        output.append("}\n\n")
        print(f"  [3] OCR new types: {len(ocr_new_type_lines)} righe totali")

    # 4. Template OCR send_army_click* — usati dal contenuto OCR nei widget button_*
    for tpl_name in ["send_army_click_province", "send_army_click", "send_army_click_county"]:
        ts, te = find_template_block(ocr_lines, tpl_name, start_from=search_from)
        if ts < 0:
            print(f"  [AVVISO] Template OCR '{tpl_name}' non trovato dopo riga {search_from+1}")
            continue
        output.extend(ocr_lines[ts : te + 1])
        output.append("\n")
        print(f"  [4] Template '{tpl_name}': righe {ts+1}-{te+1}")

    total_lines = len(output)
    print(f"\nTotale righe output: {total_lines}")

    if DRY_RUN:
        print("\n[DRY-RUN] File NON scritto.")
        # Stampa le prime 50 e ultime 20 righe come preview
        print("\n--- Prima 50 righe ---")
        print("".join(output[:50]))
        print("\n--- Ultime 20 righe ---")
        print("".join(output[-20:]))
        return

    print(f"\nScrittura: {PATCH_FILE}")
    PATCH_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PATCH_FILE, "w", encoding="utf-8") as f:
        f.writelines(output)
    print(f"  SCRITTO — {PATCH_FILE.stat().st_size // 1024} KB")
    print("\n=== Completato. Eseguire gui_validator.py per la verifica. ===")


if __name__ == "__main__":
    main()
