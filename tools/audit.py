"""
audit.py — Orchestratore audit completo. Chiama gui_validator e scope_extractor
su uno o tutti i file .gui modificati o presenti nella patch.
Opzionalmente aggiorna SKILLS_AUDIT_REPORT.md con i risultati.

Uso:
    python tools/audit.py [--all] [--window <nome>] [--update-report]

Dipendenze: solo stdlib Python 3.8+
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Aggiunge la directory radice al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import re as _re
from tools.config import PATCH_GUI, PATCH_ROOT, VANILLA_TYPES_GUI
from tools.gui_validator import analizza_file as _valida
from tools.scope_extractor import (
    estrai_binding, carica_whitelist, classifica_tutti
)
from tools.tri_diff import analizza_fedelta as _analizza_fedelta

REPORT_PATH = PATCH_ROOT / "SKILLS_AUDIT_REPORT.md"

# Regex per rilevare l'istanziazione v1.1 nel wrapper (es: army_patch_vanilla = {)
_RE_TYPE_INST_IN_WRAPPER = _re.compile(r'^\s*(\w+)_patch_vanilla\s*=\s*\{', _re.MULTILINE)


# ---------------------------------------------------------------------------
# Selezione file da analizzare
# ---------------------------------------------------------------------------

def _file_da_git_diff() -> list[Path]:
    """
    Restituisce i file .gui modificati rispetto all'HEAD via git diff.
    Se git non è disponibile o non ci sono diff, restituisce lista vuota.
    """
    try:
        risultato = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True,
            cwd=str(PATCH_ROOT), timeout=10,
        )
        righe = risultato.stdout.splitlines()
        return [
            PATCH_ROOT / r for r in righe
            if r.endswith(".gui") and "ocr_support_compatibility_pach/gui/" in r
        ]
    except Exception:
        return []


def _seleziona_file(tutti: bool, window: str | None) -> list[Path]:
    """Seleziona i file da analizzare in base ai parametri CLI."""
    if tutti:
        file_wrapper = sorted(PATCH_GUI.glob("*.gui"))
        file_type = sorted(VANILLA_TYPES_GUI.glob("*.gui")) if VANILLA_TYPES_GUI.exists() else []
        return file_wrapper + file_type
    if window:
        percorso = PATCH_GUI / f"{window}.gui"
        if not percorso.exists():
            print(f"ERRORE: file non trovato: {percorso}", file=sys.stderr)
            sys.exit(1)
        return [percorso]
    # Default: file modificati via git diff
    da_diff = _file_da_git_diff()
    if da_diff:
        return da_diff
    print(
        "Nessun file .gui modificato rilevato da git diff. "
        "Usa --all per analizzare tutti i file o --window <nome> per uno specifico.",
        file=sys.stderr,
    )
    sys.exit(0)


# ---------------------------------------------------------------------------
# Analisi singolo file

def _trova_file_type_associato(percorso_wrapper: Path) -> Path | None:
    """
    Controlla se il wrapper usa il pattern v1.1 (*_patch_vanilla = {}) e
    restituisce il Path atteso del file type in gui/vanilla/.
    Restituisce None se il wrapper non usa il pattern v1.1.
    """
    try:
        contenuto = percorso_wrapper.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    m = _RE_TYPE_INST_IN_WRAPPER.search(contenuto)
    if not m:
        return None
    prefix = m.group(1)
    return VANILLA_TYPES_GUI / f"{prefix}_patch_vanilla.gui"

# ---------------------------------------------------------------------------

def _analizza_singolo(percorso: Path) -> dict:
    """
    Esegue validator e scope_extractor su un file.
    Restituisce un dict riepilogativo.
    """
    # Validazione pattern
    risultato_val = _valida(percorso)

    # Estrazione binding
    whitelist = carica_whitelist()
    binding_estratti = estrai_binding(percorso)
    risultati_scope = classifica_tutti(binding_estratti, whitelist, percorso.name)
    assenti = [r for r in risultati_scope if r["stato"] == "ASSENTE"]
    da_verificare = [r for r in risultati_scope if r["stato"] == "DA VERIFICARE"]

    # Analisi fedelta' tri-repo (advisory — non modifica il gate nella v1)
    risultato_fedelta = _analizza_fedelta(percorso)

    # Stato complessivo (la fedelta' vanilla e' advisory nella v1)
    if risultato_val["verdict"] == "BLOCCANTE" or da_verificare:
        stato = "BLOCCANTE"
    elif risultato_val["verdict"] == "CON AVVERTENZE" or assenti:
        stato = "CON AVVERTENZE"
    else:
        stato = "OK"

    # Pattern v1.1: rilevamento e audit del file type associato
    tipo_file = _trova_file_type_associato(percorso)
    risultato_val_type = None
    tipo_avviso = None
    if tipo_file is not None:
        if tipo_file.exists():
            risultato_val_type = _valida(tipo_file)
            if risultato_val_type["verdict"] == "BLOCCANTE":
                stato = "BLOCCANTE"
            elif risultato_val_type["verdict"] == "CON AVVERTENZE" and stato == "OK":
                stato = "CON AVVERTENZE"
        else:
            tipo_avviso = (
                f"ATTENZIONE: file vanilla type atteso non trovato: "
                f"gui/vanilla/{tipo_file.name}"
            )
            if stato == "OK":
                stato = "CON AVVERTENZE"

    return {
        "file": percorso.name,
        "verdetto_validator": risultato_val["verdict"],
        "critici": risultato_val["critical_count"],
        "avvertenze": risultato_val["warning_count"],
        "binding_assenti": len(assenti),
        "binding_da_verificare": len(da_verificare),
        "fedelta_verdetto": risultato_fedelta["verdetto"],
        "fedelta_feature_mancanti": len(risultato_fedelta["feature_ocr_mancanti"]),
        "stato_complessivo": stato,
        "dettaglio_validator": risultato_val["issues"],
        "dettaglio_assenti": [r["riga_whitelist"] for r in assenti],
        "dettaglio_fedelta": risultato_fedelta,
        # Campi v1.1 — None se il wrapper non usa il pattern type-separated
        "type_file": tipo_file.name if tipo_file else None,
        "type_file_trovato": tipo_file.exists() if tipo_file else None,
        "type_avviso": tipo_avviso,
        "verdetto_validator_type": risultato_val_type["verdict"] if risultato_val_type else None,
        "critici_type": risultato_val_type["critical_count"] if risultato_val_type else 0,
        "avvertenze_type": risultato_val_type["warning_count"] if risultato_val_type else 0,
        "dettaglio_validator_type": risultato_val_type["issues"] if risultato_val_type else [],
    }


# ---------------------------------------------------------------------------
# Formattazione output
# ---------------------------------------------------------------------------

def _formatta_tabella(risultati: list[dict]) -> str:
    """Tabella riepilogativa Markdown."""
    righe = [
        "| File | Validator | Critici | Avvertenze | Binding assenti | Fedelta' | Stato |",
        "|------|-----------|---------|------------|-----------------|----------|-------|"  ,
    ]
    icone = {"OK": "[OK]", "CON AVVERTENZE": "[AVVERTENZE]", "BLOCCANTE": "[BLOCCANTE]"}
    icone_fed = {
        "ALLINEATO": "[OK]",
        "DISCREPANZE_MINORI": "[MINOR]",
        "DISCREPANZE": "[DIFF]",
        "SKIP": "[--]",
    }
    for r in risultati:
        fed = r.get("fedelta_verdetto", "--")
        righe.append(
            f"| {r['file']} | {r['verdetto_validator']} | {r['critici']} | "
            f"{r['avvertenze']} | {r['binding_assenti']} | "
            f"{icone_fed.get(fed, fed)} | {icone.get(r['stato_complessivo'], r['stato_complessivo'])} |"
        )
    return "\n".join(righe)


def _formatta_report_completo(risultati: list[dict]) -> str:
    """Report completo con tabella riepilogativa e dettagli per file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sezioni = [
        f"## Audit OCR Support Patch — {timestamp}",
        "",
        "### Riepilogo",
        "",
        _formatta_tabella(risultati),
        "",
    ]

    for r in risultati:
        sezioni.append(f"### Dettaglio: {r['file']}")
        sezioni.append("")
        if r["dettaglio_validator"]:
            sezioni.append("**Problemi rilevati dal validator:**")
            for issue in r["dettaglio_validator"]:
                icona = "[CRITICO]" if issue["severity"] == "CRITICO" else "[ATTENZIONE]"
                sezioni.append(f"- {icona} Riga {issue['line']}: {issue['pattern']} — {issue['fix']}")
        else:
            sezioni.append("Nessun problema dal validator.")
        if r["dettaglio_assenti"]:
            sezioni.append("")
            sezioni.append("**Binding assenti dalla whitelist (righe pronte):**")
            for riga in r["dettaglio_assenti"]:
                sezioni.append(riga)
        # Dettagli file type v1.1
        if r.get("type_file"):
            sezioni.append("")
            sezioni.append(f"**File type v1.1 associato:** `{r['type_file']}`")
            if r.get("type_avviso"):
                sezioni.append(f"- [ATTENZIONE] {r['type_avviso']}")
            elif r.get("dettaglio_validator_type"):
                sezioni.append("**Problemi nel file type:**")
                for issue in r["dettaglio_validator_type"]:
                    icona = "[CRITICO]" if issue["severity"] == "CRITICO" else "[ATTENZIONE]"
                    sezioni.append(f"- {icona} Riga {issue['line']}: {issue['pattern']} — {issue['fix']}")
            else:
                sezioni.append("File type: nessun problema rilevato.")
        sezioni.append("")

    return "\n".join(sezioni)


# ---------------------------------------------------------------------------
# Entry point CLI
# ---------------------------------------------------------------------------

def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Audit completo OCR Support Patch: validator + scope extractor su file .gui."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--all", action="store_true",
        help="Analizza tutti i file .gui nella patch."
    )
    group.add_argument(
        "--window",
        help="Analizza solo il file specificato (nome senza estensione)."
    )
    parser.add_argument(
        "--update-report", action="store_true",
        help=f"Aggiorna {REPORT_PATH.name} con i risultati di questa esecuzione."
    )
    args = parser.parse_args()

    file_da_analizzare = _seleziona_file(args.all, args.window)
    print(f"File da analizzare: {len(file_da_analizzare)}")

    risultati = []
    for percorso in file_da_analizzare:
        print(f"  Analisi: {percorso.name} ... ", end="", flush=True)
        r = _analizza_singolo(percorso)
        risultati.append(r)
        print(r["stato_complessivo"])

    # Output tabella su stdout
    print()
    print(_formatta_tabella(risultati))

    # Aggiorna report se richiesto
    if args.update_report:
        nuova_sezione = _formatta_report_completo(risultati)
        if REPORT_PATH.exists():
            with open(REPORT_PATH, encoding="utf-8") as f:
                contenuto_esistente = f.read()
            nuovo_contenuto = nuova_sezione + "\n\n---\n\n" + contenuto_esistente
        else:
            nuovo_contenuto = nuova_sezione
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write(nuovo_contenuto)
        print(f"\nReport aggiornato: {REPORT_PATH}")

    # Codice di uscita non zero se almeno un file è BLOCCANTE
    if any(r["stato_complessivo"] == "BLOCCANTE" for r in risultati):
        sys.exit(2)


if __name__ == "__main__":
    main()
