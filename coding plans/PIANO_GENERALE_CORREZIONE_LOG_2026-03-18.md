# Piano Generale Correzione Errori Log CK3

Data: 2026-03-18
Branch: experiment/dual-mode-type-separation
Stato: preparazione completata, in attesa di conferma prima dell'implementazione

## Obiettivo

Ridurre gli errori runtime di CK3 in modo ordinato, intervenendo per gruppi coerenti di problemi, separati per fonte/mod collegata, correlazione tecnica e gravita'.

Questo piano sostituisce i vecchi tentativi presenti in `coding plans`.
Le informazioni utili dei piani precedenti sono state assorbite qui, senza portarci dietro ipotesi ormai troppo strette o obsolete.

## Regola operativa obbligatoria

- [ ] Procedere in implementazione seguendo questo piano in ordine di fase, senza saltare avanti salvo nuova evidenza forte nei log.
- [ ] Aggiornare la checkbox della fase subito dopo il completamento effettivo della fase.
- [ ] Aggiornare anche `coding plans/todo.md` durante la fase attiva, voce per voce.
- [ ] Non iniziare l'implementazione finche' non arriva conferma esplicita del modder.

## Visione generale dei problemi rilevati

### A. Patch diretta: file GUI coperti dalla patch

Questa e' l'area primaria di intervento. Qui cade la parte maggiore del rumore runtime.

1. Critico, cluster parser/struttura:
   - `window_activity.gui`
   - correlazione: duplicate property, token letti come proprieta' invalide, parse desync a cascata
   - impatto: massimo, perche' genera centinaia di errori secondari

2. Critico, cluster espressioni visibilita'/data statement:
   - `window_faith.gui`
   - correlazione: `Isnt/Has/Or` in combinazioni che il motore sta degradando in errori `IsNot/HasNot`
   - impatto: molto alto, errore ripetitivo e concentrato

3. Alto, cluster datacontext/type/localize:
   - `window_county_view.gui`
   - correlazione: `GUIBuildingItem`, `Building.HasVariants`, `Title.GetAverageFertilityDesc`
   - impatto: alto, ma confinato a una finestra specifica

4. Alto, cluster datacontext/type/localize:
   - `window_character_lifestyle.gui`
   - correlazione: `PerkGuiItem`, `PerkTreeItem`, `FocusItem`, testo localizzato con funzioni non risolte
   - impatto: alto, ma meno rumoroso dei due cluster P0

5. Medio-alto, cluster minimo ma pulito da correggere:
   - `window_decisions.gui`
   - correlazione: `Select_CVector2f` e vettori stringati
   - impatto: limitato, ma fix veloce e a basso rischio

6. Medio, cluster lessicale/localizzazione rapida:
   - `frontend_main.gui`
   - `window_dynasty_legacy.gui`
   - `window_inventory.gui`
   - `interaction_modify_vassal_window.gui`
   - parte di `window_faith.gui`
   - correlazione: backslash non parser-safe, chiavi testo non localizzate, stringhe brevi non corrette
   - impatto: singoli errori rapidi da eliminare

### B. OCR upstream + vanilla, file non patchati

Questa area va affrontata dopo la stabilizzazione dei file patchati, perche' oggi puo' essere in parte rumore indotto.

1. Medio:
   - `window_activity_locale.gui`
   - `window_hybridize_culture.gui`
   - `window_manage_tax_slots.gui`
   - correlazione: widget/type mancanti o non risolti

2. Medio:
   - `preload/00_types_OCR.gui`
   - `_OCR_WIDGET.gui`
   - correlazione: dipendenze OCR-only, plugin widget, game view non risolta

### C. Asset, overlay, e residui non GUI

1. Medio:
   - texture mancanti (`icon_fertility.dds`, `icon_variants.dds`, ecc.)
   - possibile effetto secondario oppure asset realmente non presenti nello stack attivo

2. Basso-medio:
   - `game.log` con errori culture/succession
   - da trattare solo dopo bonifica GUI

## Strategia generale di esecuzione

Il piano parte dalle correzioni piu' semplici e rapide, anche se non sempre sono le piu' gravi in assoluto, per ottenere subito riduzione del rumore e una baseline piu' leggibile. Successivamente si passa ai cluster strutturali piu' complessi.

## Fasi operative

### Fase 1 - Quick wins e pulizia immediata

- [ ] Fase 1 completata

Obiettivo:
ridurre in poco tempo gli errori piu' isolati, semplici e a basso rischio, cosi' da pulire i log prima di intervenire sui cluster strutturali maggiori.

Ambito:
- patch diretta
- errori lessicali/localizzazione/minimumsize
- singoli fix senza refactor pesante

Gruppi inclusi:
- `frontend_main.gui` e `window_dynasty_legacy.gui`: verifica definitiva delle stringhe parser-safe nel contenitore effettivamente usato dalla patch
- `window_inventory.gui`: correzione lessicale del backslash non parser-safe
- `interaction_modify_vassal_window.gui`: testo non localizzato o proprieta' da convertire a `raw_text`
- `window_faith.gui`: testi letterali brevi non localizzati (`CLOSE_WINDOW`, `BACK`, `,`) se presenti nel ramo patchato
- `window_decisions.gui`: correzione `Select_CVector2f` e vettori stringati

Esito atteso:
- rimozione dei blocker lessicali rapidi
- riduzione del rumore localize/minimumsize
- log piu' puliti per leggere meglio i cluster successivi

### Fase 2 - Stabilizzazione mirata di window_faith.gui

- [ ] Fase 2 completata

Obiettivo:
isolare e correggere il gruppo coerente di errori sulle condizioni di `visible`, mantenendo fedelta' dual-mode e compatibilita' CK3 1.17.1.

Ambito:
- patch diretta
- file singolo, cluster coerente, severita' alta

Gruppi inclusi:
- espressioni `Isnt/Has/Or` collegate ai tab `faith_view_tabs`, `doctrine`, `doctrines`, `faith_followers_sort`
- eventuali effetti collaterali di localizzazione causati dal parse fallito del contenitore

Esito atteso:
- forte abbattimento degli errori concentrati su `window_faith.gui`
- separazione netta tra problemi del file e residui esterni

### Fase 3 - Stabilizzazione strutturale di window_activity.gui

- [ ] Fase 3 completata

Obiettivo:
correggere il cluster piu' rumoroso del progetto, partendo dai primi punti di rottura che causano la cascata parser.

Ambito:
- patch diretta
- cluster strutturale complesso
- severita' critica

Gruppi inclusi:
- duplicate property (`text`, `visible`)
- blocchi dual-mode non chiusi correttamente o wrapper sbilanciati
- token interpretati come widget/property invalide
- eventuali template vuoti derivati dal desync parser

Esito atteso:
- abbattimento massivo del rumore in `error.log` e `gui_warnings.log`
- recupero della leggibilita' del resto dei log

### Fase 4 - Datacontext e binding building di window_county_view.gui

- [ ] Fase 4 completata

Obiettivo:
correggere i binding/type della contea senza introdurre regressioni sul ramo vanilla separato.

Ambito:
- patch diretta
- pattern v1.1 con file vanilla separato
- severita' alta

Gruppi inclusi:
- `GUIBuildingItem.GetBuilding`
- `Building.HasVariants`
- `Building.GetType.GetTabIcon`
- `Building.GetConstructionProgress`
- `Title.GetAverageFertilityDesc`

Esito atteso:
- riduzione consistente del rumore specifico county view
- maggiore affidabilita' del type vanilla separato collegato

### Fase 5 - Datacontext e localize di window_character_lifestyle.gui

- [ ] Fase 5 completata

Obiettivo:
correggere i type e le stringhe dinamiche non risolte del lifestyle, distinguendo problemi di wrapper da problemi di contenuto vanilla separato.

Ambito:
- patch diretta
- pattern v1.1 con file vanilla separato
- severita' alta

Gruppi inclusi:
- `PerkGuiItem`, `PerkTreeItem`, `FocusItem`
- `Perk.GetDescription`, `FocusType.GetDescription`
- `GetIndexString`, `Pluralize_int32`
- metriche lifestyle come `GetLifestyleExperience`

Esito atteso:
- drastica riduzione errori lifestyle
- chiarimento finale su cosa e' incompatibilita' di tipo e cosa e' solo localize derivata

### Fase 6 - File non patchati, overlay OCR upstream e dipendenze runtime

- [ ] Fase 6 completata

Obiettivo:
affrontare i file citati nei log ma non coperti dalla patch, per distinguere problemi di deploy/load order da veri difetti strutturali upstream.

Ambito:
- OCR upstream + vanilla non patchati
- severita' media

Gruppi inclusi:
- `window_activity_locale.gui`
- `window_hybridize_culture.gui`
- `window_manage_tax_slots.gui`
- `preload/00_types_OCR.gui`
- `_OCR_WIDGET.gui`
- `plugin_widgets.h` e `unknown game view ''` come sintomi correlati

Esito atteso:
- inventario chiaro di cosa resta fuori dalla patch
- base pulita per decidere se servono override locali futuri

### Fase 7 - Asset mancanti e residui non GUI

- [ ] Fase 7 completata

Obiettivo:
chiudere i residui meno urgenti dopo la stabilizzazione dei cluster GUI principali.

Ambito:
- texture mancanti
- errori `game.log`
- severita' media o bassa

Gruppi inclusi:
- texture non trovate nel VFS
- errori culture/innovation
- succession order invalid

Esito atteso:
- logs residui più puliti
- chiusura del ciclo di stabilizzazione

## Criteri di avanzamento tra fasi

- [ ] Prima di passare alla fase successiva, rieseguire un run e rileggere almeno `error.log` e `gui_warnings.log`.
- [ ] Se emerge un nuovo blocker iniziale piu' grave della fase corrente, fermarsi e rivalutare il piano.
- [ ] Se un cluster si riduce ma non scompare, completare comunque la fase solo dopo aver fissato i punti strutturali principali del gruppo.

## Definizione di completamento del piano

Il piano si considera completato quando:

- [ ] Le fasi 1-7 sono tutte spuntate.
- [ ] `coding plans/todo.md` e' stato aggiornato fase per fase fino all'ultima fase.
- [ ] I log finali mostrano la scomparsa dei cluster P0 e una forte riduzione dei P1.
