# .github/prompts — Prompt riutilizzabili per task frequenti

Questa cartella contiene i file `.prompt.md` che incapsulano istruzioni pronte per i task di sviluppo più ricorrenti nella patch.

## Descrizione

I prompt qui definiti si usano come punti di partenza rapidi in Copilot Chat o nel picker di VS Code. Differiscono dalle istruzioni (che si attivano automaticamente) perché si invocano deliberatamente quando si vuole eseguire un task specifico.

Ogni prompt è progettato per un caso d'uso singolo e ben definito. Contiene il contesto necessario, i tool abilitati, il modello consigliato e le istruzioni operative per il task. Usare i prompt riduce il tempo di setup a inizio sessione e garantisce coerenza tra sessioni diverse.

I prompt non sostituiscono il workflow completo definito in `workflow-nuova-finestra.instructions.md`. Sono strumenti complementari: il workflow governa la sequenza, i prompt accelerano l'esecuzione dei singoli passi.

## File presenti

**converti-finestra-dual-mode.prompt.md** — Punto di ingresso per la conversione di una singola finestra al sistema dual-mode OCR/Vanilla. Rispetta il vincolo "una finestra alla volta". Copre i passi dal tri_diff all'audit. Da usare dopo aver verificato la tabella di esclusione in `copilot-instructions.md`.

**analizza-finestra.prompt.md** — Analizza la struttura di una finestra GUI e produce un report: widget presenti, binding usati, differenze strutturali tra i tre repository. Input: nome file. Output: report testuale.

**verifica-dual-mode.prompt.md** — Verifica la correttezza del sistema dual-mode in un file già convertito: presenza delle due `visible` mutuamente esclusive, parità funzionale OCR/vanilla, assenza di pattern vietati.

**fix-bloccante.prompt.md** — Risolve i CRITICO aperti in una finestra nella sezione "Bloccanti" del tracker. Invoca l'Implementatore Patch. Usare quando `audit.py` ha riportato critici aperti che bloccano il commit.

**genera-container-ocr.prompt.md** — Genera il container OCR per una sezione specifica di una finestra. Da usare quando la conversione riguarda solo una parte del file, non la finestra intera. Richiede il sorgente OCR upstream Agamidae come riferimento.

**debug-errore-jomini.prompt.md** — Analizza un errore Jomini dai log CK3 e propone un fix. Input: testo dell'errore o riga del log. Output: diagnosi e modifica suggerita. Non scrive file: produce la proposta da valutare prima dell'applicazione.

**aggiornamento-upstream.prompt.md** — Confronta la patch con l'upstream OCR Agamidae e con il vanilla per rilevare aggiornamenti del gioco che richiedono adeguamento della patch. Da usare dopo un aggiornamento di CK3 o dell'upstream.

## Come si usa

In Copilot Chat: aprire il picker prompt (icona documento con matita in VS Code), selezionare il prompt desiderato. In alternativa, aprire il file `.prompt.md` e usare il pulsante "Run" in VS Code Insiders.

Ogni prompt può ricevere input aggiuntivi nel campo di testo dopo la selezione. Esempio: selezionare `converti-finestra-dual-mode` e aggiungere `window_title.gui mode C`.

## Dipendenze

- `.github/instructions/workflow-nuova-finestra.instructions.md` — il workflow completo a cui i prompt si appoggiano
- `.github/instructions/patch-boundaries.instructions.md` — rispettato da tutti i prompt che scrivono file
- `tools/` — script Python invocati dai prompt tramite terminal
- I tre repository nel workspace (patch, OCR upstream, vanilla) — necessari per i prompt di analisi e confronto
