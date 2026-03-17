# Report diagnostico - CK3 blocco in debug mode

Data analisi: 2026-03-16
Workspace analizzati (cross-source):
- Patch attiva: `ocr_support_compatibility_pach/gui/`
- OCR upstream: `../CK3-OCR/OCR-Support/gui/`
- Vanilla CK3: `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/`
- Runtime logs: `~/Documents/Paradox Interactive/Crusader Kings III/logs/`
- Crash bundle: `~/Documents/Paradox Interactive/Crusader Kings III/crashes/ck3_20260316_184236/`

---

## 1) Sintesi esecutiva

Il blocco in debug mode non appare come un singolo errore isolato, ma come **effetto cumulativo** di:

1. **Errori parser GUI massivi e ripetuti** in fase bootstrap (pre-menu), con sintomi di file non perfettamente validi in CK3 1.17.1.
2. **Incoerenze tra sorgenti mod attive** (patch + OCR Support workshop/upstream + altre mod abilitate) che amplificano warning/errori e possono rompere alcuni tipi/widget.
3. **Crash finale audio FMOD** (`EXCEPTION_ACCESS_VIOLATION`) probabilmente secondario a stato runtime degradato o shutdown non pulito.

Conclusione tecnica: la causa più probabile è un **mix di incompatibilità sintattiche GUI + conflitto/overlay di mod**, che in modalità debug viene esposto in modo più severo (log spam + parser strict path), fino a freeze/crash.

---

## 2) Evidenze principali dai log

### 2.1 Errori lessicali (backslash) già in bootstrap GUI
Da `error.log`:
- `gui/frontend_main.gui(355): Backslash followed by neither quote nor backslash`
- `gui/window_dynasty_legacy.gui(88): Backslash followed by neither quote nor backslash`
- `gui/window_inventory.gui(378): Backslash followed by neither quote nor backslash`

Confronto tri-source:
- `frontend_main.gui` non esiste nella patch, esiste in OCR upstream: riga compatibile con stringa `Can\'t`.
- `window_dynasty_legacy.gui` non è in patch, presente in OCR upstream: riga compatibile con `Don\'t`.
- `window_inventory.gui` è in patch e contiene `Don\'t` (`raw_text`).

Interpretazione: presenza di escaping con backslash in contesti che il lexer CK3 segnala come non validi.

### 2.2 Errori strutturali su window_activity
Da `error.log` e `gui_warnings.log`:
- Duplicate property `text` in `window_activity.gui` (linee 412, 498)
- Duplicate property `visible` (linea 681)
- Cascata di `not a valid widget/type/property` (es. da linea 771 in poi)

Confronto su file patch:
- In `window_activity.gui` sono presenti pattern anomali coerenti con i messaggi runtime, tra cui:
  - proprietà duplicate nello stesso blocco (`datacontext` ripetuto)
  - token anomalo `, = {}`

Questa combinazione è tipica di parse desync: dopo il primo punto di rottura, molti token successivi vengono interpretati come proprietà invalide.

### 2.3 Errori data binding / funzioni non risolte
Nei log compaiono molte voci del tipo:
- `Could not find data system function ...`
- `Failed converting statement ...`
- esempi su `window_faith.gui`, `window_character_lifestyle.gui`, `window_county_view.gui`.

Sono coerenti con espressioni non riconosciute in quel contesto/versione o con data context non valido dopo parse failure.

### 2.4 Segnali audio e crash finale
Nel bundle crash:
- `exception.txt`: `Unhandled Exception C0000005 (EXCEPTION_ACCESS_VIOLATION)` in `fmodstudio.dll`
- `error.log`/`debug.log` verso fine sessione:
  - `audio2_fmod.cpp:312: PdxAudio2: release system error (An invalid parameter was passed...)`

Interpretazione: il crash avviene nello stack audio, ma dopo una lunga fase con centinaia/migliaia di errori GUI/script.

---

## 3) Evidenze cross-source (patch vs OCR upstream vs vanilla)

### 3.1 File non patchati ma segnalati in errore
- `frontend_main.gui` e `window_dynasty_legacy.gui` non sono nella patch.
- Le segnalazioni quindi puntano a file provenienti da OCR Support/mod attive esterne alla patch.

### 3.2 File patchati con pattern a rischio parser
- `window_inventory.gui` (patch): stringa con `Don\'t`.
- `window_activity.gui` (patch): duplicati e token `, = {}` coerenti con errori runtime.

### 3.3 Vanilla come baseline
- Le sezioni vanilla corrispondenti non mostrano gli stessi pattern lessicali/anomali letti nelle versioni OCR/patch.

---

## 4) Ipotesi causale ordinata per probabilità

1. **Primaria (alta probabilità)**: errori sintattici/strutturali GUI in file OCR/patch (`window_activity`, `window_inventory`, altri) che in debug mode causano degrado grave in bootstrap GUI.
2. **Contributiva (alta probabilità)**: conflitto/stratificazione mod (OCR workshop + patch + traduzione + possibili override condivisi) con type/widget non allineati.
3. **Secondaria (media probabilità)**: crash FMOD come conseguenza (non necessariamente causa iniziale) di stato runtime compromesso.

---

## 5) Perché normale sembra avviarsi e debug no

Spiegazione plausibile (compatibile con i log):
- In avvio normale, parte degli errori può restare non bloccante e l'utente percepisce avvio corretto.
- In debug mode, il motore produce più controlli/tracing e amplifica errori parser/datasystem, con forte impatto su bootstrap e stabilità.
- Il risultato percepito è freeze pre-menu o crash precoce.

---

## 6) Strategia di risoluzione (senza modifiche in questa sessione)

### Fase A - Isolamento riproducibile (obbligatoria)
1. Eseguire una matrice di avvio debug con profilo mod controllato:
   - A1: solo vanilla
   - A2: vanilla + OCR Support (workshop)
   - A3: vanilla + patch (se possibile senza workshop)
   - A4: vanilla + OCR Support + patch
   - A5: A4 + traduzione italiana
2. Per ogni run, salvare `error.log`, `debug.log`, `gui_warnings.log` con timestamp separato.
3. Obiettivo: individuare la combinazione minima che introduce i parser error bloccanti.

### Fase B - Bonifica parser (priorità alta)
1. Correggere stringhe con apostrofo in contesti problematici (`Can\'t`, `Don\'t`) usando forma parser-safe CK3 1.17.1.
2. Eliminare token anomali `, = {}` dove non supportati.
3. Rimuovere proprietà duplicate nello stesso blocco (`datacontext`, `text`, `visible` duplicati).
4. Validare i file più rumorosi prima: `window_activity.gui`, `window_inventory.gui`, `window_faith.gui`, `window_character_lifestyle.gui`.

### Fase C - Allineamento multi-sorgente
1. Verificare per ogni file problematico quale sorgente deve essere autoritativa:
   - patch dual-mode
   - OCR upstream
   - vanilla
2. Evitare mix ibridi nello stesso file che introducono sintassi divergente.

### Fase D - Re-test tecnico
1. Re-test debug su combinazione minima corretta.
2. Confermare riduzione drastica in `gui_warnings.log` e assenza errori lessicali early bootstrap.
3. Solo dopo stabilizzazione GUI, ri-valutare eventuale residuo audio FMOD.

---

## 7) Rischi e priorità operative

Priorità immediata:
- parser/lexer GUI (bloccante funzionale in debug)

Priorità successiva:
- coerenza mod stack e override

Priorità finale:
- audio FMOD (potrebbe sparire dopo bonifica parser)

---

## 8) Limiti tecnici incontrati in questa sessione

Gli script Python del framework (`tools/audit.py`, `tools/gui_validator.py`, `tools/tri_diff.py`) non sono eseguibili in questo ambiente perché né `python` né `py` risultano installati/configurati nel terminale corrente.

Impatto:
- la diagnosi è stata fatta con evidenze dirette da log e confronto file cross-source;
- manca il verdetto automatico degli script in questa sessione.

---

## 9) Conclusione

Il problema in debug mode è altamente coerente con una **degradazione parser GUI multi-file** (non un singolo bug puntuale), aggravata da **sovrapposizione mod** e seguita da crash audio FMOD. La via più efficace è isolare la combinazione minima e bonificare prima i file GUI ad alta rumorosità (in primis `window_activity.gui`), poi ri-testare debug.
