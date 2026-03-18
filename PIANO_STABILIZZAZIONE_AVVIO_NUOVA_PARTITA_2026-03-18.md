# Piano di Stabilizzazione Avvio e Nuova Partita - 2026-03-18

## Sommario per fasi
- [ ] Fase 0 - Congelare il run di riferimento: lavorare solo sul crash bundle `ck3_20260318_191045` e su log freschi successivi, verificando sempre la copia live della mod caricata dal launcher.
- [ ] Fase 1 - Stabilizzare i file GUI caricati all'ingresso in partita: isolare e correggere prima i file che entrano in gioco dopo la scelta del sovrano, con priorita' a `window_activity.gui` e alle sue dipendenze dirette.
- [ ] Fase 2 - Ripristinare i type condivisi mancanti o corrotti: riallineare `window_faith.gui`, `window_county_view.gui` e i rispettivi type/shared OCR da cui dipendono altre finestre in-game.
- [ ] Fase 3 - Rieseguire il caricamento di una nuova partita con logging pulito: verificare il superamento della scelta del sovrano e l'arrivo alla mappa senza stack overflow.
- [ ] Fase 4 - Audit di regressione in-game: solo dopo la stabilizzazione, riesaminare finestre secondarie come intrigue, court, lifestyle, army e diverge culture.

## Obiettivo
Stabilizzare due transizioni critiche:
1. avvio fino al menu principale;
2. caricamento di una nuova partita dopo la scelta del sovrano.

Il focus di questo piano e' il secondo punto, cioe' il crash che avviene dopo il menu principale durante l'ingresso effettivo in partita.

## Diagnosi incrociata

### 1) Esito del crash bundle
Il crash bundle `crashes/ck3_20260318_191045` riporta:
- `Unhandled Exception C00000FD (EXCEPTION_STACK_OVERFLOW)`;
- nessuna assert di contenuto gameplay o database nei materiali letti;
- profilo compatibile con ricorsione o risoluzione ciclica lato GUI/type registry durante il caricamento dell'interfaccia in-game.

Questo e' diverso da un semplice parse error che blocca il menu: qui il gioco arriva al frontend, consente la scelta del sovrano e cade nella fase in cui vengono inizializzate finestre e type usati solo dopo l'ingresso in partita.

### 2) Evidenze da error.log del run crashato
Nel run che genera il crash compaiono due famiglie di errori.

#### A. Corruzioni gia' note ma ancora presenti
- `gui/window_character.gui:263 - Duplicate property 'name'`
- `gui/window_council.gui:2895 - Duplicate property 'name'`
- type mancanti in `window_faith.gui`, `window_county_view.gui`, `window_faith_creation.gui`, `window_army.gui`, `window_character_ocr.gui`, `gui/shared/cooltip.gui`

Questi errori dimostrano che il registry GUI non e' ancora sano nemmeno dopo l'arrivo al menu.

#### B. Errori nuovi o particolarmente rilevanti per il crash post-menu
- `gui/window_activity.gui` presenta parse failure ripetuti gia' alle prime centinaia di righe, poi una cascata molto piu' ampia in cui token come `type`, `=`, `{`, condizioni e localizzazioni vengono interpretati come proprieta' invalide.
- `gui/window_activity_locale.gui` perde type fondamentali come `activity_event_widget_base`, `activity_header`, `vbox_activity_conclusion`, `hbox_activity_progress_ocr`.
- `gui/window_intrigue.gui` produce errori su proprieta' e testi in una fase che sembra successiva all'ingresso in partita, non al menu.
- `gui/window_diverge_culture.gui` perde `name_entry_big`.
- `gui/window_court.gui` perde `prison_interactions_hbox`.

La combinazione e' coerente con un crash durante il caricamento dell'insieme di finestre in-game, non del frontend.

### 3) Confronto con CK3 vanilla originale
Il confronto con la fonte vanilla mostra che:
- `window_activity.gui` vanilla e' strutturato come un file coerente con `window = { ... }` seguito da `types ActivityWindowTypes`, senza la cascata di proprieta' duplicate e senza token letti come widget/property.
- `window_intrigue.gui` vanilla non contiene il layer OCR personalizzato presente nella patch, quindi gli errori su schemi e tab non sono originari del gioco base.
- `window_court.gui`, `window_faith.gui`, `window_county_view.gui` e `window_diverge_culture.gui` in vanilla definiscono regolarmente i type che nella patch risultano mancanti o non registrati.

Conclusione dal confronto vanilla: il crash non deriva dal contenuto originale Paradox, ma da una divergenza strutturale introdotta nella patch.

### 4) Confronto con OCR Support originale upstream
Il confronto con OCR upstream mostra che:
- `OCR-Support/gui/window_activity.gui` definisce regolarmente `activity_header`, `activity_event_widget_base`, `vbox_activity_conclusion`, `hbox_activity_progress`, `vbox_activity_conclusion_ocr`, `hbox_activity_progress_ocr` e gli altri type richiamati da `window_activity_locale.gui`.
- `OCR-Support/gui/window_intrigue.gui` contiene il branch OCR con testi e shortcut coerenti, quindi l'idea funzionale e' valida, ma la patch attuale non lo sta caricando in uno stato sintatticamente affidabile.
- `OCR-Support/gui/window_faith.gui` e `OCR-Support/gui/window_county_view.gui` contengono type shared OCR che nella patch attuale risultano rimossi o non piu' registrati.

Conclusione dal confronto OCR upstream: la patch attuale ha perso continuita' strutturale con l'upstream proprio nei file che dovrebbero fornire type OCR condivisi a finestre caricate in-game.

## Causa probabile del crash in nuova partita
La causa piu' probabile non e' un singolo file, ma una catena di corruzioni GUI con un trigger principale piu' tardivo.

### Causa radice
Il progetto ha ancora un registry GUI incoerente a causa di conversioni dual-mode incomplete o corrotte. In particolare:
- type shared OCR rimossi da `window_faith.gui` e `window_county_view.gui` continuano a essere referenziati da altre finestre;
- blocchi vanilla/type-separated di alcuni file restano sintatticamente invalidi;
- `window_character.gui` e `window_council.gui` conservano proprieta' duplicate.

### Trigger piu' probabile del crash post-menu
Quando il gioco entra in nuova partita e inizializza le finestre in-game, `window_activity.gui` appare il candidato piu' forte come trigger immediato:
- e' uno dei primi file con errori strutturali gravi nel run crashato;
- la cascata di errori mostra che il parser perde il contesto del file e comincia a leggere interi blocchi come proprieta' invalide;
- `window_activity_locale.gui` dipende direttamente dai suoi type e fallisce subito dopo;
- questo profilo e' coerente con ricorsione/risoluzione patologica dei type, cioe' con uno stack overflow.

In pratica:
- prima del menu il gioco sopravvive a una parte della corruzione;
- dopo la scelta del sovrano vengono caricati altri file in-game, in particolare activity e finestre collegate;
- la nuova ondata di type mancanti e blocchi sintatticamente corrotti porta alla crescita ricorsiva della risoluzione GUI fino allo stack overflow.

## Strategia correttiva proposta

### Fase 0 - Baseline e controllo deploy
1. Verificare che il launcher stia caricando la copia live in `Documents/Paradox Interactive/Crusader Kings III/mod/ocr_support_compatibility_pach` e non una versione desincronizzata.
2. Archiviare il crash bundle `ck3_20260318_191045` come baseline del problema post-menu.
3. Dopo ogni correzione futura, validare sempre su log freschi e non riutilizzare `error.log` storico come unica prova.

### Fase 1 - Priorita' massima: activity family
Target primari:
1. `ocr_support_compatibility_pach/gui/window_activity.gui`
2. `ocr_support_compatibility_pach/gui/window_activity_locale.gui`

Obiettivo:
- riportare `window_activity.gui` a una struttura sintatticamente coerente con la fonte OCR upstream e con i type caricabili dal motore;
- garantire che i type richiesti da `window_activity_locale.gui` tornino registrati prima del caricamento della partita.

Nota operativa:
- questo e' il primo fronte da attaccare anche se altri file sono ancora rotti, perche' e' il candidato piu' forte al crash post-menu.

### Fase 2 - Ripristino dei type shared che contaminano l'in-game
Target secondari ma ancora bloccanti:
1. `ocr_support_compatibility_pach/gui/window_faith.gui`
2. `ocr_support_compatibility_pach/gui/vanilla/faith_patch_vanilla.gui`
3. `ocr_support_compatibility_pach/gui/window_county_view.gui`
4. `ocr_support_compatibility_pach/gui/vanilla/county_view_patch_vanilla.gui`
5. `ocr_support_compatibility_pach/gui/window_character.gui`
6. `ocr_support_compatibility_pach/gui/window_council.gui`

Obiettivo:
- rimettere in piedi il registry dei type OCR condivisi;
- eliminare i `Duplicate property` residui sui wrapper inline;
- prevenire nuovi fallback patologici durante il caricamento della partita.

### Fase 3 - Finestre dipendenti caricate in-game
Solo dopo le fasi 1 e 2:
1. verificare `window_intrigue.gui` su log puliti;
2. verificare `window_character_lifestyle.gui` su log puliti;
3. verificare `window_court.gui`, `window_diverge_culture.gui` e `window_army.gui` su log puliti.

Motivo:
- oggi questi file sono rumorosi, ma una parte dei loro errori puo' essere solo un effetto domino dei type mancanti a monte.

### Fase 4 - Gate di stabilizzazione nuova partita
Il fix si considera valido solo se tutti i punti seguenti passano:
1. il gioco raggiunge il menu principale;
2. la scelta del sovrano non causa crash;
3. la mappa della nuova partita viene caricata;
4. il nuovo `error.log` non mostra piu' errori strutturali su `window_activity.gui` e `window_activity_locale.gui`;
5. il nuovo crash bundle non viene generato.

## Ordine operativo consigliato
1. Riparare `window_activity.gui` contro OCR upstream e vanilla.
2. Riparare `window_activity_locale.gui` solo dopo che i type base activity sono tornati validi.
3. Ripristinare i type shared di faith e county view.
4. Chiudere i `Duplicate property` di character e council.
5. Solo dopo riesaminare intrigue, lifestyle, court, army e diverge culture.

## Criteri di accettazione
- Nessun `EXCEPTION_STACK_OVERFLOW` nel caricamento nuova partita.
- Nessuna cascata parser su `window_activity.gui` nel run di prova.
- Nessun `... is not a valid widget/type/property` per i type base activity e per i type shared faith/county usati da altre finestre.
- Menu principale e ingresso in partita entrambi stabili.

## Rischi da evitare durante l'implementazione futura
- correggere prima i file secondari rumorosi e lasciare intatto `window_activity.gui`;
- fidarsi dei log storici senza riallineare la mod live;
- trattare come cause primarie texture mancanti o warning di localizzazione, che al momento hanno priorita' inferiore rispetto alle corruzioni strutturali GUI.