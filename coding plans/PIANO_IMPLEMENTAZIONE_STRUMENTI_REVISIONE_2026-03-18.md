# Piano Implementazione Strumenti Revisione Codice

Data: 2026-03-18
Stato: analisi esplorativa completata, nessuna implementazione avviata
Ambito: integrazione strumenti nel piano correzione errori GUI/CK3

## Obiettivo

Integrare in modo operativo istruzioni, regole, risorse, skills, agenti e script Python nel flusso di fix della patch, con uso deterministico per fase e tracciamento chiaro nel piano generale e nel TODO.

## 1) Esito analisi dei 2 file piano

File analizzati:
- coding plans/PIANO_GENERALE_CORREZIONE_LOG_2026-03-18.md
- coding plans/todo.md

Punti forti:
- buona priorita' per gravita' e correlazione errori
- fasi sequenziali corrette
- checklist operativa gia' presente

Gap rilevati:
- mancano note operative esplicite su quale strumento usare in ogni fase
- manca una procedura standard per il passaggio "analisi log -> file target -> validazione"
- manca una strategia formalizzata per i cluster non patchati (OCR upstream/vanilla)
- manca la definizione di un agente specializzato orientato ai cluster errore

## 2) Inventario strumenti disponibili (framework attuale)

### Istruzioni attive utili
- .github/instructions/gui-jomini.instructions.md
- .github/instructions/gui-jomini-scopes.instructions.md
- .github/instructions/workflow-nuova-finestra.instructions.md
- .github/instructions/patch-boundaries.instructions.md
- .github/instructions/gui-conversion-progress.instructions.md

### Risorse utili
- .github/resources/jomini_scope_whitelist.md
- .github/resources/dual_mode_pattern_canonical.md
- .github/resources/requirement-enforcement-matrix.md
- .github/resources/domain_boundaries.md
- .github/resources/conversion-patterns.md

### Skills utili
- .github/copilot-skills/deprecated-pattern-scanner.skill.md
- .github/copilot-skills/scope-whitelist-check.skill.md
- .github/copilot-skills/tri-repo-diff.skill.md
- .github/copilot-skills/vanilla-fidelity-check.skill.md
- .github/copilot-skills/accessibility-checklist-runner.skill.md

### Agenti utili
- .github/agents/implementatore-patch.agent.md
- .github/agents/revisore-accessibilita.agent.md
- .github/agents/revisore-vanilla.agent.md
- .github/agents/auditore-finale.agent.md
- .github/agents/analista-tri-repo.agent.md

### Script Python / toolchain utili
- tools/audit.py
- tools/gui_validator.py
- tools/scope_extractor.py
- tools/tri_diff.py
- tools/assemble_dualmode.py
- tools/repair_missing_types.py

### Script secondari utili ma non standardizzati
- tools/_analyze_errors.py
- tools/_check_vanilla_integrity.py
- tools/_deploy_sync.ps1
- tools/add_missing_toplevel_blocks.py

## 3) Note operative da integrare nel piano di implementazione patch

Queste note sono da applicare in ogni fase del piano generale.

### Nota operativa N1 - Ciclo minimo obbligatorio per ogni file toccato
- usare tools/gui_validator.py prima di edit
- applicare fix
- rieseguire tools/gui_validator.py dopo edit
- eseguire tools/scope_extractor.py
- aggiornare whitelist solo per binding verificati nel vanilla

### Nota operativa N2 - Verifica fedelta' vanilla per file ad alto rischio
- usare tools/tri_diff.py per window_faith, window_activity, window_county_view, window_character_lifestyle
- usare skill vanilla-fidelity-check per conferma rapida lato revisione

### Nota operativa N3 - Gate fase
- a fine fase usare tools/audit.py --window per ogni finestra toccata
- a fine blocco usare tools/audit.py --all come controllo cumulativo

### Nota operativa N4 - Copertura accessibilita'
- usare skill accessibility-checklist-runner dopo i fix OCR
- usare Revisore Accessibilita per sign-off di fase

### Nota operativa N5 - Gestione cluster non patchati
- usare skill tri-repo-diff + tools/tri_diff.py per distinguere errore patch vs upstream
- non fare fix nella patch se la causa e' solo upstream/non patchata

### Nota operativa N6 - Tracciamento
- aggiornare coding plans/todo.md a ogni step completato
- aggiornare checkbox fase nel piano generale solo dopo log post-fix

## 4) Mappatura Fasi -> Strumenti consigliati

### Fase 1 (quick wins)
- tools/gui_validator.py
- tools/scope_extractor.py
- skill deprecated-pattern-scanner
- tools/audit.py --window

### Fase 2 (window_faith)
- tools/tri_diff.py --window window_faith
- tools/gui_validator.py
- skill vanilla-fidelity-check
- skill scope-whitelist-check
- tools/audit.py --window window_faith

### Fase 3 (window_activity)
- tools/gui_validator.py
- tools/repair_missing_types.py (solo se emergono type mancanti)
- skill deprecated-pattern-scanner
- tools/audit.py --window window_activity

### Fase 4 (window_county_view)
- tools/tri_diff.py --window window_county_view
- tools/scope_extractor.py
- skill vanilla-fidelity-check
- tools/audit.py --window window_county_view

### Fase 5 (window_character_lifestyle)
- tools/tri_diff.py --window window_character_lifestyle
- tools/scope_extractor.py
- skill scope-whitelist-check
- tools/audit.py --window window_character_lifestyle

### Fase 6 (non patchati)
- tools/tri_diff.py
- skill tri-repo-diff
- Analista Tri-Repo

### Fase 7 (asset e residui)
- tools/audit.py --all
- script secondari di diagnostica (solo lettura)

## 5) Valutazione: servono nuovi strumenti?

Risposta breve: SI, ma solo per orchestrazione e non per reinventare la validazione.

Copertura attuale:
- valida per lint, scope, audit e confronto tri-repo

Gap reali ancora aperti:
- assenza di orchestratore unico phase-based
- assenza di parser log ufficiale che mappi errori direttamente alle fasi del piano
- assenza di agente specializzato esplicito per risoluzione cluster errori runtime

## 6) Strategia proposta per nuovi strumenti (senza implementazione ora)

### Strumento S1 - Orchestratore fase (script)
Proposta file:
- tools/phase_gate_runner.py

Funzione:
- dato nome fase e lista file target, esegue in sequenza validator/scope/audit
- produce report sintetico pass/fail per la fase

### Strumento S2 - Parser cluster log (script)
Proposta file:
- tools/log_cluster_phase_mapper.py

Funzione:
- legge logs/error.log + gui_warnings.log
- raggruppa errori per signature
- mappa ogni signature su fase del piano
- output markdown pronto per aggiornare todo

### Strumento S3 - Skill di supporto fase
Proposta file:
- .github/copilot-skills/phase-review-runner.skill.md

Funzione:
- standardizzare il prompt operativo per revisione di una fase
- richiamare gli script S1/S2 come pre-run suggerito

### Strumento S4 - Agente specializzato correzione errori
Proposta file:
- .github/agents/specialista-risoluzione-errori.agent.md

Funzione:
- usare in modo guidato istruzioni + skills + script
- target: risoluzione cluster di errori runtime, non conversione nuova finestra

## 7) Piano di implementazione degli strumenti proposti

### Fase T1 - Progettazione specifiche
- [ ] definire I/O di S1
- [ ] definire I/O di S2
- [ ] definire schema output markdown standard
- [ ] definire policy errori bloccanti vs warning

### Fase T2 - Integrazione documentale
- [ ] aggiornare piano generale con note operative N1-N6
- [ ] aggiornare todo con sezione "strumenti fase attiva"

### Fase T3 - Implementazione minima strumenti
- [ ] creare tools/phase_gate_runner.py
- [ ] creare tools/log_cluster_phase_mapper.py
- [ ] creare skill phase-review-runner
- [ ] creare agente specialista-risoluzione-errori

### Fase T4 - Validazione strumenti
- [ ] test su Fase 1 del piano attuale
- [ ] confronto output S2 con report log gia' creato
- [ ] eventuale tuning regole signature

### Fase T5 - Adozione operativa
- [ ] usare S1/S2 all'inizio e fine di ogni fase
- [ ] mantenere tracciamento checkbox piano+todo allineato agli output

## 8) Vincoli e prerequisiti

- Python disponibile nel terminale usato per tools/
- path in tools/config.py corretti
- nessuna modifica fuori confini autorizzati senza conferma esplicita

## 9) Decisione richiesta prima di procedere

Implementazione NON avviata.

Serve conferma del modder su quale percorso seguire:
- Opzione A: integrare subito solo note operative N1-N6 nei due file piano esistenti
- Opzione B: implementare anche strumenti nuovi S1/S2 + skill + agente specializzato
- Opzione C: fare prima un prototipo solo S2 (parser cluster log) e rimandare gli altri
