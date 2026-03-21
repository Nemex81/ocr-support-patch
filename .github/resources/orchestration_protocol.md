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
- Python è invocabile come `python3.14` (non bare `python`)
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

## Fase 0 — Pre-Check (main agent, nessun subagent)

**Azioni del main agent:**

1. Leggere la tabella "Gestione Alternativa OCR" in `copilot-instructions.md`
   - Se la finestra è presente → **STOP**, informare il modder
2. Leggere `.github/resources/domain_boundaries.md`
   - Se indica "non toccare" → **STOP**
3. Verificare che la finestra sia nella sezione "Da Convertire" di `gui-conversion-progress.instructions.md`
   - Annotare il **Pattern** (A/B/C/D) dalla colonna corrispondente
   - **Mapping pattern → mode CLI**: A=`simple` | B=`tabs` | C/D=`complex`
4. Verificare esistenza file sorgente:
   - Vanilla: `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/{nome}.gui`
   - OCR upstream: `../CK3-OCR/OCR-Support/gui/{nome}.gui`
   - Se uno manca → **STOP**, informare il modder

---

## Fase 1 — Analisi (subagent: Analista Tri-Repo)

**Pre-run main agent:**
```
python3.14 tools/tri_diff.py --window {nome_finestra}
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
python3.14 tools/scope_extractor.py --file "C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/{nome}.gui"
```
Catturare output binding.

```
python3.14 tools/assemble_dualmode.py --window {nome} --mode {pattern} --dry-run
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
python3.14 tools/assemble_dualmode.py --window {nome} --mode {pattern}
```
Questo scrive il file nella patch.

```
python3.14 tools/gui_validator.py --file ocr_support_compatibility_pach/gui/{nome}.gui
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
python3.14 tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/{nome}.gui --update-whitelist
python3.14 tools/gui_validator.py --file ocr_support_compatibility_pach/gui/{nome}.gui
```
Catturare output post-check per Fase 4.

**Output da conservare:** Report implementazione + output post-check

---

## Fase 4 — Audit Automatico (main agent, nessun subagent)

**Azioni del main agent:**
```
python3.14 tools/audit.py --window {nome_finestra}
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
python3.14 tools/gui_validator.py --file ocr_support_compatibility_pach/gui/{nome}.gui
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
1. Leggo esclusioni e tracker (Fase 0)
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
