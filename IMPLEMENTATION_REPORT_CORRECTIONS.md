# Rapporto Implementazione Correzioni — 2026-03-13

Applicato: 3 correzioni al framework OCR Support Patch.
Motivazione: allineamento dei file di istruzioni alla realtà verificata del filesystem
(vanilla CK3 1.17.1 e OCR upstream Agamidae).

---

## CORREZIONE 1 — `gui-conversion-progress.instructions.md`

### a) Rimossa da "Da Convertire — Priorità ALTA"

| File rimosso | Motivazione rimozione |
|---|---|
| `window_war_overview.gui` | Override OCR completo (2496 righe) già presente in Agamidae upstream. Non richiede conversione dual-mode. |

### b) Aggiunta nuova sezione "Gestione Alternativa OCR"

Inserita PRIMA della sezione "Da Convertire". Contiene la lista dei file
esclusi dalla conversione dual-mode perché coperti dall'upstream Agamidae.

**Voce aggiunta alla tabella esclusioni:**

| File | Meccanismo OCR alternativo | Shortcut |
|---|---|---|
| `window_war_overview.gui` | Override OCR completo (2496 righe) in upstream Agamidae + shortcut apertura | Shift+W |

### c) Aggiornata motivazione `window_title.gui` in "Priorità ALTA"

**Prima:** `Gestione titoli`

**Dopo:** `GAP PARZIALE: info base (nome, contea, liege) già in griglia mappa OCR.
Mancano: crea/usurpa/distruggi titolo, linea successione, claimant, storia titolo,
vassalli de jure navigabili.`

---

## CORREZIONE 2 — `.github/copilot-instructions.md`

### Aggiunta sezione "Finestre con Gestione OCR Alternativa"

Inserita tra "## Principi Irrinunciabili" e "## Istruzioni Attive per Dominio".

**Contenuto:** tabella delle finestre escluse dal dual-mode con motivazione e
regola operativa obbligatoria (STOP se il file è presente nella tabella).

**Voce nella tabella:**

| File | Perché escluso | Meccanismo OCR |
|---|---|---|
| `window_war_overview.gui` | Override OCR completo (2496 righe) già presente in upstream Agamidae | Shortcut Shift+W → apertura diretta del file con override OCR attivo |

---

## CORREZIONE 3 — `.github/instructions/workflow-nuova-finestra.instructions.md`

### Aggiunto Passo 0 alla Sequenza Operativa

Inserito come prima riga della tabella "Sequenza Operativa", prima del precedente
passo 1 (numerazione dei passi esistenti invariata da 1 a 8).

**Passo 0 aggiunto:**

| Passo | Chi | Azione |
|---|---|---|
| **0** | **Agente** | **Verifica tabella "Gestione Alternativa OCR" in `copilot-instructions.md`. Se il file è presente: STOP immediato — rispondere al modder che il file ha copertura OCR alternativa e non va convertito.** |

---

## File Modificati

| File | Tipo modifica |
|---|---|
| `.github/instructions/gui-conversion-progress.instructions.md` | Rimossa voce, aggiunta sezione, aggiornata motivazione |
| `.github/copilot-instructions.md` | Aggiunta sezione "Finestre con Gestione OCR Alternativa" |
| `.github/instructions/workflow-nuova-finestra.instructions.md` | Aggiunto passo 0 alla sequenza operativa |

---

## Note Tecniche

- `window_war_overview.gui` esiste in vanilla (2944 righe) e in OCR upstream Agamidae (2496 righe con `using = base_ocr_window`).
- Il nome `window_war.gui` non esiste né in vanilla né in OCR upstream — il file corretto è `window_war_overview.gui`.
- Shift+W (`shortcut = map_mode_10`) esegue `[WarItem.OnClick]` che apre `window_war_overview.gui`. Con l'override OCR di Agamidae attivo, la finestra viene già servita in modalità accessibile senza necessità di dual-mode nella patch.
