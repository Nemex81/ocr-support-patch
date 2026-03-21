# Protocollo Orchestrazione Autonoma — Ciclo Completo Conversione

Creato: 2026-03-20 | Fase C — Governance Framework
Scopo: istruire il main agent su come orchestrare l'intero ciclo di conversione
invocando i subagent specializzati in sequenza, passando il contesto corretto,
rispettando i checkpoint e gestendo i loop-back.

> Riferimento: `workflow-nuova-finestra.instructions.md` per la sequenza canonica.
> Questo documento aggiunge HOW (invocazione subagent, context passing, pre-run).

---

## Prerequisiti

- Il main agent ha accesso a: `runSubagent`, `run_in_terminal`, `read_file`, `replace_string_in_file`
- I subagent sono **stateless**: ogni invocazione parte da zero
- Il **contesto va passato interamente nel prompt** del subagent
- **Nessun subagent ha accesso a `terminal`** quando invocato via `runSubagent`
  - Il main agent DEVE eseguire TUTTI gli script necessari (pre-run e post-run)
  - Il main agent passa gli output degli script nel prompt del subagent
- Il comando Python corretto per la macchina corrente è definito in
  `tools/config.py` come `PYTHON_CMD`. Nei comandi di questo protocollo
  si usa `python` come riferimento generico — assicurarsi che `python`
  nel PATH punti alla versione corretta, oppure usare `sys.executable`
  nei sottoprocessi.
- Impostare `$env:PYTHONIOENCODING = "utf-8"` prima dei comandi Python che producono output con emoji

---

## Sequenza Fasi

```
Fase 0  PRE-CHECK (main agent)
   ↓
Fase 1  ANALISI (subagent: Analista Tri-Repo)
   ↓
Fase 2  PROGETTAZIONE (subagent: Architetto Dual-Mode)
   ↓
████ CHECKPOINT 1 — Modder approva design ████
   ↓
Fase 3  IMPLEMENTAZIONE (subagent: Implementatore Patch)
   ↓
Fase 4  AUDIT AUTOMATICO (main agent esegue audit.py)
   ↓
████ CHECKPOINT 2 — Modder vede verdetto ████
   ↓
Fase 5  REVISIONE (subagent: Revisore Accessibilità + Revisore Vanilla)
   ↓
Fase 6  AUDIT FINALE (subagent: Auditore Finale)
   ↓
Fase 7  CHIUSURA (main agent aggiorna tracker)
```

---

## Fase 0 — Pre-Check e Onboarding (main agent + subagent Analista)

### Sub-fase 0a — Verifica tracker (subagent: Analista Tri-Repo)

**Invocazione subagent:**
```
runSubagent(
  agentName: "Analista Tri-Repo",
  description: "Verifica tracker {nome_finestra}",
  prompt: """
    Verifica se '{nome_finestra}' è presente nel tracker.
    Leggi: .github/instructions/gui-conversion-progress.instructions.md
    Cerca il nome in tutte le sezioni.
    Riporta solo: nome sezione trovata oppure "NON TROVATA".
    Nessuna altra analisi.
  """
)
```

**Routing in base al risultato:**

| Risultato | Azione |
|-----------|--------|
| "Da Convertire" | Procedi a Sub-fase 0b (check sorgenti) |
| "Convertite — *" | STOP — "La finestra è già convertita. Usa: aggiorna {nome}" |
| "Convertite — Bloccanti" | STOP — "La finestra ha critici aperti. Usa: risolvi critici {nome}" |
| "Gestione Alternativa OCR" | STOP DEFINITIVO — "Questa finestra non va convertita al dual-mode." |
| "NON TROVATA" | Procedi a Sub-fase 0c (onboarding) |

### Sub-fase 0b — Verifica sorgenti (main agent, se in "Da Convertire")

**Azioni del main agent:**

1. Leggere la tabella "Gestione Alternativa OCR" in `copilot-instructions.md`
   - Se la finestra è presente → **STOP**, informare il modder
2. Leggere `.github/resources/domain_boundaries.md`
   - Se indica "non toccare" → **STOP**
3. Annotare il **Pattern** (A/B/C/D) dalla colonna "Da Convertire" del tracker
   - **Mapping pattern → mode CLI**: A=`simple` | B=`tabs` | C/D=`complex`
4. Verificare esistenza file sorgente:
   - Vanilla: `{VANILLA_GUI}/{nome}.gui`
   - OCR upstream: `{OCR_GUI}/{nome}.gui`
   - Se uno manca → **STOP**, informare il modder

### Sub-fase 0c — Onboarding (main agent, se "NON TROVATA")

**Pre-run:**
```
python tools/tri_diff.py --window {nome_finestra} --onboarding
```
Catturare output completo.

**Verifica:**
- File vanilla assente → STOP, informare il modder
- File OCR assente → avvertire il modder, chiedere conferma
- File presente in patch → segnalare al modder (parziale)

**CHECKPOINT 0:**
Presentare output onboarding al modder.
Chiedere conferma inserimento tracker e scelta pipeline (se parziale).
ATTENDERE risposta esplicita.

**Scrittura tracker (solo dopo conferma):**
- Ricomincia → aggiunge riga in "Da Convertire", poi procede a Sub-fase 0b
- Aggiorna → aggiunge riga in "Convertite — Revisione Necessaria",
  informa il modder di usare pipeline aggiornamento-upstream, STOP

---

## Fase 1 — Analisi (subagent: Analista Tri-Repo)

**Pre-run main agent:**
```
python tools/tri_diff.py --window {nome_finestra}
```
Catturare l'output completo.

**Invocazione subagent:**
```
runSubagent(
  agentName: "Analista Tri-Repo",
  description: "Analisi tri-repo {nome_finestra}",
  prompt: """
    Analizza la finestra '{nome_finestra}' nei tre repository.

    Output di tri_diff.py:
    {output_tri_diff_completo}

    Produci il report strutturato con le 4 sezioni:
    A) Albero widget vanilla
    B) Feature OCR mancanti nella patch
    C) Discrepanze container vanilla
    D) Stato generale

    Includi raccomandazioni per l'Architetto.
  """
)
```

**Output da conservare:** Report Analista (testo completo)

---

## Fase 2 — Progettazione (subagent: Architetto Dual-Mode)

**Pre-run main agent:**
```
python tools/scope_extractor.py --file "C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/{nome}.gui"
```
Catturare output binding.

```
python tools/assemble_dualmode.py --window {nome} --mode {pattern} --dry-run
```
Catturare bozza dry-run.

**Invocazione subagent:**
```
runSubagent(
  agentName: "Architetto Dual-Mode",
  description: "Progettazione dual-mode {nome_finestra}",
  prompt: """
    Progetta la conversione dual-mode per '{nome_finestra}'.
    Pattern di conversione: {pattern} ({A=simple/B=tabs/C=complex/D=multi-window}).

    === REPORT ANALISTA TRI-REPO ===
    {report_analista_completo}

    === BINDING ESTRATTI (vanilla) ===
    {output_scope_extractor}

    === BOZZA DRY-RUN assemble_dualmode.py ===
    {output_dry_run}

    Produci il documento di progetto con le 7 sezioni obbligatorie:
    1. Struttura container OCR
    2. Binding con tipo
    3. Sezioni e header testo
    4. Bottoni OCR con tooltip
    5. Conferma container vanilla invariato
    6. Rischi e pattern ambigui
    7. Sequenza implementazione

    Segnala con [NUOVO SCOPE] eventuali binding non in whitelist.
  """
)
```

**Output da conservare:** Design doc Architetto (testo completo)

---

## CHECKPOINT 1 — Approvazione Modder

**Il main agent DEVE:**

1. Presentare al modder una **sintesi strutturata** che include:
   - Risultato pre-check (Fase 0)
   - Report Analista (sintesi delle 4 sezioni)
   - Design doc Architetto (completo)
   - Bozza dry-run (estratto significativo)
2. Chiedere esplicitamente: "Approvi il design? Vuoi modifiche?"
3. **ATTENDERE risposta** — non procedere senza conferma esplicita
4. Se il modder chiede modifiche → tornare a Fase 2 con feedback

---

## Fase 3 — Implementazione (subagent: Implementatore Patch)

**Pre-run main agent:**
```
python tools/assemble_dualmode.py --window {nome} --mode {pattern}
```
Questo scrive il file nella patch.

```
python tools/gui_validator.py --file ocr_support_compatibility_pach/gui/{nome}.gui
```
Catturare output validazione pre-revisione.

**Invocazione subagent:**
```
runSubagent(
  agentName: "Implementatore Patch",
  description: "Implementazione {nome_finestra}",
  prompt: """
    Il modder ha approvato il design per '{nome_finestra}'.
    Il file è stato generato da assemble_dualmode.py ed è in:
    ocr_support_compatibility_pach/gui/{nome}.gui

    === DESIGN DOC APPROVATO ===
    {design_doc_completo}

    === VALIDAZIONE PRE-REVISIONE (gui_validator.py) ===
    {output_validator}

    Compiti:
    1. Leggi il file generato
    2. Verifica che il container vanilla sia copia fedele del CK3 originale
    3. Affina il container OCR seguendo il design doc
    4. Risolvi eventuali CRITICO segnalati dal validator
    5. NON eseguire script (non hai terminal) — il main agent li eseguirà dopo

    Riporta: modifiche effettuate, critici risolti, aree da verificare.
  """
)
```

**Post-run main agent (dopo che l'Implementatore ha finito):**
```
python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/{nome}.gui --update-whitelist
python tools/gui_validator.py --file ocr_support_compatibility_pach/gui/{nome}.gui
```
Catturare output post-check per Fase 4.

**Output da conservare:** Report implementazione + output post-check

---

## Fase 4 — Audit Automatico (main agent, nessun subagent)

**Azioni del main agent:**
```
python tools/audit.py --window {nome_finestra}
```

Catturare:
- Verdetto complessivo (OK / CON AVVERTENZE / BLOCCANTE)
- Tabella riepilogativa
- Dettaglio critici e avvertenze

---

## CHECKPOINT 2 — Verdetto al Modder

**Il main agent DEVE:**

1. Presentare il **verdetto audit.py completo** con:
   - Stato complessivo
   - Numero critici e avvertenze
   - Binding assenti
   - Fedeltà vanilla
2. Se BLOCCANTE: elencare i critici con riga e descrizione
3. Chiedere: "Procedo con le revisioni?" oppure "Vuoi che corregga i critici?"
4. **ATTENDERE risposta** — non procedere senza conferma
5. Se fix richiesti → loop a Fase 3 con lista critici

---

## Fase 5 — Revisione (subagent paralleli)

**Pre-run main agent:**
```
python tools/gui_validator.py --file ocr_support_compatibility_pach/gui/{nome}.gui
```
Catturare output validator fresco (necessario per Revisore Accessibilità che non ha terminal).

### 5a — Revisore Accessibilità
```
runSubagent(
  agentName: "Revisore Accessibilità",
  description: "Revisione accessibilità {nome_finestra}",
  prompt: """
    Verifica la qualità OCR/NVDA del file:
    ocr_support_compatibility_pach/gui/{nome}.gui

    === OUTPUT gui_validator.py (pre-computato) ===
    {output_validator}

    === VERDETTO AUDIT.PY ===
    {verdetto_audit}

    Esegui la checklist completa NVDA (8 punti) sul container OCR.
    Se non puoi eseguire gui_validator.py (no terminal), usa l'output fornito sopra.
    Produci: Report NVDA con verdetto PASS / PASS CON RISERVE / FAIL.
  """
)
```

### 5b — Revisore Vanilla
```
runSubagent(
  agentName: "Revisore Vanilla",
  description: "Revisione vanilla {nome_finestra}",
  prompt: """
    Verifica la fedeltà del container vanilla nel file:
    ocr_support_compatibility_pach/gui/{nome}.gui

    Confronta il container vanilla (visible = "[GetVariableSystem.Exists('ocr')]")
    con il file vanilla originale:
    C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/{nome}.gui

    Produci: Verdetto FEDELE / MODIFICATO CON BUG / DA RIFARE con lista differenze.
  """
)
```

**Output da conservare:** Entrambi i report revisori

---

## Fase 6 — Audit Finale (subagent: Auditore Finale)

```
runSubagent(
  agentName: "Auditore Finale",
  description: "Audit finale {nome_finestra}",
  prompt: """
    Audit finale pre-commit per '{nome_finestra}'.
    File: ocr_support_compatibility_pach/gui/{nome}.gui

    === VERDETTO AUDIT.PY ===
    {verdetto_audit_completo}

    === REPORT REVISORE ACCESSIBILITÀ ===
    {report_accessibilita}

    === REPORT REVISORE VANILLA ===
    {report_vanilla}

    Esegui la checklist completa a 7 sezioni.
    Emetti verdetto vincolante: APPROVED o BLOCKED.
    Se BLOCKED: lista esatta dei critici con fix richiesto.
  """
)
```

**Output da conservare:** Verdetto finale (APPROVED/BLOCKED)

---

## Fase 7 — Chiusura (main agent)

### Se APPROVED:

1. Aggiornare `gui-conversion-progress.instructions.md`:
   - Rimuovere la finestra dalla sezione "Da Convertire"
   - Aggiungere alla sezione appropriata:
     - "Convertite — Validate" se audit = OK
     - "Convertite — Revisione Necessaria" se audit = CON AVVERTENZE
     - "Convertite — Bloccanti" se audit = BLOCCANTE (ma Auditore ha detto APPROVED → non dovrebbe succedere)
2. Informare il modder del completamento con riepilogo

### Se BLOCKED:

1. Presentare al modder i critici dell'Auditore con fix richiesti
2. Chiedere se procedere con fix automatico
3. Se sì → loop a Fase 3 con lista critici come input aggiuntivo
4. Se no → lasciare il file come "Convertita — Bloccanti" nel tracker

---

## Regole Trasversali

1. **Mai saltare una fase** — il protocollo è sequenziale e deterministico
2. **CP1 e CP2 richiedono SEMPRE risposta esplicita del modder** — non inferire approvazione
3. **Una finestra alla volta** — mai avviare una seconda conversione prima di chiudere la prima
4. **Contesto completo nel prompt** — ogni subagent riceve l'output integrale dei passi precedenti rilevanti
5. **Pre-run script come compensazione** — se un subagent non ha `terminal`, il main agent esegue lo script e passa l'output nel prompt
6. **Comunicazione in italiano** — tutti i report e le interazioni col modder sono in italiano, chiari e descrittivi
7. **Errori bloccanti** — se un subagent fallisce o produce output inatteso, il main agent segnala al modder e non prosegue

---

## Template Compatto Avvio

Quando l'utente chiede "converti {nome_finestra}" o "inizia la conversione di {nome}", il main agent:

```
1. Eseguo Fase 0 completa: verifica tracker (Sub-fase 0a) + verifica sorgenti (Sub-fase 0b). Se finestra NON TROVATA → onboarding automatico (Sub-fase 0c) prima di procedere.
2. Se OK → "Avvio il ciclo completo per {nome}. Inizio con l'analisi tri-repo."
3. Eseguo Fasi 1-2 in sequenza
4. Presento al modder sintesi + design doc (CP1)
5. Attendo approvazione
6. Eseguo Fasi 3-4
7. Presento verdetto audit (CP2)
8. Attendo conferma
9. Eseguo Fasi 5-6
10. Se APPROVED → Fase 7 → "Conversione completata."
11. Se BLOCKED → presento critici → propongo fix
```

***

## Pipeline aggiornamento-upstream

Scopo: risincronizzare una finestra già convertita nella patch con le modifiche
recenti dell'upstream OCR (Agamidae), preservando il container vanilla invariato.

### Fase 0 — Pre-Check

1. Verificare che la finestra sia nella sezione "Convertite" del tracker.
    Se non è già convertita: STOP — usare la pipeline converti-finestra.
2. Leggere domain_boundaries.md — se indica "non toccare": STOP.
3. Verificare esistenza file sorgente (upstream e vanilla). Se mancanti: STOP.

### Fase 1 — Analisi delta upstream

Pre-run main agent:
python tools/tri_diff.py --window {nome_finestra}

runSubagent(
   agentName: "Analista Tri-Repo",
   prompt: """
      Analizza le differenze tra l'upstream OCR attuale e la versione nella patch
      per la finestra '{nome_finestra}'.

      Output tri_diff.py:
      {output_tri_diff}

      Produci:
      A) Modifiche upstream non ancora nella patch (feature nuove, fix, refactor)
      B) Container vanilla nella patch: allineato o divergente dal CK3 originale?
      C) Rischio regressione per ogni modifica upstream
      D) Raccomandazione: applicare / valutare / ignorare — con motivazione
   """
)

Output da conservare: Report delta Analista

### Fase 2 — Valutazione impatto (subagent: Architetto Dual-Mode)

Pre-run main agent:
python tools/assemble_dualmode.py --window {nome} --mode {pattern} --dry-run

runSubagent(
   agentName: "Architetto Dual-Mode",
   prompt: """
      Valuta l'impatto delle modifiche upstream per '{nome_finestra}'.

      === REPORT ANALISTA ===
      {report_analista}

      === BOZZA DRY-RUN ===
      {output_dry_run}

      Determina per ogni modifica raccomandata:
      - Riscrittura completa del container OCR
      - Aggiornamento parziale (widget specifici)
      - Nessun intervento necessario

      Produci piano di aggiornamento con sequenza e rischi.
   """
)

### CHECKPOINT 1 — Approvazione Modder

Presentare al modder:
- Report delta Analista
- Piano di aggiornamento Architetto
Chiedere: "Approvi il piano? Procedo con l'aggiornamento?"
ATTENDERE risposta esplicita.

### Fase 3 — Aggiornamento (subagent: Implementatore Patch)

Pre-run main agent (solo se il piano prevede riscrittura):
python tools/assemble_dualmode.py --window {nome} --mode {pattern}
python tools/gui_validator.py --file ocr_support_compatibility_pach/gui/{nome}.gui

runSubagent(
   agentName: "Implementatore Patch",
   prompt: """
      Applica il piano di aggiornamento approvato per '{nome_finestra}'.

      === PIANO APPROVATO ===
      {piano_aggiornamento}

      === OUTPUT VALIDATOR ===
      {output_validator}

      Applica solo le modifiche nel piano. Non toccare il container vanilla.
      Riporta: modifiche effettuate, widget aggiornati, critici risolti.
   """
)

Post-run:
python tools/audit.py --window {nome_finestra}

### CHECKPOINT 2 — Verdetto Audit al Modder

Presentare verdetto audit completo.
Chiedere conferma prima di procedere ai revisori.

### Fase 4 — Revisione e chiusura

Eseguire Fasi 5-7 della pipeline converti-finestra (stessa sequenza).
Aggiornare il tracker con il nuovo stato della finestra.

### Template Compatto Avvio — aggiornamento-upstream

Quando l'utente chiede "aggiorna {nome_finestra}" o "risincronizza {nome}":

1. Eseguo Sub-fase 0a (verifica tracker). Se in "Convertite": procedo. Se "NON TROVATA": onboarding automatico (Sub-fase 0c) → poi informo il modder di usare pipeline converti-finestra. Se altra sezione: STOP con indicazione pipeline corretta.
2. Verifico domain_boundaries.md e sorgenti.
3. Se OK → "Avvio aggiornamento upstream per {nome}. Inizio con l'analisi delta."
4. Eseguo Fasi 1-2 in sequenza.
5. Presento al modder report delta + piano Architetto (CP1).
6. Attendo approvazione.
7. Eseguo Fase 3 (implementazione + audit).
8. Presento verdetto audit (CP2).
9. Attendo conferma.
10. Eseguo Fase 4 (revisori + auditore + chiusura).
11. Se APPROVED → aggiorno tracker → "Aggiornamento completato."
12. Se BLOCKED → presento critici → propongo fix.

***

## Pipeline fix-bloccante

Scopo: risolvere i CRITICO aperti su una finestra già nella sezione
"Convertite — Bloccanti" del tracker.

### Fase 0 — Pre-Check

1. Verificare che la finestra sia nella sezione "Bloccanti" del tracker.
    Se non è bloccante: usare la pipeline corretta.
2. Leggere domain_boundaries.md — se indica "non toccare": STOP.

### Fase 1 — Audit iniziale (main agent)

python tools/audit.py --window {nome_finestra}

Catturare lista completa dei CRITICO con riga, descrizione e causa.

### CHECKPOINT 1 — Presentazione critici al Modder

Presentare al modder la lista CRITICO con descrizione chiara di ogni problema.
Chiedere: "Procedo con la risoluzione automatica?"
ATTENDERE risposta esplicita.

### Fase 2 — Fix (subagent: Implementatore Patch)

Pre-run main agent:
python tools/gui_validator.py --file ocr_support_compatibility_pach/gui/{nome}.gui

runSubagent(
   agentName: "Implementatore Patch",
   prompt: """
      Risolvi i CRITICO aperti in '{nome_finestra}'.
      File: ocr_support_compatibility_pach/gui/{nome}.gui

      === LISTA CRITICO DA RISOLVERE ===
      {lista_critico}

      === OUTPUT VALIDATOR ===
      {output_validator}

      Risolvi esclusivamente i problemi elencati. Non introdurre modifiche non richieste.
      Non toccare il container vanilla salvo che il CRITICO riguardi il vanilla.
      Riporta: fix applicati per ciascun critico, codice modificato, righe cambiate.
   """
)

Post-run:
python tools/audit.py --window {nome_finestra}

### CHECKPOINT 2 — Verdetto Post-Fix al Modder

Presentare il verdetto audit post-fix completo.
Se ancora BLOCCANTE: ripresentare critici residui e chiedere istruzioni.
Se OK o CON AVVERTENZE: procedere.

### Fase 3 — Revisione e chiusura

Eseguire Fasi 5-7 della pipeline converti-finestra.
Aggiornare il tracker spostando la finestra dalla sezione "Bloccanti"
alla sezione corretta (Validate o Revisione Necessaria).

### Template Compatto Avvio — fix-bloccante

Quando l'utente chiede "risolvi critici {nome}" o "fix bloccante {nome}":

1. Eseguo Sub-fase 0a (verifica tracker). Se in "Bloccanti": procedo. Se "NON TROVATA": onboarding automatico (Sub-fase 0c) → poi informo il modder di usare pipeline converti-finestra. Se altra sezione: STOP con indicazione pipeline corretta.
2. Verifico domain_boundaries.md.
3. Se OK → Eseguo audit.py iniziale.
4. Presento al modder lista CRITICO (CP1).
5. Attendo approvazione.
6. Eseguo Fase 2 (fix Implementatore + re-audit).
7. Presento verdetto post-fix (CP2).
8. Attendo conferma.
9. Eseguo Fase 3 (revisori + auditore + chiusura).
10. Se APPROVED → sposto finestra da "Bloccanti" alla sezione corretta nel tracker.
11. Se ancora BLOCKED → ripresento critici residui → chiedo istruzioni modder.

***

## Procedura Onboarding — Inserimento finestra nel tracker

Questa procedura è parte integrante della Fase 0 di ogni pipeline.
Non è una pipeline autonoma — si attiva automaticamente quando
la finestra non è trovata nel tracker durante il Pre-Check.

Riferimento completo: `.github/instructions/workflow-onboarding-finestra.instructions.md`

### Template Compatto — onboarding

Quando in Fase 0 la finestra risulta "NON TROVATA" nel tracker:

1. Eseguo tri_diff.py --onboarding per verificare sorgenti e Pattern.
2. Presento al modder output onboarding + scelta pipeline (CP0).
3. Attendo conferma esplicita.
4. Se ricomincia → scrivo riga in "Da Convertire" → procedo a Sub-fase 0b.
5. Se aggiorna → scrivo riga in "Convertite — Revisione Necessaria"
   → informo il modder di usare "aggiorna {nome}" → STOP.
6. Se modder rifiuta → STOP, nessuna modifica al tracker.
