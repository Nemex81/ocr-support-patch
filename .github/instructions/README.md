# .github/instructions — Istruzioni operative automatiche

Questa cartella contiene i file `.instructions.md` che Copilot carica automaticamente in base al tipo di file aperto o al contesto attivo.

## Descrizione

Le istruzioni qui definite si attivano tramite il frontmatter `applyTo:` senza bisogno di invocazione manuale. Quando Copilot apre o lavora su un file che corrisponde al pattern dichiarato, carica l'istruzione corrispondente nel contesto. Questo garantisce che le regole operative siano sempre presenti senza dover essere ripetute a ogni sessione.

Le istruzioni in questa cartella coprono tre aree principali: i confini operativi (cosa si può e non si può modificare), il workflow completo di conversione (sequenza agenti, checkpoint, passi tecnici), e le regole di codice Jomini (widget, scoping, template canonico, checklist pre-commit).

I file `.instructions.md` non si modificano durante una conversione attiva: le modifiche entrano in vigore alla sessione successiva. Non sono file di gioco e non devono mai essere copiati nella cartella mod.

## File presenti

**patch-boundaries.instructions.md** (applyTo: `**`) — Definisce i percorsi scrivibili e vietati per Copilot. Percorso scrivibile principale: `ocr_support_compatibility_pach/gui/`. Qualsiasi modifica fuori da questo percorso richiede conferma esplicita del modder. Include riferimento al file machine-readable `domain_boundaries.md`.

**workflow-nuova-finestra.instructions.md** (applyTo: `**`) — Sequenza operativa completa per la conversione di una finestra al sistema dual-mode. Include la tabella dei passi con i checkpoint CP1 e CP2, i comandi da eseguire, e le condizioni di STOP. Obbligatorio da seguire nell'ordine indicato.

**gui-jomini.instructions.md** (applyTo: `**/*.gui`) — Regole di codice Jomini per CK3 1.17.1: widget supportati, proprietà obbligatorie, template canonico dual-mode, checklist pre-commit. Si attiva automaticamente quando si apre o modifica un file `.gui`.

**gui-jomini-scopes.instructions.md** (applyTo: `**/*.gui`) — Regole di scope e binding Jomini. Definisce come verificare e dichiarare i binding, come usare la whitelist scope, e i vincoli specifici per CK3 1.17.1. Si attiva in coppia con `gui-jomini.instructions.md`.

**gui-conversion-progress.instructions.md** (applyTo: `**`) — Registro aggiornato di tutte le finestre del progetto: convertite e validate, in revisione, bloccanti, da escludere, da convertire. Da consultare prima di avviare qualsiasi nuova conversione per evitare duplicazioni o conflitti.

**localization-ocr.instructions.md** (applyTo: `**/localization/**/*.yml`) — Convenzioni di localizzazione per i file `.yml` della patch. Si attiva automaticamente sui file di localizzazione. Definisce chiavi, encoding, struttura e regole di naming.

## Come si usa

Non richiedono invocazione manuale. Copilot le carica in automatico. Per verificare quali istruzioni sono attive in una sessione, aprire Copilot Chat e chiedere "quali istruzioni sono attive?"

> Nota di compatibilità: l'attivazione automatica tramite `applyTo` richiede
> VS Code con GitHub Copilot in modalità agent mode. Su versioni stabili di
> VS Code o con Copilot in modalità chat standard il comportamento può
> differire. Prima di affidarsi all'attivazione automatica, verificare che
> agent mode sia abilitato nella configurazione Copilot.

Per aggiungere una nuova istruzione: creare un file `.instructions.md` in questa cartella con frontmatter YAML `applyTo: pattern`. La nuova istruzione sarà attiva alla sessione successiva. Prima di aggiungerla, verificare che non ci siano conflitti con istruzioni esistenti.

## Dipendenze

- `.github/copilot-instructions.md` — istruzioni globali, caricato prima di tutte le altre
- `.github/resources/domain_boundaries.md` — referenziato da `patch-boundaries.instructions.md`
- `.github/resources/jomini_scope_whitelist.md` — referenziato da `gui-jomini-scopes.instructions.md`
- `.github/resources/conversion-patterns.md` — referenziato da `workflow-nuova-finestra.instructions.md`
