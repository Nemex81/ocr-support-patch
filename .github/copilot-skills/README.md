# .github/copilot-skills — Skill Copilot riutilizzabili

Questa cartella contiene le skill invocabili in Copilot Chat con la sintassi `#nome-skill`. Ogni skill incapsula logica di analisi o verifica specifica per il progetto.

## Descrizione

Le skill sono unità di conoscenza o procedura riutilizzabili, indipendenti dal contesto di conversazione corrente. Differiscono dagli agenti per granularità: dove un agente gestisce un intero flusso di lavoro, una skill esegue un singolo controllo o genera un singolo artefatto.

Gli agenti invocano le skill nel proprio flusso. Per esempio, l'Auditore Finale usa `#vanilla-fidelity-check` e `#scope-whitelist-check` come parte del suo processo di review. Ma le skill possono anche essere invocate direttamente in Copilot Chat senza passare per un agente.

Tutte le skill in questa cartella sono in sola lettura rispetto alla mod: producono report, analisi o template, ma non scrivono mai file nella patch direttamente.

## File presenti

**accessibility-checklist-runner.skill.md** — Esegue la checklist completa di accessibilità NVDA su un file `.gui` convertito. Verifica ogni punto in modo automatico e produce un report pass/fail con riferimento alla riga del file. Input: percorso file `.gui`. Output: report strutturato per punti.

**deprecated-pattern-scanner.skill.md** — Scansiona un file `.gui` e segnala tutti i pattern deprecati, vietati o pericolosi per CK3 1.17.1 e per il sistema dual-mode. Include il pattern `GameRules.GetRule('ocr_accessibility_mode')` che non deve mai essere usato. Output: tabella con riga, pattern trovato, gravità, fix consigliato.

**dual-mode-template-generator.skill.md** — Genera lo scheletro Jomini dual-mode completo per una finestra CK3. Da usare SOLO per finestre senza sorgente OCR esistente nell'upstream Agamidae. Per le finestre normali preferire `assemble_dualmode.py --dry-run` che estrae contenuto reale dai file sorgente.

**scope-whitelist-check.skill.md** — Data una lista di binding Jomini, verifica la loro presenza in `.github/resources/jomini_scope_whitelist.md`. Classifica ogni binding come PRESENTE, ASSENTE o DA VERIFICARE. Input: lista binding. Output: tabella classificazione.

**tri-repo-diff.skill.md** — Legge il file `.gui` corrispondente nei tre repository (patch attiva, OCR upstream Agamidae, vanilla CK3 originale) e produce un report strutturato con le differenze per sezioni widget. Alternativa leggera a `tri_diff.py` per confronti rapidi.

**vanilla-fidelity-check.skill.md** — Confronta il container vanilla nel file della patch con il corrispondente file CK3 originale. Emette PASS o FAIL con lista delle differenze non autorizzate. Verifica binaria: il container vanilla deve essere identico all'originale senza alcuna modifica.

## Come si usa

In Copilot Chat digitare `#nome-skill` (senza estensione del file) per caricare la skill nel contesto. Poi descrivere il task.

Esempio: `#scope-whitelist-check verifica i binding di window_title.gui`

Le skill possono essere combinate nella stessa sessione. Esempio: invocare `#deprecated-pattern-scanner` e poi `#vanilla-fidelity-check` sullo stesso file.

## Dipendenze

- `.github/resources/jomini_scope_whitelist.md` — richiesta da `scope-whitelist-check`
- `.github/resources/dual_mode_pattern_canonical.md` — pattern di riferimento usato da `dual-mode-template-generator`
- I tre repository nel workspace (patch, OCR upstream, vanilla) — richiesti da `tri-repo-diff` e `vanilla-fidelity-check`
