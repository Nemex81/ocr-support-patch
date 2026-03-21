***
applyTo: "**"
***

# Workflow — Onboarding Nuova Finestra nel Tracker

Procedura per inserire una finestra nel tracker prima di avviare
una pipeline di conversione. Eseguita dall'Orchestratore in Fase 0
quando la finestra richiesta non è presente nel tracker.

***

## Quando si attiva

L'Orchestratore attiva questa procedura automaticamente se in Fase 0
la finestra richiesta NON è trovata in nessuna sezione del tracker
(`gui-conversion-progress.instructions.md`).

***

## Flusso Operativo

### Sub-fase 0a — Verifica tracker (delegata all'Analista Tri-Repo)

L'Orchestratore invoca l'Analista Tri-Repo come subagent con questo compito:

1. Cerca il nome della finestra in TUTTE le sezioni del tracker:
   - "Convertite — Validate"
   - "Convertite — Revisione Necessaria"
   - "Convertite — Bloccanti"
   - "Gestione Alternativa OCR"
   - "Da Convertire"
2. Riporta in quale sezione si trova (o "NON TROVATA").
3. Non eseguire nessuna analisi strutturale — solo ricerca nel testo.

L'Orchestratore usa il risultato per decidere il percorso:

| Stato trovato | Azione Orchestratore |
|---------------|---------------------|
| "Da Convertire" | Procede normalmente a Fase 1 |
| "Convertite — *" | STOP — suggerisce pipeline aggiornamento-upstream |
| "Convertite — Bloccanti" | STOP — suggerisce pipeline fix-bloccante |
| "Gestione Alternativa OCR" | STOP DEFINITIVO — non convertire mai |
| "NON TROVATA" | Attiva Sub-fase 0b |

### Sub-fase 0b — Onboarding automatico

**Pre-run Orchestratore:**
```
python tools/tri_diff.py --window {nome_finestra} --onboarding
```
Catturare l'output completo.

**Verifica incrociata:**
- Il file vanilla esiste? Se no → STOP, informare il modder.
- Il file OCR upstream esiste? Se no → avvertire il modder (conversione
  possibile ma senza riferimento OCR — chiedere conferma).
- Il file è presente nella patch (parzialmente convertito)?
  → Se sì: attivare Checkpoint 0 con scelta ricomincia/aggiorna.

### CHECKPOINT 0 — Conferma onboarding al Modder

L'Orchestratore presenta al modder:
- Output onboarding_check (esistenza sorgenti + Pattern consigliato)
- Se file presente nella patch: segnalare righe e chiedere scelta

Domanda al modder:
- Se file NON in patch:
  "La finestra non è nel tracker. Pattern consigliato: {X}.
   La aggiungo in 'Da Convertire' e procedo con la conversione?"
- Se file IN patch (parziale):
  "Il file è già presente nella patch ({N} righe) — potrebbe essere
   parzialmente convertito. Vuoi ricominciare da zero (pipeline
   converti-finestra) o aggiornare il lavoro esistente (pipeline
   aggiornamento-upstream)?"

**ATTENDERE risposta esplicita del modder. Non procedere senza conferma.**

### Scrittura tracker

L'Orchestratore aggiorna `gui-conversion-progress.instructions.md`:

**Caso A — ricomincia da zero:**
Aggiunge riga nella sezione "Da Convertire" con priorità MEDIA (default):
```
| `{nome_finestra}.gui` | {motivazione breve} | {Pattern} |
```

**Caso B — aggiorna lavoro esistente:**
Aggiunge riga nella sezione "Convertite — Revisione Necessaria":
```
| `{nome_finestra}.gui` | {dim}KB | Onboarding da parziale | {data} | ? | ? | ? |
```
Poi comunica al modder di usare la pipeline aggiornamento-upstream.

***

## Regole

- L'Orchestratore è l'UNICO agente autorizzato a scrivere nel tracker.
- L'Analista in Sub-fase 0a fa SOLO ricerca testuale — nessuna analisi strutturale.
- Il Pattern consigliato da onboarding_check è una stima — l'Architetto
  può ridefinirlo in Fase 2 dopo l'analisi completa.
- Se il modder rifiuta l'onboarding al Checkpoint 0: STOP, nessuna modifica.
