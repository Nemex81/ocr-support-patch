# tools — Script Python per assemblaggio, audit e validazione

Questa cartella contiene tutti gli script Python del framework. Sono gli strumenti eseguibili del progetto: assemblano i file dual-mode, validano la sintassi Jomini, estraggono binding, confrontano i tre repository e eseguono l'audit completo.

## Descrizione

Gli script in `tools/` sono il braccio operativo del framework. Mentre gli agenti Copilot pianificano e verificano, sono questi script a fare il lavoro concreto: generare i file `.gui` dual-mode, estrarre e aggiornare la whitelist scope, confrontare strutturalmente i tre repository, validare la sintassi, e produrre il verdetto di audit.

Tutti gli script importano i path da `config.py`. Non devono mai contenere path hardcodati. Il file `config.py` è la fonte di verità per tutti i percorsi ai tre repository.

Gli script sono pensati per essere invocati da riga di comando (o dal terminale integrato di VS Code) dagli agenti Copilot nel corso del workflow. Alcuni script (`assemble_dualmode.py`, `audit.py`) supportano il flag `--dry-run` per produrre output senza scrivere file: questo è il meccanismo del checkpoint CP1.

## File presenti

**config.py** — Centralizza tutti i path ai tre repository: patch attiva (`PATCH_GUI`), OCR upstream (`OCR_GUI`), vanilla GitHub (`VANILLA_GUI`), installazione CK3 locale (`CK3_INSTALL_GUI`), whitelist scope (`WHITELIST_PATH`). Tutti gli altri script lo importano. Eseguirlo direttamente mostra lo stato (EXISTS/MISSING) di ogni path.

**assemble_dualmode.py** — Script generico per assemblare qualsiasi finestra in dual-mode. Prende il file OCR upstream e il file vanilla, li combina aggiungendo le `visible` mutuamente esclusive. Flag: `--window nome_file`, `--mode A|B|C|D`, `--dry-run` (stampa senza scrivere). Output: file `.gui` in `ocr_support_compatibility_pach/gui/`.

**assemble_army_dualmode.py** — Versione specializzata di `assemble_dualmode.py` per `window_army.gui`. Mantenuta separatamente per gestire strutture particolari di quella finestra. Da non generalizzare: usare `assemble_dualmode.py` per tutte le altre finestre.

**audit.py** — Gate completo pre-commit. Esegue: validazione strutturale Jomini (via `gui_validator.py`), verifica binding contro whitelist scope, confronto fedeltà vanilla. Emette verdetto BLOCCANTE, CON AVVERTENZE o OK. Flag: `--window nome_file`, `--all` (tutte le finestre nella patch). Output: report testuale con critici, avvertenze, binding assenti.

**gui_validator.py** — Lint strutturale dei file `.gui`. Verifica: bilanciamento parentesi graffe, presenza `visible` nei container dual-mode, `tooltip` su ogni button interattivo, assenza di pattern deprecati. Classificazione errori: CRITICO (blocca commit), ATTENZIONE (richiede verifica). Usabile standalone o invocato da `audit.py`.

**scope_extractor.py** — Estrae tutti i binding `[...]` da un file `.gui` e li confronta con `jomini_scope_whitelist.md`. Aggiunge alla whitelist i binding ASSENTI dopo verifica nel vanilla. Flag: `--file percorso`. Output: lista binding classificati e aggiornamento automatico della whitelist.

**tri_diff.py** — Confronto strutturale tra i tre repository per una finestra specifica. Legge il file corrispondente in patch, OCR upstream e vanilla, produce un report con le sezioni presenti in ciascuno e le differenze. Flag: `--window nome_file`. Output: report strutturato per sezioni widget.

**annotate_datamodels.py** — Strumento di manutenzione per aggiungere annotazioni datamodel ai file `.gui`. Usato occasionalmente per aggiunte in blocco, non nel workflow standard di conversione.

**_commit_msg.txt** — File di testo con template per i messaggi di commit del progetto. Non è uno script.

## Come si usa

Tutti gli script si invocano da riga di comando dalla radice del repository. Esempi:

```
python tools/tri_diff.py --window window_title
python tools/assemble_dualmode.py --window window_title --mode C --dry-run
python tools/assemble_dualmode.py --window window_title --mode C
python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/window_title.gui
python tools/audit.py --window window_title
python tools/config.py
```

Il flag `--dry-run` su `assemble_dualmode.py` stampa il file che verrebbe generato senza scriverlo: questo è il meccanismo obbligatorio del checkpoint CP1.

Non modificare `config.py` per aggiungere path temporanei: usarlo solo per i path permanenti ai quattro repository.

## Dipendenze

- Python 3.11 o superiore
- `config.py` configurato correttamente con i path ai tre repository locali
- `.github/resources/jomini_scope_whitelist.md` — letta e aggiornata da `scope_extractor.py`
- I repository nel workspace: patch (`ocr_support_compatibility_pach/`), OCR upstream (`../CK3-OCR/`), vanilla (installazione CK3 locale — `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/`)
