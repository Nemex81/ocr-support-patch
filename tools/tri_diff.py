"""
tri_diff.py — Confronta un file .gui nei tre repository (patch, OCR upstream,
vanilla CK3) e produce un report strutturato con le differenze categorizzate.

Uso:
    python tools/tri_diff.py --window <nome_finestra> [--output-file <percorso>]

Dipendenze: solo stdlib Python 3.8+
"""

import argparse
import difflib
import re
import sys
from datetime import datetime
from pathlib import Path

# Aggiunge la directory radice al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.config import PATCH_GUI, OCR_GUI, VANILLA_GUI


# ---------------------------------------------------------------------------
# Funzioni di utilità
# ---------------------------------------------------------------------------

def _leggi_file(percorso: Path) -> tuple[bool, list[str]]:
    """Legge il file se esiste, restituisce (esiste, righe)."""
    if not percorso.exists():
        return False, []
    with open(percorso, encoding="utf-8") as f:
        return True, f.readlines()


def _conta_righe(righe: list[str]) -> int:
    return len(righe)


# ---------------------------------------------------------------------------
# Sezione A — blocchi top-level del vanilla
# ---------------------------------------------------------------------------

# Cattura righe tipo: window = {, types NomeX_types {, template nome {
RE_TOPLEVEL = re.compile(
    r"^(window|types|template)\s*(?:=\s*\{|[\w_]+\s*(?::\s*\w+\s*)?\{)",
    re.IGNORECASE,
)
RE_WINDOW_NAME = re.compile(r'name\s*=\s*"([^"]+)"')


def _estrai_blocchi_toplevel(righe: list[str]) -> list[str]:
    """
    Estrae i blocchi di primo livello dal file vanilla.
    Ogni elemento è una stringa descrittiva come 'window = { name = "faith_window" }'.
    """
    blocchi = []
    i = 0
    while i < len(righe):
        riga = righe[i]
        if RE_TOPLEVEL.match(riga.strip()):
            # cerca name nelle prossime 5 righe
            nome = None
            for j in range(i, min(i + 5, len(righe))):
                m = RE_WINDOW_NAME.search(righe[j])
                if m:
                    nome = m.group(1)
                    break
            tipo = riga.strip().split()[0]
            if nome:
                blocchi.append(f"`{tipo} {{ name = \"{nome}\" }}`")
            else:
                blocchi.append(f"`{riga.strip()[:60]}`")
        i += 1
    return blocchi


# ---------------------------------------------------------------------------
# Sezione B — feature OCR mancanti nella patch
# ---------------------------------------------------------------------------

def _estrai_nomi_toplevel(righe: list[str]) -> set[str]:
    """Estrae i nomi dei widget di primo livello (window/types/template)."""
    nomi = set()
    for riga in righe:
        if RE_TOPLEVEL.match(riga.strip()):
            m = RE_WINDOW_NAME.search(riga)
            if m:
                nomi.add(m.group(1))
    return nomi


def _feature_ocr_mancanti(righe_ocr: list[str], righe_patch: list[str]) -> list[str]:
    """
    Confronta i blocchi top-level in OCR upstream vs patch.
    Restituisce i nomi presenti in OCR ma assenti nella patch.
    """
    nomi_ocr = _estrai_nomi_toplevel(righe_ocr)
    nomi_patch = _estrai_nomi_toplevel(righe_patch)
    return sorted(nomi_ocr - nomi_patch)


# ---------------------------------------------------------------------------
# Sezione C — diff container vanilla vs CK3 originale
# ---------------------------------------------------------------------------

RE_VANILLA_CONTAINER = re.compile(r'name\s*=\s*"vanilla_')
RE_VANILLA_ALT_NAME = re.compile(r'name\s*=\s*"(?:normal_mode|grafic_version)', re.IGNORECASE)
RE_VANILLA_BLOCK_HINT = re.compile(r'^\s*[\w_]+\s*=\s*\{', re.IGNORECASE)
RE_VISIBLE_VANILLA_EXISTS = re.compile(r'visible\s*=\s*"\[GetVariableSystem\.Exists\(\'ocr\'\)\]"')
RE_VISIBLE_VANILLA_SHORTHAND = re.compile(r'visible\s*=\s*"\[[^\]]*\bIs\(\'ocr\'\)[^\]]*\]"')
RE_USING_VANILLA = re.compile(r'using\s*=\s*vanilla\b', re.IGNORECASE)


def _is_vanilla_visibility(riga: str) -> bool:
    return bool(RE_VISIBLE_VANILLA_EXISTS.search(riga) or RE_VISIBLE_VANILLA_SHORTHAND.search(riga))


def _estrai_container_vanilla(righe: list[str]) -> list[str]:
    """
    Estrae le righe del blocco vanilla dalla patch.
    Strategia a tre livelli:
    1. Cerca blocco con name = 'vanilla_*' o name = 'normal_mode*' / 'grafic_version*'
    2. Fallback: cerca blocco con visible = Exists('ocr') — qualsiasi naming
    3. Se nessuno trovato: restituisce lista vuota (segnalato in _diff_container_vanilla)
    """
    profondita = 0
    for i, riga in enumerate(righe):
        if profondita != 1:
            profondita += riga.count("{") - riga.count("}")
            continue

        if not RE_VANILLA_BLOCK_HINT.match(riga):
            profondita += riga.count("{") - riga.count("}")
            continue

        fine = _trova_fine_blocco(righe, i)
        if fine <= i:
            profondita += riga.count("{") - riga.count("}")
            continue

        # Controlla l'intero blocco (non solo le prime 12 righe) per visibility
        blocco = righe[i:fine + 1]
        if any(_is_vanilla_visibility(r) for r in blocco):
            return blocco

        if RE_VANILLA_CONTAINER.search(riga) or RE_VANILLA_ALT_NAME.search(riga):
            return blocco

        profondita += riga.count("{") - riga.count("}")

    # Fallback: scansione completa del file per visible = Exists('ocr') —
    # cattura container vanilla con naming non standard
    profondita = 0
    for i, riga in enumerate(righe):
        profondita += riga.count("{") - riga.count("}")
        if _is_vanilla_visibility(riga) and profondita >= 1:
            # backtrack fino all'inizio del blocco che contiene questa riga
            for j in range(i - 1, max(i - 20, -1), -1):
                stripped = righe[j].strip()
                if RE_VANILLA_BLOCK_HINT.match(righe[j]) and stripped.endswith("{"):
                    fine = _trova_fine_blocco(righe, j)
                    if fine > j:
                        return righe[j:fine + 1]
                    break

    return []


def _is_template_vanilla_delegation(righe_container: list[str]) -> bool:
    """Rileva wrapper vanilla che delegano il contenuto a un template shared via `using = vanilla`."""
    if not righe_container:
        return False

    corpo_significativo = [
        r.strip() for r in righe_container[1:-1]
        if r.strip() and not r.strip().startswith("#")
    ]
    if not corpo_significativo:
        return False

    ha_using_vanilla = any(RE_USING_VANILLA.search(r) for r in corpo_significativo)
    ha_blocchi_annidati = any("{" in r for r in corpo_significativo)
    return ha_using_vanilla and not ha_blocchi_annidati


def _normalizza_container_vanilla(righe_container: list[str]) -> list[str]:
    """
    Rimuove il wrapper di dual-mode lasciando il contenuto vanilla confrontabile.
    Mantiene eventuali proprietà extra del wrapper come differenze reali.
    """
    if not righe_container:
        return []

    corpo = righe_container[1:-1]
    profondita = 0
    normalizzate = []
    for riga in corpo:
        stripped = riga.strip()
        if stripped.startswith("#"):
            continue

        if profondita == 0:
            if not stripped:
                continue
            if stripped.startswith("name = ") and (
                RE_VANILLA_CONTAINER.search(riga) or RE_VANILLA_ALT_NAME.search(riga)
            ):
                continue
            if _is_vanilla_visibility(riga):
                continue
            if "{" not in riga:
                continue

        normalizzate.append(riga)
        profondita += riga.count("{") - riga.count("}")

    return normalizzate


def _linee_significative(righe: list[str]) -> list[str]:
    return [r.strip() for r in righe if r.strip() and not r.strip().startswith("#")]


def _normalizza_per_diff(righe: list[str]) -> list[str]:
    """Ignora differenze di sola indentazione o righe vuote nel confronto."""
    linee = [r.strip() for r in righe if r.strip() and not r.strip().startswith("#")]
    canonicali = []
    for linea in linee:
        if linea == "{" and canonicali:
            canonicali[-1] = canonicali[-1].rstrip("\n") + " {\n"
            continue
        canonicali.append(f"{linea}\n")
    return canonicali


def _ritaglia_vanilla_riferimento(righe_vanilla: list[str], contenuto_patch: list[str]) -> list[str]:
    """
    Se il dual-mode duplica solo un ramo interno della window, allinea il confronto
    al primo anchor significativo condiviso invece di usare sempre l'intero file.
    """
    patch_significative = _linee_significative(contenuto_patch)
    if not patch_significative:
        return righe_vanilla

    primo_anchor = patch_significative[0]
    for indice, riga in enumerate(righe_vanilla):
        if riga.strip() == primo_anchor:
            return righe_vanilla[indice:]

    return righe_vanilla


def _trova_fine_blocco(righe: list[str], inizio: int) -> int:
    """Trova la riga di chiusura del blocco (bilanciamento {})."""
    profondita = 0
    for i in range(inizio, len(righe)):
        profondita += righe[i].count("{") - righe[i].count("}")
        if profondita <= 0:
            return i
    return len(righe) - 1


def _diff_container_vanilla(righe_patch: list[str], righe_vanilla: list[str], window_name: str) -> list[str]:
    """
    Confronta il container vanilla della patch con il file vanilla originale.
    Restituisce le righe del diff unificato, oppure messaggio di parità.
    """
    container = _estrai_container_vanilla(righe_patch)
    if not container:
        return [
            "[AVVERTENZA] CONTAINER VANILLA NON TROVATO nella patch.",
            "Possibili cause:",
            "  1. Il file patch non ha ancora il dual-mode (da convertire)",
            "  2. Il container vanilla usa un naming non standard — verifica visible",
            "  3. Il blocco vanilla non contiene la proprieta' visible corretta",
        ]

    if _is_template_vanilla_delegation(container):
        return ["Nessuna discrepanza automatica: ramo vanilla delegato tramite template `vanilla`."]

    contenuto_vanilla_patch = _normalizza_container_vanilla(container)
    righe_vanilla_riferimento = _ritaglia_vanilla_riferimento(righe_vanilla, contenuto_vanilla_patch)

    vanilla_normalizzato = _normalizza_per_diff(righe_vanilla_riferimento)
    patch_normalizzato = _normalizza_per_diff(contenuto_vanilla_patch)
    if len(vanilla_normalizzato) > len(patch_normalizzato):
        vanilla_normalizzato = vanilla_normalizzato[:len(patch_normalizzato)]

    diff = list(difflib.unified_diff(
        vanilla_normalizzato,
        patch_normalizzato,
        fromfile=f"{window_name}.gui (vanilla CK3)",
        tofile=f"{window_name}.gui (patch — container vanilla)",
        lineterm="",
        n=3,
    ))
    if not diff:
        return ["Nessuna discrepanza. Container vanilla identico al CK3 originale. OK"]
    return diff


# ---------------------------------------------------------------------------
# Costruzione report
# ---------------------------------------------------------------------------

def _verdetto(ha_discrepanze_c: bool, mancanti_b: list[str]) -> str:
    if mancanti_b and ha_discrepanze_c:
        return "DISCREPANZE CRITICHE"
    if mancanti_b or ha_discrepanze_c:
        return "DISCREPANZE MINORI"
    return "ALLINEATO"


def genera_report(window_name: str) -> str:
    """Genera il report completo per la finestra indicata."""
    path_patch = PATCH_GUI / f"{window_name}.gui"
    path_ocr = OCR_GUI / f"{window_name}.gui"
    path_vanilla = VANILLA_GUI / f"{window_name}.gui"

    esiste_patch, righe_patch = _leggi_file(path_patch)
    esiste_ocr, righe_ocr = _leggi_file(path_ocr)
    esiste_vanilla, righe_vanilla = _leggi_file(path_vanilla)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    righe_report: list[str] = [
        f"# Tri-Repo Diff: {window_name}.gui",
        f"Generato: {timestamp}",
        "",
    ]

    # --- Sezione A ---
    righe_report.append("## A — Struttura Vanilla Originale (blocchi top-level)")
    if not esiste_vanilla:
        righe_report.append(f"File vanilla non trovato: {path_vanilla}")
    else:
        blocchi = _estrai_blocchi_toplevel(righe_vanilla)
        if blocchi:
            for b in blocchi:
                stato_patch = "PRESENTE" if esiste_patch else "—"
                righe_report.append(f"- {b} — {stato_patch}")
        else:
            righe_report.append("Nessun blocco top-level rilevato nel vanilla.")
    righe_report.append("")

    # --- Sezione B ---
    righe_report.append("## B — Feature OCR Upstream non presenti nella Patch")
    if not esiste_ocr:
        righe_report.append(f"File OCR upstream non trovato: {path_ocr}")
    elif not esiste_patch:
        righe_report.append(f"File patch non trovato: {path_patch}")
    else:
        mancanti = _feature_ocr_mancanti(righe_ocr, righe_patch)
        if mancanti:
            for m in mancanti:
                righe_report.append(f"- `{m}` — presente in OCR upstream, assente nella patch")
        else:
            righe_report.append("Nessuna feature mancante rilevata. ✅")
    righe_report.append("")

    # --- Sezione C ---
    righe_report.append("## C — Discrepanze Container Vanilla vs CK3 Originale")
    ha_discrepanze = False
    if not esiste_vanilla:
        righe_report.append("File vanilla non disponibile — confronto impossibile.")
    elif not esiste_patch:
        righe_report.append("File patch non disponibile — confronto impossibile.")
    else:
        diff_lines = _diff_container_vanilla(righe_patch, righe_vanilla, window_name)
        ha_discrepanze = not any("identico" in l or l.startswith("Nessuna") for l in diff_lines)
        if ha_discrepanze:
            righe_report.append("```diff")
            righe_report.extend(l.rstrip() for l in diff_lines[:80])  # limita output a 80 righe
            if len(diff_lines) > 80:
                righe_report.append(f"... ({len(diff_lines) - 80} righe aggiuntive omesse)")
            righe_report.append("```")
        else:
            righe_report.extend(diff_lines)
    righe_report.append("")

    # --- Sezione D ---
    righe_report.append("## D — Stato Generale")
    righe_report.append("")
    righe_report.append("| File | Esiste | Righe |")
    righe_report.append("|------|--------|-------|")
    righe_report.append(f"| Patch | {'✅' if esiste_patch else '❌'} | {_conta_righe(righe_patch)} |")
    righe_report.append(f"| OCR Upstream | {'✅' if esiste_ocr else '❌'} | {_conta_righe(righe_ocr)} |")
    righe_report.append(f"| Vanilla | {'✅' if esiste_vanilla else '❌'} | {_conta_righe(righe_vanilla)} |")
    righe_report.append("")

    mancanti_b = _feature_ocr_mancanti(righe_ocr, righe_patch) if (esiste_ocr and esiste_patch) else []
    verdetto = _verdetto(ha_discrepanze, mancanti_b)
    righe_report.append(f"**Verdetto**: {verdetto}")

    return "\n".join(righe_report)


# ---------------------------------------------------------------------------
# Analisi strutturata per integrazione in audit.py
# ---------------------------------------------------------------------------

def analizza_fedelta(percorso: Path) -> dict:
    """
    Analisi strutturata di fedelta' tri-repo per un file .gui nella patch.
    Usata da audit.py come pass aggiuntivo sul gate automatico.

    Verdetto (advisory — non blocca il gate nella v1):
        ALLINEATO          — nessuna discrepanza e nessuna feature OCR mancante
        DISCREPANZE_MINORI — alcune discrepanze o pochi feature mancanti (<= 3)
        DISCREPANZE        — molte feature mancanti o discrepanze rilevanti
        SKIP               — file patch non trovato
    """
    window_name = percorso.stem
    esiste_patch, righe_patch = _leggi_file(percorso)
    esiste_vanilla, righe_vanilla = _leggi_file(VANILLA_GUI / f"{window_name}.gui")
    esiste_ocr, righe_ocr = _leggi_file(OCR_GUI / f"{window_name}.gui")

    if not esiste_patch:
        return {
            "verdetto": "SKIP",
            "feature_ocr_mancanti": [],
            "ha_discrepanze_vanilla": False,
            "righe_diff": [],
            "esiste_vanilla": False,
            "esiste_ocr": False,
        }

    feature_mancanti: list = []
    if esiste_ocr:
        feature_mancanti = _feature_ocr_mancanti(righe_ocr, righe_patch)

    ha_discrepanze = False
    righe_diff: list = []
    if esiste_vanilla:
        diff_lines = _diff_container_vanilla(righe_patch, righe_vanilla, window_name)
        ha_discrepanze = not any(
            "identico" in l.lower() or l.startswith("Nessuna")
            for l in diff_lines
        )
        if ha_discrepanze:
            righe_diff = diff_lines[:30]

    if len(feature_mancanti) > 3 or (ha_discrepanze and feature_mancanti):
        verdetto = "DISCREPANZE"
    elif feature_mancanti or ha_discrepanze:
        verdetto = "DISCREPANZE_MINORI"
    else:
        verdetto = "ALLINEATO"

    return {
        "verdetto": verdetto,
        "feature_ocr_mancanti": feature_mancanti,
        "ha_discrepanze_vanilla": ha_discrepanze,
        "righe_diff": righe_diff,
        "esiste_vanilla": esiste_vanilla,
        "esiste_ocr": esiste_ocr,
    }


# ---------------------------------------------------------------------------
# Entry point CLI
# ---------------------------------------------------------------------------

def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Confronta un file .gui nei tre repository (patch, OCR upstream, vanilla)."
    )
    parser.add_argument(
        "--window", required=True,
        help="Nome della finestra senza estensione (es: window_faith)."
    )
    parser.add_argument(
        "--output-file", default=None,
        help="Se fornito, salva il report su file invece che su stdout."
    )
    args = parser.parse_args()

    report = genera_report(args.window)

    if args.output_file:
        out_path = Path(args.output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report salvato in: {out_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
