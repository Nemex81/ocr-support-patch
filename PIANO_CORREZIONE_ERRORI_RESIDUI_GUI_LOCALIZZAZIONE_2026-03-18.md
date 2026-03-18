# Piano Correttivo Avvio Menu Principale - GUI e Localizzazione (Aggiornato 2026-03-18)

## Ambito
Analisi incrociata tra:
- log runtime: logs/error.log (run attuale con timestamp 22:15:27 -> 22:15:51)
- patch attiva: ocr_support_compatibility_pach
- OCR upstream: CK3-OCR/OCR-Support
- vanilla CK3 locale: game/

Obiettivo: rimuovere i blocchi che impediscono di arrivare stabilmente al menu principale.

## Stato sintetico attuale (run 22:15)

### Blocker reali per bootstrap/menu
1. Duplicate localization key:
- TAX_SLOT_OVERVIEW_WINDOW_TAX_SLOTS_WARNING duplicata tra:
  - localization/spanish/ocr_states_l_spanish.yml (patch)
  - localization/spanish/tax_collector_l_spanish.yml (vanilla)

2. Errore parser GUI in window_county_view:
- gui/window_county_view.gui:669/671
- token invalidi: type, =, { (effetto tipico di struttura sbilanciata a graffe).

### Errori non-bloccanti ma da chiudere nel piano
3. Unlocalized in interaction_modify_vassal_window:
- NON_FEUDAL_SUBJECT_CONTRACT_OBLIGATIONS_TITLE
- NON_FEUDAL_SUBJECT_CONTRACT_OBLIGATIONS_TITLE_LEVIES

4. Texture mancanti e data/localization errors esterni multipli:
- prevalenza in asset/script non direttamente legati al wrapper dual-mode appena toccato.

## Validazione incrociata con fonti

### A) window_county_view.gui
- Vanilla e OCR upstream hanno blocchi county_tooltip strutturalmente validi.
- Patch attuale mostra una chiusura in eccesso nel blocco county_control_tooltip_container subito prima del type successivo (coerente con errore parser su linee 669/671).

Conclusione: correzione deterministica copiando fedelmente i tre blocchi county tooltip dalla fonte vanilla (stessa struttura OCR upstream).

### B) TAX_SLOT_OVERVIEW_WINDOW_TAX_SLOTS_WARNING
- La key esiste gia' in vanilla spanish (tax_collector_l_spanish.yml).
- L'override diretto dentro ocr_states_l_spanish.yml genera duplicate key.

Conclusione: non va tenuta in ocr_states_l_spanish.yml; va spostata su meccanismo replace coerente con il progetto o rimossa del tutto se non necessaria dopo fix GUI.

### C) NON_FEUDAL_SUBJECT_CONTRACT_OBLIGATIONS_TITLE*
- Le chiavi esistono in vanilla (my_realm_window_l_spanish.yml e my_realm_window_l_english.yml).
- OCR upstream le usa in interaction_modify_vassal_window.gui.

Conclusione: l'unlocalized dipende dal merge localizzazione attivo (stack mod) e va gestito con fallback patch minimali solo se il problema persiste dopo pulizia duplicate key.

## Checklist implementazioni

### Gia' implementato
- [x] Sostituzione dei token tooltip_paragraph con cooltip_paragraph nei tooltip county.
- [x] Aggiornamento close tab OCR in hud.gui su chiave locale stabile (ocr_close_view).
- [x] Aggiornamento interaction_blackmail.gui su chiave locale ocr_blackmail_select_secret.
- [x] Aggiunta chiave ocr_blackmail_select_secret in localizzazione english.
- [x] Aggiunta chiave ocr_blackmail_select_secret in localizzazione spanish.

### Nuove correzioni da implementare (priorita' avvio)
- [x] N1 - Ripristinare integrita' strutturale di window_county_view.gui:
  - riallineare i tre blocchi county_*_tooltip_container alla struttura vanilla/OCR senza graffe extra.
  - validare assenza errori parser su linee 669/671.

- [x] N2 - Eliminare duplicate key TAX_SLOT_OVERVIEW_WINDOW_TAX_SLOTS_WARNING:
  - rimuovere la key da ocr_states_l_spanish.yml.
  - rimuovere la key da ocr_states_l_english.yml per coerenza cross-lingua.
  - se serve override funzionale, creare file in localization/<lingua>/replace/tax_collector_l_<lingua>.yml secondo pattern replace del progetto, evitando duplicati.

- [x] N3 - Fallback difensivo modify-vassal preparato lato patch:
  - aggiunte 2 chiavi NON_FEUDAL_SUBJECT_CONTRACT_OBLIGATIONS_TITLE* nella localizzazione replace della lingua attiva.
  - resta necessaria una nuova run per confermare l'eliminazione dell'unlocalized a runtime.

- [x] N4 - Verifica regressione (statica su file patch):
  - confermare nessuna regressione su hud.gui, interaction_blackmail.gui e type condivisi OCR.

## Criteri di uscita aggiornati
- [x] C1 - Nessun duplicate key su TAX_SLOT_OVERVIEW_WINDOW_TAX_SLOTS_WARNING (lato patch: key rimossa dai file OCR states).
- [x] C2 - Nessun parser error su gui/window_county_view.gui (linee 669/671 o equivalenti) lato struttura file.
- [ ] C3 - Arrivo al menu principale senza blocco bootstrap (da confermare con nuova run).
- [x] C4 - Nessuna nuova regressione nei fix gia' implementati (blackmail/close tab) lato file.

## Convalida implementazione (post-fix codice)
- [x] V1 - Verifica strutturale file patch completata:
  - window_county_view.gui valido (nessun errore statico sui blocchi corretti).
  - hud.gui e interaction_blackmail.gui senza nuovi errori statici.
- [x] V2 - Verifica rimozione duplicate key lato patch completata:
  - nessuna occorrenza della key TAX_SLOT_OVERVIEW_WINDOW_TAX_SLOTS_WARNING nei file OCR states della patch.
- [ ] V3 - Verifica runtime post-fix non ancora disponibile:
  - error.log attuale (22:15:51) e' precedente alla nuova run dopo gli ultimi fix.

## Esito convalida piano (checkpoint corrente)
- Stato: NON PASS
- Motivo 1: manca un error.log post-fix, quindi non e' possibile validare i criteri runtime C3 in modo affidabile.
- Motivo 2: la fase R3 riguarda file OCR upstream esterni al perimetro patch attivo e non puo' essere trattata come implementazione immediata nella patch.

## Nuove fasi correttive residue (revisione strategia)

### Fase R1 - Validazione runtime dopo fix N1/N2
- [ ] Avviare una nuova run pulita e acquisire un nuovo error.log.
- [ ] Confermare scomparsa definitiva di:
  - duplicate key TAX_SLOT_OVERVIEW_WINDOW_TAX_SLOTS_WARNING
  - parser error su window_county_view.gui

### Fase R2 - Unlocalized modify-vassal (fallback difensivo)
- [x] Fallback preventivo applicato nella lingua attiva.
- [ ] Verificare nel nuovo log se NON_FEUDAL_SUBJECT_CONTRACT_OBLIGATIONS_TITLE* scompare realmente.
- [ ] Se persiste ancora, riclassificare il problema come conflitto di stack localizzazione e non come semplice key mancante.

### Fase R3 - Tracciamento esterno OCR upstream (fuori implementazione patch)
- [ ] Aprire sotto-task separato di coordinamento upstream per:
  - common/scripted_guis/ARMIES_ocr.txt (confirm_title non riconosciuto)
  - common/scripted_guis/sgui_ocr.txt (special_buildings_switch con argomento vuoto)
- [ ] Non implementare questa fase nella patch corrente finche' non viene approvata una procedura specifica di intervento su OCR upstream.

### Fase R4 - Cluster localizzazione esterna/modpack
- [ ] Tracciare separatamente gli errori data/localize non patch-specific (es. corte, Concept close_family, create_artifact_bow_tooltip, ecc.).
- [ ] Classificare quali dipendono dalla traduzione attiva esterna e quali richiedono override mirati della patch.

### Fase R5 - Gate decisionale prima di nuove implementazioni
- [ ] Eseguire prima R1 (nuovo log post-fix).
- [ ] Solo dopo R1: decidere se attivare R2 (fix patch) oppure lasciare in monitoraggio se l'unlocalized scompare.
- [ ] Mantenere R3/R4 come track separata non bloccante per il bootstrap della patch.

## Note operative
- Eseguire una sola finestra/problem cluster alla volta (regola progetto).
- Priorita' assoluta: risolvere prima i due blocker N1/N2, poi rivalutare N3 solo sul nuovo log.
- In assenza di nuova run, nessun errore runtime puo' essere dichiarato risolto in modo definitivo.
- Le fasi implementabili nella patch senza nuova run sono sospese: serve prima il gate R1.
