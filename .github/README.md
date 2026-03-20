# .github — Framework di sviluppo OCR Support Patch

Questa cartella contiene tutto il sistema di sviluppo assistito da AI per il progetto OCR Support Patch. Non contiene file di gioco.

## Descrizione

La cartella `.github/` è il cuore del framework. Ospita le istruzioni operative che Copilot legge automaticamente, gli agenti specializzati invocabili dal picker di VS Code, le skill disponibili in Copilot Chat, i prompt riutilizzabili per i task ricorrenti, e le risorse di riferimento (pattern canonici, whitelist scope, regole modello).

Il framework è pensato per assistere un modder non vedente: ogni componente è progettato in modo che l'AI possa operare con autonomia controllata, rispettando checkpoint manuali obbligatori prima di scrivere file nella patch.

## Confini di accesso (policy globale)

Nel workspace multi-root corrente:

- Scrittura consentita solo nella root patch `C:/Users/nemex/OneDrive/Documenti/GitHub/ocr-support-patch/`
- Sola lettura obbligatoria su:
	- `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/`
	- `C:/Users/nemex/OneDrive/Documenti/GitHub/CK3-OCR/`
	- `C:/Users/nemex/OneDrive/Documenti/Paradox Interactive/Crusader Kings III/logs/`

All'interno della root patch, i percorsi effettivamente scrivibili restano quelli definiti in `patch-boundaries.instructions.md`.

## File presenti

**copilot-instructions.md** — Istruzioni globali del progetto. Caricate automaticamente da Copilot ad ogni sessione. Definiscono identità, percorsi, principi irrinunciabili, distinzione framework/mod, agenti disponibili e note operative.

## Sottocartelle

**agents/** — Definizioni degli agenti Copilot specializzati per ruolo nel workflow di conversione.

**copilot-skills/** — Skill invocabili in Copilot Chat con il prefisso `#nome-skill`. Contengono logica di analisi e verifica riutilizzabile.

**instructions/** — File `.instructions.md` attivati automaticamente da Copilot in base al pattern `applyTo`. Regolano comportamento, percorsi scrivibili, workflow e convenzioni per tipo di file.

**prompts/** — Prompt `.prompt.md` riutilizzabili per i task più frequenti (converti finestra, verifica dual mode, debug errore Jomini, ecc.).

**resources/** — Pattern canonici, whitelist scope Jomini, regole modello, liste priorità, conversion patterns. File di riferimento statici consultati da script e agenti.

**workflows/** — GitHub Actions. Esegue automaticamente `audit.py` su ogni push che modifica file `.gui` nella patch.

## Come si usa

Questa cartella non si usa direttamente: Copilot e VS Code la leggono in automatico quando apri il workspace. Le istruzioni in `instructions/` si attivano per `applyTo`, gli agenti appaiono nel picker agenti, le skill sono disponibili con `#nome-skill` in Copilot Chat.

Il file `copilot-instructions.md` è il punto di ingresso globale: viene caricato ad ogni sessione e definisce tutto il comportamento di base.

Per modificare le istruzioni, aprire il file corrispondente e editarlo. Le modifiche sono attive alla sessione successiva.

## Dipendenze

- VS Code con estensione GitHub Copilot abilitata
- Account GitHub con Copilot attivo (piano Individual, Business o Enterprise)
- Python 3.11+ installato (richiesto per gli script in `tools/` invocati dagli agenti)
- `tools/config.py` configurato correttamente con i path ai repository usati in consultazione (patch, CK3 vanilla, CK3-OCR)
