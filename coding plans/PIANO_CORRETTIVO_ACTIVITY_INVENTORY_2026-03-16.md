# Piano Correttivo - Stabilizzazione Avvio Pre-Menu (Revisione 2026-03-17)
**Data analisi:** 17 marzo 2026
**Branch:** experiment/dual-mode-type-separation
**Metodo:** correlazione log runtime + confronto file tra repository patch e cartella mod live montata dal launcher.

---

## Sintesi esecutiva aggiornata

La causa primaria del blocco non e' piu' un errore dentro i file del repository patch, ma un **disallineamento di deploy**:

1. il repository contiene gia' le stringhe parser-safe in `frontend_main.gui` e `window_dynasty_legacy.gui`;
2. CK3 sta pero' caricando una cartella mod live incompleta (`Documents/.../mod/ocr_support_compatibility_pach/gui`) che non contiene quei due file;
3. in assenza dell'override patch, il gioco ricade sull'upstream OCR workshop, dove i due `\'` sono ancora presenti;
4. i lexer error risultanti sono i primi errori in `error.log` e sono coerenti con il sintomo "non arriva al menu principale".

Conclusione: la priorita' non e' riscrivere di nuovo i file nel repo, ma **riallineare la mod live al contenuto del repository**.

---

## Evidenze verificate

### 1) Errori iniziali nei log

`error.log` apre con:

- `gui/frontend_main.gui(355): Backslash followed by neither quote nor backslash`
- `gui/window_dynasty_legacy.gui(88): Backslash followed by neither quote nor backslash`

Questi restano i primi blocker GUI rilevati.

### 2) Stato reale dei file nel repository

Nel repository patch:

- `frontend_main.gui:355` contiene `Cannot` (non `Can\'t`)
- `window_dynasty_legacy.gui:88` contiene `Do not` (non `Don\'t`)

Quindi il fix lessicale in repo e' gia' presente.

### 3) Stato reale dei file nel layer live montato da CK3

La cartella live montata dal launcher risulta:

- esistente, ma con **24 file** GUI contro **35 file** nel repository;
- **mancanti**: `frontend_main.gui`, `window_dynasty_legacy.gui`, `window_army.gui`, `interaction_blackmail.gui`, vari file type-separati in `gui/vanilla/`;
- **presenti extra legacy** non allineati (esempio: `vanilla/00_temp_vanilla.gui`, `vanilla/window_title.gui`, zip di appoggio).

Questa differenza spiega perche' i fix presenti nel repo non vengono effettivamente caricati nel run.

### 4) Indicatore aggiuntivo di stack rumoroso

Resta nel log: `Invalid supported_version in file: mod/ugc_2848213069.mod line: 6`.

Non e' la causa primaria del blocco menu, ma rende i run meno puliti e va isolato in una fase successiva.

---

## Diagnosi aggiornata ordinata per probabilita'

### Causa primaria (alta confidenza)

**Deploy drift tra repository patch e cartella mod live caricata da CK3.**

Effetto diretto: gli override parser-safe non entrano nel VFS runtime.

### Causa contributiva (media confidenza)

**Stack mod non minimizzato**, con warning/rumore che complica l'analisi dei blocker iniziali.

### Cause secondarie (bassa priorita' adesso)

Errori datamodel/gui su finestre avanzate (`window_faith`, `window_character_lifestyle`, `window_county_view`, ecc.) da affrontare solo dopo il ripristino del menu.

---

## Piano operativo corretto

### Fase 0 - Baseline e congelamento ipotesi obsolete

1. Trattare il piano del 16/03 come storico.
2. Non riaprire subito `window_activity.gui` e `window_inventory.gui` come blocker avvio, salvo nuove evidenze nei primi errori.

Esito atteso: focus sui blocker reali del run corrente.

### Fase 1 - Riallineamento deploy (repo -> mod live)

1. Sincronizzare `ocr_support_compatibility_pach/gui/` del repository verso la cartella mod live montata da CK3.
2. Garantire la presenza live di almeno:
   - `frontend_main.gui`
   - `window_dynasty_legacy.gui`
   - file type-separati in `gui/vanilla/` richiesti dai wrapper correnti.
3. Eliminare o isolare file legacy extra non presenti nel repository che possono inquinare il caricamento.

Esito atteso: VFS runtime allineato allo stato reale del branch.

### Fase 2 - Smoke test bootstrap

1. Avvio con stack minimo consigliato: `vanilla + OCR Support + patch`.
2. Controllo immediato dei primi errori in `error.log`.
3. Verifica che spariscano i due lexer error su `frontend_main` e `window_dynasty_legacy`.

Esito atteso: superamento bootstrap e arrivo al menu principale.

### Fase 3 - Isolamento rumore mod stack

Matrice raccomandata:

1. vanilla puro
2. vanilla + OCR Support
3. vanilla + patch
4. vanilla + OCR Support + patch
5. configurazione reale completa

Per ogni run: acquisire `error.log`, `debug.log`, `gui_warnings.log`.

Esito atteso: separazione netta tra blocker primari e warning secondari.

### Fase 4 - Bonifica secondaria post-menu

Solo dopo ripristino menu:

1. parser/datamodel errors sulle finestre avanzate;
2. warning texture/localization non bloccanti.

---

## Convalida del piano corretto

Checklist di convalida:

1. I primi errori di log sono spiegati dal piano? **SI**
2. Le evidenze sui file correnti contraddicono il piano? **NO**
3. Le azioni proposte sono eseguibili senza toccare upstream OCR? **SI**
4. Il piano distingue chiaramente blocker bootstrap vs rumore secondario? **SI**
5. Esiste una verifica oggettiva post-fix (smoke test + log)? **SI**

**Esito convalida:** PASS

Con convalida PASS, e' autorizzata l'implementazione delle correzioni operative in ordine Fase 1 -> Fase 2.

---

## Cosa NON fare

1. Non modificare direttamente `CK3-OCR` upstream.
2. Non inseguire prima warning secondari se i primi errori restano lexer/pre-menu.
3. Non considerare il repository "a posto" senza verificare la cartella live realmente montata dal launcher.
4. Non dichiarare risolto senza conferma menu principale + nuovi log puliti sui blocker iniziali.

Se il menu torna a comparire:

- il vecchio piano su activity/inventory va archiviato come fase storica gia' risolta;
- il lavoro successivo si sposta dalla stabilizzazione avvio alla riduzione dei warning residui.

Se il menu non torna a comparire:

- il prossimo piano dovra' essere costruito esclusivamente sui **nuovi primi errori** del log successivo, non sul crash bundle storico 18:40.

---

## Conclusione

Il piano precedente era utile per spiegare il crash storico, ma oggi e' tecnicamente fuorviante se usato come guida operativa.

Lo stato reale del repository e dei log correnti indica che:

- `window_inventory.gui` e `window_activity.gui` non sono piu' il primo fronte da attaccare;
- i blocker attuali pre-menu sono due file OCR upstream con backslash illegale;
- la correzione giusta, compatibile con la patch, e' un override locale in `ocr_support_compatibility_pach/gui/` piu' un test con stack mod isolato.
