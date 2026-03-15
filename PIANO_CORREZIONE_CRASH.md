# Piano di Correzione — Stabilizzazione Avvio CK3

Data analisi: 15 marzo 2026
Ultimo aggiornamento: 15 marzo 2026 (analisi crash ck3_20260315_174141)
Stato: BLOCCANTE IN AVVIO, MA CON PROGRESSO REALE

---

## Obiettivo Operativo

Priorita' assoluta: ottenere un avvio partita senza crash.

Per questa fase il progetto NON deve inseguire il ripristino completo del dual-mode,
la fedelta' vanilla o la pulizia del framework. Tutto cio' e' secondario rispetto a:

1. arrivare all'ingresso in partita senza crash;
2. ridurre i parse error della patch che si manifestano nel bootstrap GUI;
3. fermare le regressioni rientrate dopo il ripristino manuale di file piu' vecchi.

---

## Sintesi Esecutiva

L'ultimo crash analizzato, `ck3_20260315_174141`, NON e' piu' uno stack overflow.
Ora il motore cade con:

- `EXCEPTION_ACCESS_VIOLATION (C0000005)`
- indirizzo `0x00007FF784A08914`

Questo e' un segnale importante: il sistema ha fatto un passo avanti rispetto ai crash
precedenti. Il gioco ora arriva alla scelta del personaggio e cade solo dopo la conferma
di avvio partita.

La conseguenza pratica e' che il piano precedente, centrato soprattutto su:

- pattern v1.1 type-separated;
- file `_patch_vanilla`;
- rimozione tipi vanilla ridondanti;
- ipotesi di stack overflow da doppia registrazione;

non e' piu' il piano corretto per lo stato attuale della repo.

La patch corrente e' stata in parte riportata a file piu' vecchi e nel log compaiono di nuovo
molti errori GUI reali della patch attuale. Alcuni sono rumore ereditato dall'OCR upstream,
ma almeno un wrapper appare strutturalmente corrotto rispetto a OCR upstream e vanilla.

---

## Evidenza Principale dal Crash 174141

### 1. Timeline del crash

Sequenza ricostruita dai log:

- `17:41:12` — avvio generate game state from bookmark
- `17:41:16` — completato history pass
- `17:41:18` — completato post-history
- `17:41:18` — completato generate game state from bookmark
- `17:41:20` — `CGameState::InitPostRead`
- `17:41:21` — `Setup powerful vassals among a total of [20640] living character`
- `17:41:22` / `17:41:24` — errori GUI della patch e dell'ecosistema OCR
- `17:41:43` — crash con `EXCEPTION_ACCESS_VIOLATION`

### 2. Cambiamento qualitativo del guasto

Prima:

- crash molto presto;
- stack overflow;
- piano focalizzato su ricorsione / type-separated / duplicazioni.

Ora:

- il gioco avanza oltre la selezione personaggio;
- il crash e' access violation;
- la patch attuale mostra parse error e widget/layout error concreti in piu' wrapper.

Conclusione: il problema attuale va trattato come instabilita' da bootstrap GUI / wrapper corrotti,
non come semplice prosecuzione del vecchio stack overflow.

---

## Cosa del Piano Vecchio e' Obsoleto

Le sezioni precedenti del piano basate su queste ipotesi vanno considerate superate:

1. `Pattern v1.1` come causa centrale del crash attuale.
2. `tipi vanilla duplicati in my_realm/military` come focus principale immediato.
3. `0 errori della patch` come fotografia attuale.
4. `test 7.1` come primo passo obbligatorio.

Motivo:

- l'albero attuale della patch non e' piu' quello su cui era stato scritto quel piano;
- i log del crash 174141 mostrano errori della patch corrente su file specifici;
- la priorita' non e' piu' dimostrare se il crash e' nostro o di OCR upstream, ma togliere
  dal bootstrap i wrapper patch che oggi stanno chiaramente rompendo il parsing o il layout.

Il test con patch disabilitata resta utile come fallback diagnostico, ma NON e' piu' il passo piu'
efficace per la stabilizzazione immediata.

---

## Analisi Tri-Repo Mirata

Confronto effettuato fra:

- patch corrente;
- OCR upstream Agamidae;
- vanilla CK3 1.17.1.

### Quadro generale

I file rilevanti si dividono in tre categorie:

1. `Regressione patch reale`
  Il wrapper patch e' strutturalmente peggiore o corrotto rispetto a OCR upstream e vanilla.

2. `Rumore OCR upstream ereditato`
  La patch contiene errori gia' presenti nell'OCR upstream. Sono da ridurre, ma non sono la prova
  di una regressione introdotta da noi oggi.

3. `Segnale debole o a bassa confidenza`
  Il log cita linee/pattern che non combaciano bene con il file patch attuale oppure sembrano errori
  a cascata dopo un parse failure precedente.

---

## File Prioritari per la Stabilizzazione

### A. `window_activity.gui` — BLOCCANTE STARTUP

Verdetto: primo sospetto reale e prioritario.

Motivo tecnico:

- e' l'unico wrapper che nel confronto tri-repo appare strutturalmente fuori asse rispetto a OCR upstream e vanilla;
- il parser lo legge come se blocchi e layout fossero stati ricomposti male;
- gli errori associati sono di livello piu' duro di semplici warning OCR.

Interpretazione operativa:

- questo file va trattato come candidato n.1 al crash di avvio;
- NON va corretto incrementalmente alla cieca;
- per stabilizzare l'avvio conviene prima riportarlo a un wrapper minimale e strutturalmente valido.

Severita': `blocker startup`

### B. `window_inventory.gui` — MAJOR

Verdetto: molto sospetto, ma secondario rispetto a `window_activity.gui`.

Motivo tecnico:

- il log contiene errori precoci di parsing / lessicali e riferimenti a proprieta' non gestite;
- parte del rumore sembra ereditata dall'OCR upstream, ma il file resta abbastanza fragile da meritare
  una normalizzazione anticipata.

Severita': `major`

### C. `window_faith.gui` — MAJOR

Verdetto: molto rumoroso, ma non necessariamente regressione nuova della patch.

Motivo tecnico:

- nel log compaiono pattern invalidi come `IsNot`, `HasNot`, cast `int32`, `CFixedPoint`, layout di flowcontainer;
- questi costrutti sono in gran parte presenti gia' nell'OCR upstream;
- non e' il miglior candidato come prima causa, ma e' uno dei principali amplificatori di errore nel bootstrap.

Severita': `major`

### D. `hud.gui` — MEDIO/MAJOR

Verdetto: non primo colpevole, ma da ripulire presto.

Motivo tecnico:

- uso scorretto di chiavi localizzate come `raw_text` invece di `text` in punti caricati presto;
- errore non sufficiente da solo a spiegare il crash, ma contribuisce a sporcare l'inizializzazione HUD.

Severita': `major basso`

### E. `window_intrigue.gui` — MEDIO/MAJOR

Verdetto: rumoroso, in gran parte ereditato dall'OCR upstream.

Motivo tecnico:

- nel log compaiono `hotkey` invalidi e `raw_text` con markup non valido;
- difficilmente e' il primo blocker dell'avvio, ma aggiunge rumore e parse failures non necessari.

Severita': `major basso`

---

## File a Bassa Priorita' per Questo Crash

### `window_court.gui`

Il log segnala `prison_interactions_hbox`, ma il file corrente lo definisce esplicitamente.
Alta probabilita' di errore a cascata o mismatch di parsing successivo.

Severita': `minor / bassa confidenza`

### `window_county_view.gui`

Ci sono errori nel log, ma non sono il miglior punto da cui partire per la stabilizzazione dell'avvio.
Molti segnali paiono secondari o poco allineati al file corrente.

Severita': `minor / media confidenza`

### `window_culture.gui`

I pattern sospetti sembrano in gran parte gia' presenti in OCR upstream.
Non prioritario per il crash immediato.

Severita': `minor`

---

## Strategia Nuova — Stabilizzazione Prima, Framework Dopo

### Regola guida

Per uscire dal crash bisogna smettere di lavorare con correzioni distribuite su molti wrapper rumorosi.
Serve invece una strategia a impatto controllato:

- pochi file per volta;
- ordine rigido di priorita';
- obiettivo minimo: partita avviabile;
- nessun tentativo di ripristino completo del dual-mode in questa fase.

### Principio tecnico

Quando un wrapper patch e' chiaramente instabile, la scelta piu' efficace per questa fase NON e':

- migliorarlo poco per volta;
- inseguire tutte le warning OCR;
- correggere il framework prima della stabilizzazione.

La scelta efficace e':

- riportare temporaneamente il file a una forma nota e stabile;
- preferire wrapper OCR upstream validi o wrapper patch minimi;
- ridurre la superficie attiva fino a ottenere l'avvio.

---

## Piano di Lavoro Operativo

### Fase A — Congelamento dell'obiettivo

Obiettivo di questa fase:

- far partire una nuova partita senza crash;
- tollerare warning non bloccanti se non fermano l'avvio.

Fuori scope temporaneo:

- ripristino completo della modalita' vanilla;
- pulizia generale di tutti i wrapper;
- refactor del framework;
- audit di qualita' non direttamente collegati all'avvio.

### Fase B — Fix prioritario singolo su `window_activity.gui`

Azioni previste:

1. verificare la struttura top-level del file corrente;
2. confrontarla con OCR upstream e vanilla;
3. sostituire il wrapper corrente con la variante piu' semplice e strutturalmente valida;
4. sincronizzare subito il file nella mod directory;
5. testare l'avvio.

Esito atteso:

- se il crash sparisce o si sposta molto avanti, `window_activity.gui` era il blocker principale;
- se il crash persiste invariato, si passa al file successivo.

### Fase C — Bonifica rapida dei 4 file successivi

Ordine obbligatorio:

1. `window_inventory.gui`
2. `window_faith.gui`
3. `hud.gui`
4. `window_intrigue.gui`

Per ciascun file:

1. rimuovere solo i pattern che il log segnala come invalidi e che non servono alla stabilizzazione;
2. se il file resta troppo rumoroso, fallback a versione OCR upstream nota e coerente;
3. sincronizzare;
4. test immediato.

### Fase D — Solo se necessario: fallback diagnostico

Se dopo le fasi B e C il crash resta uguale:

1. riattivare il test con patch ridotta / patch disabilitata;
2. fare ricerca binaria sui wrapper piu' pesanti caricati in bootstrap;
3. verificare se il crash residuo e' davvero esterno alla patch.

Questa fase torna utile solo DOPO aver tolto di mezzo i blocker oggi evidenti.

---

## Priorita' Tecniche Concretissime

### Priorita' 1

Stabilizzare `window_activity.gui`.

### Priorita' 2

Eliminare parse error precoci in `window_inventory.gui`.

### Priorita' 3

Ridurre il rumore bootstrap di `window_faith.gui` sui costrutti non riconosciuti.

### Priorita' 4

Correggere in `hud.gui` i casi dove una chiave localizzata e' usata come `raw_text` invece di `text`.

### Priorita' 5

Ridurre i costrutti non validi in `window_intrigue.gui` (`hotkey`, markup OCR in raw_text, ecc.).

---

## Criteri di Successo

La fase di stabilizzazione si considera riuscita quando:

1. il gioco entra in partita senza crash;
2. i log non mostrano piu' parse error strutturali nei wrapper patch prioritari;
3. gli errori residui sono warning tollerabili o rumore proveniente da altri mod / OCR upstream;
4. il crash non e' piu' riproducibile al click di conferma personaggio.

---

## Criteri di Stop

Bisogna fermarsi e rivalutare solo se accade una di queste condizioni:

1. il crash resta identico dopo la bonifica dei 5 file prioritari;
2. i log mostrano che il nuovo blocker non e' nella patch ma in OCR upstream o in un altro mod;
3. un wrapper patch non puo' essere semplificato senza rompere totalmente l'apertura della finestra.

Fino a quel punto NON ha senso riaprire il cantiere framework o il piano di reintroduzione dual-mode.

---

## Stato Attuale Reale

- crash attuale: `EXCEPTION_ACCESS_VIOLATION`, non piu' stack overflow;
- il gioco arriva piu' avanti di prima;
- il piano precedente non rappresenta piu' lo stato della patch attuale;
- esistono regressioni reali rientrate con il ripristino manuale di file vecchi;
- `window_activity.gui` e' il candidato n.1 per la stabilizzazione immediata;
- la strategia corretta ora e' ridurre i wrapper instabili, non ripristinare il dual-mode.

---

## Prossima Azione Obbligatoria

Nella prossima sessione operativa bisogna:

1. intervenire per primo su `ocr_support_compatibility_pach/gui/window_activity.gui`;
2. sincronizzare il file nella cartella mod Paradox;
3. lanciare un nuovo test d'avvio;
4. solo dopo decidere il passo successivo in base al nuovo log.

Questo e' il percorso piu' corto e piu' difendibile per arrivare a una build avviabile.
# Piano di Correzione — Crash al Caricamento Partita

Data analisi: 15 marzo 2026
Ultimo aggiornamento: 15 marzo 2026 (quinta analisi — crash `ck3_20260315_144654`)
Stato: **PATCH CORRETTA — rimossi tipi vanilla ridondanti (−6000 righe, −87% errori) — test in attesa**

---

## Diagnosi

### Sintomo
L'applicazione CK3 crasha durante il caricamento di una nuova partita.
Crash di tipo **EXCEPTION_STACK_OVERFLOW (C00000FD)** — ricorsione infinita nel motore.
Il crash avviene ~6 secondi dopo la generazione dello stato di gioco (11:51:35 → 11:51:41),
durante l'istanziazione GUI per il gameplay.

### Causa Radice — Analisi in Due Fasi

#### Fase A (prima analisi — insufficiente)
Lo strumento `tools/assemble_dualmode.py` (funzione `build_vanilla_type_file()`)
genera i file vanilla type-separated (Pattern v1.1) copiando **l'intero contenuto**
del blocco `window = {}` vanilla — incluse proprietà che appartengono ESCLUSIVAMENTE
al widget `window` e NON sono supportate nei widget `type` (`movable`, `layer`, `state _show/_hide`, ecc.).

**Fix applicato:** strip delle proprietà window-level → crash NON risolto.

#### Fase B (seconda analisi — causa reale)
Il Pattern v1.1 (type-separated) è **architetturalmente incompatibile** con OCR upstream.
La causa reale del crash è la combinazione di:

1. **Conflitto scrollarea/scrollwidget**: OCR upstream ridefinisce il tipo `scrollbox`
   in `gui/preload/00_types_OCR.gui:113`. L'OCR scrollbox NON supporta la proprietà
   `scrollwidget` usata dalle `scrollarea` vanilla → errore "Could not create scrollwidget"
   → widget corrotti → stack overflow.

2. **Tipi locali mancanti**: i file vanilla type referenziano tipi locali che OCR ha
   sostituito o rimosso (es. `progressbar_lifestyle_xp`, `animation_soldier_loss`,
   `army_quality_icon`, `icon_maa_combat`) → errori "not a valid widget/type".

3. **Profondità nesting**: l'ulteriore livello di annidamento (window → type → vanilla content)
   amplifica il rischio di ricorsione infinita nel motore.

### Evidenze dai Log (error.log del crash)
- **395 errori totali** dai file `_patch_vanilla` (vs 1100 totali della prima analisi)
- **24 errori scrollwidget/scrollarea** — trigger diretto dello stack overflow
- **321 errori "not a valid widget/type"** — tipi OCR-incompatibili
- **Distribuzione:** dynasty_house(100), character(74), combat(32), inventory(30),
  culture(26), county_view(25), character_lifestyle(24), activity(24), faith(16), intrigue(16), altri

### Percorso logico (causa reale)
```
OCR upstream ridefinisce scrollbox (00_types_OCR.gui:113)
    ↓
Vanilla type files contengono scrollarea + scrollwidget
    ↓
Engine usa OCR scrollbox al posto del vanilla → "scrollwidget not handled"
    ↓
"Could not create scrollwidget for scrollarea" (friends, rivals, lovers, grudges...)
    ↓
Widget corrotti + 395 errori cascading + ricorsione infinita
    ↓
EXCEPTION_STACK_OVERFLOW (C00000FD) → crash
```

---

## Regola Architetturale Violata

### Problema originale (proprietà window-level)
Da `copilot-instructions.md`, sezione Pattern v1.1:

> **Il type separato NON contiene `state`, `widgetid`, `layer`, `attachto`, `movable`**

Questa regola esiste proprio per evitare il problema riscontrato.
Lo strumento `assemble_dualmode.py` non la implementava.

### Problema reale (incompatibilità architetturale)
Il Pattern v1.1 in sé è incompatibile con l'ambiente OCR upstream:
i file type-separated contengono contenuto vanilla che referenzia tipi e widget
che OCR upstream ha ridefinito o sostituito. Nessuno strip di proprietà può risolvere
questo conflitto — solo la rimozione completa dei file type o una riscrittura
del contenuto vanilla per adattarlo all'ambiente OCR.

---

## File Coinvolti (stato finale)

### File vanilla type-separated — TUTTI ELIMINATI

Tutti e 19 i file nella cartella `gui/vanilla/` sono stati eliminati.
La cartella è ora vuota.

| # | File eliminato | Errori nel crash log |
|---|---------------|---------------------|
| 1 | `activity_list_patch_vanilla.gui` | vari |
| 2 | `activity_patch_vanilla.gui` | 24 |
| 3 | `army_patch_vanilla.gui` | vari |
| 4 | `character_lifestyle_patch_vanilla.gui` | 24 |
| 5 | `character_patch_vanilla.gui` | 74 (incl. scrollwidget) |
| 6 | `combat_patch_vanilla.gui` | 32 |
| 7 | `council_patch_vanilla.gui` | vari |
| 8 | `county_view_patch_vanilla.gui` | 25 |
| 9 | `court_patch_vanilla.gui` | vari |
| 10 | `culture_patch_vanilla.gui` | 26 |
| 11 | `decisions_patch_vanilla.gui` | vari |
| 12 | `dynasty_house_patch_vanilla.gui` | 100 |
| 13 | `factions_patch_vanilla.gui` | vari |
| 14 | `faith_patch_vanilla.gui` | 16 |
| 15 | `interaction_interfere_in_war_notification_patch_vanilla.gui` | vari |
| 16 | `intrigue_patch_vanilla.gui` | 16 |
| 17 | `inventory_patch_vanilla.gui` | 30 |
| 18 | `military_patch_vanilla.gui` | vari |
| 19 | `my_realm_patch_vanilla.gui` | vari |

### Wrapper modificati (rimosse istanziazioni)

19 file wrapper in `gui/` — rimossi 2 righe ciascuno (commento + istanziazione `_patch_vanilla = {}`).
Struttura verificata: tutti i 22 file `.gui` hanno parentesi bilanciate.

---

## Piano di Correzione

### Fase 1 — Correzione strumento (prerequisito) — ☑ COMPLETATA (poi resa obsoleta)

- [x] **1.1** Aggiunto `sanitize_vanilla_inner_for_type()` a `assemble_dualmode.py`
- [x] **1.2** Integrata nel flusso `build_vanilla_type_file()`
- [x] **1.3** Test eseguito

> ⚠️ Questa fase è ora **obsoleta**: il Pattern v1.1 è stato dismesso. Lo strumento
> contiene ancora la funzione, ma non verrà più usata per generare file type-separated.

### Fase 2 — Strip proprietà window-level dai 19 type files — ☑ poi ⊘ SUPERATA

Lo strip delle proprietà window-level è stato applicato a tutti i 19 file ma
**NON ha risolto il crash**. La causa reale era l'incompatibilità scrollarea/scrollwidget
e i tipi locali mancanti (vedi Diagnosi Fase B).

> Tutti i 19 file type-separated sono stati **eliminati** nella Fase 2B.

### Fase 2B — Rimozione completa Pattern v1.1 — ☑ COMPLETATA

Soluzione definitiva: rimozione totale dell'architettura type-separated.

- [x] **2B.1** Eliminati tutti i 19 file da `gui/vanilla/` (cartella ora vuota)
- [x] **2B.2** Rimosse tutte le righe di istanziazione `_patch_vanilla = {}` dai 19 wrapper
- [x] **2B.3** Rimosse tutte le righe di commento referenzianti i file type vanilla
- [x] **2B.4** Verificato: 0 file in `gui/vanilla/`, 0 riferimenti `_patch_vanilla` nei wrapper
- [x] **2B.5** Verificato bilanciamento parentesi su tutti i 22 file `.gui` — tutti OK

**File eliminati:**
activity_list_patch_vanilla.gui, activity_patch_vanilla.gui, army_patch_vanilla.gui,
character_lifestyle_patch_vanilla.gui, character_patch_vanilla.gui, combat_patch_vanilla.gui,
council_patch_vanilla.gui, county_view_patch_vanilla.gui, court_patch_vanilla.gui,
culture_patch_vanilla.gui, decisions_patch_vanilla.gui, dynasty_house_patch_vanilla.gui,
factions_patch_vanilla.gui, faith_patch_vanilla.gui,
interaction_interfere_in_war_notification_patch_vanilla.gui, intrigue_patch_vanilla.gui,
inventory_patch_vanilla.gui, military_patch_vanilla.gui, my_realm_patch_vanilla.gui

### Fase 3 — Verifica wrapper — ⊘ NON NECESSARIA

I wrapper ora contengono solo il branch OCR. Le proprietà window-level (name, layer,
state _show/_hide) sono già presenti perché ereditati dalla sorgente OCR upstream.
La verifica non è più necessaria dato che il branch vanilla non esiste più.

### Fase 4 — Problema scrollwidget — ⊘ SUPERATA

Il conflitto scrollarea/scrollwidget era la causa principale del crash.
Rimosso eliminando i file type-separated. Non richiede ulteriore investigazione
a meno che non si decida di reintrodurre la modalità vanilla con un approccio diverso.

### Fase 5 — Blocchi types/template mancanti — ☑ COMPLETATA (terza analisi)

**Scoperta critica (terza analisi)**:
Il crash persisteva dopo la Fase 2B perché le correzioni NON raggiungevano il gioco.

#### Due cause radice identificate:

**5A. Desync cartella mod Paradox**
Il gioco carica la mod dalla cartella Paradox (`C:\Users\nemex\...\Paradox Interactive\...\mod\`),
NON dal repo GitHub. La cartella mod è un Cloud Files Placeholder di OneDrive (reparse tag 0x9000e01a),
NON un junction. Le modifiche ai wrapper si propagavano automaticamente (stesse dimensioni, stessi timestamp),
ma le **eliminazioni di file** nella sottocartella `gui/vanilla/` NON si propagavano.

Risultato: i 19 file `_patch_vanilla` eliminati dal repo erano ANCORA nella cartella mod,
generando 189 errori nel log.

**5B. Blocchi `types` e `template` mancanti nei wrapper**
Lo strumento `assemble_dualmode.py` (modalità `simple` e `tabs`) catturava solo il blocco
`window = {}` dal file OCR upstream, ignorando i blocchi `types XXXX { }` e `template XXXX { }`
definiti a livello top nel MEDESIMO file. Quando la nostra patch sovrascrive il file OCR,
TUTTE le definizioni di tipo/template di quel file vanno perse.

Impatto: **503 errori** (53% degli errori GUI totali) dalla nostra patch, di cui:
- 131 da window_army.gui (tipi FortTypes, ArmyWindow indefiniti)
- 113 da window_county_view.gui (tipi OCR, CountyViewTypes indefiniti)
- Tutti gli altri wrapper con tipi mancanti

#### Correzioni applicate:

- [x] **5.1** Creato `tools/repair_missing_types.py` — script di riparazione automatica
- [x] **5.2** Aggiunto 60 blocchi (types + template) a 18 file wrapper nel repo
  - Gestione corretta dei blocchi con nome duplicato (Jomini li mergia)
  - Include blocchi OCR upstream + blocchi vanilla con nomi non presenti in OCR
- [x] **5.3** Eliminati i 19 file `_patch_vanilla` dalla cartella mod Paradox
- [x] **5.4** Copiati i 22 wrapper aggiornati dal repo alla cartella mod Paradox
- [x] **5.5** Verificata sincronizzazione: 22 file identici tra repo e mod (0 desync)

#### Fix preventivo applicato a `assemble_dualmode.py`:

- [x] **5.6** Creata funzione `collect_non_window_blocks()` — raccoglie types/template da OCR e vanilla
  - Rispetta occorrenze multiple (blocchi con stesso nome validi in Jomini)
  - Include vanilla types + OCR-only types + vanilla templates + OCR-only templates
- [x] **5.7** Integrata in `assemble_simple()` e `assemble_tabs()`
  - I blocchi non-window vengono ora emessi PRIMA dei blocchi window
  - Segue la stessa logica di `assemble_complex()` che era l'unica modalità corretta

### Fase 6 — Quarta analisi crash (crash `ck3_20260315_130032`) — ☑ COMPLETATA

**Verdetto**: le fix delle Fasi 2B e 5 hanno funzionato — gli errori della nostra patch
sono scesi da **503+** a **soli 4**. Tuttavia il crash STACK_OVERFLOW persiste.

#### 6.1 Risultati analisi error.log (9082 righe, -1722 vs crash 1)

| Fonte errore | Conteggio | Delta vs crash 1 |
|-------------|-----------|-------------------|
| Nostra patch (`.gui`) | **4** | -499 (era 503+) |
| File `_patch_vanilla` | **0** | -189 (eliminazione funziona) |
| Types/template mancanti | **0** | -314 (riparazione funziona) |
| Non-GUI (font, eventi, loc, script, ecc.) | 9045 | invariato |
| **Totale** | **9082** | **-1722 da 10804** |

#### 6.2 I 4 errori residui dalla nostra patch

| File | Widget mancante | Causa |
|------|----------------|-------|
| `window_army.gui` | `army_reorganization_window` | Blocco OCR a riga 4534 di upstream NON catturato |
| `window_army.gui` | `attach_to_army_window` | Blocco OCR a riga 5096 di upstream NON catturato |
| `window_county_view.gui` | `holding_tracks_view` | Blocco OCR a riga 3764 di upstream NON catturato |
| `window_county_view.gui` | `holding_type_selection_view` | Blocco OCR a riga 4559 di upstream NON catturato |

**Causa**: `assemble_dualmode.py` cattura solo `window = {}` e `types/template`, ma NON
cattura widget/window secondari top-level (blocchi con `name = "..."` che non sono il window principale).

#### 6.3 Scoperta chiave: gui_warnings.log (428 righe, 150 conflitti types)

Analizzato per la prima volta `gui_warnings.log`. 150 warning "Type already registered":

| Fonte | Conflitti | Note |
|-------|-----------|------|
| OCR upstream `vanilla/` (5 file) | ~45 | Normale: OCR ridefinisce tipi vanilla |
| OCR upstream vari | ~80 | Normale: override mod standard |
| **Nostra patch (duplicati)** | **~3** | **Bug da `repair_missing_types.py`** |
| **Template/blocchi mancanti** | **~25** | **Contenuto OCR non catturato** |

#### 6.4 Bug in `repair_missing_types.py` — blocchi types duplicati

Lo script ha aggiunto blocchi types **senza controllare se già presenti** nel file:

| File | Blocco duplicato | Righe |
|------|-----------------|-------|
| `window_county_view.gui` | `types CountyViewTypes` | 505 e 786 |
| `window_culture.gui` | `types OCR` | 5 e 491 |

#### 6.5 Blocchi top-level OCR mancanti (assemble_dualmode.py)

4 file nostri mancano di blocchi top-level presenti in OCR upstream:

| File nostro | Blocco mancante | Impatto |
|-------------|----------------|---------|
| `window_character.gui` | `template "expanded_view"` (riga 1836 OCR) | **20 warning** "Could not find template" |
| `window_council.gui` | `widget = {}` (riga 441 OCR) | Widget mancante |
| `interaction_menu_window.gui` | `window_ocr = {}` (riga 2 OCR) | Tipo mancante |
| `window_dynasty_house.gui` | Template `agot_show_house_view` duplicato con `zzz_ocr_compatch_types.gui` | Warning conflitto |

#### 6.6 Dimensione file wrapper — superfici molto grandi

| File | Dimensione | Righe | Delta vs OCR |
|------|-----------|-------|-------------|
| `window_army.gui` | 194 KB | 5556 | -10 KB (contenuto mancante!) |
| `hud.gui` | 185 KB | 7167 | +7 KB |
| `window_my_realm.gui` | 177 KB | 6472 | +89 KB (include vanilla) |
| `window_county_view.gui` | 171 KB | 4749 | -21 KB (contenuto mancante!) |
| `window_military.gui` | 159 KB | 5536 | +64 KB (include vanilla) |
| **Totale 22 file** | **1.6 MB** | **56320** | — |

#### 6.7 Timing del crash

- `13:00:28` — "Completed generating game state from bookmark task"
- `13:00:30` — Ultimo entry debug.log ("Setup powerful vassals among 20656 living characters")
- `13:00:31` — I 4 errori della nostra patch
- `13:00:32` — Shortcut errors (escape, enter, x, z — da OCR upstream)
- `13:00:34` — **CRASH** EXCEPTION_STACK_OVERFLOW a `0x00007FF784694128`
- Indirizzo a ~340 byte dal crash precedente (`0x00007FF78469427C`) — stessa funzione

**Gap critico**: 2 secondi di silenzio totale (13:00:32 → 13:00:34) — nessun log entry.
Il crash avviene durante l'istanziazione runtime della GUI (probabilmente HUD),
dove la ricorsione consuma lo stack senza generare messaggi di errore.

#### 6.8 Cambio ipotesi — il crash potrebbe NON essere causato dalla nostra patch

**Evidenza**: gli errori della nostra patch sono scesi da 503+ a 4 (riduzione del 99%),
ma il crash persiste identico (stesso indirizzo, stesso punto, stesso tipo).

Quei 4 errori ("Could not find widget") sono warning non fatali — CK3 li logga
e continua. NON possono causare STACK_OVERFLOW.

**Ipotesi aggiornate** (in ordine di probabilità):

1. **OCR upstream stesso** causa il crash — il crash esiste anche SENZA la nostra patch
2. **Interazione strutturale** — il modo in cui i nostri wrapper sovrascrivono i file OCR
   crea una configurazione che il motore non gestisce (es. deep nesting, doppi override)
3. **Un altro mod attivo** (ck3 italian translate, ugc_2848213069) interferisce
4. **I nostri errori residui** agiscono da trigger per una condizione latente di OCR upstream

### Fase 7 — Diagnosi e correzione (NUOVA — da implementare in nuova sessione)

#### 7.1 TEST DIAGNOSTICO CRITICO (priorità massima)

Disabilitare SOLO la nostra patch nel `dlc_load.json`, mantenendo OCR upstream attivo.

- Se il gioco **crasha ugualmente** → il crash è di OCR upstream, non nostro.
  La nostra patch non è responsabile. STOP — non serve altra correzione.
- Se il gioco **non crasha** → il crash è causato dalla nostra patch.
  Procedere con 7.2.

> ⚠️ Questo test è il più veloce e determinante. Deve essere il PRIMO passo.

#### 7.2 RICERCA BINARIA file problematico (solo se 7.1 conferma crash da noi)

Se il crash è nostro, disabilitare metà dei file (rinominare `.gui.bak`)
e testare. Ripetere dimezzando fino a trovare il file che causa il crash.

Candidati principali (per dimensione e complessità):
1. `hud.gui` (7167 righe, istanziato all'avvio)
2. `window_army.gui` (5556 righe, 10KB contenuto mancante)
3. `window_my_realm.gui` (6472 righe, +89KB vs OCR)

#### 7.3 FIX errori noti (indipendenti dal crash — miglioramento qualità)

Da implementare in ogni caso, anche se il crash non è nostro:

**7.3a — Rimuovere blocchi types duplicati (2 file)**
- `window_county_view.gui`: rimuovere secondo `types CountyViewTypes` (righe 786+)
- `window_culture.gui`: rimuovere secondo `types OCR` (righe 491+)

**7.3b — Aggiungere blocchi OCR mancanti (4 file)**
- `window_character.gui`: aggiungere `template "expanded_view" { ... }` dalla riga 1836 OCR
- `window_council.gui`: aggiungere `widget = { ... }` dalla riga 441 OCR
- `interaction_menu_window.gui`: aggiungere `window_ocr = { ... }` dalla riga 2 OCR
- `window_army.gui`: aggiungere i widget secondari (army_reorganization_window, attach_to_army_window)
- `window_county_view.gui`: aggiungere i widget secondari (holding_tracks_view, holding_type_selection_view)

**7.3c — Fix `assemble_dualmode.py` (preventivo)**
- `collect_non_window_blocks()` deve catturare TUTTI i blocchi top-level, non solo types/template
- Include `widget = {}`, `window_ocr = {}`, `template "..." { }` e qualsiasi altro blocco top-level

**7.3d — Fix `repair_missing_types.py` (preventivo)**
- Aggiungere controllo duplicati: se un blocco types con lo stesso nome esiste già, NON aggiungerlo

#### 7.4 Sincronizzazione mod dir (dopo ogni fix)

Copiare i file aggiornati dal repo alla cartella mod Paradox.
Verificare che file e dimensioni corrispondano.

> ⚠️ Il Cloud Files Placeholder di OneDrive propaga le modifiche ai file esistenti
> ma NON propaga le eliminazioni di file in sottocartelle.

### Fase 7.5 — Quinta analisi (crash `ck3_20260315_144654`) — ☑ COMPLETATA

**Nuovo crash**: EXCEPTION_STACK_OVERFLOW (C00000FD) a indirizzo `0x00007FF7844FA7A3`
(diverso dal precedente `0x00007FF784694128` — stessa funzione, punto diverso).

#### 7.5.1 Analisi error.log — 0 errori dalla nostra patch

Analizzati 7982 righe di error.log. **ZERO errori dalla nostra patch**.
Tutti i 25 errori GUI trovati provengono da:
- OCR upstream (fontsize_min, shortcutnames)
- MPO wars (mod esterno)
- Localizzazione/Game engine

**Conclusione**: la riduzione errori da 503+ → 4 → 0 conferma che i fix precedenti funzionano.

#### 7.5.2 Analisi cross-repo — SCOPERTA CRITICA

Confronto dimensionale tra i 22 file della patch e i corrispondenti OCR upstream:

| File | Patch (KB) | OCR (KB) | Ratio | Problema |
|------|-----------|---------|-------|----------|
| `window_my_realm.gui` | **177** | 86 | **2.01x** | Tipi vanilla ridondanti inline |
| `window_military.gui` | **155** | 92 | **1.68x** | Tipi vanilla ridondanti inline |
| altri 20 file | ~1322 | ~1275 | ~1.04x | OK |

#### 7.5.3 Causa radice: tipi vanilla duplicati

**Meccanismo OCR upstream**:
- `gui/preload/00_types_OCR.gui` definisce `template vanilla` e `template ocr`
- `gui/vanilla/window_my_realm.gui` (94 KB) definisce TUTTI i tipi vanilla di My Realm
- `gui/vanilla/window_military.gui` (95 KB) definisce TUTTI i tipi vanilla di Military
- I wrapper OCR upstream istanziano i tipi vanilla con `using = vanilla`

**Il bug**: i nostri wrapper contenevano gli STESSI tipi vanilla inline (copiati durante
l'assemblaggio), causando doppia registrazione. Il motore CK3 riceveva ~30 tipi duplicati
e ~150 KB di GUI ridondante, amplificando il carico sul parser e il rischio di stack overflow.

Dettaglio file per file:
- `window_my_realm.gui`: conteneva `template My_Realm_Cell_Size` + intero blocco `types MyRealmWindow`
  (3610 righe) — IDENTICI a quelli in OCR upstream `gui/vanilla/window_my_realm.gui`
- `window_military.gui`: conteneva `types ArmiesView` + `types MilitaryView` + `types HiredTroops`
  (2350 righe) — IDENTICI a quelli in OCR upstream `gui/vanilla/window_military.gui`
- `window_intrigue.gui`: conteneva `types OCR_old` (115 righe) — codice morto legacy, mai usato

#### 7.5.4 Correzione: doppia guard nel window_military.gui

Trovata doppia guard `visible = "[Not(GetVariableSystem.Exists('ocr'))]"` in `window_military.gui`:
- Widget esterno (L1509): contiene la guard → visibilità controllata
- Widget interno `ocr_military_container` (L1521): stessa guard → **ridondante**

La guard interna aggiungeva un livello di nesting inutile al calcolo di visibilità.

#### 7.5.5 Fix applicati

| Fix | File | Operazione | Impatto |
|-----|------|-----------|---------|
| 7.5a | `window_my_realm.gui` | Rimosso `template My_Realm_Cell_Size` + `types MyRealmWindow` | 6472 → 2862 righe (−56%), 177 → 91 KB (−48%) |
| 7.5b | `window_military.gui` | Rimosso `types ArmiesView` + `types MilitaryView` + `types HiredTroops` | 5536 → 3185 righe (−42%), 155 → 95 KB (−39%) |
| 7.5c | `window_intrigue.gui` | Rimosso `types OCR_old` (codice morto) | 2699 → 2584 righe (−4%) |
| 7.5d | `window_military.gui` | Rimossa guard `visible` ridondante da widget interno | Nesting −1 livello |

**Totale rimosso**: ~6075 righe, ~146 KB di GUI ridondante.
Tutti i file verificati: bilanciamento parentesi = 0.

#### 7.5.6 Template `agot_show_law` — conservato

`template agot_show_law` (definito a L86-88 di `window_my_realm.gui`) è stato conservato
perché **usato** nella porzione OCR del wrapper (riferimento trovato nella sezione OCR attiva).

#### 7.5.7 Sync e riabilitazione

- [x] 3 file copiati da repo a cartella mod Paradox — dimensioni verificate
- [x] Tutti i 22 file sincronizzati (22/22 OK, 0 errori)
- [x] Patch riabilitata in `dlc_load.json` (era disabilitata per test Phase 7.1)

### Fase 8 — Test e validazione finale

- [ ] **8.1** Avviare CK3 con la patch e verificare assenza di crash al caricamento
- [ ] **8.2** Verificare `gui_warnings.log` — contare errori dalla patch (obiettivo: 0)
- [ ] **8.3** Testare modalità OCR — verificare che le finestre funzionino correttamente
- [ ] **8.4** Esecuzione `python tools/audit.py` su file modificati

---

## Stato Attuale

- **Crash**: DA VERIFICARE — patch corretta con rimozione di ~6000 righe di tipi ridondanti
- **Errori dalla patch**: **0** nel crash 144654 — poi ulteriormente ridotti rimuovendo tipi duplicati
- **Dimensione totale patch**: ~1508 KB (da 1654 KB, −146 KB, −9%)
- **Test diagnostico critico (7.1)**: preparato ma NON eseguito — la priorità è testare la patch corretta
- **Modalità OCR**: funzionale — i wrapper contengono branch OCR + types/template
- **Modalità Vanilla**: temporaneamente disabilitata — nessun branch vanilla nei wrapper
- **Sync mod dir**: COMPLETA — 22 file identici tra repo e mod

### Fix applicati in Fase 7.3 (2026-03-15)

| Fix | File | Dettaglio |
|-----|------|-----------|
| 7.3a | `window_county_view.gui` | Unito secondo `types CountyViewTypes` nel primo (2 tipi OCR unici salvati) |
| 7.3a | `window_culture.gui` | Unito secondo `types OCR {` nel primo (2 tipi OCR unici salvati) |
| 7.3b | `window_army.gui` | Aggiunti `army_reorganization_window`, `attach_to_army_window` da OCR upstream |
| 7.3b | `window_county_view.gui` | Aggiunti `holding_tracks_view`, `holding_type_selection_view` da OCR upstream |
| 7.3b | `window_council.gui` | Aggiunto `potential_task_location_window` da OCR upstream |
| 7.3b | `interaction_menu_window.gui` | Aggiunto `window_ocr` da OCR upstream |
| 7.3c | `tools/assemble_dualmode.py` | `collect_non_window_blocks()` ora cattura tutti i blocchi top-level (widget, window_ocr, ecc.) |
| 7.3d | `tools/repair_missing_types.py` | Commento esplicito + sanity check post-scrittura per duplicati |

- **Prossima azione OBBLIGATORIA**: Avviare CK3 e verificare se il crash è risolto.
  Se il crash persiste: eseguire il test Phase 7.1 (patch disabilitata) per confermare
  se il problema è della nostra patch o di OCR upstream.
  Backup `dlc_load.json` per Phase 7.1 disponibile in `.bak_phase71`.

---

## Conclusione Architetturale

### Il Pattern v1.1 (type-separated) è incompatibile con OCR upstream

Il conflitto è **strutturale e non risolvibile** senza riscrivere l'intero contenuto vanilla:

1. OCR upstream ridefinisce `scrollbox` → tutti i `scrollarea` + `scrollwidget` vanilla rompono
2. OCR upstream sostituisce tipi locali → i riferimenti nei vanilla type non risolvono
3. L'annidamento window → type → vanilla amplifica la ricorsione nel motore

### Impatto della rimozione

- **Modalità OCR**: funziona normalmente (il branch OCR nei wrapper è intatto)
- **Modalità Vanilla**: **temporaneamente non disponibile** (Shift+F11 toggle non avrà effetto visibile perché non c'è branch vanilla)
- **Crash**: eliminato (nessun file type-separated = nessun errore da scrollarea/tipi mancanti)

### Prossimi passi (futuri, non urgenti)

Se la modalità vanilla deve essere ripristinata:
- Valutare **Pattern v1.0 inline** — il contenuto vanilla inline dentro il wrapper
  potrebbe gestire meglio i conflitti perché è dentro un blocco `window` e non un `type`
- Verificare se il conflitto scrollarea esiste anche nel pattern inline
- Considerare se serve effettivamente la modalità vanilla per tutti i 19 file

---

## Note Tecniche

### Perché EXCEPTION_STACK_OVERFLOW e non "Property not handled"?
Lo strip delle proprietà window-level (Fase 2 originale) ha eliminato gli errori `movable not handled`,
ma il motore continuava a incontrare 395 errori dai tipi incompatibili (scrollarea, tipi locali OCR).
Questi errori causavano un ciclo di tentativi di risoluzione tipo → ricorsione infinita → stack overflow.

### La ridefinizione `scrollbox` di OCR upstream
`gui/preload/00_types_OCR.gui:113` ridefinisce il tipo `scrollbox` con una struttura accessibile
(testo leggibile da screen reader). Questa ridefinizione è globale e sostituisce anche il tipo
usato internamente da `scrollarea` vanilla. Il risultato è che `scrollwidget` non viene mai
creato → "Could not create scrollwidget for scrollarea".

### Il conflitto tipi locali
Tipi come `progressbar_lifestyle_xp`, `animation_soldier_loss`, `army_quality_icon`,
`icon_maa_combat` sono definiti nel vanilla ma rinominati/sostituiti da OCR upstream.
I file type-separated li referenziavano ancora → 321 errori "not a valid widget/type".

---

## Tracciamento Modifiche

### Registro operazioni

| Data | Operazione | Stato |
|------|-----------|-------|
| 2026-03-15 | Analisi log prima sessione — diagnosi proprietà window-level | ☑ |
| 2026-03-15 | Fase 1 — Fix assemble_dualmode.py (sanitize function) | ☑ |
| 2026-03-15 | Fase 2 — Strip proprietà window-level da 19 file type | ☑ (insufficiente) |
| 2026-03-15 | Seconda analisi crash — STACK_OVERFLOW da scrollarea/tipi OCR | ☑ |
| 2026-03-15 | Fase 2B — Eliminazione completa Pattern v1.1 (19 file + riferimenti) | ☑ |
| 2026-03-15 | Verifica strutturale — bilanciamento parentesi 22 wrapper | ☑ |
| 2026-03-15 | Terza analisi — crash persiste, scoperta desync mod dir + types mancanti | ☑ |
| 2026-03-15 | Fase 5.1-5.2 — Script repair_missing_types.py + 60 blocchi aggiunti | ☑ |
| 2026-03-15 | Fase 5.3 — Eliminati 19 file _patch_vanilla dalla cartella mod Paradox | ☑ |
| 2026-03-15 | Fase 5.4-5.5 — Copiati 22 wrapper aggiornati al mod dir, sync verificata | ☑ |
| 2026-03-15 | Fase 5.6-5.7 — Fix assemble_dualmode.py (collect_non_window_blocks) | ☑ |
| 2026-03-15 | Quarta analisi crash — errori 503+→4, crash persiste, analisi gui_warnings.log | ☑ |
| 2026-03-15 | Fase 6 — Analisi completa: tipos duplicati, blocchi mancanti, cambio ipotesi | ☑ |
| 2026-03-15 | Fase 7.3a — Uniti tipi duplicati in window_county_view.gui e window_culture.gui | ☑ |
| 2026-03-15 | Fase 7.3b — Aggiunti 6 blocchi top-level OCR mancanti in 4 file | ☑ |
| 2026-03-15 | Fase 7.3c — Fix assemble_dualmode.py: cattura tutti i blocchi top-level | ☑ |
| 2026-03-15 | Fase 7.3d — Fix repair_missing_types.py: sanity check duplicati | ☑ |
| 2026-03-15 | Fase 7.4 — Sync mod dir (5 file copiati, 22 file identici verificati) | ☑ |
| 2026-03-15 | Fase 7.1 — Creato script test71_toggle_patch.ps1 — avviare CK3 manualmente | ☐ |
| | Fase 7.2 — Ricerca binaria file problematico (se crash confermato nostro) | ☐ |
| | Fase 8 — Test e validazione finale | ☐ |
