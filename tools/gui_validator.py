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

# Pattern di visibilità invertita: rilevati con analisi multi-riga (vedi sotto)
# Qui solo i regex usati nella logica dedicata.
RE_OCR_NAME = re.compile(r'name\s*=\s*"ocr_', re.IGNORECASE)
RE_VANILLA_NAME = re.compile(r'name\s*=\s*"vanilla_', re.IGNORECASE)
RE_VISIBLE_VANILLA = re.compile(r'visible\s*=\s*"\[GetVariableSystem\.Exists\(\'ocr\'\)\]"')
RE_VISIBLE_OCR = re.compile(r'visible\s*=\s*"\[Not\(GetVariableSystem\.Exists\(\'ocr\'\)\)\]"')

# Regex per analisi blocchi (icon/button senza tooltip, fontsize OCR)
RE_BLOCK_OPEN = re.compile(r'^\s*(icon|button|button_standard|button_primary|button_icon)\s*=\s*\{', re.IGNORECASE)
RE_TOOLTIP = re.compile(r'\btooltip\s*=')
RE_FONTSIZE = re.compile(r'\bfontsize\s*=\s*(\d+)')
RE_TEXT_WIDGET = re.compile(r'\b(text_single|text_multi|text_label)\s*=\s*\{', re.IGNORECASE)
RE_OCR_CONTAINER = re.compile(r'name\s*=\s*"ocr_')


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


def _scansione_semplice(righe: list[str]) -> list[dict]:
    """Applica i SIMPLE_PATTERNS riga per riga."""
    problemi = []
    compilati = [(re.compile(p["regex"], re.IGNORECASE), p) for p in SIMPLE_PATTERNS]
    for num, riga in enumerate(righe, start=1):
        for pattern_re, p in compilati:
            if pattern_re.search(riga):
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
    in_ocr_contesto = False  # traccia se siamo dentro un container ocr_

    # Stack per nome container corrente (semplificato: nomi trovati sull'ultima riga di apertura)
    for i, riga in enumerate(righe):
        num_riga = i + 1

        # Aggiorna il contesto OCR
        if RE_OCR_CONTAINER.search(riga):
            in_ocr_contesto = True
        # Uscita da contesto OCR su chiusura di livello elevato (euristica: riga sola "}")
        if riga.strip() == "}" and in_ocr_contesto:
            in_ocr_contesto = False

        # --- Visibilità invertita ---
        if RE_OCR_NAME.search(riga):
            # cerca visible nelle prossime 10 righe
            finestra = righe[i:i + 10]
            for riga_f in finestra:
                if RE_VISIBLE_VANILLA.search(riga_f):
                    problemi.append({
                        "line": num_riga,
                        "pattern": "Container ocr_* con visibility vanilla (invertita)",
                        "category": "VISIBILITA",
                        "severity": "CRITICO",
                        "fix": "Usare visible = \"[Not(GetVariableSystem.Exists('ocr'))]\" per container ocr_*",
                    })
                    break

        if RE_VANILLA_NAME.search(riga):
            finestra = righe[i:i + 10]
            for riga_f in finestra:
                if RE_VISIBLE_OCR.search(riga_f):
                    problemi.append({
                        "line": num_riga,
                        "pattern": "Container vanilla_* con visibility OCR (invertita)",
                        "category": "VISIBILITA",
                        "severity": "CRITICO",
                        "fix": "Usare visible = \"[GetVariableSystem.Exists('ocr')]\" per container vanilla_*",
                    })
                    break

        # --- icon/button senza tooltip ---
        if RE_BLOCK_OPEN.match(riga):
            fine = _trova_fine_blocco(righe, i)
            if fine == -1:
                fine = min(i + 15, len(righe) - 1)
            blocco = righe[i:fine + 1]
            ha_tooltip = any(RE_TOOLTIP.search(r) for r in blocco)
            if not ha_tooltip:
                tipo_widget = RE_BLOCK_OPEN.match(riga).group(1).lower()
                problemi.append({
                    "line": num_riga,
                    "pattern": f"{tipo_widget} senza tooltip",
                    "category": "STRUTTURALE",
                    "severity": "CRITICO",
                    "fix": f"Aggiungere tooltip descrittivo al {tipo_widget} (obbligatorio per accessibilità OCR)",
                })

        # --- fontsize < 18 in contesto OCR ---
        if in_ocr_contesto and RE_TEXT_WIDGET.match(riga):
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


def analizza_file(percorso: Path) -> dict:
    """
    Analisi completa di un file .gui.
    Restituisce un dict con: file, verdict, critical_count, warning_count, issues.
    """
    righe = _apri_file(percorso)
    problemi = _scansione_semplice(righe) + _scansione_blocchi(righe)

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
    return "🔴 CRITICO" if severity == "CRITICO" else "🟡 ATTENZIONE"


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
