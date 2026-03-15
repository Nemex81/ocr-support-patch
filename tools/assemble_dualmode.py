#!/usr/bin/env python3
"""
assemble_dualmode.py — Assembla un file .gui dual-mode (OCR + vanilla) per qualsiasi
finestra CK3.

Principio fondamentale: il sistema non inventa nulla.
- Container OCR:     estratto dal file OCR upstream (Agamidae)
- Container vanilla: copia fedele del file CK3 originale

Uso:
    python tools/assemble_dualmode.py --window <nome_finestra> --mode simple|tabs|complex [--dry-run] [--separate-vanilla]

Modalità:
    simple  — Pattern A: una sola window, struttura semplice
    tabs    — Pattern B: window principale + sub-windows
    complex — Pattern C/D: window + types + templates separati

Opzioni:
    --dry-run           Stampa l'output su stdout senza scrivere il file nella patch
    --separate-vanilla  Pattern v1.1: vanilla in type separato in gui/vanilla/
                        Produce DUE file: wrapper + {nome}_patch_vanilla.gui
"""

import sys
import re
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import OCR_GUI, VANILLA_GUI, PATCH_GUI, VANILLA_TYPES_GUI

TOGGLE_OCR_OFF = "[Not(GetVariableSystem.Exists('ocr'))]"
TOGGLE_OCR_ON  = "[GetVariableSystem.Exists('ocr')]"


# ---------------------------------------------------------------------------
# Utility — lettura e ricerca blocchi
# ---------------------------------------------------------------------------

def read_file(path: Path) -> list[str]:
    # utf-8-sig rimuove automaticamente eventuale BOM iniziale (fbbbf)
    # presente in alcuni file vanilla/OCR e che romperebbe il parsing di "window = {".
    with open(path, encoding="utf-8-sig") as f:
        return f.readlines()


def find_window_end(lines: list[str], start: int) -> int:
    """
    Trova la riga di chiusura (}) del blocco che inizia a 'start'.
    Ignora le righe commento puro per evitare scompensi nelle graffe.
    """
    depth = 0
    for i in range(start, len(lines)):
        if lines[i].lstrip().startswith("#"):
            continue
        depth += lines[i].count("{") - lines[i].count("}")
        if depth == 0:
            return i
    raise ValueError(f"Blocco alla riga {start + 1} non chiuso correttamente")


def find_block_end(lines: list[str], start: int) -> int:
    """
    Come find_window_end ma gestisce blocchi con { sulla riga SUCCESSIVA
    rispetto alla riga iniziale (es. 'types ArmyWindow\\n{').
    Attende di entrare nel blocco (depth > 0) prima di restituire depth == 0.
    """
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
    raise ValueError(f"Blocco alla riga {start + 1} non chiuso correttamente")


def find_top_level_windows(lines: list[str]) -> list[tuple[int, int, str]]:
    """Restituisce lista di (start, end, name) per ogni window top-level nel file."""
    results = []
    i = 0
    while i < len(lines):
        stripped = lines[i].rstrip()
        if stripped == "window = {" or stripped.startswith("window = {"):
            end = find_window_end(lines, i)
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


def find_type_block(lines: list[str], type_name: str, start_from: int = 0) -> tuple[int, int]:
    """Trova 'type <type_name> = ...' nel file. Restituisce (-1, -1) se assente."""
    pattern = re.compile(r'^\s*type\s+' + re.escape(type_name) + r'\s*=')
    for i in range(start_from, len(lines)):
        if pattern.match(lines[i]):
            return i, find_block_end(lines, i)
    return -1, -1


def find_template_block(lines: list[str], template_name: str, start_from: int = 0) -> tuple[int, int]:
    """
    Trova 'template <template_name> { ... }' nel file.
    Usa match esatto del nome per evitare falsi positivi.
    Restituisce (-1, -1) se assente.
    """
    pattern = re.compile(r'^\s*template\s+' + re.escape(template_name) + r'\s*(\{\s*)?$')
    for i in range(start_from, len(lines)):
        if pattern.match(lines[i].rstrip()):
            return i, find_block_end(lines, i)
    return -1, -1


def extract_window_content(lines: list[str]) -> list[dict]:
    """
    Estrae tutti i blocchi top-level da un file .gui.
    Restituisce lista di dict: {type, name, start, end}
    type: 'window' | 'type' | 'template' | 'types_block' | 'other'
    """
    re_window      = re.compile(r'^\s*window\s*=\s*\{')
    re_type        = re.compile(r'^\s*type\s+(\w+)\s*=')
    re_template    = re.compile(r'^\s*template\s+(\w+)')
    re_types_block = re.compile(r'^\s*types\s+(\w+)')

    results = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        if re_window.match(line):
            end = find_window_end(lines, i)
            name = "unknown"
            for j in range(i, min(i + 6, end + 1)):
                if "name" in lines[j]:
                    parts = lines[j].split('"')
                    if len(parts) >= 2:
                        name = parts[1]
                        break
            results.append({"type": "window", "name": name, "start": i, "end": end})
            i = end + 1
            continue

        m_type = re_type.match(line)
        if m_type:
            end = find_block_end(lines, i)
            results.append({"type": "type", "name": m_type.group(1), "start": i, "end": end})
            i = end + 1
            continue

        m_tmpl = re_template.match(line)
        if m_tmpl:
            end = find_block_end(lines, i)
            results.append({"type": "template", "name": m_tmpl.group(1), "start": i, "end": end})
            i = end + 1
            continue

        m_types_block = re_types_block.match(line)
        if m_types_block:
            end = find_block_end(lines, i)
            results.append({"type": "types_block", "name": m_types_block.group(1), "start": i, "end": end})
            i = end + 1
            continue

        # Catch-all: qualsiasi blocco top-level non riconosciuto che contenga '{'
        # (es. widget = {}, window_ocr = {}, blocchi anonimi, ecc.)
        if "{" in stripped:
            end = find_block_end(lines, i)
            # Deriva un nome identificativo dalla riga header o dalle prime righe
            name = f"anon_{i}"
            if "=" in stripped:
                # Prova a estrarre il nome dal lato sinistro di '='
                lhs = stripped.split("=")[0].strip().rstrip()
                if lhs:
                    name = lhs
            # Cerca anche 'name = "..."' nelle prime righe del blocco
            for j in range(i, min(i + 5, end + 1)):
                m_name = re.search(r'name\s*=\s*"([^"]+)"', lines[j])
                if m_name:
                    name = m_name.group(1)
                    break
            results.append({"type": "other", "name": name, "start": i, "end": end})
            i = end + 1
            continue

        i += 1

    return results


def indent_lines(lines: list[str], extra_tabs: int = 1) -> list[str]:
    """Aggiunge 'extra_tabs' tabulazioni a ogni riga non vuota."""
    tab = "\t" * extra_tabs
    return [tab + line if line.strip() else line for line in lines]


# ---------------------------------------------------------------------------
# Derivazione prefisso nomi container
# ---------------------------------------------------------------------------

def _derive_prefix(window_name: str) -> str:
    """
    Deriva il prefisso del container dal nome della window.
    Rimuove il prefisso 'window_' iniziale se presente.
    Esempi:
        'window_faith'  → 'faith'
        'window_army'   → 'army'
        'army_window'   → 'army'
    """
    if window_name.startswith("window_"):
        return window_name[len("window_"):]
    if window_name.endswith("_window"):
        return window_name[:-len("_window")]
    return window_name


# ---------------------------------------------------------------------------
# Builder — container OCR e vanilla
# ---------------------------------------------------------------------------

def build_ocr_container(container_prefix: str, body_lines: list[str],
                        extra_indent: int = 1) -> list[str]:
    """
    Avvolge il contenuto OCR nel container standard con
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"
    """
    tab = "\t" * extra_indent
    result = [
        "\n",
        f"{tab}# ============================================================\n",
        f"{tab}# BLOCCO OCR — testo, screen reader ready\n",
        f"{tab}# variabile ocr ASSENTE = modalita' non vedente\n",
        f"{tab}# ============================================================\n",
        f"{tab}widget = {{\n",
        f"{tab}\tname = \"ocr_{container_prefix}_container\"\n",
        f"{tab}\tvisible = \"{TOGGLE_OCR_OFF}\"\n",
        f"{tab}\tsize = {{ 100% 100% }}\n\n",
    ]
    result += indent_lines(body_lines, extra_tabs=extra_indent + 1)
    result.append(f"{tab}}}\n")
    return result


def build_vanilla_container(container_prefix: str, vanilla_inner: list[str],
                             extra_indent: int = 1) -> list[str]:
    """
    Avvolge il contenuto vanilla nel container standard con
    visible = "[GetVariableSystem.Exists('ocr')]"
    Il contenuto vanilla non viene mai modificato — copia fedele.
    """
    tab = "\t" * extra_indent
    result = [
        "\n",
        f"{tab}# ============================================================\n",
        f"{tab}# BLOCCO VANILLA — copia fedele CK3 originale\n",
        f"{tab}# variabile ocr PRESENTE = modalita' normo-vedente\n",
        f"{tab}# NON MODIFICARE MAI — identico al vanilla\n",
        f"{tab}# ============================================================\n",
        f"{tab}widget = {{\n",
        f"{tab}\tname = \"vanilla_{container_prefix}_container\"\n",
        f"{tab}\tvisible = \"{TOGGLE_OCR_ON}\"\n\n",
    ]
    result += indent_lines(vanilla_inner, extra_tabs=extra_indent + 1)
    result.append(f"{tab}}}\n")
    return result


def sanitize_vanilla_inner_for_type(vanilla_inner: list[str]) -> list[str]:
    """
    Rimuove dal body vanilla le proprieta' window-level che non sono valide
    dentro un type widget separato (Pattern v1.1).

    Nota: in ``vanilla_inner`` la profondita' 0 corrisponde al livello top del
    vecchio ``window = { ... }`` originale.
    """
    forbidden_top_level_props = {
        "movable",
        "layer",
        "attachto",
        "widgetid",
        "parentanchor",
        "allow_outside",
        "gfxtype",
        "alwaystransparent",
        "size",
        "position",
    }

    sanitized: list[str] = []
    depth = 0
    skipping_state = False
    state_depth = 0

    for line in vanilla_inner:
        stripped = line.strip()
        open_count = line.count("{")
        close_count = line.count("}")

        if skipping_state:
            state_depth += open_count - close_count
            depth += open_count - close_count
            if state_depth <= 0:
                skipping_state = False
                state_depth = 0
            continue

        if depth == 0:
            key = stripped.split("=", 1)[0].strip() if "=" in stripped else ""
            if key in forbidden_top_level_props:
                depth += open_count - close_count
                continue

            if stripped.startswith("state") and stripped.endswith("{"):
                # I blocchi _show/_hide appartengono al window wrapper, non al type.
                skipping_state = True
                state_depth = 1
                depth += open_count - close_count
                continue

        sanitized.append(line)
        depth += open_count - close_count

    return sanitized


# ---------------------------------------------------------------------------
# Builder — sub-window dual-mode generica

# ---------------------------------------------------------------------------
# Builder — file type vanilla separato (Pattern v1.1)
# ---------------------------------------------------------------------------

def build_vanilla_type_file(type_name: str, vanilla_inner: list[str],
                             window_name: str, mode: str) -> list[str]:
    """
    Genera il contenuto del file type separato (Pattern v1.1).
    Il tipo ha nome '{prefix}_patch_vanilla' dentro il blocco types OCR_PATCH_VANILLA.
    La guard visible è esplicita dentro il type.
    """
    sanitized_inner = sanitize_vanilla_inner_for_type(vanilla_inner)

    output = [
        f"# {type_name}.gui — OCR Support Patch — Vanilla type separato (Pattern v1.1)\n",
        f"# Generato da: tools/assemble_dualmode.py --window {window_name} --mode {mode} --separate-vanilla\n",
        f"# ATTENZIONE: contenuto vanilla identico al file CK3 originale — non modificare.\n",
        f"# La guard visible vive QUI — il wrapper istanzia questo type senza visible esplicita.\n",
        "\n",
        "types OCR_PATCH_VANILLA {\n",
        f"\ttype {type_name} = widget {{\n",
        f"\t\tname = \"vanilla_{type_name}_container\"\n",
        f"\t\tvisible = \"{TOGGLE_OCR_ON}\"\n",
        "\n",
    ]
    output += indent_lines(sanitized_inner, extra_tabs=2)
    output += [
        "\t}\n",
        "}\n",
    ]
    return output


def build_wrapper_with_type_ref(window_name: str, type_name: str,
                                 ocr_lines: list[str], ocr_win: tuple[int, int],
                                 vanilla_win: tuple[int, int],
                                 vanilla_header_lines: list[str]) -> list[str]:
    """
    Costruisce il wrapper per il pattern v1.1:
    - header window-level (state, layer, name, size, movable…) dalla finestra vanilla
    - container OCR inline
    - istanziazione del type vanilla separato senza visible esplicita
    """
    os_idx, oe_idx = ocr_win
    vs_idx, ve_idx = vanilla_win

    ocr_inner = ocr_lines[os_idx + 1 : oe_idx]
    prefix = _derive_prefix(window_name)

    # Separa header da body OCR
    body_start = len(ocr_inner)
    for i, line in enumerate(ocr_inner):
        stripped = line.strip()
        if (stripped.startswith("vbox = {") or stripped.startswith("vbox={")) and \
                not any(kw in line for kw in ("state", "attachto", "using", "layer")):
            body_start = i
            break
        if stripped.startswith("hbox = {") and i > 5:
            body_start = i
            break

    header_lines = ocr_inner[:body_start]
    body_lines   = ocr_inner[body_start:]

    result = ["window = {\n"]
    result += header_lines
    result += build_ocr_container(prefix, body_lines, extra_indent=1)
    result += [
        "\n",
        "\t# ============================================================\n",
        "\t# BLOCCO VANILLA — type separato (Pattern v1.1)\n",
        "\t# visible gestita dentro il type — non aggiungere visible qui\n",
        "\t# ============================================================\n",
        f"\t{type_name} = {{}}\n",
        "}\n",
    ]
    return result

# ---------------------------------------------------------------------------

def build_sub_window_dual(ocr_lines: list[str],
                           vanilla_lines: list[str],
                           ocr_win: tuple[int, int],
                           vanilla_win: tuple[int, int],
                           window_name: str,
                           container_prefix: str = None) -> list[str]:
    """
    Costruisce una window dual-mode generica.
    Separa header OCR (state, using, layer, size, attachto) da body
    (primo vbox/hbox/container di contenuto), poi avvolge body e vanilla
    nei rispettivi container.
    Se container_prefix non è fornito, viene derivato da window_name.
    """
    if container_prefix is None:
        container_prefix = _derive_prefix(window_name)

    os_idx, oe_idx = ocr_win
    vs_idx, ve_idx = vanilla_win

    ocr_inner     = ocr_lines[os_idx + 1 : oe_idx]
    vanilla_inner = vanilla_lines[vs_idx + 1 : ve_idx]

    # Separa header (attributi window-level) da body (contenuto principale)
    body_start = len(ocr_inner)
    for i, line in enumerate(ocr_inner):
        stripped = line.strip()
        if (stripped.startswith("vbox = {") or stripped.startswith("vbox={")) and \
                not any(kw in line for kw in ("state", "attachto", "using", "layer")):
            body_start = i
            break
        if stripped.startswith("hbox = {") and i > 5:
            body_start = i
            break

    # La prima riga di ocr_inner e' sempre 'name = "..."' — NON aggiungere
    # il nome esplicitamente per evitare duplicati nel file output.
    header_lines = ocr_inner[:body_start]
    body_lines   = ocr_inner[body_start:]

    result = [f"window = {{\n"]
    result += header_lines
    result += build_ocr_container(container_prefix, body_lines, extra_indent=1)
    result += build_vanilla_container(container_prefix, vanilla_inner, extra_indent=1)
    result += ["}\n"]
    return result


# ---------------------------------------------------------------------------
# Helper — raccolta blocchi non-window (types, templates, local_template)
# ---------------------------------------------------------------------------

def collect_non_window_blocks(ocr_lines: list[str],
                               vanilla_lines: list[str]) -> list[str]:
    """
    Raccoglie blocchi top-level non-window (types, template, type, local_template)
    da entrambi i file sorgente, usando la stessa strategia di assemble_complex:
      1. Tutti i blocchi vanilla (servono a entrambi i container)
      2. Blocchi OCR-only (nomi non presenti in vanilla)

    In Jomini, blocchi con lo stesso nome sono validi (vengono mergiati),
    quindi si rispettano le occorrenze multiple.
    """
    ocr_content = extract_window_content(ocr_lines)
    van_content = extract_window_content(vanilla_lines)

    output: list[str] = []

    # -- Types e types_block --
    van_types = [b for b in van_content if b["type"] in ("type", "types_block")]
    van_type_names = {}
    for b in van_types:
        van_type_names[b["name"]] = van_type_names.get(b["name"], 0) + 1
        output += vanilla_lines[b["start"] : b["end"] + 1]
        output.append("\n")

    ocr_types = [b for b in ocr_content if b["type"] in ("type", "types_block")]
    ocr_only_types = []
    ocr_type_counts = {}
    for b in ocr_types:
        ocr_type_counts[b["name"]] = ocr_type_counts.get(b["name"], 0) + 1
        van_count = van_type_names.get(b["name"], 0)
        if ocr_type_counts[b["name"]] > van_count:
            ocr_only_types.append(b)

    if ocr_only_types:
        output.append("# ============================================================\n")
        output.append("# Types OCR-only — necessari per la modalita' non vedente\n")
        output.append("# ============================================================\n\n")
        for b in ocr_only_types:
            output += ocr_lines[b["start"] : b["end"] + 1]
            output.append("\n")

    # -- Templates --
    van_templates = [b for b in van_content if b["type"] == "template"]
    van_tpl_names = {}
    for b in van_templates:
        van_tpl_names[b["name"]] = van_tpl_names.get(b["name"], 0) + 1
        output += vanilla_lines[b["start"] : b["end"] + 1]
        output.append("\n")

    ocr_templates = [b for b in ocr_content if b["type"] == "template"]
    ocr_only_templates = []
    ocr_tpl_counts = {}
    for b in ocr_templates:
        ocr_tpl_counts[b["name"]] = ocr_tpl_counts.get(b["name"], 0) + 1
        van_count = van_tpl_names.get(b["name"], 0)
        if ocr_tpl_counts[b["name"]] > van_count:
            ocr_only_templates.append(b)

    if ocr_only_templates:
        output.append("# ============================================================\n")
        output.append("# Templates OCR-only — necessari per la modalita' non vedente\n")
        output.append("# ============================================================\n\n")
        for b in ocr_only_templates:
            output += ocr_lines[b["start"] : b["end"] + 1]
            output.append("\n")

    # -- Blocchi top-level "other" da OCR (widget, window_ocr, window secondari, ecc.) --
    # Questi blocchi non hanno controparte vanilla — sono completamente OCR-only.
    ocr_others = [b for b in ocr_content if b["type"] == "other"]
    van_other_names = {b["name"] for b in van_content if b["type"] == "other"}
    ocr_only_others = [b for b in ocr_others if b["name"] not in van_other_names]

    if ocr_only_others:
        output.append("# ============================================================\n")
        output.append("# Blocchi extra OCR-only (widget, window_ocr, ecc.)\n")
        output.append("# ============================================================\n\n")
        for b in ocr_only_others:
            output += ocr_lines[b["start"] : b["end"] + 1]
            output.append("\n")

    # -- Finestre secondarie vanilla (window top-level con name != window principale) --
    # Queste finestre esistono in vanilla come blocchi top-level extra e devono
    # essere presenti nel wrapper per evitare "Could not find widget".
    van_extra_windows = [b for b in van_content if b["type"] == "window"]
    ocr_window_names = {b["name"] for b in ocr_content if b["type"] == "window"}
    van_only_extra_windows = [b for b in van_extra_windows if b["name"] not in ocr_window_names]

    if van_only_extra_windows:
        output.append("# ============================================================\n")
        output.append("# Finestre secondarie vanilla (non presenti in OCR upstream)\n")
        output.append("# ============================================================\n\n")
        for b in van_only_extra_windows:
            output += vanilla_lines[b["start"] : b["end"] + 1]
            output.append("\n")

    return output


# ---------------------------------------------------------------------------
# Assembly — Pattern A (simple)
# ---------------------------------------------------------------------------

def assemble_simple(window_name: str, ocr_lines: list[str],
                    vanilla_lines: list[str]) -> list[str]:
    """
    Pattern A: una sola window, struttura semplice.
    Estrae la prima window da OCR e da vanilla e costruisce la dual-mode.
    Include anche blocchi types/template da entrambi i file sorgente.
    """
    ocr_wins = find_top_level_windows(ocr_lines)
    van_wins = find_top_level_windows(vanilla_lines)

    if not ocr_wins:
        raise ValueError(f"Nessuna window trovata nel file OCR di {window_name}")
    if not van_wins:
        raise ValueError(f"Nessuna window trovata nel file vanilla di {window_name}")

    # Prima i blocchi non-window (types, templates)
    result = collect_non_window_blocks(ocr_lines, vanilla_lines)

    prefix = _derive_prefix(window_name)
    result += build_sub_window_dual(
        ocr_lines, vanilla_lines,
        (ocr_wins[0][0], ocr_wins[0][1]),
        (van_wins[0][0], van_wins[0][1]),
        window_name, prefix,
    )
    result.append("\n")
    return result


# ---------------------------------------------------------------------------
# Assembly — Pattern B (tabs)
# ---------------------------------------------------------------------------

def assemble_tabs(window_name: str, ocr_lines: list[str],
                  vanilla_lines: list[str]) -> list[str]:
    """
    Pattern B: window principale + sub-windows.
    Abbina le window per nome (fallback posizionale se i nomi divergono).
    Ordine output: sequenza del file vanilla (coerenza con CK3).
    Window presente solo in vanilla → solo vanilla_container.
    Window presente solo in OCR → solo ocr_container.
    Include anche blocchi types/template da entrambi i file sorgente.
    """
    ocr_wins = find_top_level_windows(ocr_lines)
    van_wins = find_top_level_windows(vanilla_lines)

    ocr_by_name = {w[2]: w for w in ocr_wins}
    van_by_name = {w[2]: w for w in van_wins}

    # Prima i blocchi non-window (types, templates)
    output = collect_non_window_blocks(ocr_lines, vanilla_lines)

    # Verifica se è necessario il fallback posizionale
    names_diverge = len(ocr_wins) != len(van_wins) or any(
        w[2] not in van_by_name for w in ocr_wins if w[2] != "unknown"
    )

    if names_diverge:
        print("  [AVVISO] Nomi window divergenti tra OCR e vanilla — uso fallback posizionale")
        for ocr_w, van_w in zip(ocr_wins, van_wins):
            prefix = _derive_prefix(ocr_w[2])
            section = build_sub_window_dual(
                ocr_lines, vanilla_lines,
                (ocr_w[0], ocr_w[1]),
                (van_w[0], van_w[1]),
                ocr_w[2], prefix,
            )
            output += section
            output.append("\n")
    else:
        # Ordine vanilla
        for van_w in van_wins:
            name = van_w[2]
            prefix = _derive_prefix(name)
            if name in ocr_by_name:
                ocr_w = ocr_by_name[name]
                section = build_sub_window_dual(
                    ocr_lines, vanilla_lines,
                    (ocr_w[0], ocr_w[1]),
                    (van_w[0], van_w[1]),
                    name, prefix,
                )
                output += section
            else:
                # Solo in vanilla
                vanilla_inner = vanilla_lines[van_w[0] + 1 : van_w[1]]
                output += [f"window = {{\n", f"\tname = \"{name}\"\n"]
                output += build_vanilla_container(prefix, vanilla_inner, extra_indent=1)
                output += ["}\n"]
                print(f"  [INFO] Window '{name}' solo in vanilla — solo container vanilla")
            output.append("\n")

        # Window solo in OCR
        for ocr_w in ocr_wins:
            if ocr_w[2] not in van_by_name:
                prefix = _derive_prefix(ocr_w[2])
                ocr_inner = ocr_lines[ocr_w[0] + 1 : ocr_w[1]]
                output += [f"window = {{\n", f"\tname = \"{ocr_w[2]}\"\n"]
                output += build_ocr_container(prefix, ocr_inner, extra_indent=1)
                output += ["}\n", "\n"]
                print(f"  [INFO] Window '{ocr_w[2]}' solo in OCR — solo container OCR")

    return output


# ---------------------------------------------------------------------------
# Assembly — Pattern C/D (complex)
# ---------------------------------------------------------------------------

def assemble_complex(window_name: str, ocr_lines: list[str],
                     vanilla_lines: list[str]) -> list[str]:
    """
    Pattern C/D: window + types + templates separati.

    Logica:
    - Window: stesso abbinamento per nome di assemble_tabs (fallback posizionale)
    - Types vanilla: inclusi per intero (servono a entrambi i container)
    - Types solo-OCR: aggiunti dopo i types vanilla con commento '# OCR-only'
    - Types condivisi (stesso nome): usa versione vanilla come base
    - Templates: stessa logica dei types
    Ordine output: window blocks → types blocks → template blocks
    """
    ocr_content = extract_window_content(ocr_lines)
    van_content = extract_window_content(vanilla_lines)

    output = []

    # -- Windows --
    ocr_wins = [b for b in ocr_content if b["type"] == "window"]
    van_wins = [b for b in van_content if b["type"] == "window"]
    ocr_win_by_name = {b["name"]: b for b in ocr_wins}
    van_win_by_name = {b["name"]: b for b in van_wins}

    names_diverge = len(ocr_wins) != len(van_wins) or any(
        w["name"] not in van_win_by_name for w in ocr_wins if w["name"] != "unknown"
    )

    if names_diverge:
        print("  [AVVISO] Nomi window divergenti — uso fallback posizionale")
        for ocr_w, van_w in zip(ocr_wins, van_wins):
            prefix = _derive_prefix(ocr_w["name"])
            section = build_sub_window_dual(
                ocr_lines, vanilla_lines,
                (ocr_w["start"], ocr_w["end"]),
                (van_w["start"], van_w["end"]),
                ocr_w["name"], prefix,
            )
            output += section
            output.append("\n")
    else:
        for van_w in van_wins:
            name = van_w["name"]
            prefix = _derive_prefix(name)
            if name in ocr_win_by_name:
                ocr_w = ocr_win_by_name[name]
                section = build_sub_window_dual(
                    ocr_lines, vanilla_lines,
                    (ocr_w["start"], ocr_w["end"]),
                    (van_w["start"], van_w["end"]),
                    name, prefix,
                )
                output += section
            else:
                van_inner = vanilla_lines[van_w["start"] + 1 : van_w["end"]]
                output += [f"window = {{\n", f"\tname = \"{name}\"\n"]
                output += build_vanilla_container(prefix, van_inner, extra_indent=1)
                output += ["}\n"]
                print(f"  [INFO] Window '{name}' solo in vanilla")
            output.append("\n")

        for ocr_w in ocr_wins:
            if ocr_w["name"] not in van_win_by_name:
                prefix = _derive_prefix(ocr_w["name"])
                ocr_inner = ocr_lines[ocr_w["start"] + 1 : ocr_w["end"]]
                output += [f"window = {{\n", f"\tname = \"{ocr_w['name']}\"\n"]
                output += build_ocr_container(prefix, ocr_inner, extra_indent=1)
                output += ["}\n", "\n"]
                print(f"  [INFO] Window '{ocr_w['name']}' solo in OCR")

    # -- Types e types_block --
    # Prima tutti i types vanilla (servono a entrambi i container)
    van_types = [b for b in van_content if b["type"] in ("type", "types_block")]
    van_type_names = {b["name"] for b in van_types}
    for b in van_types:
        output += vanilla_lines[b["start"] : b["end"] + 1]
        output.append("\n")

    # Poi i types presenti solo in OCR (necessari per la modalità non vedente)
    ocr_types = [b for b in ocr_content if b["type"] in ("type", "types_block")]
    ocr_only_types = [b for b in ocr_types if b["name"] not in van_type_names]
    if ocr_only_types:
        output.append("# ============================================================\n")
        output.append("# Types OCR-only — necessari per la modalita' non vedente\n")
        output.append("# ============================================================\n\n")
        for b in ocr_only_types:
            output += ocr_lines[b["start"] : b["end"] + 1]
            output.append("\n")
            print(f"  [OCR-only type] {b['name']}")

    # -- Templates --
    # Prima tutti i templates vanilla
    van_templates = [b for b in van_content if b["type"] == "template"]
    van_tpl_names = {b["name"] for b in van_templates}
    for b in van_templates:
        output += vanilla_lines[b["start"] : b["end"] + 1]
        output.append("\n")

    # Poi i templates OCR-only
    ocr_templates = [b for b in ocr_content if b["type"] == "template"]
    ocr_only_templates = [b for b in ocr_templates if b["name"] not in van_tpl_names]
    if ocr_only_templates:
        output.append("# ============================================================\n")
        output.append("# Templates OCR-only — necessari per la modalita' non vedente\n")
        output.append("# ============================================================\n\n")
        for b in ocr_only_templates:
            output += ocr_lines[b["start"] : b["end"] + 1]
            output.append("\n")
            print(f"  [OCR-only template] {b['name']}")

    return output


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assembla un file .gui dual-mode OCR+vanilla per CK3 1.17.1."
    )
    parser.add_argument(
        "--window", required=True,
        help="Nome della finestra senza estensione (es. window_faith, window_council)",
    )
    parser.add_argument(
        "--mode", required=True, choices=["simple", "tabs", "complex"],
        help="Strategia di assemblaggio: simple (Pattern A) | tabs (Pattern B) | complex (Pattern C/D)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Stampa l'output su stdout senza scrivere il file nella patch",
    )
    parser.add_argument(
        "--separate-vanilla", action="store_true",
        help="Pattern v1.1: vanilla in type separato in gui/vanilla/. Produce DUE file.",
    )
    args = parser.parse_args()

    window_name  = args.window
    ocr_file     = OCR_GUI / f"{window_name}.gui"
    vanilla_file = VANILLA_GUI / f"{window_name}.gui"
    patch_file   = PATCH_GUI / f"{window_name}.gui"

    # Costanti per il pattern v1.1
    prefix    = _derive_prefix(window_name)
    type_name = f"{prefix}_patch_vanilla"
    type_file = VANILLA_TYPES_GUI / f"{type_name}.gui"

    print(f"=== Assemblaggio {window_name}.gui — Dual Mode ({args.mode}) ===\n")

    # Verifica esistenza sorgenti
    if not ocr_file.exists():
        print(f"[ERRORE] File OCR upstream non trovato:\n  {ocr_file}")
        sys.exit(1)
    if not vanilla_file.exists():
        print(f"[ERRORE] File vanilla non trovato:\n  {vanilla_file}")
        sys.exit(1)

    # Crea gui/vanilla/ se necessaria (solo in modalità scrittura)
    if args.separate_vanilla and not args.dry_run:
        if not VANILLA_TYPES_GUI.exists():
            print(f"[INFO] Creazione cartella gui/vanilla/: {VANILLA_TYPES_GUI}")
            VANILLA_TYPES_GUI.mkdir(parents=True, exist_ok=True)

    print(f"Lettura OCR upstream:  {ocr_file}")
    ocr_lines = read_file(ocr_file)
    print(f"  {len(ocr_lines)} righe lette")

    print(f"Lettura vanilla CK3:   {vanilla_file}")
    vanilla_lines = read_file(vanilla_file)
    print(f"  {len(vanilla_lines)} righe lette\n")

    # -----------------------------------------------------------------------
    # Pattern v1.1 — vanilla type separato
    # -----------------------------------------------------------------------
    if args.separate_vanilla:
        print(f"Assemblaggio ({args.mode}) — Pattern v1.1 (vanilla separato)...")
        van_wins = find_top_level_windows(vanilla_lines)
        ocr_wins = find_top_level_windows(ocr_lines)
        if not van_wins or not ocr_wins:
            print("[ERRORE] Nessuna window trovata nel file OCR o vanilla.")
            sys.exit(1)

        # Header wrapper
        wrapper_output = [
            f"# {window_name}.gui — OCR Support Patch — Wrapper (Pattern v1.1)\n",
            f"# Il branch vanilla è nel type separato: gui/vanilla/{type_name}.gui\n",
            f"# Dual Mode: OCR (screen reader) + Vanilla CK3 1.17.1\n",
            f"# Generato da: tools/assemble_dualmode.py --window {window_name}"
            f" --mode {args.mode} --separate-vanilla\n",
            "\n",
        ]
        wrapper_output += build_wrapper_with_type_ref(
            window_name, type_name,
            ocr_lines, (ocr_wins[0][0], ocr_wins[0][1]),
            (van_wins[0][0], van_wins[0][1]),
            [],
        )

        # File type vanilla
        vanilla_inner = vanilla_lines[van_wins[0][0] + 1 : van_wins[0][1]]
        type_output = build_vanilla_type_file(type_name, vanilla_inner, window_name, args.mode)

        print(f"\nRighe wrapper:    {len(wrapper_output)}")
        print(f"Righe type file:  {len(type_output)}")

        if args.dry_run:
            print("\n[DRY-RUN] Nessun file scritto.\n")
            print("=== PREVIEW WRAPPER ===")
            print("".join(wrapper_output[:60]))
            print("\n=== PREVIEW TYPE FILE VANILLA ===")
            print("".join(type_output[:60]))
            return

        print(f"\nScrittura wrapper: {patch_file}")
        patch_file.parent.mkdir(parents=True, exist_ok=True)
        with open(patch_file, "w", encoding="utf-8") as f:
            f.writelines(wrapper_output)
        print(f"  SCRITTO — {patch_file.stat().st_size // 1024} KB")

        print(f"Scrittura type:    {type_file}")
        with open(type_file, "w", encoding="utf-8") as f:
            f.writelines(type_output)
        print(f"  SCRITTO — {type_file.stat().st_size // 1024} KB")
        print(f"\n=== Completato (v1.1). Eseguire audit.py --window {window_name} per la verifica. ===")
        return

    # -----------------------------------------------------------------------
    # Pattern v1.0 — inline (comportamento originale)
    # -----------------------------------------------------------------------
    output = [
        f"# {window_name}.gui — OCR Support Patch\n",
        f"# Dual Mode: OCR (screen reader) + Vanilla CK3 1.17.1\n",
        f"# Generato da: tools/assemble_dualmode.py --window {window_name} --mode {args.mode}\n",
        f"# NON modificare il container vanilla — identico al file originale Paradox.\n",
        "\n",
    ]

    print(f"Assemblaggio ({args.mode})...")
    if args.mode == "simple":
        output += assemble_simple(window_name, ocr_lines, vanilla_lines)
    elif args.mode == "tabs":
        output += assemble_tabs(window_name, ocr_lines, vanilla_lines)
    elif args.mode == "complex":
        output += assemble_complex(window_name, ocr_lines, vanilla_lines)

    total_lines = len(output)
    print(f"\nTotale righe output: {total_lines}")

    if args.dry_run:
        print("\n[DRY-RUN] File NON scritto. Preview:\n")
        print("--- Prime 60 righe ---")
        print("".join(output[:60]))
        print(f"\n--- Ultime 20 righe ---")
        print("".join(output[-20:]))
        return

    print(f"\nScrittura: {patch_file}")
    patch_file.parent.mkdir(parents=True, exist_ok=True)
    with open(patch_file, "w", encoding="utf-8") as f:
        f.writelines(output)
    size_kb = patch_file.stat().st_size // 1024
    print(f"  SCRITTO — {size_kb} KB")
    print(f"\n=== Completato. Eseguire audit.py --window {window_name} per la verifica. ===")


if __name__ == "__main__":
    main()
