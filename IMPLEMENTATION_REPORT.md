# Rapporto di Implementazione — Framework Restructure Plan

**Progetto**: OCR Support Patch — CK3 1.17.1
**Data**: 2026-03-12
**Stato complessivo**: ✅ Tutte e 7 le fasi completate e validate

---

## Panoramica

L'implementazione del `FRAMEWORK_RESTRUCTURE_PLAN.md` è stata completata integralmente.
Tutte le 7 fasi sono state eseguite in sequenza, con validazione automatica al termine
di ciascuna. Di seguito il dettaglio per ogni fase.

---

## FASE 1 — Pulizia Repository

### 1.1 Rimozione script obsoleti

Eliminati 6 script che non facevano più parte del workflow attivo:

| Script rimosso | Motivo |
|---------------|--------|
| `fix_faith_types.py` | Fix una tantum, non più necessario |
| `fix_remaining_types.py` | Fix una tantum, non più necessario |
| `classify_critico.py` | Funzionalità assorbita da `audit.py` |
| `test_enc.py` | Script diagnostico temporaneo |
| `debug_ocr_windows.py` | Debug temporaneo |
| `debug_vanilla_blocks.py` | Debug temporaneo |

**Validazione**: ✅ Tutti e 6 i file confermati assenti dal filesystem.

### 1.2 Eliminazione file `- Copia`

Rimossi **35 file backup** (`- Copia`) sparsi nell'intero repository. Questi file erano
duplicati generati da Windows e non facevano parte del progetto.

**Validazione**: ✅ Ricerca ricorsiva restituisce 0 risultati.

### 1.3 Correzione path hardcoded in `assemble_army_dualmode.py`

Il blocco di inizializzazione path (righe 17-24) è stato sostituito con un import
centralizzato:

```python
from config import OCR_GUI, VANILLA_GUI, PATCH_GUI
```

Questo allinea lo script specializzato con `config.py`, eliminando la dipendenza
da percorsi assoluti scritti nel codice.

**Validazione**: ✅ `from config import` confermato alla riga 20.

---

## FASE 2 — Refactoring Script Core

### 2.1 Creazione di `assemble_dualmode.py`

Creato un assemblatore generico da **611 righe** che supporta 3 pattern di conversione:

| Pattern | Funzione | Quando usarlo |
|---------|----------|---------------|
| A — Simple | `assemble_simple()` | 1 sola window, struttura semplice |
| B — Tabs | `assemble_tabs()` | Tab navigation, sub-windows modali |
| C — Complex | `assemble_complex()` | Multi-colonna, grid dinamici, custom types |

**Funzionalità chiave**:
- `--dry-run` obbligatorio: genera l'output senza scrivere su disco
- Rileva automaticamente i **type OCR-only** (presenti in OCR ma non in vanilla)
- Costruisce container OCR e vanilla con `visible` mutuamente esclusivi
- Opzione `--mode` per selezionare il pattern

**Bug fix applicato durante lo sviluppo**: rimossa generazione duplicata di `name = "..."`
nella funzione `build_sub_window_dual` (il nome era già incluso nelle `header_lines`).

**Test di regressione**: eseguito su `window_army` (output: 7562 righe) e `window_faith`
(output: 3463 righe). Il test ha confermato che lo script specializzato
`assemble_army_dualmode.py` produce un output strutturalmente diverso (8260 righe)
perché inietta il container vanilla dentro un widget `{800 100%}`. Decisione: **mantenere
entrambi gli script**.

**Validazione**: ✅ 611 righe, 3 funzioni `assemble_*`, dry-run funzionante.

### 2.2 Fix di `tri_diff.py` — Sezione C

Corretti due problemi nella rilevazione del container vanilla:

1. **Finestra di scansione visibilità**: estesa da 12 righe a tutto il blocco
   (`righe[i:fine + 1]`), con fallback su scansione dell'intero documento per
   `visible = "[GetVariableSystem.Exists('ocr')]"`.

2. **Messaggio di errore migliorato**: "Blocco vanilla non trovato" sostituito con
   avviso esplicito `CONTAINER VANILLA NON TROVATO` che elenca 3 possibili cause.

**Validazione**: ✅ Fix confermato alla riga 271.

---

## FASE 3 — Aggiornamento Agenti

Aggiunto il tool `terminal` a 3 agenti che devono eseguire script Python:

| Agente | Tools prima | Tools dopo |
|--------|------------|------------|
| Analista Tri-Repo | `[read, search]` | `[read, search, terminal]` |
| Implementatore Patch | `[edit, read, search]` | `[edit, read, search, terminal]` |
| Auditore Finale | `[read, search]` | `[read, search, terminal]` |

Per ciascun agente sono stati aggiornati anche i passi operativi con riferimenti
espliciti all'esecuzione dei comandi Python via terminale.

Gli agenti **non modificati** (Architetto, Revisore Accessibilità, Revisore Vanilla)
rimangono correttamente con soli tool di lettura.

**Validazione**: ✅ `terminal` confermato in tutti e 3 gli agenti aggiornati.

---

## FASE 4 — Riscrittura Prompt `converti-finestra-dual-mode`

Il prompt è stato completamente riscritto con:

- **8 passi sequenziali** (da PASSO 1 a PASSO 8)
- **2 checkpoint obbligatori** (CP1 prima della scrittura, CP2 prima dei revisori)
- Variabili aggiornate: `nomeFinestra` + `pattern` (prima era solo `nomeFile`)
- Tool aggiornati: `[read, search, terminal]`
- `--dry-run` come passo obbligatorio (PASSO 3) prima del checkpoint modder

**Flusso**:
```
1. tri_diff → 2. verifica sorgenti → 3. dry-run → [CP1 MODDER] →
4. scrittura → 5. scope → 6. audit → [CP2 MODDER] →
7. revisori → 8. chiusura
```

**Validazione**: ✅ 8 PASSO + 2 CHECKPOINT confermati.

---

## FASE 5 — Riallineamento Skills

### `dual-mode-template-generator.skill.md`

- Aggiunti parametri opzionali `ocr_source_path` e `vanilla_source_path`
- Aggiunta nota "PERCORSO CONSIGLIATO" che indirizza verso `assemble_dualmode.py --dry-run`
- Vincoli aggiornati: con percorsi → contenuto reale; senza → placeholder (legacy)

### `tri-repo-diff.skill.md`

- Esecuzione via terminale designata come **percorso primario**
- Logica LLM ridotta a **fallback** per i soli casi senza accesso al terminale
- Interpretazione qualitativa della Sezione C rimane responsabilità LLM

**Validazione**: ✅ Entrambe le skill aggiornate correttamente.

---

## FASE 6 — Aggiornamento Instructions

### `workflow-nuova-finestra.instructions.md`

Riscritta completamente con:
- Tabella operativa con colonna **Chi** (Agente/MODDER)
- 2 righe checkpoint esplicite (CP1, CP2)
- Riferimenti a `assemble_dualmode.py` (non più `assemble_army_dualmode.py`)
- `--dry-run` come passo obbligatorio
- Nota per la scelta del `--mode` dalla colonna Pattern

### `gui-conversion-progress.instructions.md`

Aggiunta colonna **Pattern** (A/B/C/D) a tutte e 3 le tabelle "Da Convertire":

| Finestra | Pattern assegnato |
|----------|------------------|
| `window_war.gui` | C (complex) |
| `window_title.gui` | C (complex) |
| `window_government.gui` | B (tabs) |
| `window_vassal_contracts.gui` | B (tabs) |
| `window_schemes.gui` | B (tabs) |
| `window_hook.gui` | A (simple) |
| `window_travel.gui` | B (tabs) |
| `window_struggle.gui` | C (complex) |

**Validazione**: ✅ 9 riferimenti CP/assemble nel workflow, 18 match Pattern nel progress.

---

## FASE 7 — Aggiornamento `copilot-instructions.md`

- **Sezione tools/** ampliata: ora elenca tutti gli 8 script attivi con descrizione
- **Nuova sezione**: "Principio di Controllo Manuale (non negoziabile)" con 4 regole:
  1. Il modder approva SEMPRE prima della scrittura (CP1)
  2. Il modder vede SEMPRE il verdetto audit prima dei revisori (CP2)
  3. Il sistema NON avvia mai la conversione successiva automaticamente
  4. Una finestra alla volta, sempre
- Descrizione skill `dual-mode-template-generator` aggiornata

**Validazione**: ✅ `assemble_dualmode.py` e `Principio di Controllo Manuale` confermati.

---

## Riepilogo Validazione

| Fase | Descrizione | Stato |
|------|-------------|-------|
| 1.1 | Rimozione 6 script obsoleti | ✅ |
| 1.2 | Eliminazione 35 file `- Copia` | ✅ |
| 1.3 | Fix path hardcoded | ✅ |
| 2.1 | `assemble_dualmode.py` (611 righe, 3 pattern) | ✅ |
| 2.2 | Fix `tri_diff.py` Sezione C | ✅ |
| 3 | Terminal in 3 agenti | ✅ |
| 4 | Prompt 8 passi + 2 checkpoint | ✅ |
| 5 | 2 skill riallineate | ✅ |
| 6 | Workflow + progress con Pattern | ✅ |
| 7 | `copilot-instructions.md` aggiornato | ✅ |
| Test | Dry-run `window_faith` (3463 righe) | ✅ |

---

## Suggerimenti per Procedere

### 1. GitHub Actions CI

Configurare una pipeline CI che esegua automaticamente su ogni Pull Request:
- `gui_validator.py` su tutti i file `.gui` nella patch
- `audit.py` sulle finestre modificate
- `tri_diff.py` per verificare la coerenza tri-repo

Questo eliminerebbe il rischio di regressioni non rilevate e renderebbe
il gate di qualità automatico e ripetibile.

### 2. Test di Regressione Automatizzati

Creare uno script `tools/regression_test.py` che per ogni finestra già convertita:
- Rigeneri l'output con `assemble_dualmode.py --dry-run`
- Confronti il numero di righe e la struttura con il file attuale nella patch
- Segnali divergenze significative

Questo sarebbe particolarmente utile quando si aggiorna `assemble_dualmode.py`
o quando Paradox rilascia una nuova versione del gioco.

### 3. Aggiornamento README e Documentazione Operativa

Il `README.md` attuale non riflette il nuovo workflow. Aggiornarlo con:
- Descrizione del sistema dual-mode
- Guida rapida per nuovi contributori
- Elenco degli script disponibili e come usarli
- Riferimento al workflow `converti-finestra-dual-mode`

### 4. Verifica Whitelist Scope Jomini

Eseguire `scope_extractor.py` su tutte le finestre già convertite per:
- Popolare la whitelist con tutti i binding effettivamente usati
- Identificare binding potenzialmente non validi per CK3 1.17.1
- Creare una baseline documentata per future verifiche

### 5. Audit NVDA sulle Finestre Prioritarie

Avviare test NVDA reali sulle finestre nella sezione "Convertite — Revisione Necessaria":
- `window_army.gui` (55 avvertenze)
- `window_character.gui` (64 avvertenze)
- `window_faith.gui` (32 avvertenze)

Le avvertenze potrebbero non essere tutte problemi reali — il test NVDA
permetterebbe di distinguere i falsi positivi dai problemi effettivi.

### 6. Decisione su `assemble_army_dualmode.py`

Lo script specializzato per army produce un output strutturalmente diverso
dall'assemblatore generico (8260 vs 7562 righe). Opzioni:

- **A — Mantenere entrambi**: lo specializzato per army, il generico per tutto il resto
- **B — Estendere il generico**: aggiungere un pattern D (o sotto-opzione di C) che replichi
  l'iniezione dentro widget `{800 100%}` usata dallo specializzato

La scelta dipende da quante finestre future richiederanno lo stesso pattern di iniezione.

### 7. Pre-commit Hooks e Linting

Configurare hook pre-commit che blocchino i commit contenenti:
- Pattern deprecati (`GameRules.GetRule`)
- File `.gui` con errori di sintassi rilevabili da `gui_validator.py`
- Binding non presenti nella whitelist scope

### 8. Conversione Finestre Prioritarie

Con il framework ora completo, procedere con le conversioni dalla lista "Da Convertire":

| Priorità | Finestra | Pattern |
|----------|----------|---------|
| ALTA | `window_war.gui` | C |
| ALTA | `window_title.gui` | C |
| ALTA | `window_government.gui` | B |
| MEDIA | `window_vassal_contracts.gui` | B |
| MEDIA | `window_schemes.gui` | B |

Il workflow è ora standardizzato: `tri_diff → dry-run → CP1 → scrittura → audit → CP2 → revisori`.

### 9. Risoluzione Critici nelle Finestre Bloccanti

8 finestre sono nella sezione "Bloccanti" con critici aperti. Priorità suggerita
per la risoluzione:

| Finestra | Critici | Impatto |
|----------|---------|---------|
| `window_court.gui` | 1 | Basso — probabile fix rapido |
| `window_activity_list.gui` | 1 | Basso |
| `window_intrigue.gui` | 1 | Medio — 34 avvertenze associate |
| `window_inventory.gui` | 1 | Medio |
| `window_military.gui` | 2 | Alto — tab eserciti |
| `window_character_lifestyle.gui` | 3 | Alto — stile di vita |
| `window_county_view.gui` | 4 | Alto — 269KB, 45 avvertenze |
| `window_my_realm.gui` | 6 | Critico — tab regno, 27 avvertenze |

---

## Conclusione

Il framework è ora strutturato, documentato e validato. Gli strumenti automatici
(`assemble_dualmode.py`, `audit.py`, `tri_diff.py`) coprono l'intero ciclo di vita
di una conversione. I checkpoint obbligatori (CP1, CP2) garantiscono il controllo
umano su ogni modifica. Il prossimo passo naturale è scegliere tra le attività
suggerite sopra in base alle priorità del progetto.



###

Rapporto di risposta elaborata da Perplexity:

# RAPPORTO ANALISI — Finestre Scoperte e Aggiornamento Framework

**Data:** 2026-03-13 | **Versione CK3:** 1.17.1 | **Repo patch:** [ocr-support-patch](https://github.com/Nemex81/ocr-support-patch)

***

## 1. Contesto dell'Analisi

L'analisi nasce dalla domanda: le finestre assenti dall'OCR upstream significano "non servono al gameplay" o "sono gestite in modo alternativo"? L'indagine ha coperto la struttura del [repo OCR Agamidae](https://github.com/Agamidae/CK3-OCR), il file `_OCR_WIDGET.gui`, e lo stato attuale del framework della patch.

***

## 2. Le Tre Strategie OCR per le Finestre

Dall'analisi dell'upstream OCR emergono tre categorie distinte — non tutti i file assenti sono uguali:

**Categoria A — Riscrittura completa con file `_ocr` gemello.** Esempio: `window_character_ocr.gui`. Agamidae ha prodotto sia la versione vanilla riscritta sia la versione OCR separata, applicando il pattern dual-mode con nome esplicito `_ocr`.

**Categoria B — Override diretto con dual-mode integrato.** La maggior parte dei `window_*.gui` presenti nella root OCR. Agamidae ha integrato i widget OCR direttamente dentro la finestra riscritta usando il meccanismo `ocr_mode` interno, senza file gemello separato.

**Categoria C — Finestre NON nell'override OCR attivo, coperte da meccanismo alternativo.** Queste finestre non hanno né un file nella root OCR né un file `_ocr` gemello. Il sistema OCR le raggiunge tramite shortcut da tastiera e overlay personalizzati definiti in `_OCR_WIDGET.gui` e `hud.gui`. Sono la categoria più importante per il framework.

***

## 3. Analisi delle Tre Finestre Pendenti

### `window_war.gui` — ESCLUSA DAL DUAL-MODE (gestione alternativa confermata)

Confermato dal modder durante l'analisi: le funzionalità di guerra sono accessibili tramite **Shift+W** nella schermata principale durante una guerra in corso. Questo shortcut è definito nell'`hud.gui` OCR riscritto e attiva un overlay testuale con tutti i dati della guerra (warscore, partecipanti, pulsanti di risoluzione). La finestra `window_war.gui` vanilla continua a caricarsi normalmente per i normo-vedenti, ma il non vedente ha un canale OCR dedicato e funzionante.

**Conseguenza per il framework:** `window_war.gui` **non deve essere convertita al dual-mode**. Va spostata da "Priorità ALTA Da Convertire" a una nuova sezione "Gestione Alternativa OCR".

### `window_title.gui` — PARZIALMENTE COPERTA, GAP REALI IDENTIFICATI

L'analisi del `_OCR_WIDGET.gui` ha rivelato che le informazioni sui titoli sono parzialmente accessibili tramite la griglia mappa OCR (`map_explorer`) e l'`hud.gui` riscritto. Nello specifico: nome titolo, contea, e nome del liege supremo sono già esposti tramite `Province.GetCounty.GetTitle.GetNameNoTierNoTooltip` e `Province.GetCounty.GetCount.GetTopLiege.GetPrimaryTitle.GetNameNoTierNoTooltip` nella griglia mappa.

**Quello che manca realmente** — non coperto da nessun meccanismo OCR alternativo:
- Linea di successione e lista claimant (esclusive di `window_title.gui`)
- Azioni dirette: **crea titolo**, **usurpa**, **distruggi**, **rendi primario**
- Storia del titolo (`TitleViewWindow.ToggleHistory`)
- Lista vassalli de jure in forma navigabile

**Conseguenza per il framework:** `window_title.gui` **rimane in "Da Convertire"** ma la motivazione va aggiornata: non è una finestra completamente scoperta — ha un gap parziale e preciso. La conversione dual-mode deve coprire solo i widget mancanti, non riduplicate ciò che la griglia mappa già espone.

### `window_struggle.gui` — RIMANDATO, PRIORITÀ BASSA CONFERMATA

La finestra è DLC-dipendente (Fate of Iberia e regioni Struggle analoghe). OCR Support dichiara copertura quasi totale dei DLC, ma questa finestra non è attiva in una partita standard. Non ha un meccanismo alternativo noto, ma data la dipendenza DLC e la frequenza di utilizzo marginale, la priorità bassa è confermata. Già classificata correttamente nel framework.

***

## 4. Aggiornamenti Richiesti ai File del Framework

### `gui-conversion-progress.instructions.md` — AGGIORNAMENTO NECESSARIO

Il file registra `window_war.gui` come "Priorità ALTA Da Convertire" — questa classificazione è **errata** alla luce dell'analisi. Vanno apportate le seguenti modifiche:

**Aggiungere una nuova sezione** tra "Convertite" e "Da Convertire":

```markdown
## Gestione Alternativa OCR (NON convertire al dual-mode)

Queste finestre NON devono essere aggiunte al sistema dual-mode.
Il sistema OCR le copre tramite shortcut da tastiera e overlay nell'hud.gui/OCR_WIDGET.
Convertirle causerebbe duplicazione e potenziale conflitto con i meccanismi esistenti.

| File | Meccanismo OCR alternativo | Shortcut |
|------|---------------------------|----------|
| `window_war.gui` | Overlay guerra in `hud.gui` OCR — dati guerra, warscore, azioni | Shift+W |
```

**Modificare la sezione "Da Convertire — Priorità ALTA"**: rimuovere `window_war.gui` e aggiornare la motivazione di `window_title.gui`:

```markdown
### Priorità ALTA

| File | Motivazione |
|------|-------------|
| `window_title.gui` | GAP PARZIALE: info base già in griglia mappa OCR. Mancano: crea/usurpa/distruggi titolo, linea successione, claimant, storia titolo, vassalli de jure navigabili. |
| `window_government.gui` | Governo/leggi |
```

### `copilot-instructions.md` — AGGIORNAMENTO NECESSARIO

Aggiungere una sezione esplicita sui file con gestione alternativa, immediatamente dopo "Principi Irrinunciabili":

```markdown
## Finestre con Gestione OCR Alternativa

Alcune finestre vanilla NON devono essere convertite al dual-mode perché il sistema OCR
le gestisce tramite shortcut da tastiera e overlay dedicati in `hud.gui` / `_OCR_WIDGET.gui`.

Convertirle al dual-mode causerebbe:
1. Duplicazione di funzionalità già accessibili
2. Potenziale conflitto con gli overlay OCR esistenti
3. Aumento inutile della superficie di manutenzione

**Lista file ESCLUSI dal dual-mode:**

| File | Perché escluso | Meccanismo OCR |
|------|---------------|----------------|
| `window_war.gui` | Coperta da overlay Shift+W in hud.gui | Shortcut Shift+W → overlay testuale guerra |

> ⚠️ Prima di avviare qualsiasi nuova conversione dual-mode, verificare in questa lista
> che il file non abbia già una copertura OCR alternativa tramite hud.gui o OCR_WIDGET.
```

### `workflow-nuova-finestra.instructions.md` — AGGIORNAMENTO CONSIGLIATO

Aggiungere come **primo passo** nel workflow di analisi pre-conversione la verifica della copertura OCR alternativa:

```markdown
### Passo 0 — Verifica copertura OCR alternativa (PRIMA di qualsiasi altra cosa)

Controllare in `copilot-instructions.md` sezione "Finestre con Gestione OCR Alternativa"
se il file target è già coperto da shortcut/overlay in hud.gui o _OCR_WIDGET.gui.
Se presente: STOP — non procedere con la conversione dual-mode.
```

### `FRAMEWORK_RESTRUCTURE_PLAN.md` — AGGIORNAMENTO CONSIGLIATO

Se il piano menziona `window_war.gui` o `window_title.gui` come target futuri, aggiornare le descrizioni con le stesse precisazioni di priorità e gap documentate qui.

***

## 5. Sintesi delle Azioni per Copilot

| Azione | File | Tipo modifica |
|--------|------|---------------|
| Rimuovere `window_war.gui` da "Da Convertire" | `gui-conversion-progress.instructions.md` | Spostamento di sezione |
| Aggiungere sezione "Gestione Alternativa OCR" | `gui-conversion-progress.instructions.md` | Nuova sezione |
| Aggiornare motivazione `window_title.gui` | `gui-conversion-progress.instructions.md` | Testo motivazione |
| Aggiungere sezione "Finestre con Gestione OCR Alternativa" | `.github/copilot-instructions.md` | Nuova sezione |
| Aggiungere Passo 0 pre-conversione | `workflow-nuova-finestra.instructions.md` | Inserimento in testa al workflow |
| Aggiornare riferimenti a `window_war.gui` se presenti | `FRAMEWORK_RESTRUCTURE_PLAN.md` | Verifica e aggiornamento |

***

## 6. Invarianti — Cosa Non Cambia

`window_title.gui` rimane in lavorazione futura ma con scope preciso: non una riscrittura completa, ma l'aggiunta dei **4 widget mancanti** (azioni titolo, successione, claimant, storia). La griglia mappa OCR già copre info geografiche e detentore. `window_struggle.gui` rimane priorità bassa, nessuna modifica al suo stato attuale nel framework. Il meccanismo dual-mode con toggle `ocr`/`Not(ocr)` rimane invariato per tutti gli altri file già in lavorazione.
---

istruzioni per copilot:

Devi aggiornare quattro file del framework con modifiche precise e chirurgiche.
NON riscrivere i file dall'inizio — applica solo le modifiche indicate.

---

### MODIFICA 1 — `.github/instructions/gui-conversion-progress.instructions.md`

a) Rimuovi `window_war.gui` dalla sezione "Da Convertire — Priorità ALTA".

b) Aggiorna la riga di `window_title.gui` nella sezione "Da Convertire — Priorità ALTA",
   sostituendo la motivazione attuale con:
   "GAP PARZIALE: info base (nome titolo, contea, liege) già coperte dalla griglia mappa
   OCR in hud.gui/_OCR_WIDGET.gui. Mancano: azioni dirette (crea/usurpa/distruggi/rendi
   primario titolo), linea successione, lista claimant, storia titolo, vassalli de jure
   navigabili."

c) Aggiungi questa nuova sezione PRIMA della sezione "Da Convertire":

---
## Gestione Alternativa OCR (NON convertire al dual-mode)

Queste finestre NON devono essere convertite al sistema dual-mode.
Il sistema OCR le copre tramite shortcut da tastiera e overlay dedicati
in `hud.gui` e/o `_OCR_WIDGET.gui` dell'upstream Agamidae.
Convertirle causerebbe duplicazione e potenziale conflitto con i meccanismi esistenti.

| File | Meccanismo OCR alternativo | Shortcut |
|------|---------------------------|----------|
| `window_war.gui` | Overlay guerra in `hud.gui` OCR — dati guerra, warscore, azioni di risoluzione | Shift+W |

---

### MODIFICA 2 — `.github/copilot-instructions.md`

Aggiungi questa nuova sezione DOPO "## Principi Irrinunciabili" e PRIMA di
"## Istruzioni Attive per Dominio":

---
## Finestre con Gestione OCR Alternativa

Alcune finestre vanilla NON devono essere convertite al dual-mode perché il sistema OCR
le gestisce già tramite shortcut da tastiera e overlay dedicati in `hud.gui` /
`_OCR_WIDGET.gui` dell'upstream Agamidae.

Convertirle al dual-mode causerebbe:
1. Duplicazione di funzionalità già accessibili al non vedente
2. Potenziale conflitto con gli overlay OCR esistenti
3. Aumento inutile della superficie di manutenzione

**Lista file ESCLUSI dal dual-mode:**

| File | Perché escluso | Meccanismo OCR |
|------|---------------|----------------|
| `window_war.gui` | Coperta da overlay Shift+W | Shortcut Shift+W → overlay testuale guerra in hud.gui |

> ⚠️ REGOLA OBBLIGATORIA: prima di avviare qualsiasi nuova conversione dual-mode,
> verificare in questa tabella che il file non abbia già copertura OCR alternativa.
> Se presente: STOP — non procedere con la conversione.

---

### MODIFICA 3 — `.github/instructions/workflow-nuova-finestra.instructions.md`

Aggiungi questo blocco come PRIMO PASSO del workflow, prima di qualsiasi step
già esistente (rinumera gli step esistenti di conseguenza):

---
### Passo 0 — Verifica copertura OCR alternativa (OBBLIGATORIO, prima di tutto)

Controllare la sezione "Finestre con Gestione OCR Alternativa" in
`.github/copilot-instructions.md`.

Se il file target è presente in quella lista: **STOP IMMEDIATO**.
Non aprire file, non analizzare, non proporre nulla.
Rispondere: "Il file [nome] ha già copertura OCR alternativa tramite [meccanismo].
Non va convertito al dual-mode. Consultare copilot-instructions.md per dettagli."

---

### MODIFICA 4 — `FRAMEWORK_RESTRUCTURE_PLAN.md`

Cerca nel documento ogni occorrenza di `window_war.gui`.
Per ogni occorrenza trovata: aggiungi una nota inline nel formato:
`<!-- AGGIORNATO 2026-03-13: window_war.gui esclusa dal dual-mode —
coperta da overlay Shift+W in hud.gui OCR. Vedi copilot-instructions.md. -->`
NON rimuovere il testo originale, aggiungi solo la nota.

---

Aggiorna la data "Ultimo aggiornamento" in `gui-conversion-progress.instructions.md`
a 2026-03-13.

Dopo aver applicato tutte le modifiche, elenca i file modificati con un riepilogo
di cosa è cambiato in ciascuno.
