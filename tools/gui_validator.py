"""
gui_validator.py — Scansione meccanica di file .gui per pattern deprecati,
vietati e problemi strutturali nel sistema dual mode OCR Support Patch.

Uso:
    python tools/gui_validator.py --file <percorso_file> [--format json|markdown]

Dipendenze: solo stdlib Python 3.8+
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Aggiunge la directory radice al path in modo che 'from tools.config import ...' funzioni
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ---------------------------------------------------------------------------
# Definizione pattern
# ---------------------------------------------------------------------------

# Ogni pattern è un dict con campi:
#   regex       : espressione regolare (stringa, compilata al runtime)
#   category    : DEPRECATO | VIETATO | STRUTTURALE | VISIBILITA
#   severity    : CRITICO | ATTENZIONE
#   description : testo leggibile del pattern trovato
#   fix         : fix consigliato
#   multiline   : True se richiede analisi su blocco multi-riga (gestito a parte)

SIMPLE_PATTERNS = [
    # --- DEPRECATO ---
    {
        "regex": r"""GameRules\s*\.\s*GetRule\s*\(\s*['"]ocr_accessibility_mode['"]\s*\)""",
        "category": "DEPRECATO",
        "severity": "CRITICO",
        "description": "GameRules.GetRule('ocr_accessibility_mode')",
        "fix": "Sostituire con GetVariableSystem.Exists('ocr') (o Not(...) per OCR)",
    },
    # --- VIETATO ---
    {
        "regex": r"\bshow_when\s*=",
        "category": "VIETATO",
        "severity": "CRITICO",
        "description": "show_when usato al posto di visible",
        "fix": "Sostituire show_when con visible",
    },
    {
        "regex": r"\[ROOT\b|ROOT\.Get|ROOT\.Has|ROOT\.Is",
        "category": "VIETATO",
        "severity": "CRITICO",
        "description": "Scope ROOT usato in binding GUI senza verifica",
        "fix": "Verificare il tipo di scope corretto nel file vanilla e aggiornare la whitelist",
    },
    {
        "regex": r"\[THIS\b|THIS\.Get|THIS\.Has|THIS\.Is",
        "category": "VIETATO",
        "severity": "CRITICO",
        "description": "Scope THIS usato in binding GUI senza verifica",
        "fix": "Verificare il tipo di scope corretto nel file vanilla e aggiornare la whitelist",
    },
    {
        "regex": r"\bdatamodel\s*=",
        "category": "VIETATO",
        "severity": "ATTENZIONE",
        "description": "datamodel senza nota di verifica del type",
        "fix": "Verificare il type nel file vanilla e nella whitelist scope prima di usare datamodel",
    },
]

# Pattern di naming/modalità: il repository usa naming misto.
RE_OCR_NAME = re.compile(r'name\s*=\s*"(?:ocr_|ocr_mode|.*_ocr\b)', re.IGNORECASE)
RE_VANILLA_NAME = re.compile(r'name\s*=\s*"(?:vanilla_|normal_mode|grafic_version)', re.IGNORECASE)
RE_OCR_BLOCK_HINT = re.compile(r'^\s*(?:window_ocr|\w+_ocr)\s*=\s*\{', re.IGNORECASE)

# Regex per visibilità OCR/vanilla, inclusi shorthand Agamidae Is/Isnt.
RE_VISIBLE_VANILLA_EXISTS = re.compile(r'visible\s*=\s*"\[GetVariableSystem\.Exists\(\'ocr\'\)\]"')
RE_VISIBLE_OCR_EXISTS = re.compile(r'visible\s*=\s*"\[Not\(GetVariableSystem\.Exists\(\'ocr\'\)\)\]"')
RE_VISIBLE_VANILLA_SHORTHAND = re.compile(r'visible\s*=\s*"\[[^\]]*\bIs\(\'ocr\'\)[^\]]*\]"')
RE_VISIBLE_OCR_SHORTHAND = re.compile(r'visible\s*=\s*"\[[^\]]*\bIsnt\(\'ocr\'\)[^\]]*\]"')

# Regex per analisi blocchi (icon/button senza tooltip, fontsize OCR)
RE_BLOCK_OPEN = re.compile(r'^\s*(icon|button|button_standard|button_primary|button_icon)\s*=\s*\{', re.IGNORECASE)
RE_TOOLTIP = re.compile(r'\b(tooltip|tooltipwidget)\s*=')
RE_FONTSIZE = re.compile(r'\bfontsize\s*=\s*(\d+)')
RE_TEXT_WIDGET = re.compile(r'\b(text_single|text_multi|text_label)\s*=\s*\{', re.IGNORECASE)
RE_BUTTON_TEXT = re.compile(r'\b(text|raw_text)\s*=')
RE_SHORTCUT = re.compile(r'\bshortcut\s*=')
RE_WINDOW_ROOT = re.compile(r'^\s*window\s*=\s*\{', re.IGNORECASE)

# --- Regex per completezza OCR ---
# raw_text statico: il valore non inizia con '[' (binding) ne' '{' (reference)
RE_STATIC_RAW_TEXT = re.compile(r'\braw_text\s*=\s*"[^\[{]')
RE_COLOR_HEADER_CANONICAL = re.compile(r'\bcolor\s*=\s*\{\s*255\s+221\s+136\s+255\s*\}')
RE_BUTTON_WIDGET_ANY = re.compile(
    r'^\s*(button|button_standard|button_primary|button_icon|iconbutton)\s*=\s*\{',
    re.IGNORECASE,
)
RE_DATAMODEL_LINE = re.compile(r'\bdatamodel\s*=')


def _is_ocr_visibility(riga: str) -> bool:
    return bool(RE_VISIBLE_OCR_EXISTS.search(riga) or RE_VISIBLE_OCR_SHORTHAND.search(riga))


def _is_vanilla_visibility(riga: str) -> bool:
    return bool(RE_VISIBLE_VANILLA_EXISTS.search(riga) or RE_VISIBLE_VANILLA_SHORTHAND.search(riga))


def _is_ocr_block_header(riga: str) -> bool:
    return bool(RE_OCR_NAME.search(riga) or RE_OCR_BLOCK_HINT.search(riga))


def _linea_in_range(num_riga: int, ranges: list[tuple[int, int]]) -> bool:
    return any(inizio <= num_riga <= fine for inizio, fine in ranges)


def _trova_blocchi_modalita(righe: list[str], modalita: str) -> list[tuple[int, int]]:
    """
    Trova i blocchi principali OCR/vanilla usando naming e visibility reali.
    Restituisce tuple (linea_inizio, linea_fine) 1-based.
    """
    ranges = []
    predicato = _is_ocr_visibility if modalita == "ocr" else _is_vanilla_visibility

    for i, riga in enumerate(righe):
        if "{" not in riga:
            continue

        fine = _trova_fine_blocco(righe, i)
        if fine == -1:
            continue

        finestra = righe[i:min(fine + 1, i + 12)]
        ha_visibility = any(predicato(r) for r in finestra)
        ha_nome = _is_ocr_block_header(riga) if modalita == "ocr" else bool(RE_VANILLA_NAME.search(riga))

        if ha_visibility or ha_nome:
            ranges.append((i + 1, fine + 1))

    # Rimuove blocchi contenuti interamente in un altro blocco della stessa modalità.
    ranges.sort()
    filtrati = []
    for inizio, fine in ranges:
        if any(prev_inizio <= inizio and fine <= prev_fine for prev_inizio, prev_fine in filtrati):
            continue
        filtrati.append((inizio, fine))
    return filtrati


def _trova_blocchi_nascosti(righe: list[str]) -> list[tuple[int, int]]:
    """Trova i container helper invisibili usati per shortcut keyboard-only."""
    ranges = []
    for i, riga in enumerate(righe):
        if "{" not in riga:
            continue

        fine = _trova_fine_blocco(righe, i)
        if fine <= i:
            continue

        finestra = righe[i:min(fine + 1, i + 12)]
        ha_visible_no = any("visible = no" in r for r in finestra)
        ha_size_zero = any("size = { 0 0 }" in r for r in finestra)
        if ha_visible_no and ha_size_zero:
            ranges.append((i + 1, fine + 1))
    return ranges


# ---------------------------------------------------------------------------
# Funzioni di analisi
# ---------------------------------------------------------------------------

def _apri_file(percorso: Path) -> list[str]:
    """Legge il file e restituisce le righe. Termina con errore se non esiste."""
    if not percorso.exists():
        print(f"ERRORE: file non trovato: {percorso}", file=sys.stderr)
        sys.exit(1)
    with open(percorso, encoding="utf-8") as f:
        return f.readlines()


_RE_VERIFICA_DATAMODEL = re.compile(r"#\s*datamodel\s+verificato\s*:", re.IGNORECASE)


def _scansione_semplice(righe: list[str]) -> list[dict]:
    """Applica i SIMPLE_PATTERNS riga per riga."""
    problemi = []
    compilati = [(re.compile(p["regex"], re.IGNORECASE), p) for p in SIMPLE_PATTERNS]
    for num, riga in enumerate(righe, start=1):
        for pattern_re, p in compilati:
            if pattern_re.search(riga):
                # Esenzione speciale per la regola datamodel:
                # 1. Riga commentata (inizia con #) → codice inattivo, non segnalare
                # 2. Riga contiene '# datamodel verificato:' inline → già verificato
                # 3. Riga precedente contiene '# datamodel verificato:' → già verificato
                if p["description"] == "datamodel senza nota di verifica del type":
                    if riga.lstrip().startswith("#"):
                        continue
                    riga_prec = righe[num - 2] if num >= 2 else ""
                    if _RE_VERIFICA_DATAMODEL.search(riga) or _RE_VERIFICA_DATAMODEL.search(riga_prec):
                        continue
                problemi.append({
                    "line": num,
                    "pattern": p["description"],
                    "category": p["category"],
                    "severity": p["severity"],
                    "fix": p["fix"],
                })
    return problemi


def _trova_fine_blocco(righe: list[str], inizio: int) -> int:
    """
    Dato l'indice di inizio di un blocco aperto con '{', trova la riga
    di chiusura corrispondente (bilanciamento parentesi graffe).
    Restituisce l'indice (0-based) della riga con '}' di chiusura,
    o -1 se non trovato entro la fine del file.
    """
    profondita = 0
    for i in range(inizio, len(righe)):
        profondita += righe[i].count("{") - righe[i].count("}")
        if profondita <= 0:
            return i
    return -1


def _scansione_blocchi(righe: list[str]) -> list[dict]:
    """
    Analisi multi-riga:
    - icon/button senza tooltip nello stesso blocco → CRITICO
    - text widget con fontsize < 18 in contesto OCR → ATTENZIONE
    - visibilità invertita (ocr_ con visible vanilla, vanilla_ con visible ocr) → CRITICO
    """
    problemi = []
    blocchi_ocr = _trova_blocchi_modalita(righe, "ocr")
    blocchi_vanilla = _trova_blocchi_modalita(righe, "vanilla")
    blocchi_nascosti = _trova_blocchi_nascosti(righe)

    for i, riga in enumerate(righe):
        num_riga = i + 1

        # --- Visibilità invertita ---
        if _is_ocr_block_header(riga):
            fine = _trova_fine_blocco(righe, i)
            finestra = righe[i:(fine + 1 if fine != -1 else i + 1)]
            for riga_f in finestra:
                if _is_vanilla_visibility(riga_f):
                    problemi.append({
                        "line": num_riga,
                        "pattern": "Blocco OCR con visibility vanilla (invertita)",
                        "category": "VISIBILITA",
                        "severity": "CRITICO",
                        "fix": "Usare visible OCR corretto: [Not(GetVariableSystem.Exists('ocr'))] o equivalente Isnt('ocr')",
                    })
                    break

        if RE_VANILLA_NAME.search(riga):
            fine = _trova_fine_blocco(righe, i)
            finestra = righe[i:(fine + 1 if fine != -1 else i + 1)]
            for riga_f in finestra:
                if _is_ocr_visibility(riga_f):
                    problemi.append({
                        "line": num_riga,
                        "pattern": "Blocco vanilla con visibility OCR (invertita)",
                        "category": "VISIBILITA",
                        "severity": "CRITICO",
                        "fix": "Usare visible vanilla corretto: [GetVariableSystem.Exists('ocr')] o equivalente Is('ocr')",
                    })
                    break

        # --- icon/button senza tooltip ---
        if _linea_in_range(num_riga, blocchi_ocr) and not _linea_in_range(num_riga, blocchi_nascosti) and not _linea_in_range(num_riga, blocchi_vanilla) and RE_BLOCK_OPEN.match(riga):
            fine = _trova_fine_blocco(righe, i)
            if fine == -1:
                fine = min(i + 15, len(righe) - 1)
            blocco = righe[i:fine + 1]
            ha_tooltip = any(RE_TOOLTIP.search(r) for r in blocco)
            ha_testo = any(RE_BUTTON_TEXT.search(r) for r in blocco)
            e_shortcut_helper = any(RE_SHORTCUT.search(r) for r in blocco) and not ha_testo
            if not ha_tooltip:
                if e_shortcut_helper:
                    continue
                tipo_widget = RE_BLOCK_OPEN.match(riga).group(1).lower()
                problemi.append({
                    "line": num_riga,
                    "pattern": f"{tipo_widget} senza tooltip",
                    "category": "STRUTTURALE",
                    "severity": "CRITICO",
                    "fix": f"Aggiungere tooltip descrittivo al {tipo_widget} (obbligatorio per accessibilità OCR)",
                })

        # --- fontsize < 18 in contesto OCR ---
        if _linea_in_range(num_riga, blocchi_ocr) and not _linea_in_range(num_riga, blocchi_vanilla) and RE_TEXT_WIDGET.match(riga):
            fine = _trova_fine_blocco(righe, i)
            if fine == -1:
                fine = min(i + 10, len(righe) - 1)
            blocco = righe[i:fine + 1]
            for riga_b in blocco:
                m = RE_FONTSIZE.search(riga_b)
                if m:
                    valore = int(m.group(1))
                    if valore < 18:
                        problemi.append({
                            "line": num_riga,
                            "pattern": f"fontsize = {valore} in blocco OCR (minimo 18)",
                            "category": "STRUTTURALE",
                            "severity": "ATTENZIONE",
                            "fix": "Impostare fontsize >= 18 in tutti i widget del blocco OCR",
                        })
                    break  # fontsize trovato nel blocco, non serve continuare

    return problemi


def _scansione_completezza_dual_mode(righe: list[str]) -> list[dict]:
    """Verifica minima: una finestra dual-mode deve esporre entrambe le modalità."""
    problemi = []
    blocchi_ocr = _trova_blocchi_modalita(righe, "ocr")
    blocchi_vanilla = _trova_blocchi_modalita(righe, "vanilla")

    if not blocchi_ocr and not blocchi_vanilla:
        problemi.append({
            "line": 1,
            "pattern": "Nessuna struttura dual mode rilevata",
            "category": "STRUTTURALE",
            "severity": "CRITICO",
            "fix": "Aggiungere blocchi OCR e vanilla con visibility mutuamente esclusiva",
        })
        return problemi

    if blocchi_ocr and not blocchi_vanilla:
        problemi.append({
            "line": blocchi_ocr[0][0],
            "pattern": "Blocco vanilla non rilevato",
            "category": "STRUTTURALE",
            "severity": "ATTENZIONE",
            "fix": "Verificare che la modalità normovedente abbia un blocco con visible = [GetVariableSystem.Exists('ocr')] o equivalente",
        })

    if blocchi_vanilla and not blocchi_ocr:
        problemi.append({
            "line": blocchi_vanilla[0][0],
            "pattern": "Blocco OCR non rilevato",
            "category": "STRUTTURALE",
            "severity": "ATTENZIONE",
            "fix": "Verificare che la modalità OCR abbia un blocco con visible = [Not(GetVariableSystem.Exists('ocr'))] o equivalente",
        })

    return problemi


def _scansione_copertura_multiwindow(righe: list) -> list:
    """
    In file con piu' blocchi window al livello radice (profondita' 0), verifica
    che ogni blocco abbia visibilita' OCR o vanilla, o sia deliberatamente nascosto.
    Si applica solo a file con 2+ blocchi window radice.
    """
    problemi = []
    finestre_root = []
    profondita = 0

    for i, riga in enumerate(righe):
        aperture = riga.count("{")
        chiusure = riga.count("}")
        if profondita == 0 and RE_WINDOW_ROOT.match(riga):
            fine = _trova_fine_blocco(righe, i)
            finestre_root.append((i + 1, fine + 1 if fine != -1 else i + 1))
        profondita += aperture - chiusure

    if len(finestre_root) <= 1:
        return problemi  # file con una sola window radice: gia' gestito da _scansione_completezza_dual_mode

    for inizio, fine in finestre_root:
        # Cerca dual-mode nell'intero blocco window (non solo le prime righe)
        # ma limita a max 200 righe per efficienza su file enormi
        limite = min(fine, inizio - 1 + 200)
        finestra = righe[inizio - 1:limite]
        ha_ocr = any(_is_ocr_visibility(r) for r in finestra)
        ha_vanilla = any(_is_vanilla_visibility(r) for r in finestra)
        # Per visible=no e size 0 0 basta le prime righe (helper nascosti sono piccoli)
        finestra_header = righe[inizio - 1:min(inizio + 14, fine)]
        ha_visible_no = any("visible = no" in r for r in finestra_header)
        ha_size_zero = any("size = { 0 0 }" in r for r in finestra_header[:10])

        if not ha_ocr and not ha_vanilla and not ha_visible_no and not ha_size_zero:
            problemi.append({
                "line": inizio,
                "pattern": "Blocco window radice senza dual-mode esplicito",
                "category": "STRUTTURALE",
                "severity": "CRITICO",
                "fix": "Ogni blocco window radice deve avere dual-mode OCR/vanilla o essere un helper nascosto (visible = no + size = { 0 0 })",
            })

    return problemi


def _scansione_header_ocr(righe: list) -> list:
    """
    Nei blocchi OCR, ogni widget text con fontsize=20 (header canonico) deve usare
    il colore { 255 221 136 255 }. Se fontsize=20 e' presente ma il colore canonico
    e' assente nel widget, segnala ATTENZIONE.
    Non segnala widget senza fontsize=20: solo quelli che dichiarano esplicitamente
    di essere header ma mancano del colore.
    """
    problemi = []
    blocchi_ocr = _trova_blocchi_modalita(righe, "ocr")
    blocchi_vanilla = _trova_blocchi_modalita(righe, "vanilla")
    blocchi_nascosti = _trova_blocchi_nascosti(righe)

    for i, riga in enumerate(righe):
        num_riga = i + 1
        if not _linea_in_range(num_riga, blocchi_ocr):
            continue
        if _linea_in_range(num_riga, blocchi_vanilla) or _linea_in_range(num_riga, blocchi_nascosti):
            continue
        if not RE_TEXT_WIDGET.match(riga):
            continue

        fine = _trova_fine_blocco(righe, i)
        if fine == -1:
            fine = min(i + 12, len(righe) - 1)
        blocco_widget = righe[i:fine + 1]

        ha_fontsize_20 = False
        for r in blocco_widget:
            m = RE_FONTSIZE.search(r)
            if m and int(m.group(1)) == 20:
                ha_fontsize_20 = True
                break
        if not ha_fontsize_20:
            continue

        if not any(RE_COLOR_HEADER_CANONICAL.search(r) for r in blocco_widget):
            problemi.append({
                "line": num_riga,
                "pattern": "Header OCR (fontsize=20) senza colore canonico { 255 221 136 255 }",
                "category": "COMPLETEZZA",
                "severity": "CRITICO",
                "fix": "Aggiungere color = { 255 221 136 255 } al widget testo header nel blocco OCR",
            })
    return problemi


def _scansione_fallback_datamodel_ocr(righe: list) -> list:
    """
    Nei blocchi OCR che usano datamodel, verifica la presenza di almeno un
    raw_text statico (non-binding) che possa fungere da messaggio di fallback
    per lista vuota. Se assente, segnala ATTENZIONE.
    Limite noto: non verifica la correttezza semantica del fallback a runtime;
    verifica solo la presenza strutturale di un testo statico nel blocco.
    """
    problemi = []
    blocchi_ocr = _trova_blocchi_modalita(righe, "ocr")

    for inizio_ocr, fine_ocr in blocchi_ocr:
        righe_blocco = righe[inizio_ocr - 1:fine_ocr]
        if not any(RE_DATAMODEL_LINE.search(r) for r in righe_blocco):
            continue
        if not any(RE_STATIC_RAW_TEXT.search(r) for r in righe_blocco):
            problemi.append({
                "line": inizio_ocr,
                "pattern": "Blocco OCR con datamodel senza testo di fallback statico rilevato",
                "category": "COMPLETEZZA",
                "severity": "CRITICO",
                "fix": (
                    "Aggiungere un widget con raw_text statico come messaggio di lista vuota "
                    "(es: raw_text = \"NESSUN_ELEMENTO\"). "
                    "Nota: la verifica semantica runtime e' fuori scopo del gate automatico v1."
                ),
            })
    return problemi


def _scansione_completezza_ocr(righe: list) -> list:
    """
    Confronto euristico tra blocchi OCR e vanilla: se il vanilla ha almeno 3 button
    interattivi e il blocco OCR ne ha zero, segnala ATTENZIONE (rischio di azioni
    vanilla non accessibili in modalita' OCR).
    Limite noto: il conteggio e' puramente strutturale, non verifica la visibilita'
    condizionale o lo stato enabled/disabled a runtime (fuori scopo gate v1).
    """
    problemi = []
    blocchi_ocr = _trova_blocchi_modalita(righe, "ocr")
    blocchi_vanilla = _trova_blocchi_modalita(righe, "vanilla")

    if not blocchi_ocr or not blocchi_vanilla:
        return problemi  # assenza dual-mode e' gia' segnalata altrove

    n_btn_ocr = sum(
        1 for i, r in enumerate(righe)
        if _linea_in_range(i + 1, blocchi_ocr)
        and not _linea_in_range(i + 1, blocchi_vanilla)
        and RE_BUTTON_WIDGET_ANY.match(r)
    )
    n_btn_vanilla = sum(
        1 for i, r in enumerate(righe)
        if _linea_in_range(i + 1, blocchi_vanilla)
        and not _linea_in_range(i + 1, blocchi_ocr)
        and RE_BUTTON_WIDGET_ANY.match(r)
    )

    if n_btn_vanilla >= 3 and n_btn_ocr == 0:
        problemi.append({
            "line": blocchi_ocr[0][0],
            "pattern": (
                f"Nessun button nel blocco OCR, vanilla ne ha {n_btn_vanilla}: "
                "possibile gap di azioni interattive"
            ),
            "category": "COMPLETEZZA",
            "severity": "ATTENZIONE",
            "fix": (
                "Verificare che le azioni principali del vanilla siano accessibili in modalita' OCR. "
                "Nota: la verifica di azioni condizionali a runtime e' fuori scopo gate v1."
            ),
        })
    return problemi


def analizza_file(percorso: Path) -> dict:
    """
    Analisi completa di un file .gui.
    Restituisce un dict con: file, verdict, critical_count, warning_count, issues.
    """
    righe = _apri_file(percorso)
    problemi = (
        _scansione_semplice(righe)
        + _scansione_blocchi(righe)
        + _scansione_completezza_dual_mode(righe)
        + _scansione_copertura_multiwindow(righe)
        + _scansione_header_ocr(righe)
        + _scansione_fallback_datamodel_ocr(righe)
        + _scansione_completezza_ocr(righe)
    )

    # Rimuove duplicati (stessa riga + categoria)
    visti = set()
    unici = []
    for p in problemi:
        chiave = (p["line"], p["category"], p["pattern"])
        if chiave not in visti:
            visti.add(chiave)
            unici.append(p)

    critici = sum(1 for p in unici if p["severity"] == "CRITICO")
    avvertenze = sum(1 for p in unici if p["severity"] == "ATTENZIONE")

    if critici > 0:
        verdetto = "BLOCCANTE"
    elif avvertenze > 0:
        verdetto = "CON AVVERTENZE"
    else:
        verdetto = "PULITO"

    return {
        "file": str(percorso),
        "verdict": verdetto,
        "critical_count": critici,
        "warning_count": avvertenze,
        "issues": sorted(unici, key=lambda x: x["line"]),
    }


# ---------------------------------------------------------------------------
# Formattazione output
# ---------------------------------------------------------------------------

def _icona_gravita(severity: str) -> str:
    return "[CRITICO]" if severity == "CRITICO" else "[ATTENZIONE]"


def formatta_markdown(risultato: dict) -> str:
    """Produce output Markdown leggibile da screen reader."""
    nome_file = Path(risultato["file"]).name
    righe = [
        f"## Risultati Validazione: {nome_file}",
        "",
    ]
    if not risultato["issues"]:
        righe.append("Nessun problema trovato.")
    else:
        righe.append("| Riga | Pattern trovato | Categoria | Gravità | Fix consigliato |")
        righe.append("|------|----------------|-----------|---------|-----------------|")
        for issue in risultato["issues"]:
            gravita = _icona_gravita(issue["severity"])
            righe.append(
                f"| {issue['line']} | {issue['pattern']} | {issue['category']} | {gravita} | {issue['fix']} |"
            )
    righe += [
        "",
        f"**Verdetto**: {risultato['verdict']}",
        f"**Problemi critici**: {risultato['critical_count']}",
        f"**Avvertenze**: {risultato['warning_count']}",
    ]
    return "\n".join(righe)


def formatta_json(risultato: dict) -> str:
    return json.dumps(risultato, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Entry point CLI
# ---------------------------------------------------------------------------

def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Valida un file .gui CK3 per pattern deprecati e problemi strutturali."
    )
    parser.add_argument(
        "--file", required=True,
        help="Percorso del file .gui da analizzare (assoluto o relativo)."
    )
    parser.add_argument(
        "--format", choices=["json", "markdown"], default="markdown",
        help="Formato di output: markdown (default) o json."
    )
    args = parser.parse_args()

    percorso = Path(args.file)
    if not percorso.is_absolute():
        # Risolve relativo alla directory di lavoro corrente
        percorso = Path.cwd() / percorso

    risultato = analizza_file(percorso)

    if args.format == "json":
        print(formatta_json(risultato))
    else:
        print(formatta_markdown(risultato))

    # Codice di uscita non zero se bloccante
    if risultato["verdict"] == "BLOCCANTE":
        sys.exit(2)


if __name__ == "__main__":
    main()
