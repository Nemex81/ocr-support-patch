"""
scope_extractor.py — Estrae tutti i binding Jomini da un file .gui,
confronta con jomini_scope_whitelist.md e produce le righe pronte
da aggiungere per i binding assenti.

Uso:
    python tools/scope_extractor.py --file <percorso_gui> [--format json|markdown]

Dipendenze: solo stdlib Python 3.8+
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Aggiunge la directory radice al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.config import WHITELIST_PATH


# ---------------------------------------------------------------------------
# Regex di estrazione
# ---------------------------------------------------------------------------

# Tutto ciò che sta tra [ e ] (non annidato)
RE_BINDING = re.compile(r"\[([^\[\]]+)\]")

# Prefissi validi di scope/funzione Jomini
PREFISSI_VALIDI = (
    "Get", "Has", "Is", "Can", "Not", "And", "Or",
    "EqualTo", "NotEqualTo", "GreaterThan", "LessThan",
    "Select", "Add", "Make", "Scope",
)

# Operatori logici contenitore: estrarne i sottocontenuti invece
RE_CONTENITORI = re.compile(
    r"^(Not|And|Or)\s*\((.+)\)\s*$", re.IGNORECASE | re.DOTALL
)


def _normalizza_binding(raw: str) -> str | None:
    """
    Dato un testo grezzo estratto da [...], restituisce il nome del binding
    normalizzato (senza argomenti), oppure None se non è un riferimento a scope.
    Esempi:
        "GetPlayer.GetTrait('perk')" → "GetPlayer.GetTrait"
        "Not(GetVariableSystem.Exists('ocr'))" → None (è un contenitore)
        "1" → None (numerico)
        "GetFaith.GetFervor|=+2" → "GetFaith.GetFervor"
    """
    raw = raw.strip()

    # Scarta contenitori logici (Not, And, Or)
    if RE_CONTENITORI.match(raw):
        return None

    # Scarta se non contiene un punto (non è un riferimento scope)
    if "." not in raw:
        return None

    # Rimuove argomenti: prende solo la parte fino alla prima '(' o '|'
    base = re.split(r"[|(]", raw)[0].strip()

    # Scarta se non inizia con un prefisso valido
    if not any(base.startswith(p) for p in PREFISSI_VALIDI):
        return None

    # Scarta se contiene spazi interni (non è un binding semplice)
    if " " in base:
        return None

    return base


def estrai_binding(percorso: Path) -> set[str]:
    """
    Estrae tutti i binding unici e normalizzati da un file .gui.
    """
    if not percorso.exists():
        print(f"ERRORE: file non trovato: {percorso}", file=sys.stderr)
        sys.exit(1)

    with open(percorso, encoding="utf-8") as f:
        testo = f.read()

    trovati: set[str] = set()
    for match in RE_BINDING.finditer(testo):
        raw = match.group(1)
        normalizzato = _normalizza_binding(raw)
        if normalizzato:
            trovati.add(normalizzato)
    return trovati


# ---------------------------------------------------------------------------
# Caricamento whitelist
# ---------------------------------------------------------------------------

RE_WHITELIST_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|")


def carica_whitelist() -> set[str]:
    """
    Legge jomini_scope_whitelist.md e restituisce il set dei binding presenti.
    """
    if not WHITELIST_PATH.exists():
        print(f"ERRORE: whitelist non trovata: {WHITELIST_PATH}", file=sys.stderr)
        sys.exit(1)

    presenti: set[str] = set()
    with open(WHITELIST_PATH, encoding="utf-8") as f:
        for riga in f:
            m = RE_WHITELIST_ROW.match(riga)
            if m:
                presenti.add(m.group(1).strip())
    return presenti


# ---------------------------------------------------------------------------
# Classificazione
# ---------------------------------------------------------------------------

def _classifica_binding(binding: str, whitelist: set[str]) -> str:
    """Restituisce PRESENTE, ASSENTE o DA VERIFICARE."""
    if binding in whitelist:
        return "PRESENTE"
    # DA VERIFICARE: scope non standard (prefisso non riconosciuto Jomini)
    prefissi_standard = ("Get", "Has", "Is", "Can", "Not", "And", "Or",
                         "EqualTo", "NotEqualTo", "GreaterThan", "LessThan",
                         "Select", "Add", "Make", "Scope", "CFixed")
    if not any(binding.startswith(p) for p in prefissi_standard):
        return "DA VERIFICARE"
    return "ASSENTE"


def classifica_tutti(binding_set: set[str], whitelist: set[str], contesto: str) -> list[dict]:
    """
    Classifica ogni binding e prepara la lista ordinata di risultati.
    """
    risultati = []
    for b in sorted(binding_set):
        stato = _classifica_binding(b, whitelist)
        riga_whitelist = (
            f"| `{b}` | {contesto} | verificato in vanilla CK3 1.17.1 |"
            if stato == "ASSENTE" else ""
        )
        risultati.append({
            "binding": b,
            "stato": stato,
            "riga_whitelist": riga_whitelist,
        })
    return risultati


# ---------------------------------------------------------------------------
# Formattazione output
# ---------------------------------------------------------------------------

def formatta_markdown(nome_file: str, risultati: list[dict], contesto: str) -> str:
    presenti = [r for r in risultati if r["stato"] == "PRESENTE"]
    assenti = [r for r in risultati if r["stato"] == "ASSENTE"]
    da_verificare = [r for r in risultati if r["stato"] == "DA VERIFICARE"]

    righe = [
        f"## Estrazione Binding: {nome_file}",
        "",
        "| Binding | Stato | Note |",
        "|---------|-------|------|",
    ]
    icone = {"PRESENTE": "✅ PRESENTE", "ASSENTE": "❌ ASSENTE", "DA VERIFICARE": "⚠️ DA VERIFICARE"}
    note = {"PRESENTE": "—", "ASSENTE": "Aggiungere alla whitelist", "DA VERIFICARE": "Verifica manuale nel vanilla"}
    for r in risultati:
        righe.append(f"| `{r['binding']}` | {icone[r['stato']]} | {note[r['stato']]} |")

    if assenti:
        righe += [
            "",
            "### Righe pronte per jomini_scope_whitelist.md",
            "",
        ]
        for r in assenti:
            righe.append(r["riga_whitelist"])

    righe += [
        "",
        f"**Riepilogo**: PRESENTI: {len(presenti)} | ASSENTI: {len(assenti)} | DA VERIFICARE: {len(da_verificare)}",
    ]
    return "\n".join(righe)


def formatta_json(nome_file: str, risultati: list[dict]) -> str:
    assenti = [r["riga_whitelist"] for r in risultati if r["stato"] == "ASSENTE"]
    return json.dumps({
        "file": nome_file,
        "bindings": risultati,
        "righe_whitelist_pronte": assenti,
        "riepilogo": {
            "presenti": sum(1 for r in risultati if r["stato"] == "PRESENTE"),
            "assenti": sum(1 for r in risultati if r["stato"] == "ASSENTE"),
            "da_verificare": sum(1 for r in risultati if r["stato"] == "DA VERIFICARE"),
        },
    }, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Entry point CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estrae i binding Jomini da un file .gui e li confronta con la whitelist."
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
        percorso = Path.cwd() / percorso

    contesto = percorso.name
    binding_estratti = estrai_binding(percorso)
    whitelist = carica_whitelist()
    risultati = classifica_tutti(binding_estratti, whitelist, contesto)

    if args.format == "json":
        print(formatta_json(percorso.name, risultati))
    else:
        print(formatta_markdown(percorso.name, risultati, contesto))

    # Codice di uscita 1 se ci sono binding DA VERIFICARE
    if any(r["stato"] == "DA VERIFICARE" for r in risultati):
        sys.exit(1)


if __name__ == "__main__":
    main()
