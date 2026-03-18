# Piano Correttivo Normovedenti (Vanilla) - 2026-03-    18

## Sommario operativo per fasi
- [ ] Fase 0 - Congelare il bootstrap GUI e acquisire una baseline pulita: confermare quali errori sono davvero riproducibili nel run corrente, distinguendo blocker di avvio da rumore storico o drift di deploy.
- [ ] Fase 1 - Riparare i wrapper rotti introdotti dalla regressione: correggere i branch vanilla inline di `window_character.gui` e `window_council.gui`, che oggi dichiarano proprieta' duplicate nello stesso widget radice.
- [ ] Fase 2 - Ripristinare i due file type-separated incompleti: `window_faith.gui` e `window_county_view.gui` devono tornare ad avere tutti i type OCR usati dal wrapper, mentre i rispettivi type vanilla separati devono essere sintatticamente validi e fedeli al vanilla.
- [ ] Fase 3 - Risincronizzare e validare la mod live: riallineare la copia in `Documents/.../mod/ocr_support_compatibility_pach`, rieseguire il bootstrap e raccogliere nuovi log per verificare che il menu principale venga raggiunto.
- [ ] Fase 4 - Audit funzionale normovedenti: controllare le regressioni utente residue su personaggio, fede, county view, council e interaction menu solo dopo la stabilizzazione dell'avvio.

## Obiettivo
Ripristinare un avvio corretto dell'app e, subito dopo, la piena funzionalita' della modalita' normovedenti (variabile `ocr` presente) mantenendo fedelta' vanilla CK3 1.17.1 e compatibilita' dual-mode.

## Diagnosi aggiornata

### 1) Causa radice piu' probabile del blocco di avvio
L'analisi incrociata tra log correnti, patch attiva, CK3 vanilla e OCR upstream indica come causa primaria una regressione strutturale introdotta nelle conversioni dual-mode recenti, non un singolo bug funzionale isolato.

In particolare:
- `gui/window_character.gui` genera `Duplicate property 'name'` alla riga 263.
- `gui/window_council.gui` genera `Duplicate property 'name'` alla riga 2895.
- `gui/window_faith.gui` continua a referenziare type OCR come `widget_doctrine_item_ocr`, ma tali definizioni non sono piu' presenti nel file wrapper.
- `gui/window_county_view.gui` continua a referenziare type OCR come `button_shores`, `flow_crossing_ocr`, `widget_building_text`, `active_task_hbox`, `county_task_button`, `button_sea`, `adjacent_county_button`, ma tali definizioni sono state rimosse dal file wrapper.
- `gui/vanilla/faith_patch_vanilla.gui` e `gui/vanilla/county_view_patch_vanilla.gui` risultano a loro volta strutturalmente invalidi: aprono un `type ... = widget` e poi inseriscono direttamente un secondo `name = ...` senza creare un widget figlio vanilla valido.

Effetto pratico: il registry dei widget/type GUI viene corrotto gia' nel bootstrap, il parser fallisce su type fondamentali e l'app non arriva stabilmente al menu principale.

### 2) Prova incrociata con le fonti autorevoli

#### CK3 vanilla locale
- In vanilla, i root window originali di character, council, faith e county view sono strutture complete e coerenti, senza wrapper intermedi con proprieta' duplicate.
- Il contenuto vanilla non contiene il pattern oggi presente nei type separati della patch (`type ... = widget` seguito da un secondo `name` allo stesso livello).

#### OCR Support originale upstream
- In `OCR-Support/gui/window_faith.gui`, i type `container_tenet_item_ocr`, `widget_doctrine_item_ocr`, `container_tenet_item` e `fervor_container_vbox` esistono e sono definiti nello stesso file, mentre nella patch wrapper sono referenziati ma non piu' definiti.
- In `OCR-Support/gui/window_county_view.gui`, i type `button_shores`, `flow_crossing_ocr`, `widget_building_text`, `active_task_hbox`, `active_court_task_hbox`, `county_task_button`, `court_task_button`, `button_sea`, `button_sea_far` e `adjacent_county_button` esistono nel file originale, mentre nella patch wrapper sono referenziati ma non piu' definiti.

Conclusione: le due conversioni type-separated sono state applicate in modo incompleto. E' stato estratto il branch vanilla, ma sono stati rimossi anche type OCR/shared che dovevano restare nel wrapper, rompendo sia il file stesso sia altri file che dipendono da quei type.

### 3) Effetti a cascata gia' visibili nei log
I log confermano che la regressione non resta confinata ai quattro file principali:
- `gui/shared/cooltip.gui` perde `fervor_container_vbox` e `container_tenet_item`.
- `gui/window_faith_creation.gui` perde `container_tenet_item_ocr` e `widget_doctrine_item_ocr`.
- `gui/_OCR_WIDGET.gui`, `gui/window_character_ocr.gui` e `gui/window_army.gui` perdono type provenienti storicamente da `window_county_view.gui`, come `button_sea`, `button_sea_far` e `adjacent_county_button`.

Questo spiega perche' la regressione di avvio appare globale: il bootstrap GUI fallisce su type condivisi, non solo su singole finestre utente.

### 4) Errori secondari da ricontrollare dopo la stabilizzazione
I log riportano anche errori di lexer in `frontend_main.gui`, `window_dynasty_legacy.gui` e `window_inventory.gui`, oltre a errori in `window_activity.gui`.

Questi errori vanno trattati, ma non sono ancora affidabili come causa primaria della regressione attuale per due motivi:
- una parte coincide con sintassi storica OCR upstream e potrebbe provenire da run precedenti o da copie non riallineate;
- finche' il registry GUI e' spezzato da character/council/faith/county, il rumore residuo non e' diagnostico abbastanza pulito.

Per questo la nuova strategia li sposta in una fase successiva alla riparazione del bootstrap principale, salvo riproduzione immediata su log freschi dopo il fix strutturale.

## Correlazione con i sintomi utente
- Mancato arrivo al menu principale -> coerente con rottura del bootstrap GUI e type registry corrotto gia' in fase di caricamento.
- Finestra personaggio rotta -> coerente con branch vanilla inline corrotto in `window_character.gui`.
- Finestra fede decentrata e tooltip/tenet rotti -> coerente con `window_faith.gui` incompleto e type shared mancanti.
- Tasto Costruisci e viste county/army non affidabili -> coerente con type county OCR rimossi ma ancora referenziati.
- Cambio consiglieri e chiusure non affidabili -> coerente con `window_council.gui` strutturalmente corrotto.

## Nuova strategia correttiva
Approccio: stabilizzazione del bootstrap prima di ogni fix funzionale fine. Si interviene in ordine di dipendenza, usando solo le fonti autorevoli e i tool del progetto.

### Fase 0 - Baseline e controllo deploy
1. Verificare che la mod live caricata dal launcher corrisponda davvero alla copia in `Documents/.../mod/ocr_support_compatibility_pach`.
2. Salvare una baseline dei log correnti e poi lavorare solo su log rigenerati dopo ogni intervento.
3. Trattare come blocker solo gli errori riproducibili nel run successivo al fix strutturale.

### Fase 1 - Riparazione wrapper inline rotti
File target:
1. `ocr_support_compatibility_pach/gui/window_character.gui`
2. `ocr_support_compatibility_pach/gui/window_council.gui`

Correzione prevista:
- ricostruire il branch vanilla inline in forma valida, con vero widget figlio vanilla e senza proprieta' duplicate;
- riallineare struttura, `widgetid`, `layer`, `movable`, `attachto` e altri attributi solo dove presenti nel vanilla reale.

### Fase 2 - Riparazione conversioni type-separated incomplete
File target:
1. `ocr_support_compatibility_pach/gui/window_faith.gui`
2. `ocr_support_compatibility_pach/gui/vanilla/faith_patch_vanilla.gui`
3. `ocr_support_compatibility_pach/gui/window_county_view.gui`
4. `ocr_support_compatibility_pach/gui/vanilla/county_view_patch_vanilla.gui`

Correzione prevista:
- reintegrare nel wrapper tutti i type OCR/shared che provengono da OCR upstream e sono ancora referenziati dal file o da dipendenze note;
- mantenere nel type separato solo il branch vanilla fedele al file CK3 originale;
- garantire che il type separato contenga un widget figlio vanilla valido e non proprieta' duplicate sul widget contenitore.

### Fase 3 - Validazione di avvio
1. Eseguire `tri_diff.py --window ...` sui quattro target prima delle scritture finali.
2. Applicare la correzione con il tool di assemblaggio solo se produce output strutturalmente coerente; altrimenti intervenire manualmente sui wrapper generati.
3. Eseguire `audit.py --window ...` sui file corretti.
4. Rigenerare i log e verificare come criterio minimo il raggiungimento del menu principale senza nuovi errori parser/type bloccanti sugli stessi target.

### Fase 4 - Rifinitura post-avvio
Solo dopo il ripristino del bootstrap:
1. riesaminare `frontend_main.gui`, `window_activity.gui`, `window_dynasty_legacy.gui` e `window_inventory.gui` su log freschi;
2. correggere eventuali residui di lexer o proprieta' duplicate ancora riproducibili;
3. verificare `interaction_menu_window.gui` come possibile effetto secondario, non come causa primaria.

## Gate di convalida
Il piano e' valido solo se passano tutti i gate seguenti:
1. Nessun `Duplicate property` residuo nei quattro target primari.
2. Nessun `... is not a valid widget/type/property` per i type OCR/shared storicamente definiti in faith e county view.
3. Nessun `... patch_vanilla is not a valid widget/type/property` per i type separati riparati.
4. Raggiungimento del menu principale su log freschi.
5. Audit strutturale senza blocker sui file corretti.

## Criteri di accettazione
- Avvio completato fino al menu principale.
- Registry GUI stabile: i type shared di faith e county view sono di nuovo registrati e riutilizzabili da altri file.
- Branch vanilla con guard corretta `visible = "[GetVariableSystem.Exists('ocr')]"` e fedelta' sostanziale a CK3 vanilla.
- Branch OCR conservato rispetto a OCR upstream salvo gli adattamenti dual-mode strettamente necessari.
- Solo dopo questi punti: verifica funzionale su personaggio, fede, county view, council e interaction menu.

## Piano di fallback
Se un gate fallisce:
- produrre un report per file con causa, riga, dipendenze e impatto sul bootstrap;
- ridurre l'ambito del fix al minimo set di file che sblocca il menu principale;
- rieseguire log freschi prima di affrontare errori secondari non piu' prioritari.
