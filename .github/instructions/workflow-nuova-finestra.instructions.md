---
applyTo: "**"
---

# Workflow — Nuova Conversione Finestra Dual Mode

Sequenza operativa standard. Seguire nell'ordine indicato senza saltare passi.

---

## Sequenza Operativa (approccio completo)

> L'**Orchestratore** (`orchestratore.agent.md`) esegue ogni passo via tool `terminal` e coordina i subagent specializzati. Il modder interviene ONLY ai due checkpoint.

| Passo | Chi | Azione |
|-------|-----|--------|
| **0** | **Orchestratore** | **Verifica la tabella "Gestione Alternativa OCR" in `copilot-instructions.md` e il file machine-readable `.github/resources/domain_boundaries.md`. Se uno dei due indica copertura OCR alternativa o "non toccare la mod": STOP immediato — informare il modder e non procedere.** |
| 1 | **Orchestratore** | `python tools/tri_diff.py --window nome` — report strutturale nei 3 repo |
| 2 | **Orchestratore** | Verifica esistenza file OCR upstream e vanilla. Se mancanti: STOP |
| 3 | **Orchestratore** | `python tools/assemble_dualmode.py --window nome --mode X --dry-run` |
| **CP1** | **MODDER** | **Approva la bozza o chiede modifiche. Nessuno scrive senza conferma** |
| 4 | **Orchestratore** | `python tools/assemble_dualmode.py --window nome --mode X` |
| 5 | **Orchestratore** | `python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/nome.gui` |
| 6 | **Orchestratore** | `python tools/audit.py --window nome` |
| **CP2** | **MODDER** | **Riceve il verdetto audit completo prima dei revisori** |
| 7 | **Orchestratore** | **Revisore Accessibilità** → **Revisore Vanilla** → **Auditore Finale** |
| 8 | **Orchestratore** | Aggiorna `gui-conversion-progress.instructions.md` |

---

## Passi Tecnici (Implementatore Patch)

0. `python tools/gui_validator.py --file ocr_support_compatibility_pach/gui/nome_file.gui`
   → se BLOCCANTE: correggere tutti i CRITICO prima di procedere
1. Verifica esistenza dei file sorgente:
   - OCR upstream: `../CK3-OCR/OCR-Support/gui/nome_file.gui`
   - Vanilla CK3: `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/nome_file.gui`
     (path effettivo letto da `tools/config.py` — VANILLA_GUI)
   - Se uno dei due manca: segnalare al modder, STOP
2. **DRY-RUN obbligatorio** — genera bozza senza scrivere:
   `python tools/assemble_dualmode.py --window nome_file --mode X --dry-run`
   Mostrare l'output completo al modder e attendere approvazione (CP1)
3. **Solo dopo CP1** — scrivi il file nella patch:
   `python tools/assemble_dualmode.py --window nome_file --mode X`
4. Verifica che le due `visible` siano mutuamente esclusive nel file scritto
5. `python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/nome_file.gui`
   → aggiungi alla whitelist `.github/resources/jomini_scope_whitelist.md` tutti i binding ASSENTI
6. `python tools/audit.py --window nome_file`
   → gate completo: validator (CRITICO/ATTENZIONE) + scope whitelist + fedelta' vanilla (advisory)
   → risolvi tutti i CRITICO prima di passare ai revisori
   → avvertenze CON AVVERTENZE richiedono sign-off esplicito dei revisori o fix
   → mostrare verdetto completo al modder (CP2)
7. Esegui la checklist pre-commit in `gui-jomini.instructions.md`
8. Aggiorna `gui-conversion-progress.instructions.md` spostando la voce nella sezione corretta:
    - **Convertite — Validate**: se audit.py = OK
    - **Convertite — Revisione Necessaria**: se audit.py = CON AVVERTENZE
    - **Convertite — Bloccanti**: se audit.py = BLOCCANTE (non committare)

> **Nota Python**: il comando `python` nei passi sopra deve puntare
> alla versione corretta sul PATH della macchina corrente.
> Il comando portabile è definito in `tools/config.py` come `PYTHON_CMD`.
> Su macchine con più versioni installate, verificare con `python --version`
> prima di avviare la pipeline.

> **Nota sulla scelta del mode**: usare la colonna Pattern nella sezione
> "Da Convertire" di `gui-conversion-progress.instructions.md` per scegliere
> il valore corretto di `--mode` (simple=A, tabs=B, complex=C/D).

---

## Pattern di Conversione

Scegli in base alla complessità. Dettagli completi in `.github/resources/conversion-patterns.md`.

| Pattern | Quando usarlo | Esempi tipici |
|---------|--------------|---------------|
| A — Simple Swap | 1 sola window, struttura semplice | Character, Military, Intrigue |
| B — Tabs + SubWindows | Tab navigation, sub-windows modali | Council, Activity, Factions |
| C — Complex Layout | Multi-colonna, grid dinamici, custom types | Court, Decisions, Lifestyle |
| D — Bottom-Up Multi-Window | 3+ finestre interconnesse, types condivisi | County View, Faith, Culture |
