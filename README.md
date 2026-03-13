# OCR Support Patch — CK3 Accessibility Mod

Mod per Crusader Kings III (v1.17.1) che aggiunge accessibilità per utenti non vedenti tramite screen reader (NVDA, JAWS, Narrator).

## Cos'è la mod

OCR Support Patch implementa un sistema **Dual Mode** sull'interfaccia CK3:

- **Modalità OCR** (variabile `ocr` assente): layout testuale lineare, leggibile da screen reader. Attiva per impostazione predefinita.
- **Modalità Vanilla** (variabile `ocr` presente): layout grafico originale Paradox, identico alla versione non moddificata.

Il giocatore può passare da una modalità all'altra in qualsiasi momento premendo **Shift+F11** durante la partita. Le due modalità sono funzionalmente equivalenti: nessuna funzione è disabilitata in nessuna delle due viste.

## A chi è destinata

A chiunque utilizzi uno screen reader per giocare a Crusader Kings III. La mod non modifica logica di gioco, valori, eventi o bilancio: agisce esclusivamente sull'interfaccia grafica.

## Come si installa

1. Scarica o clona questo repository.
2. Copia la cartella `ocr_support_compatibility_pach/` nella directory mod di CK3 (`Documents/Paradox Interactive/Crusader Kings III/mod/`).
3. Copia il file `ocr support compatibilty pach.mod` nella stessa directory.
4. Avvia il launcher CK3, attiva la mod insieme a **OCR Support** di Agamidae (dipendenza obbligatoria).

La mod richiede anche la mod **OCR Support** di Agamidae (upstream), da installare separatamente. I due mod lavorano insieme: OCR Support fornisce la logica di accessibilità di base, questa patch aggiunge la compatibilità dual-mode sulle finestre principali.

## Struttura del repository

Il repository è diviso in due domini distinti:

- **Mod** (`ocr_support_compatibility_pach/`): i file `.gui` della patch attiva, il font, le localizzazioni. Questo è ciò che viene installato nel gioco.
- **Framework** (`.github/` e `tools/`): strumenti di sviluppo, istruzioni operative, agenti Copilot, script Python per l'assemblaggio e la validazione. Non viene installato nel gioco.

## Documentazione del framework

Per chi contribuisce allo sviluppo:

- `.github/README.md` — panoramica del sistema di sviluppo assistito da AI
- `.github/agents/README.md` — agenti Copilot specializzati per ruolo
- `.github/copilot-skills/README.md` — skill invocabili in Copilot Chat
- `.github/instructions/README.md` — istruzioni attive per dominio e file
- `.github/prompts/README.md` — prompt riutilizzabili per task comuni
- `.github/resources/README.md` — pattern canonici, whitelist scope, regole
- `.github/workflows/README.md` — automazioni GitHub Actions
- `tools/README.md` — script Python per assemblaggio, audit e validazione

## Dipendenze

- CK3 versione 1.17.1
- Mod OCR Support di Agamidae (upstream, richiesta)

