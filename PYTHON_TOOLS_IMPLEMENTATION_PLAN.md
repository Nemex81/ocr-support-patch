# Piano Implementazione — Script Python per Framework OCR Support Patch

> **Documento per Copilot — istruzioni operative complete**
> Data: 2026-03-11
> Scopo: implementare 4 script Python nella cartella `tools/` integrati
> con agenti, skills, prompt e risorse già esistenti nel framework.
> Priorità: compatibilità CK3 1.17.1 e zero dipendenze esterne.

---

## Contesto e Obiettivo

Il framework attuale è composto da:
- 6 agenti specializzati in `.github/agents/`
- 6 skills procedurali in `.github/copilot-skills/`
- 6 prompt riutilizzabili in `.github/prompts/`
- 3 risorse dati in `.github/resources/`
- Istruzioni globali in `.github/copilot-instructions.md`

Il problema strutturale attuale: le skills eseguono compiti meccanici
(scan pattern, confronto file, estrazione binding) affidandosi all'LLM
per operazioni che sono deterministiche al 100%. Questo comporta:
- Consumo elevato di contesto su file grandi (window_council: 119KB, window_faith: 57KB)
- Risultati variabili tra sessioni diverse
- Nessuna esecuzione offline o automatica

**Soluzione**: 4 script Python in `tools/` che svolgono il lavoro meccanico
e producono output strutturato che le skills e gli agenti consumano come
contesto già elaborato. Gli script NON sostituiscono le skills — le potenziano.

**Principio architetturale**:
```
Script Python (deterministico, offline, stdlib pura)
        ↓ produce JSON/Markdown strutturato
Skill Copilot (legge output, interpreta, decide)
        ↓ delega
Agente Copilot (agisce sul file .gui)
```

---

## Regole Generali per Copilot

1. **Zero dipendenze esterne** — usare SOLO stdlib Python 3.8+:
   `pathlib`, `re`, `argparse`, `json`, `difflib`, `subprocess`, `sys`, `os`
   NON usare: `lxml`, `beautifulsoup4`, `click`, `pydantic`, o qualunque package PyPI
2. **Tutti gli script devono girare da riga di comando** con `argparse`
3. **Output sempre su stdout** in formato leggibile da Copilot (JSON o Markdown)
4. **I path dei tre repo** si leggono da `config.py` — non hardcodarli negli script
5. **Encoding UTF-8** esplicito su ogni `open()` — i file .gui usano UTF-8
6. **Gestione errori esplicita**: se un file non esiste, stampare messaggio chiaro su stderr e uscire con codice 1
7. **Commenti in italiano** — il modder è italofono e usa screen reader

---

## Fase 1 — `tools/config.py`

**File da creare**: `tools/config.py`

### Scopo
Centralizza i path assoluti dei tre repository. Tutti gli altri script lo importano.
I path rispecchiano la struttura del workspace definita in `ck3_modding.code-workspace`
e documentata in `.github/copilot-instructions.md`.

### Contenuto da implementare

```python
"""
config.py — Path centralizzati per i tre repository OCR Support Patch.
Tutti gli script in tools/ importano da qui. Non hardcodare path altrove.
"""

from pathlib import Path

# Root del workspace (directory padre che contiene tutti e tre i repo)
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent

# Repository 1 — Patch attiva (questo repo)
PATCH_ROOT = Path(__file__).resolve().parent.parent
PATCH_GUI = PATCH_ROOT / "ocr_support_compatibility_pach" / "gui"

# Repository 2 — OCR upstream (Agamidae)
OCR_ROOT = WORKSPACE_ROOT / "CK3-OCR"
OCR_GUI = OCR_ROOT / "OCR-Support" / "gui"

# Repository 3 — Vanilla CK3 1.17.1 (nota: il path usa spazi, NON trattini)
VANILLA_ROOT = WORKSPACE_ROOT / "CK3 ORIGINAL VERSION"
VANILLA_GUI = VANILLA_ROOT / "ck3origin" / "game" / "gui"

# Risorse framework
WHITELIST_PATH = PATCH_ROOT / ".github" / "resources" / "jomini_scope_whitelist.md"
RESOURCES_PATH = PATCH_ROOT / ".github" / "resources"
```

### Test di verifica post-implementazione
Dopo aver creato il file, eseguire:
```
python tools/config.py
```
Lo script, se eseguito direttamente, deve stampare i path e indicare
per ciascuno se la directory esiste (`EXISTS`) o meno (`MISSING`).
Aggiungere quindi in fondo al file:
```python
if __name__ == "__main__":
    paths = {
        "PATCH_GUI": PATCH_GUI,
        "OCR_GUI": OCR_GUI,
        "VANILLA_GUI": VANILLA_GUI,
        "WHITELIST_PATH": WHITELIST_PATH,
    }
    for nome, path in paths.items():
        stato = "EXISTS" if path.exists() else "MISSING"
        print(f"{nome}: {path} [{stato}]")
```

---

## Fase 2 — `tools/gui_validator.py`

**File da creare**: `tools/gui_validator.py`
**Priorità**: MASSIMA — blocca errori prima che arrivino all'LLM
**Integrazione**: potenzia `deprecated-pattern-scanner.skill.md` e `accessibility-checklist-runner.skill.md`
**Invocato da**: `implementatore-patch.agent.md` (passi 0 e 8)

### Scopo
Scansiona un file `.gui` con regex e verifica meccanicamente tutti i pattern
che `deprecated-pattern-scanner.skill.md` descrive. Produce output JSON
con lista dei problemi trovati, riga, categoria e gravità.

### Argomenti CLI
```
python tools/gui_validator.py --file <percorso_relativo_o_assoluto> [--format json|markdown]
```
- `--file`: percorso del file `.gui` da analizzare (obbligatorio)
- `--format`: formato output, default `markdown`

### Pattern da implementare (DEVONO corrispondere esattamente a deprecated-pattern-scanner.skill.md)

#### Categoria DEPRECATO (gravità: CRITICO)
- Regex: `GameRules\.GetRule\s*\(\s*['"]ocr_accessibility_mode['"]\s*\)`
  Fix: sostituire con `GetVariableSystem.Exists('ocr')`

#### Categoria VIETATO (gravità: CRITICO)
- `show_when` usato al posto di `visible`
  Regex: `\bshow_when\s*=`
- Scope `ROOT` in binding GUI
  Regex: `\[ROOT\b` oppure `ROOT\.Get` o simili
- Scope `THIS` in binding GUI
  Regex: `\[THIS\b` oppure `THIS\.Get` o simili
- `datamodel` senza nota di verifica
  Regex: `\bdatamodel\s*=`

#### Categoria STRUTTURALE (gravità: dipende)
- Widget `icon` senza `tooltip` nella stessa definizione di blocco
  Logica: se trovi `icon = {` o `icon={`, cerca `tooltip` entro le prossime 10 righe dentro lo stesso blocco; se assente → CRITICO
- `button` (o `button_standard`, `button_primary`) senza `tooltip`
  Logica: analoga a icon — cerca `tooltip` nelle righe successive dentro stesso blocco; se assente → CRITICO
- `text_single` o `text_multi` con `fontsize` < 18 dentro blocco OCR
  Logica: se il contesto è dentro un container il cui `name` inizia con `ocr_`, cerca `fontsize\s*=\s*(\d+)` e segnala se valore < 18 → ATTENZIONE
- `text_label` usato come header OCR senza `color = { 255 221 136 255 }`
  Logica: se `name` inizia con `ocr_` e c'è `text_label` senza quella color → ATTENZIONE

#### Categoria VISIBILITÀ (gravità: CRITICO — bug logico)
- Container `ocr_*` con visibility vanilla (invertita):
  Regex nomi: `name\s*=\s*"ocr_`
  Regex visibility errata sulle righe successive: `visible\s*=\s*"\[GetVariableSystem\.Exists\('ocr'\)\]"`
- Container `vanilla_*` con visibility OCR (invertita):
  Regex nomi: `name\s*=\s*"vanilla_`
  Regex visibility errata: `visible\s*=\s*"\[Not\(GetVariableSystem\.Exists\('ocr'\)\)\]"`

### Formato output Markdown (default)

```markdown
## Risultati Validazione: nome_file.gui

| Riga | Pattern trovato | Categoria | Gravità | Fix consigliato |
|------|----------------|-----------|---------|-----------------|
| 42   | GameRules.GetRule('ocr_accessibility_mode') | DEPRECATO | 🔴 CRITICO | Sostituire con GetVariableSystem.Exists('ocr') |

**Verdetto**: BLOCCANTE
**Problemi critici**: 1
**Avvertenze**: 0
```

Verdetti possibili:
- `BLOCCANTE` — almeno 1 problema CRITICO
- `CON AVVERTENZE` — solo problemi ATTENZIONE
- `PULITO` — nessun problema

### Formato output JSON (--format json)

```json
{
  "file": "ocr_support_compatibility_pach/gui/window_faith.gui",
  "verdict": "BLOCCANTE",
  "critical_count": 1,
  "warning_count": 0,
  "issues": [
    {
      "line": 42,
      "pattern": "GameRules.GetRule('ocr_accessibility_mode')",
      "category": "DEPRECATO",
      "severity": "CRITICO",
      "fix": "Sostituire con GetVariableSystem.Exists('ocr')"
    }
  ]
}
```

### Aggiornamento obbligatorio a `deprecated-pattern-scanner.skill.md`

Dopo aver creato lo script, aggiungere in cima alla sezione `## Logica di Esecuzione`:

```markdown
## Pre-Run Automatico

Prima di qualsiasi analisi manuale, eseguire:
```
python tools/gui_validator.py --file <file_path>
```
L'output dello script è la fonte autoritativa per tutti i problemi CRITICO.
Procedere con l'analisi manuale SOLO per completare i flag ATTENZIONE
o per fornire contesto interpretativo ai problemi già rilevati dallo script.
Se lo script riporta verdetto PULITO, la skill può concludere immediatamente
senza analisi manuale ulteriore.
```

Aggiornare identicamente `accessibility-checklist-runner.skill.md` nella
stessa sezione, limitando il Pre-Run ai check di accessibilità (font, header,
tooltip, visibilità).

---

## Fase 3 — `tools/scope_extractor.py`

**File da creare**: `tools/scope_extractor.py`
**Priorità**: ALTA — elimina il rischio di binding mancati in whitelist
**Integrazione**: potenzia `scope-whitelist-check.skill.md`
**Invocato da**: `implementatore-patch.agent.md` (passo 7), `architetto-dual-mode.agent.md`

### Scopo
Estrae tutti i binding Jomini da un file `.gui`, li confronta con
`jomini_scope_whitelist.md`, produce la lista di quelli assenti
già formattata per l'incollaggio diretto nella whitelist.

### Argomenti CLI
```
python tools/scope_extractor.py --file <percorso_gui> [--format json|markdown]
```

### Logica di estrazione binding

I binding Jomini sono racchiusi tra `[` e `]`. Regex base:
```
\[([^\[\]]+)\]
```
Da ogni match, filtrare:
- Tenere solo quelli che contengono almeno un `.` (sono riferimenti a scope)
- Escludere: `[Not(...)]`, `[And(...)]`, `[Or(...)]` come contenitori — ma estrarne il contenuto
- Escludere binding puramente numerici o booleani

Normalizzare ogni binding estratto rimuovendo argomenti (es: `GetPlayer.GetTrait('perk')` → `GetPlayer.GetTrait`).

### Confronto con whitelist

Leggere `WHITELIST_PATH` da `config.py`. Estrarre tutti i binding già presenti
nella colonna 1 della tabella Markdown (formato: `` `NomeBinding` ``).

Classificare ogni binding estratto dal file:
- **PRESENTE** ✅: già in whitelist
- **ASSENTE** ❌: non in whitelist → produce riga pronta da aggiungere
- **DA VERIFICARE** ⚠️: contiene scope non standard (non inizia con `Get`, `Has`, `Is`, `Can`, `Not`, `And`, `Or`)

### Formato output Markdown

```markdown
## Estrazione Binding: nome_file.gui

| Binding | Stato | Note |
|---------|-------|------|
| `GetPlayer.GetTreasury` | ✅ PRESENTE | — |
| `GetFaith.GetFervor` | ❌ ASSENTE | Aggiungere alla whitelist |

### Righe pronte per jomini_scope_whitelist.md
| `GetFaith.GetFervor` | window_faith — sezione fervor | verificato in vanilla CK3 1.17.1 |

**Riepilogo**: PRESENTI: 12 | ASSENTI: 3 | DA VERIFICARE: 0
```

### Aggiornamento obbligatorio a `scope-whitelist-check.skill.md`

Aggiungere in cima alla sezione `## Logica di Esecuzione`:

```markdown
## Pre-Run Automatico

Prima di qualsiasi verifica manuale, eseguire:
```
python tools/scope_extractor.py --file <percorso_file_gui>
```
Lo script produce automaticamente la lista dei binding ASSENTI con le righe
già formattate per la whitelist. Usare il suo output come input per questa skill.
La verifica manuale rimane necessaria solo per i binding DA VERIFICARE (⚠️).
```

---

## Fase 4 — `tools/tri_diff.py`

**File da creare**: `tools/tri_diff.py`
**Priorità**: MEDIA — libera contesto per l'analista
**Integrazione**: potenzia `tri-repo-diff.skill.md`
**Invocato da**: `analista-tri-repo.agent.md`

### Scopo
Confronta automaticamente lo stesso file `.gui` nei tre repository,
produce un report Markdown con le differenze categorizzate nelle 4 sezioni
già definite da `tri-repo-diff.skill.md`.

### Argomenti CLI
```
python tools/tri_diff.py --window <nome_finestra> [--output-file <percorso>]
```
- `--window`: nome della finestra senza estensione (es: `window_faith`)
- `--output-file`: se fornito, salva il report su file; altrimenti stdout

### Logica

1. Costruire i tre path: `PATCH_GUI / f"{window}.gui"`, `OCR_GUI / f"{window}.gui"`, `VANILLA_GUI / f"{window}.gui"`
2. Per ciascun file: verificare esistenza, leggere contenuto, contare righe
3. Sezione A — Struttura vanilla: estrarre tutti i blocchi di primo livello (`window =`, `types =`, `template =`) dal file vanilla usando regex
4. Sezione B — Feature OCR mancanti: confrontare blocchi top-level tra OCR upstream e patch; segnalare quelli presenti in OCR upstream ma assenti nella patch
5. Sezione C — Discrepanze container vanilla: confrontare il container `vanilla_*` nella patch con il file vanilla; usare `difflib.unified_diff` per mostrare differenze riga per riga
6. Sezione D — Stato generale: dimensioni file, numero righe, verdetto sintetico

### Formato output

```markdown
# Tri-Repo Diff: window_faith.gui
Generato: 2026-03-11 14:20:00

## A — Struttura Vanilla (blocchi top-level)
- `window = { name = "faith_window" }` — PRESENTE
- `types FaithWindow_types { ... }` — PRESENTE
- `window = { name = "religion_window" }` — PRESENTE

## B — Feature OCR Upstream non presenti nella Patch
- Nessuna feature mancante rilevata. ✅

## C — Discrepanze Container Vanilla vs CK3 Originale
[diff unificato delle differenze trovate, o "Nessuna discrepanza." se identico]

## D — Stato Generale
| File | Esiste | Righe |
|------|--------|-------|
| Patch | ✅ | 1842 |
| OCR Upstream | ✅ | 1654 |
| Vanilla | ✅ | 412 |

**Verdetto**: ALLINEATO / DISCREPANZE MINORI / DISCREPANZE CRITICHE
```

### Aggiornamento obbligatorio a `tri-repo-diff.skill.md`

Aggiungere in cima alla sezione di metodologia:

```markdown
## Pre-Run Automatico

Prima di qualsiasi analisi manuale, eseguire:
```
python tools/tri_diff.py --window <window_name>
```
Il report prodotto copre le sezioni A, B, C, D già formattate.
Usarlo come base per l'analisi — procedere con lettura manuale solo
per interpretare le discrepanze segnalate nella sezione C.
```

---

## Fase 5 — `tools/audit.py`

**File da creare**: `tools/audit.py`
**Priorità**: BASSA — ultimo da implementare, dipende dagli altri tre
**Integrazione**: potenzia `auditore-finale.agent.md`
**Invocato da**: manualmente o come GitHub Action

### Scopo
Script orchestratore. Chiama `gui_validator.py` e `scope_extractor.py`
su tutti i file `.gui` modificati (via `git diff --name-only`),
aggiorna `SKILLS_AUDIT_REPORT.md` con i risultati e un timestamp.

### Argomenti CLI
```
python tools/audit.py [--all] [--window <nome>] [--update-report]
```
- `--all`: analizza tutti i file `.gui` in `PATCH_GUI`
- `--window`: analizza solo il file specificato
- `--update-report`: sovrascrive `SKILLS_AUDIT_REPORT.md` con i risultati

### Logica
1. Determinare la lista di file da analizzare (da `--all`, `--window`, o `git diff`)
2. Per ogni file: invocare `gui_validator` come modulo (import, non subprocess)
3. Per ogni file: invocare `scope_extractor` come modulo
4. Aggregare i risultati in un dizionario per file
5. Produrre tabella riepilogativa: file, verdetto validator, binding assenti, stato complessivo
6. Se `--update-report`: aggiungere sezione datata in cima a `SKILLS_AUDIT_REPORT.md`

### Integrazione GitHub Action (opzionale)

Creare `.github/workflows/gui_audit.yml`:
```yaml
name: GUI Audit
on:
  push:
    paths:
      - 'ocr_support_compatibility_pach/gui/**'
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python tools/audit.py --all
```

---

## Aggiornamenti al Framework Esistente

### `implementatore-patch.agent.md` — modifiche ai passi 0 e 8

**Passo 0 attuale**:
> Invoca #deprecated-pattern-scanner sul file attuale prima di qualsiasi modifica.

**Passo 0 aggiornato** (dopo implementazione Fase 2):
> Esegui `python tools/gui_validator.py --file <percorso_file>`.
> Se verdetto = BLOCCANTE: correggere tutti i problemi CRITICO prima di procedere.
> Se verdetto = CON AVVERTENZE o PULITO: procedere, poi invoca #deprecated-pattern-scanner
> per analisi contestuale dei problemi residui.

**Passo 7 attuale**:
> Invoca #scope-whitelist-check su tutti i binding usati nel container OCR.

**Passo 7 aggiornato** (dopo implementazione Fase 3):
> Esegui `python tools/scope_extractor.py --file <percorso_file>`.
> Aggiungi alla whitelist tutte le righe prodotte per i binding ASSENTI.
> Poi invoca #scope-whitelist-check per i binding DA VERIFICARE (⚠️) se presenti.

**Passo 8 attuale**:
> Invoca #deprecated-pattern-scanner sul file modificato.

**Passo 8 aggiornato** (dopo implementazione Fase 2):
> Esegui nuovamente `python tools/gui_validator.py --file <percorso_file>`.
> Se verdetto != PULITO, correggere prima di passare ai revisori.
> Invoca #deprecated-pattern-scanner solo se restano flag ATTENZIONE da interpretare.

### `analista-tri-repo.agent.md` — aggiornamento metodologia

Aggiungere come primo passo della metodologia (dopo implementazione Fase 4):
> Esegui `python tools/tri_diff.py --window <nome_finestra>`.
> Usa il report prodotto come contesto base. Invoca #tri-repo-diff per
> l'interpretazione delle discrepanze trovate nella sezione C.

### `auditore-finale.agent.md` — aggiornamento checklist

Aggiungere come Sezione 0 della checklist (dopo implementazione Fase 5):
> Esegui `python tools/audit.py --window <nome_finestra>`.
> Se tutti i verdetti sono PULITO, le sezioni 1-3 sono già verificate dallo script.
> Procedere direttamente alla Sezione 4 (Completezza — verifica manuale).

---

## Struttura Directory Finale Attesa

```
ocr-support-patch/
├── tools/
│   ├── config.py               ← Fase 1 — path centralizzati
│   ├── gui_validator.py        ← Fase 2 — scanner pattern e accessibilità
│   ├── scope_extractor.py      ← Fase 3 — estrazione binding e confronto whitelist
│   ├── tri_diff.py             ← Fase 4 — confronto tri-repo
│   └── audit.py                ← Fase 5 — orchestratore audit completo
├── .github/
│   ├── agents/                 ← aggiornare passi come descritto sopra
│   ├── copilot-skills/         ← aggiornare con blocchi Pre-Run Automatico
│   └── workflows/
│       └── gui_audit.yml       ← Fase 5 opzionale — GitHub Action
```

---

## Checklist di Verifica per Copilot

Dopo ogni fase, verificare:

- [ ] Lo script gira senza errori con `python tools/<script>.py --help`
- [ ] Lo script produce output leggibile da screen reader (niente box grafici, niente unicode decorativo)
- [ ] I path usati derivano da `config.py`, non sono hardcodati
- [ ] La gestione errori copre: file non esistente, directory non trovata, whitelist non leggibile
- [ ] L'output Markdown è compatibile con il formato già usato dalle skills corrispondenti
- [ ] Il file `config.py` viene importato con `from tools.config import ...` (non path relativo fragile)
- [ ] Ogni `open()` usa `encoding='utf-8'`

---

## Vincoli Assoluti

- **NON modificare** file `.gui` in `ocr_support_compatibility_pach/gui/`
- **NON modificare** file nei repo vanilla o OCR upstream
- **NON creare** dipendenze da package non stdlib
- **NON toccare** agenti o skills fin quando lo script corrispondente non è testato
- **Aggiornare le skills** DOPO aver creato lo script, non prima
- **Aggiornare gli agenti** DOPO aver aggiornato le skills

---

*Fine del piano.*
*Generato: 2026-03-11 — per repository Nemex81/ocr-support-patch*
