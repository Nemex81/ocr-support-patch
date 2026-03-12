---
applyTo: "**"
---

# Workflow — Nuova Conversione Finestra Dual Mode

Sequenza operativa standard. Seguire nell'ordine indicato senza saltare passi.

---

## Sequenza con Agenti (approccio completo)

| Passo | Agente / Comando | Azione |
|-------|-----------------|--------|
| 0 | `python tools/tri_diff.py --window nome_file` | Report strutturale pre-analisi nei 3 repo |
| 1 | **Analista Tri-Repo** | Analizza i 3 file, produce report strutturale |
| 2 | **Architetto Dual-Mode** | Progetta struttura OCR basandosi sul report |
| 3 | **Implementatore Patch** | Scrive il codice seguendo il progetto |
| 4 | **Revisore Accessibilità** | Verifica leggibilità NVDA, tooltip, ordine lettura |
| 5 | **Revisore Vanilla** | Verifica fedeltà container vanilla al CK3 originale |
| 6 | **Auditore Finale** | Checklist completa → APPROVED o BLOCKED |
| 7 | `python tools/audit.py --window nome_file` | Verdetto automatico post-commit |

---

## Passi Tecnici (Implementatore Patch)

0. `python tools/gui_validator.py --file ocr_support_compatibility_pach/gui/nome_file.gui`
   → se BLOCCANTE: correggere tutti i CRITICO prima di procedere
1. Leggi il file vanilla da `../CK3 ORIGINAL VERSION/ck3origin/game/gui/nome_file.gui`
2. Leggi il file OCR upstream da `../CK3-OCR/OCR-Support/gui/nome_file.gui`
3. Identifica struttura widget vanilla (tipo, nome, gerarchia)
4. Invoca `#dual-mode-template-generator` con le sezioni identificate
5. Incapsula il vanilla nel container vanilla **senza nessuna modifica**
6. Verifica che le due `visible` siano mutuamente esclusive
7. `python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/nome_file.gui`
   → aggiungi alla whitelist tutti i binding ASSENTI
8. `python tools/gui_validator.py --file ocr_support_compatibility_pach/gui/nome_file.gui`
   → risolvi tutti i CRITICO prima di passare ai revisori
9. Esegui la checklist pre-commit in `gui-jomini.instructions.md`
10. Aggiorna `gui-conversion-progress.instructions.md` spostando la voce in "Già Convertite"

---

## Pattern di Conversione

Scegli in base alla complessità. Dettagli completi in `.github/resources/conversion-patterns.md`.

| Pattern | Quando usarlo | Esempi tipici |
|---------|--------------|---------------|
| A — Simple Swap | 1 sola window, struttura semplice | Character, Military, Intrigue |
| B — Tabs + SubWindows | Tab navigation, sub-windows modali | Council, Activity, Factions |
| C — Complex Layout | Multi-colonna, grid dinamici, custom types | Court, Decisions, Lifestyle |
| D — Bottom-Up Multi-Window | 3+ finestre interconnesse, types condivisi | County View, Faith, Culture |
