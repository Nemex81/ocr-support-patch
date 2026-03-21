# .github/agents — Agenti Copilot specializzati

Questa cartella contiene le definizioni degli agenti Copilot invocabili dal picker agenti di VS Code durante lo sviluppo della patch.

## Descrizione

Gli agenti qui definiti sono specializzazioni del sistema Copilot per ruoli fissi nel workflow di conversione dual-mode. Ogni agente ha un ruolo preciso, un set di tool abilitati e restrizioni esplicite su cosa può e non può fare.

Il principio fondamentale è la separazione delle responsabilità: l'agente che analizza non modifica, l'agente che scrive non decide l'architettura, l'agente che approva non è lo stesso che implementa. Questo schema riduce il rischio di errori silenziosi e mantiene il controllo nelle mani del modder ai checkpoint CP1 e CP2.

Gli agenti si passano il controllo tramite handoff espliciti dichiarati nel frontmatter YAML di ogni file. Il flusso standard è: Analista → Architetto → Implementatore → Revisore Accessibilità → Revisore Vanilla → Auditore Finale.

## File presenti

**orchestratore.agent.md** — Entry point della pipeline: coordina l'intero ciclo di conversione dual-mode, esegue i pre-run script con terminal e governa i checkpoint CP1/CP2 prima degli handoff agli agenti specializzati.

**analista-tri-repo.agent.md** — Confronta i tre repository (patch, OCR upstream Agamidae, vanilla CK3) per una finestra specifica. Usa `tri_diff.py`. Solo lettura, nessuna modifica. Passa il controllo all'Architetto.

**architetto-dual-mode.agent.md** — Progetta la struttura dual-mode per una finestra: decide il pattern di conversione (A/B/C/D), identifica i container OCR e vanilla, produce la bozza da approvare al CP1. Solo progettazione, nessuna modifica a file.

**implementatore-patch.agent.md** — Scrive e modifica i file `.gui` nella patch. Opera esclusivamente su `ocr_support_compatibility_pach/`. Invoca `assemble_dualmode.py`, `scope_extractor.py` e `gui_validator.py`. Riceve il controllo solo dopo CP1 (approvazione modder).

**revisore-accessibilita.agent.md** — Verifica la qualità del container OCR: leggibilità da screen reader, presenza di tooltip, ordine di lettura logico, assenza di widget non descritti. Solo lettura e report. Può tornare all'Implementatore se rileva problemi.

**revisore-vanilla.agent.md** — Verifica che il container vanilla sia identico al file CK3 originale. Confronto binario: fedele o non fedele. Solo lettura. Può tornare all'Implementatore se rileva deviazioni.

**auditore-finale.agent.md** — Esegue la review pre-commit completa. Invoca `audit.py`, verifica scope whitelist, fedeltà vanilla, assenza di critici. Emette verdetto APPROVED o BLOCKED. Solo lettura. Il modder vede il verdetto prima che i revisori completino il passaggio (checkpoint CP2).

## Come si usa

Gli agenti si selezionano dal picker agenti in Copilot Chat (icona robot in VS Code, oppure `@NomeAgente` nel campo input). Si usano in sequenza nel workflow di conversione, oppure individualmente per task specifici.

Per invocare un agente: aprire Copilot Chat, selezionare l'agente dal picker, descrivere il task. L'agente legge le istruzioni dal suo file e opera entro i vincoli dichiarati.

Non modificare i file `.agent.md` durante una conversione attiva: i cambiamenti sono attivi alla sessione successiva.

## Dipendenze

- `.github/copilot-instructions.md` — regole globali lette da tutti gli agenti
- `.github/instructions/workflow-nuova-finestra.instructions.md` — workflow CP1/CP2
- `.github/instructions/patch-boundaries.instructions.md` — percorsi scrivibili
- `tools/` — script Python invocati da Analista, Implementatore e Auditore
- `tools/config.py` — path ai tre repository, necessario per tutti gli script
