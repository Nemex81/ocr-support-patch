# .github/workflows — Automazioni GitHub Actions

Questa cartella contiene i workflow GitHub Actions che eseguono controlli automatici sulla patch a ogni push.

## Descrizione

I workflow qui definiti si attivano automaticamente su eventi GitHub (push, pull request). Costituiscono il gate di qualità automatico del progetto: ogni volta che si modificano file `.gui` nella patch, l'audit viene eseguito senza necessità di intervento manuale.

Questo livello di automazione è complementare al workflow manuale CP1/CP2: il controllo manuale garantisce che solo file approvati vengano scritti, il workflow automatico garantisce che i file scritti siano sempre nello stato atteso anche dopo modifiche successive.

I workflow operano in sola lettura rispetto alla patch: leggono i file, eseguono `audit.py`, e riportano il risultato come check GitHub. Non modificano file, non fanno commit, non pubblicano nulla.

## File presenti

**gui_audit.yml** — Workflow "GUI Audit". Si attiva su push che modificano file in `ocr_support_compatibility_pach/gui/`. Esegue `python tools/audit.py --all` su un runner Ubuntu con Python 3.11. Richiede checkout del repo e setup Python. In caso di critici aperti, il check fallisce e il push risulta bloccato (se configurato come required check).

## Come si usa

Il workflow si attiva automaticamente a ogni push. Non richiede invocazione manuale.

Per controllare i risultati: andare su GitHub → repository → Actions → "GUI Audit". Il check mostra output completo di `audit.py` con critici, avvertenze e binding assenti per ogni file `.gui` modificato.

Per aggiungere un nuovo workflow: creare un file `.yml` in questa cartella con il frontmatter `on:` e `jobs:` standard di GitHub Actions.

Per testare `audit.py` in locale prima del push, eseguire dal terminale nella radice del repo:

```
python tools/audit.py --all
```

oppure per un singolo file:

```
python tools/audit.py --window nome_finestra
```

## Dipendenze

- `tools/audit.py` — script principale invocato dal workflow
- `tools/config.py` — path configurati; il runner Ubuntu non ha accesso ai path locali Windows, quindi `audit.py` deve gestire gracefully i path mancanti
- `ocr_support_compatibility_pach/gui/` — percorso che triggerizza il workflow su push
- Python 3.11 sul runner GitHub Actions (ubuntu-latest)
