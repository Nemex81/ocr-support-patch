---
applyTo: "**"
---

# Workflow — Nuova Conversione Finestra Dual Mode

Sequenza operativa standard. Seguire nell'ordine indicato senza saltare passi.

---

## Sequenza Operativa (approccio completo)

> L'agente esegue ogni passo tramite tool `terminal`. Il modder interviene SOLO ai due checkpoint.

| Passo | Chi | Azione |
|-------|-----|--------|
| **0** | **Agente** | **Verifica la tabella "Gestione Alternativa OCR" in `copilot-instructions.md` e il file machine-readable `.github/resources/domain_boundaries.md`. Se uno dei due indica copertura OCR alternativa o "non toccare la mod": STOP immediato — informare il modder e non procedere.** |
| 1 | Agente | `python tools/tri_diff.py --window nome` — report strutturale nei 3 repo |
| 2 | Agente | Verifica esistenza file OCR upstream e vanilla. Se mancanti: STOP |
| 3 | Agente | `python tools/assemble_dualmode.py --window nome --mode X --dry-run` |
| **CP1** | **MODDER** | **Approva la bozza o chiede modifiche. Nessuno scrive senza conferma** |
| 4 | Agente | `python tools/assemble_dualmode.py --window nome --mode X` |
| 5 | Agente | `python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/nome.gui` |
| 6 | Agente | `python tools/audit.py --window nome` |
| **CP2** | **MODDER** | **Riceve il verdetto audit completo prima dei revisori** |
| 7 | Agente | **Revisore Accessibilità** → **Revisore Vanilla** → **Auditore Finale** |
| 8 | Agente | Aggiorna `gui-conversion-progress.instructions.md` |

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
   - Pattern v1.0 (inline):
     `python tools/assemble_dualmode.py --window nome_file --mode X --dry-run`
   - Pattern v1.1 (type-separated — se file > 2000 righe E vanilla > 40%):
     `python tools/assemble_dualmode.py --window nome_file --mode X --separate-vanilla --dry-run`
   Mostrare l'output completo al modder e attendere approvazione (CP1)
   > ⚠️ CP1 con pattern v1.1: il modder approva **due** file — wrapper e file type vanilla
3. **Solo dopo CP1** — scrivi il/i file nella patch:
   - Pattern v1.0: `python tools/assemble_dualmode.py --window nome_file --mode X`
   - Pattern v1.1: `python tools/assemble_dualmode.py --window nome_file --mode X --separate-vanilla`
4. Verifica che le due `visible` siano mutuamente esclusive nel file scritto
   - Pattern v1.1: verificare che la `visible` sia dentro il type separato, **non** sul wrapper
5. `python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/nome_file.gui`
   → aggiungi alla whitelist `.github/resources/jomini_scope_whitelist.md` tutti i binding ASSENTI
6. `python tools/audit.py --window nome_file`
   → gate completo: validator (CRITICO/ATTENZIONE) + scope whitelist + fedelta' vanilla (advisory)
   → con pattern v1.1: audit.py verifica la coppia wrapper + type; il verdetto è cumulativo
   → risolvi tutti i CRITICO prima di passare ai revisori
   → avvertenze CON AVVERTENZE richiedono sign-off esplicito dei revisori o fix
   → se file type atteso ma assente: ATTENZIONE (non critico) ma da risolvere prima del commit
   → mostrare verdetto completo al modder (CP2)
   > ⚠️ CP2 con pattern v1.1: il modder vede il verdetto unificato coppia wrapper+type
7. Esegui la checklist pre-commit in `gui-jomini.instructions.md`
   - Se pattern v1.1: eseguire anche la checklist aggiuntiva "pattern v1.1" dello stesso file
8. Aggiorna `gui-conversion-progress.instructions.md` spostando la voce nella sezione corretta:
    - **Convertite — Validate**: se audit.py = OK
    - **Convertite — Revisione Necessaria**: se audit.py = CON AVVERTENZE
    - **Convertite — Bloccanti**: se audit.py = BLOCCANTE (non committare)

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
