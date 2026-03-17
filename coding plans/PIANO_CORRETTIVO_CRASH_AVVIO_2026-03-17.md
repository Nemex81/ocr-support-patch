# Piano Correttivo — Crash in Avvio CK3 con OCR Support Patch

Data: 2026-03-17
Versione CK3: 1.17.1
Branch: experiment/dual-mode-type-separation

> **NOTA: Piano validato il 2026-03-17.** Esito validazione: PASS CON CORREZIONI.
> Correzioni integrate nella Sezione 9 in fondo al documento.
>
> **AGGIORNAMENTO 2026-03-17 (secondo intervento):** Dopo le Fasi 1–4 il gioco
> raggiunge il menù principale, ma crasha con **EXCEPTION_STACK_OVERFLOW (C00000FD)**
> durante il caricamento di una nuova partita. Nuove Fasi 5–8 aggiunte (vedi sotto).

---

## SOMMARIO IMPLEMENTAZIONE — PROGRESSO

> Legenda: `[x]` = completato | `[ ]` = da fare | `[~]` = in corso

### Fase 1 — Rimozione Proprietà Duplicate (File Inline)

- [x] `window_activity_list.gui` — container L828: rimuovere `name`, `parentanchor`, `layer`, `movable`
- [x] `window_activity_list.gui` — container L1222: rimuovere `name`, `parentanchor`, `position`, `size`, `layer`
- [x] `window_activity_list.gui` — container L1731: rimuovere `name`, `parentanchor`, `position`, `size`, `layer`
- [x] `window_character.gui` — container L263: rimuovere `name`, `widgetid`, `movable`, `layer`
- [x] `window_council.gui` — container L2895: rimuovere `name`, `widgetid`, `parentanchor`, `layer`, `movable`
- [x] `window_decisions.gui` — container L319: rimuovere `name`, `parentanchor`, `layer`, `movable`
- [x] `window_factions.gui` — container L836: rimuovere `name`, `parentanchor`, `layer`, `movable`
- [x] `window_intrigue.gui` — container L651: rimuovere `name`, `widgetid`, `parentanchor`, `layer`, `movable`

### Fase 2 — Variabile @txt_width Mancante

- [x] `window_activity_list.gui` — aggiungere `@txt_width = 700` come prima riga del file

### Fase 3 — Fix interaction_blackmail.gui

- [x] `interaction_blackmail.gui` — rimuovere/sostituire `button_standard_text` con tipo valido
- [x] `interaction_blackmail.gui` — rimuovere `Character.GetTooltip` (righe 92, 312)
- [x] `interaction_blackmail.gui` — rimuovere `OpenCharacterInteractionMenu(Character.GetID)` (riga 311)
- [x] `interaction_blackmail.gui` — correggere sound effect inesistente (riga 449)

### Fase 4 — Rimozione Proprietà Duplicate (File Type-Separated)

- [x] `vanilla/army_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/character_lifestyle_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/combat_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/county_view_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/court_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/culture_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/dynasty_house_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/faith_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/interaction_interfere_in_war_notification_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/military_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)
- [x] `vanilla/my_realm_patch_vanilla.gui` — rimuovere `name` interno (riga ~11)

### ─── STORICO: Fasi 5–6 originali (superate dal secondo intervento) ───

> Le Fasi 5 e 6 originali sono state assorbite dal Secondo Intervento (Fasi 5–8 sotto).
> La vecchia "Fase 5 opzionale" è diventata la nuova Fase 7 (CRITICO).
> La vecchia "Fase 6 anomali" è stata integrata nella Fase 8.

---

### Fase 5 — Sincronizzazione Deploy (SECONDO INTERVENTO)

- [x] Copiare TUTTI i file da `gui/vanilla/` del workspace Git al deploy path del gioco
- [x] Verificare hash MD5 di almeno 3 file dopo la copia

> **Percorso workspace**: `c:\...\GitHub\ocr-support-patch\ocr_support_compatibility_pach\gui\vanilla\`
> **Percorso deploy**: `C:\...\Paradox Interactive\Crusader Kings III\mod\ocr_support_compatibility_pach\gui\vanilla\`

### Fase 6 — Fix Proprietà Window-Level in Container Vanilla Inline (SECONDO INTERVENTO)

- [x] `window_character.gui` — rimuovere `movable = no` e `layer = middle` dal container vanilla (righe 265-266). MANTENERE `allow_outside = yes` (valida per widget)
- [x] `window_intrigue.gui` — rimuovere `layer = windows_layer`, `movable = no` dal container vanilla (righe 652-653)
- [x] Copiare i file corretti anche nel deploy path

### Fase 7 — Ripristino Blocchi `types` OCR Mancanti (SECONDO INTERVENTO — CRITICO)

- [x] `window_army.gui` — iniettare 22 tipi OCR dall'upstream (army_location, army_quality_icon, ecc.)
- [x] `window_county_view.gui` — iniettare 17 tipi OCR (adjacent_county_button, button_holding, ecc.)
- [x] `window_dynasty_house.gui` — iniettare 13 tipi OCR (hbox_access_domicile_button, legacy_progress, ecc.)
- [x] `window_culture.gui` — iniettare types OCR (vox_era_tab_ocr e altri, 4 namespace: OCR×2, CultureWindow, CultureShared)
- [x] `window_military.gui` — iniettare types OCR (widget_event_troop_item_ocr e altri, namespace OCR)
- [x] `window_faith.gui` — iniettare types OCR (name_entry_big e altri, 4 namespace: FaithCreationWindow, OCR, FaithShared, FaithWindow)
- [x] `window_combat.gui` — iniettare 5 tipi OCR (animation_soldier_loss, icon_maa_combat, ecc.)
- [x] `window_character_lifestyle.gui` — iniettare 4 tipi OCR (progressbar_lifestyle_xp, ecc.)
- [x] `window_my_realm.gui` — iniettare 4 tipi OCR (button_ruler_browser, ecc.)
- [x] `window_inventory.gui` — iniettato intero blocco InventoryViewTypes con 9 tipi (inclusi `artifact_claim_ocr` e `widget_artifact_entry_ocr`). Nessun duplicato nei file adiacenti.
- [x] `window_factions.gui` — iniettato `vbox_faction_item_ocr` nel blocco FactionWindow ESISTENTE

> **REGOLA**: Per file con blocco `types` GIÀ esistente (inventory, factions),
> iniettare solo i types singoli mancanti DENTRO il blocco esistente.
> NON creare un secondo blocco `types` — causerebbe "Duplicate type definition".
- [x] Copiare tutti i file corretti nel deploy path (hash MD5 verificato per 11/11 file)

### Fase 8 — Test Secondo Intervento

- [x] Test: avvio CK3 — errori "not valid" scesi da 661 a **5** (riduzione 99.2%)
- [x] Verificare `error.log` — conteggio errori drasticamente ridotto ✓
- [ ] PROBLEMA: il gioco si blocca dopo "End loading of history" (nessun crash dump) — non raggiunge il menu principale

> **ESITO FASE 8**: Iniezione types RIUSCITA (da 661 a 5 errori), ma il gioco si blocca prima del menu principale.
> Servono correzioni aggiuntive → Fasi 9–12.

### Fase 9 — Fix Encoding UTF-8 BOM (TERZO INTERVENTO)

I 4 file riscritti da PowerShell `Set-Content -Encoding UTF8` hanno BOM (EF BB BF) mentre tutti gli altri sono UTF-8 senza BOM. CK3 potrebbe non gestire la differenza.

- [x] `window_culture.gui` — BOM rimosso (65432 -> 65429)
- [x] `window_military.gui` — BOM rimosso (97863 -> 97860)
- [x] `window_faith.gui` — BOM rimosso (53453 -> 53450)
- [x] `window_inventory.gui` — BOM rimosso (88881 -> 88878)
- [x] Copiato nel deploy path — hash verificato OK

### Fase 10 — Fix Tipo Duplicato `building_in_vassal_warning_hbox` (TERZO INTERVENTO)

Definito DUE volte in `window_county_view.gui`: riga ~252 (versione OCR semplificata) e riga ~617 (versione vanilla con `coa_title_tiny`). La versione vanilla (riga ~617) è quella corretta.

- [x] Rimossa definizione OCR a riga 252 (mantenuta vanilla a riga 604)
- [x] Copiato nel deploy path — hash verificato OK

### Fase 11 — Iniettare Template OCR Mancanti (TERZO INTERVENTO)

I template sono definiti nel file upstream FUORI dai blocchi `types {}` — non estratti in Fase 7.

- [x] `window_army.gui` — aggiunti 4 template (righe 1109, 1173, 1180, 1188)
- [x] `window_dynasty_house.gui` — aggiunti 2 template (righe 833, 837)
- [x] `window_my_realm.gui` — aggiunto 1 template (riga 87)
- [x] Copiato nel deploy path — hash verificato OK

### Fase 12 — Iniettare Tipo Vanilla `prison_interactions_hbox` (TERZO INTERVENTO)

Tipo definito nel `window_court.gui` vanilla (riga 753) ma non nell'OCR upstream né nella patch. Referenziato in `court_patch_vanilla.gui` righe 359, 565.

- [x] Estratta definizione completa tipo `prison_interactions_hbox` dal vanilla (righe 749-817)
- [x] Iniettata in `window_court.gui` dentro blocco `types PrisonTypes {}` (riga 6, prima di window)
- [x] Copiato nel deploy path — hash verificato OK

### Fase 13 — Test e Verifica Finale (TERZO INTERVENTO)

- [ ] Test: avvio CK3, raggiungere il menu principale
- [ ] Verificare `error.log` — "not valid" ≤ 2 (tooltip_paragraph è engine-level, non risolvibile)
- [ ] Se menu raggiunto: nuova partita → selezione personaggio senza crash

---

## 4b. Diagnostica Secondo Intervento — Crash Nuova Partita (Stack Overflow)

### Sintesi

Dopo l'implementazione delle Fasi 1–4, il gioco raggiunge il menù principale
(confermando che quelle fix erano necessarie). Tuttavia, selezionando "Nuova partita",
fissando l'epoca e confermando, il gioco crasha con **EXCEPTION_STACK_OVERFLOW (C00000FD)**
durante il caricamento della fase di selezione personaggio/territorio.

### Dettagli Crash Dump

| Campo | Valore |
|-------|--------|
| Tipo eccezione | EXCEPTION_STACK_OVERFLOW (C00000FD) |
| Indirizzo | 0x00007FF63ABAA7A3 |
| Frame nello stack | **42.641** (tutti `ck3.exe`, nessun nome funzione) |
| Timestamp crash | 2026-03-17 12:14:29 |
| Crash dump | `crashes/ck3_20260317_121429/` |
| Game state generation | Completata con successo alle 12:14:27 |
| Crash point | Transizione da game state alla GUI in-game (istanziazione widget) |

### Statistiche Errori — Secondo Run

| Tipo errore | Conteggio | vs. primo run | Note |
|-------------|-----------|--------------|------|
| Duplicate property 'name' | 11 | ↓ da 19 | 8 fix inline deployate, 11 type-sep NON deployate |
| Malformed token | 0 | ↓ da 5 | Fix @txt_width deployata |
| Not valid widget/type | **661** | ↑ da 484 | Il gioco va più avanti → più GUI istanziata → più errori |
| Failed reading property | 11 | nuovo | Proprietà non gestite da widget (movable, layer) |
| Failed converting/parsing | 13 | ↑ da 18 | Binding non validi |
| Layer already registered | 12 | = | Layer duplicati (tollerato) |

### SCOPERTA CRITICA 1 — Gap di Deployment

Le fix della Fase 4 (rimozione `name` duplicato dai file type-separated) sono nel
workspace Git ma **non sono mai state copiate nel deploy path del gioco**.

| Aspetto | Workspace Git | Deploy Path Gioco |
|---------|--------------|-------------------|
| Percorso | `GitHub/ocr-support-patch/ocr_support_compatibility_pach/` | `Paradox Interactive/CK3/mod/ocr_support_compatibility_pach/` |
| File inline (24) | Corretti → **UGUALI** | Corretti → **UGUALI** |
| File vanilla/ (11) | Corretti (Fase 4) | **VECCHI — fix NON deployate!** |

Evidenza: `army_patch_vanilla.gui` nel deploy ha ancora `name = "army_window"` alla
riga 11, mentre il workspace ha la riga rimossa. Hash MD5 diverso per tutti gli 11 file.

### SCOPERTA CRITICA 2 — 97 Types OCR Persi (Root Cause dei 661 Errori)

Il nostro mod sostituisce completamente 12 file dell'OCR upstream (meccanismo override CK3).
I file originali dell'OCR upstream definiscono blocchi `types { }` con tipi personalizzati.
Quando il nostro wrapper sostituisce quei file, **i blocchi `types` scompaiono**.

**Totale types persi**: 95 (in 11 file — `frontend_main.gui` escluso: il suo unico type è già presente)
**Di cui referenziati cross-file**: 24 types usati da file OCR che NON sostituiamo

File più colpiti:
- `window_army.gui` → 22 types persi (es. `army_location` usato in `hud_outliner.gui`)
- `window_county_view.gui` → 17 types persi (es. `button_holding` usato in `_OCR_WIDGET.gui`)
- `window_dynasty_house.gui` → 13 types persi
- `window_culture.gui` → 11 types persi (es. `widget_tradition_icon` usato in 3 file)
- `window_military.gui` → 9 types persi
- `window_faith.gui` → 8 types persi (es. `container_tenet_item` usato in `window_faith_creation.gui`)

### SCOPERTA CRITICA 3 — Proprietà Window-Level in Container Widget

Due file hanno proprietà `movable` e `layer` all'interno di container `widget`
(valide solo per `window`):

- `window_character.gui:265-267` → `movable = no`, `layer = middle`, `allow_outside = yes`
- `window_intrigue.gui:652-653` → `layer = windows_layer`, `movable = no`

CK3 segnala: `Property 'movable'(819) not handled` + `Error setting properties for widget`.

### Ipotesi Stack Overflow

Con 42.641 frame nello stack (ricorsione infinita), la causa è nel motore Clausewitz
durante l'istanziazione dell'albero GUI in-game. Il crash accade dopo che il game state
è generato con successo (12:14:27), durante la costruzione dei widget (12:14:29).

**Ipotesi primaria**: la combinazione massiva di 661 errori "not valid widget/type" durante
la costruzione dell'albero widget crea uno stato corrotto in catena, provocando ricorsione
infinita nel motore di risoluzione dei tipi. Risolvere i types mancanti (Fase 7) dovrebbe
eliminare la causa o ridurla drasticamente.

**Ipotesi secondaria**: un singolo tipo mancante usato come `scrollwidget` o
`layoutwidget` in un `scrollarea` potrebbe innescare un loop di retry nel motore.
Identificabile solo eliminando i types mancanti e verificando se il crash persiste.

### Approccio Correttivo — Fasi 5–8

**Fase 5 — Sincronizzazione Deploy**: copire i file corretti dal workspace al deploy path.
Risolve il gap di deployment e porta le fix Fase 4 al gioco.

**Fase 6 — Fix proprietà window-level**: rimuovere `movable`, `layer`, `allow_outside`
dai container `widget` in `window_character.gui` e `window_intrigue.gui`.

**Fase 7 — Ripristino types OCR** (CRITICO): per ciascuno dei 12 wrapper che sostituiscono
un file OCR upstream, copiare il blocco `types { }` dall'OCR upstream e iniettarlo
all'inizio del nostro wrapper. Questo ripristina tutti i 97 types senza alterare
il funzionamento dual-mode.

**Fase 8 — Test**: avviare nuova partita e verificare che la selezione personaggio
venga raggiunta senza crash. Se persiste, isolamento progressivo.

---

Il gioco si blocca durante il caricamento e non raggiunge il menù principale.
Dai log di runtime, il motore CK3 arriva alla fase "Frontend" (`Setting idler 'Frontend'`)
ma il menù non viene renderizzato. Nessun crash dump generato (cartella crashes vuota).

**Causa radice**: effetto cumulativo di **494 errori GUI** e **5 errori di parsing**
generati dai file della patch durante il bootstrap. Il sistema GUI entra in stato
degradato e non riesce a renderizzare il frontend.

---

## 2. Statistiche Errori dal Log di Runtime

| Tipo errore | Conteggio | Gravità |
|-------------|-----------|---------|
| Duplicate property 'name' | 19 | **CRITICO** — parsing fallito |
| Malformed token (@txt_width) | 5 | **CRITICO** — parsing fallito |
| Not valid widget/type/property | 484 | ALTO — type non risolti |
| Failed converting/parsing | 18 | ALTO — binding invalidi |
| Layer already registered | 12 | BASSO — warning tollerato |

---

## 3. Cause Radice Identificate

### CAUSA 1 — Proprietà `name` duplicata nei container vanilla (CRITICA)

**Descrizione**: L'assembler `assemble_dualmode.py` crea i container vanilla
wrappando il contenuto del file CK3 originale dentro un widget con proprio `name`:

```jomini
widget = {
    name = "vanilla_X_container"        # ← name del wrapper
    visible = "[GetVariableSystem.Exists('ocr')]"

        name = "original_window_name"   # ← DUPLICATO! name del file vanilla
        widgetid = "..."                # ← anche questo è problematico
        layer = windows_layer           # ← proprietà che non dovrebbe stare qui
```

Il contenuto vanilla viene copiato integralmente senza rimuovere le proprietà
che appartengono al livello superiore (`name`, `widgetid`, `layer`, `movable`,
`parentanchor`, `attachto`). CK3 segnala "Duplicate property 'name'(27)" e
scarta la proprietà duplicata, ma il widget risultante ha una struttura corrotta.

**File coinvolti (19 totali)**:

Inline (8 file):
- `window_activity_list.gui` — 3 istanze (righe 828, 1222, 1731)
- `window_character.gui` — 1 istanza (riga 263)
- `window_council.gui` — 1 istanza (riga 2895)
- `window_decisions.gui` — 1 istanza (riga 319)
- `window_factions.gui` — 1 istanza (riga 836)
- `window_intrigue.gui` — 1 istanza (riga 651)

Type-separated (11 file, tutti a riga 11):
- `vanilla/army_patch_vanilla.gui`
- `vanilla/character_lifestyle_patch_vanilla.gui`
- `vanilla/combat_patch_vanilla.gui`
- `vanilla/county_view_patch_vanilla.gui`
- `vanilla/court_patch_vanilla.gui`
- `vanilla/culture_patch_vanilla.gui`
- `vanilla/dynasty_house_patch_vanilla.gui`
- `vanilla/faith_patch_vanilla.gui`
- `vanilla/interaction_interfere_in_war_notification_patch_vanilla.gui`
- `vanilla/military_patch_vanilla.gui`
- `vanilla/my_realm_patch_vanilla.gui`

### CAUSA 2 — Variabile locale `@txt_width` mancante (CRITICA)

**Descrizione**: `window_activity_list.gui` usa `@txt_width` in 5 punti
(righe 1162, 1180, 1181, 1194, 1195) ma la definizione (`@txt_width = 700`)
è presente solo nel file OCR upstream (riga 1). L'assembler non ha copiato
la definizione della variabile locale durante la generazione del file patch.

CK3 segnala "Malformed token: @txt_width" — errore di parsing che invalida
l'intero blocco contenente il token.

### CAUSA 3 — Type mancanti nei file vanilla type-separated (ALTA)

**Descrizione**: I file nella cartella `vanilla/` estraggono il contenuto della
finestra dal file CK3 originale, ma NON includono i type definiti altrove
nello stesso file o in file correlati. I type sono definiti in blocchi `types`
che rimangono nel file vanilla originale, ma siccome la patch fa override del file,
quei type definition vengono sostituiti dal contenuto OCR e non sono più disponibili.

**Esempi di type mancanti** (totale: ~484 errori):
- `combat_patch_vanilla.gui`: `animation_soldier_loss`, `army_quality_icon`, `icon_maa_combat`
- `culture_patch_vanilla.gui`: `container_pillar_item`, `icon_innovation`, `widget_tradition_icon`
- `faith_patch_vanilla.gui`: `fervor_container_vbox`, `container_tenet_item`, `widget_doctrine_item`
- `dynasty_house_patch_vanilla.gui`: `widget_legacy_icon`, `legacy_progress`, `widget_house_unity_status_bar`
- `military_patch_vanilla.gui` (e anche `vanilla/window_military.gui`): `hbox_soldiers_and_quality_small`, `army_quality_icon`
- `county_view_patch_vanilla.gui`: `widget_building_item`
- `court_patch_vanilla.gui`: `prison_interactions_hbox`
- `character_lifestyle_patch_vanilla.gui`: `progressbar_lifestyle_xp`, `icon_lifestyle_unspent_points`
- `army_patch_vanilla.gui`: `soldiers_and_quality_big`

**Nota**: nella cartella `vanilla/` c'è anche `window_military.gui`, che NON è
un file type-separated con naming convention corretta. Andrebbe rinominato
`military_patch_vanilla.gui` (che tra l'altro esiste già). Verificare se è un doppione.

### CAUSA 4 — Binding e funzioni invalide in `interaction_blackmail.gui` (MEDIA)

**Descrizione**: Il file patch usa binding che non esistono in CK3 1.17.1:
- `button_standard_text` (riga 87) — type inesistente
- `Character.GetTooltip` (righe 92, 312) — funzione inesistente
- `OpenCharacterInteractionMenu(Character.GetID)` (riga 311) — funzione inesistente
- Sound effect `sfx_ui_generic_pointer_over_large` (riga 449) — non trovato

Questi NON provengono dall'OCR upstream (il file upstream non li contiene).

### CAUSA 5 — Errore di parsing in `hud.gui` (MEDIA)

**Descrizione**: `hud.gui` riga 6414 usa `Character.GetTaxSlotsWithoutTaxCollectorCount`
che non è una funzione valida. Genera "Failed parsing localized text" che invalida il widget.

---

## 4. Piano di Correzione

### Fase 1 — Fix Proprietà Duplicate (PRIORITÀ MASSIMA)

**Obiettivo**: Rimuovere la proprietà `name` duplicata e le altre proprietà
di livello superiore (`widgetid`, `layer`, `movable`, `parentanchor`, `attachto`)
dal contenuto vanilla incapsulato nei container wrapper.

**Strategia**: Per ogni file, il contenuto vanilla dopo la riga
`visible = "[GetVariableSystem.Exists('ocr')]"` deve essere "innestato" correttamente.
Le proprietà che appartengono al livello `window` originale (name, widgetid, layer,
movable, attachto, parentanchor) devono essere rimosse dal contenuto incapsulato,
perché il container wrapper le fornisce già o non devono essere presenti su widget interni.

**Approccio**: Per ogni file coinvolto:
1. Individuare la riga con `name = "vanilla_*_container"` e il relativo `visible`
2. Rimuovere le righe immediatamente successive che contengono proprietà duplicate:
   - `name = "..."` (il nome originale della finestra vanilla)
   - `widgetid = "..."` (se presente)
   - `layer = ...` (se presente)
   - `movable = ...` (se presente)
   - `parentanchor = ...` (se presente — TRANNE quando è su un sotto-widget legittimo)
   - `attachto = ...` (se presente)
3. Verificare che le parentesi graffe rimangano bilanciate

**File da correggere — Inline** (8 file, ~8 modifiche totali):

| File | Riga approx. | Proprietà da rimuovere |
|------|--------------|----------------------|
| `window_activity_list.gui` | 828 | `name`, `parentanchor`, `layer`, `movable` |
| `window_activity_list.gui` | 1222 | `name`, `parentanchor`, `position`, `size`, `layer` |
| `window_activity_list.gui` | 1731 | `name`, `parentanchor`, `position`, `size`, `layer` |
| `window_character.gui` | 263 | `name`, **`widgetid`**, `movable`, `layer` |
| `window_council.gui` | 2895 | `name`, **`widgetid`**, `parentanchor`, `layer`, `movable` |
| `window_decisions.gui` | 319 | `name`, `parentanchor`, `layer`, `movable` |
| `window_factions.gui` | 836 | `name`, `parentanchor`, `layer`, `movable` |
| `window_intrigue.gui` | 651 | `name`, **`widgetid`**, `parentanchor`, `layer`, `movable` |

> **ATTENZIONE — widgetid duplicato**: `window_character.gui`, `window_council.gui`
> e `window_intrigue.gui` hanno anche un `widgetid` duplicato (lo stesso valore è
> usato sia sul `window` root che nel container vanilla). Questo causa conflitto
> nel routing degli input. Rimuovere il `widgetid` dal container vanilla.

**File da correggere — Type-separated** (11 file, 11 modifiche):

Per tutti i file in `vanilla/`, rimuovere la riga 11 (`name = "original_window_name"`)
e qualsiasi altro `widgetid`, `layer`, `movable`, `attachto`, `parentanchor` che segue.

### Fase 2 — Fix Variabile Locale @txt_width (PRIORITÀ ALTA)

**Obiettivo**: Aggiungere la definizione `@txt_width = 700` all'inizio di
`window_activity_list.gui` (prima del primo blocco `window`).

**Modifica**: Inserire la seguente riga dopo i commenti di intestazione:
```
@txt_width = 700
```

### Fase 3 — Rigenerazione File con assemble_dualmode.py corretto (PRIORITÀ ALTA)

**Obiettivo**: Correggere lo script `assemble_dualmode.py` per evitare che il bug
si ripresenti nelle future generazioni.

**Modifica allo script**: Dopo aver estratto il contenuto vanilla, prima di incapsularlo
nel container wrapper, aggiungere una fase di strip che rimuove:
- La prima occorrenza di `name = "..."`
- La prima occorrenza di `widgetid = "..."`
- Le proprietà di livello window: `layer`, `movable`, `attachto`
- `parentanchor` SOLO se è sulla riga immediatamente successiva al `name`

**Nota**: Questa modifica allo script è per prevenzione futura. I file esistenti
devono essere corretti manualmente o rigenerati dopo il fix dello script.

### Fase 4 — Fix Type Mancanti nei File Vanilla Type-Separated (PRIORITÀ MEDIA)

**Obiettivo**: Risolvere i 484 errori "not a valid widget/type/property".

**Strategia**: Ci sono due approcci possibili:

**Approccio A — Includere le definizioni type nei file type-separated** (RACCOMANDATO):
Per ogni file `vanilla/X_patch_vanilla.gui`, identificare i type usati ma non definiti,
e copiare le loro definizioni dai file vanilla originali nel blocco `types` del file.

Vantaggi: i file sono auto-contenuti.
Svantaggi: aumento dimensione file, manutenzione più complessa.

**Approccio B — Creare file di type condivisi nella cartella vanilla/**:
Creare un file `vanilla/shared_vanilla_types.gui` con tutte le definizioni type mancanti.

Vantaggi: singolo punto di manutenzione.
Svantaggi: rischio collisione nomi con OCR upstream.

**Approccio C — Convertire a inline i file che hanno troppe dipendenze type**:
Per i file con molte dipendenze type (come `culture`, `faith`, `dynasty_house`,
`military`), convertire da type-separated a inline elimina il problema perché
i type sono definiti nel file wrapper (che è l'override del file vanilla originale).

**Raccomandazione**: Approccio C per i file con > 10 type mancanti,
Approccio A per i file con pochi type mancanti (1-3).

**Dettaglio type mancanti per file**:

| File | Type mancanti | Approccio raccomandato |
|------|--------------|----------------------|
| `dynasty_house_patch_vanilla.gui` | ~30 (legacy_*, unity_*) | C (inline) |
| `culture_patch_vanilla.gui` | ~15 (pillar_*, innovation_*) | C (inline) |
| `faith_patch_vanilla.gui` | ~12 (doctrine_*, tenet_*) | C (inline) |
| `military_patch_vanilla.gui` | ~40 (soldiers_*, quality_*) | C (inline) |
| `county_view_patch_vanilla.gui` | ~5 (building_item) | A (import type) |
| `combat_patch_vanilla.gui` | ~15 (soldier_loss, maa_*) | C (inline) |
| `character_lifestyle_patch_vanilla.gui` | ~12 (progressbar_*, icon_*) | C (inline) |
| `court_patch_vanilla.gui` | ~2 (prison_interactions_hbox) | A (import type) |
| `army_patch_vanilla.gui` | ~1 (soldiers_and_quality_big) | A (import type) |

### Fase 5 — Fix Binding Invalidi in interaction_blackmail.gui (PRIORITÀ MEDIA)

**Obiettivo**: Correggere i binding non validi introdotti nella patch.

**Modifica**:
- Riga 87: `button_standard_text` → `button_standard` (type corretto vanilla)
- Riga 92: `Character.GetTooltip` → rimuovere o sostituire con tooltip valido
- Riga 311: `OpenCharacterInteractionMenu(Character.GetID)` → rimuovere
  (questa funzione non esiste in CK3 1.17.1; il file OCR upstream non la usa)
- Riga 312: `Character.GetTooltip` → rimuovere o sostituire
- Riga 449: sound effect inesistente → rimuovere o sostituire con sound valido

**Alternativa**: Rigenerare il file dall'OCR upstream + vanilla con `assemble_dualmode.py`
dopo aver corretto lo script.

### Fase 6 — Fix hud.gui (PRIORITÀ BASSA)

**Obiettivo**: Risolvere l'errore a riga 6414.

**Nota**: `GetTaxSlotsWithoutTaxCollectorCount` è una funzione del DLC Roads to Power
(EP3) che potrebbe richiedere una versione specifica. L'errore genera un fallimento di
parsing del widget ma non è critico per l'avvio. Da verificare se il binding è presente
nel file hud.gui dell'OCR upstream. Se sì, è un problema upstream, non della patch.

### Fase 7 — Verifica File Anomali (PRIORITÀ BASSA)

**File da verificare**:
- `vanilla/window_military.gui` — naming non conforme (dovrebbe essere `military_patch_vanilla.gui`,
  che peraltro esiste già). Possibile doppione. Verificare e rimuovere se duplicato.
- `window_dynasty_legacy.gui` — file OCR-only senza container vanilla. Non causa crash
  ma impedisce la finestra legacy in modalità vanilla. Valutare se aggiungere dual-mode.
- `frontend_main.gui` — copia dell'OCR upstream. Non ha errori strutturali ma è un
  override del menù principale. Verificare compatibilità con le mod abilitate.

---

## 5. Ordine di Implementazione

### Primo Intervento (COMPLETATO — Fasi 1–4)

| Priorità | Fase | Stato | Impatto |
|----------|------|-------|---------|
| 1 | Fase 1 — Fix duplicate name (inline) | ✅ Completata | Eliminati 8 errori critici |
| 2 | Fase 2 — Fix @txt_width | ✅ Completata | Eliminati 5 errori critici |
| 3 | Fase 3 — Fix blackmail bindings | ✅ Completata | Eliminati ~5 errori |
| 4 | Fase 4 — Fix duplicate name (type-sep) | ✅ Completata (workspace) | NON deployata! |

### Secondo Intervento (DA FARE — Fasi 5–8)

| Priorità | Fase | Stima impatto | Prerequisiti |
|----------|------|--------------|-------------|
| 1 | Fase 5 — Sync deploy | Deploy Fase 4 al gioco | Nessuno |
| 2 | Fase 6 — Fix movable/layer | Elimina 4 errori strutturali | Nessuno |
| 3 | **Fase 7 — Ripristino types OCR** | **Elimina ~661 errori + probabile fix stack overflow** | **Fase 5** |
| 4 | Fase 8 — Test nuova partita | Verifica | Fasi 5-7 |

> **NOTA CRITICA**: La Fase 7 è la fix più importante del secondo intervento.
> I 95 types OCR mancanti sono la causa probabile del crash stack overflow e della
> quasi totalità dei 661 errori "not valid widget/type".

---

## 6. Test di Verifica Post-Correzione

### Dopo Primo Intervento (Fasi 1–4) — ESEGUITO
1. ✅ CK3 raggiunge il menù principale
2. ✅ Errori duplicate name inline eliminati
3. ✅ @txt_width disponibile
4. ❌ Nuova partita crasha (stack overflow) → necessario Secondo Intervento

### Dopo Secondo Intervento (Fasi 5–8) — DA ESEGUIRE
1. Avviare CK3 con la mod abilitata → deve raggiungere il menù principale
2. Selezionare "Nuova partita" → deve raggiungere la selezione personaggio SENZA crash
3. Verificare `error.log` → errori "not valid" drasticamente ridotti (target: < 50)
4. Verificare che Shift+F11 alterni correttamente OCR ↔ Vanilla
5. Se il crash persiste: isolamento progressivo (rimuovere un wrapper alla volta, testare)

---

## 7. Rischi e Mitigazioni

| Rischio | Mitigazione |
|---------|------------|
| Rimozione eccessiva di proprietà dal contenuto vanilla | Confrontare sempre con il file vanilla originale prima di rimuovere |
| Conversione inline di file grandi potrebbe creare file > 200KB | Verificare dimensione risultante; se > 200KB, usare approccio A |
| Fix dello script assemble_dualmode.py potrebbe regredire file già corretti | Mai rigenerare file corretti senza verifica esplicita |
| La Fase 4 (type mancanti) potrebbe richiedere molte ore | Procedere un file alla volta; testare dopo ogni file |

---

## 8. Note per il Modder

- Le Fasi 1 e 2 sono le più urgenti e con il massimo impatto.
- La Fase 4 richiede una decisione strategica: convertire molti file da type-separated
  a inline significa file più grandi ma auto-contenuti. L'alternativa (importare type
  nei file separati) mantiene la separazione ma aggiunge complessità.
- Dopo la Fase 1+2, fare un test di avvio immediatamente per verificare se il menù
  principale appare. Se appare, le fasi successive possono essere implementate
  incrementalmente.

---

## 9. Report di Validazione (2026-03-17)

### Esito: PASS CON CORREZIONI

La validazione ha verificato ogni fix proposto contro i file reali.
Di seguito le correzioni integrate nel piano:

### 9.1 Correzioni applicate

| Aspetto | Esito | Correzione |
|---------|-------|------------|
| V1 — Duplicate name (inline) | ✓ CONFERMATO | Aggiunto `widgetid` alla lista proprietà da rimuovere per 3 file (character, council, intrigue) |
| V2 — Duplicate name (type-separated) | ✓ CONFERMATO | Nessuna correzione necessaria |
| V3 — @txt_width mancante | ✓ CONFERMATO | Nessuna correzione necessaria |
| V5 — Anomalia window_military | ✓ FALSO ALLARME | Il file `gui/vanilla/window_military.gui` nel log errori proviene dall'OCR upstream (Agamidae), NON dalla nostra patch. Non è responsabilità nostra correggerlo. Rimosso dalla Fase 7. |

### 9.2 Precisazione sulla Fase 5 (interaction_blackmail.gui)

La validazione iniziale aveva contestato gli errori di binding, dichiarandoli inesistenti.
**Verifica manuale successiva ha CONFERMATO che gli errori sono reali:**

- `button_standard_text` (riga 87): type inesistente — non definito in vanilla, OCR upstream, né altrove
- `Character.GetTooltip` (righe 92, 312): funzione inesistente in CK3 1.17.1
- `OpenCharacterInteractionMenu(Character.GetID)` (riga 311): funzione inesistente in CK3 1.17.1

Questi binding sono stati introdotti dalla patch (il file OCR upstream NON li contiene).
Il file vanilla originale NON li usa. **La Fase 5 resta valida e necessaria.**

### 9.3 Precisazione sulla distribuzione errori "not valid" (484 totali)

La validazione ha rivelato che parte degli errori "not a valid widget/type/property"
proviene dall'OCR upstream (Agamidae), non dalla nostra patch. In particolare:
- `gui/vanilla/window_military.gui` → file dell'OCR upstream
- `gui/vanilla/window_title.gui` → file dell'OCR upstream
- `gui/vanilla/window_the_great_steppe.gui` → file dell'OCR upstream

Questo riduce il numero di errori effettivamente attribuibili alla patch,
ma NON cambia la priorità delle Fasi 1 e 2 che rimangono critiche.

### 9.4 Rischio aggiuntivo identificato: widgetid duplicati

Oltre ai `name` duplicati, 3 file inline hanno anche `widgetid` duplicati:
- `window_character.gui`: `widgetid = "character_window"` sia nel root che nel container vanilla
- `window_council.gui`: `widgetid = "council_window"` sia nel root che nel container vanilla
- `window_intrigue.gui`: `widgetid = "intrigue_window"` sia nel root che nel container vanilla

**Impatto**: `widgetid` duplicati causano conflitto nel routing degli input.
Il motore Jomini potrebbe indirizzare eventi al widget sbagliato.
**Azione**: rimuovere il `widgetid` dal container vanilla (già incluso nella tabella Fase 1).

### 9.5 Verdetto finale validazione

Il piano correttivo è **VALIDATO** con le correzioni sopra integrate.
Le Fasi 1 e 2 sono confermate come le azioni più urgenti e ad alto impatto.
L'implementazione può procedere con approvazione del modder.

---

## 10. Report di Validazione Secondo Intervento (2026-03-17)

### Esito: PASS CON CORREZIONI (tutte integrate)

| # | Correzione | Gravità | Azione |
|---|------------|---------|--------|
| 1 | Fase 6: `allow_outside = yes` è valida per widget → NON rimuoverla da window_character.gui | MEDIA | ✅ Corretto nel piano |
| 2 | Fase 7: `frontend_main.gui` — 0 types mancanti, NON 1 (`left_panel_old` già presente) | BASSA | ✅ Rimosso dalla lista |
| 3 | Fase 7: `window_factions.gui` — iniettare SOLO `vbox_faction_item_ocr` (l'altro è già presente) | ALTA | ✅ Corretto nel piano |
| 4 | Fase 7: `window_inventory.gui` — iniettare SOLO 2 types `_ocr` (7 su 9 già presenti) | ALTA | ✅ Corretto nel piano |
| 5 | Fase 7: Aggiunta regola operativa per iniezione parziale nei file con types esistenti | ALTA | ✅ Aggiunta nel piano |
| 6 | Fase 7: Totale types corretto da 97 a **95** | BASSA | ✅ Corretto nel piano |

### Verifiche effettuate

- ✅ Completezza: tutte e 3 le cause sono coperte dalle Fasi 5-8
- ✅ Ordine fasi: logico e con dipendenze rispettate
- ✅ Posizione blocchi `types`: confermato che possono stare ovunque nel file .gui
- ✅ Collisione namespace: rischio basso per i 9 file senza types nel wrapper
- ✅ `allow_outside`: confermato valido per widget (verificato in console.gui e vanilla)
- ✅ Ipotesi stack overflow: plausibile (42641 frame durante istanziazione GUI in-game)

### 10.1 Verdetto finale secondo intervento

Il piano aggiornato con le Fasi 5-8 è **VALIDATO** con tutte le correzioni integrate.
La Fase 7 è confermata come l'azione più critica del secondo intervento.
L'implementazione può procedere con approvazione del modder.

---

## 11. Diagnostica Terzo Intervento — Blocco Pre-Menu (2026-03-17)

### Contesto

Dopo l'implementazione delle Fasi 5–7 (sync deploy, fix movable/layer, iniezione types):
- Il gioco NON raggiunge il menu principale (blocco dopo "End loading of history")
- Nessun crash dump generato (nessun EXCEPTION)
- Errori "not valid" scesi da **661 a 5** (iniezione types riuscita)

### Timeline caricamento (da log)

| Timestamp | Fase | Esito |
|-----------|------|-------|
| 13:55:01 | Avvio gioco | OK |
| 13:55:05-09 | Parsing GUI | OK — 5 errori (vs 661 prima) |
| 13:55:22 | Caricamento eventi | OK |
| 13:55:24 | Inizializzazione database | OK |
| 13:55:25-26 | Caricamento history | OK → "End loading of history" |
| 13:55:26+ | **Menu principale** | **NON RAGGIUNTO** |

### Errori GUI residui (5 "not valid")

| File | Riga | Tipo mancante | Causa |
|------|------|---------------|-------|
| `court_patch_vanilla.gui` | 359, 565 | `prison_interactions_hbox` | Tipo vanilla perso — vanilla definisce in `types CourtWindow {}` ma OCR upstream e patch non lo includono |
| `window_county_view.gui` | 656-768 | `tooltip_paragraph` | Widget engine-level Clausewitz — NON risolvibile via mod |

### Problemi scoperti

1. **Encoding UTF-8 BOM** (4 file): `window_culture.gui`, `window_military.gui`, `window_faith.gui`, `window_inventory.gui` hanno BOM (EF BB BF). Tutti gli altri file sono senza BOM. Possibile causa del blocco.

2. **Tipo duplicato**: `building_in_vassal_warning_hbox` definito 2 volte in `window_county_view.gui` (righe ~252 e ~617). Warning "already registered".

3. **7 template OCR mancanti** (3 file): definiti nel file upstream FUORI dai blocchi `types {}`, non estratti in Fase 7.
   - `window_army.gui`: `reorg_regiment_tooltips`, `send_army_click_province`, `send_army_click`, `send_army_click_county`
   - `window_dynasty_house.gui`: `agot_show_cadet_house`, `agot_show_house_view`
   - `window_my_realm.gui`: `agot_show_law`

4. **Tipo vanilla `prison_interactions_hbox`**: definito in vanilla `window_court.gui` (riga 753) ma non nell'OCR upstream (che lo elimina completamente). Il nostro `court_patch_vanilla.gui` lo referenzia ma non è definito nella patch.

### Ipotesi causa blocco

**Ipotesi primaria**: l'encoding UTF-8 BOM su 4 file potrebbe causare un errore silenzioso nel parser Clausewitz che blocca la generazione mappa post-history.

**Ipotesi secondaria**: la combinazione di tipo duplicato + template mancanti + tipo vanilla assente potrebbe causare un'eccezione non loggata durante l'istanziazione GUI del menu principale.

### Strategia correttiva → Fasi 9-12

1. **Fase 9**: Rimozione BOM dai 4 file (priorità massima — unica differenza rispetto al test precedente)
2. **Fase 10**: Rimozione tipo duplicato county_view
3. **Fase 11**: Iniezione 7 template mancanti
4. **Fase 12**: Iniezione tipo vanilla prison_interactions_hbox
5. **Fase 13**: Test finale

---

## 12. Diagnostica Quarto Intervento — Blocco Persistente (2026-03-17, ore 14:37)

### Contesto

Le Fasi 9-12 sono state completate, deployate e verificate con hash. Il test successivo
mostra che gli errori GUI sono quasi eliminati, ma il gioco si blocca ancora allo stesso punto.

### Risultati errori (confronto progressivo)

| Metrica | Fasi 1-4 | Fasi 5-7 | Fasi 9-12 | Direzione |
|---------|----------|----------|-----------|-----------|
| not valid (tipo GUI) | 661 | 5 | **0** | risolto |
| Duplicate name | 11 | 0 | **0** | risolto |
| Could not find template | 153 | 143 | **49** | migliorato |
| already registered | 104 | 105 | **105** | invariato (OCR upstream) |
| Raggiunge menu? | SI | NO | **NO** | regressione Fasi 5-7 |

### SCOPERTA CRITICA — Graffa sbilanciata in `army_patch_vanilla.gui`

Verifica strutturale di tutti gli 11 file vanilla/:

| File vanilla/ | `{` aperte | `}` chiuse | Diff | Stato |
|---------------|------------|------------|------|-------|
| army_patch_vanilla.gui | 346 | **347** | **-1** | **SBILANCIATO** |
| (tutti gli altri 10 file) | - | - | 0 | OK |

La `}` in eccesso chiude un blocco prematuramente, lasciando contenuto orfano
che puo causare un loop infinito o deadlock durante l'istanziazione del widget.
Questa e la causa piu probabile del blocco post-history persistente.

### Bug secondario: `space = 3` in `window_my_realm.gui`

Riga 1132: `space = 3` e una proprieta Jomini inesistente. Il parser la interpreta
come riferimento a un template chiamato `'3'`. La proprieta corretta e `spacing = 3`.

### Template mancanti residui (49, giu da 143)

Tutti i 49 template mancanti sono da file OCR upstream che NON sovrascriviamo.
Nessuno e critico — sono warning pre-esistenti nell'OCR di Agamidae.

### Nessun crash dump

L'unico crash dump presente e `ck3_20260317_121429` dal test precedente (STACK_OVERFLOW).
Nessun nuovo dump — il blocco e un hang (loop infinito o deadlock), non un crash.

---

## 13. Strategia Correttiva — Quarto Intervento (Fasi 14-16)

### Analisi causale

La regressione (il gioco non raggiunge piu il menu principale) e stata introdotta nelle
Fasi 5-7. I fix successivi (Fasi 9-12) hanno risolto errori GUI ma NON il blocco,
perche la causa del blocco non era tra quelli affrontati.

La graffa sbilanciata in `army_patch_vanilla.gui` e l'unica anomalia strutturale
trovata tra tutti i 35 file deployati. Un tipo malformato causa un hang silenzioso
durante l'istanziazione post-history.

### Fase 14 — Fix graffa sbilanciata `army_patch_vanilla.gui` (PRIORITA MASSIMA)

Confrontare con il sorgente vanilla per localizzare e rimuovere la `}` in eccesso.

- [x] Localizzare la `}` in eccesso confrontando con vanilla
- [x] Rimuovere la `}` extra (era a riga 1448, ultima riga del file — saldo confermato -1)
- [x] Verificare bilanciamento: Opens 346 = Closes 346, saldo 0 ✓
- [x] Copiare nel deploy path e verificare hash — hash deploy: 637EAEFD ✓
- [x] Verifica no-BOM: primi 3 byte = 35 32 97 (nessun BOM) ✓

### Fase 15 — Fix `space = 3` in `window_my_realm.gui`

Riga 1132: sostituire `space = 3` con `spacing = 3`.

- [x] Correggere `space` con `spacing` a riga 1131 ✓
- [x] Copiare nel deploy path e verificare hash — hash deploy: 37808988 ✓

### Fase 16 — Test e Verifica


### Piano B — Se il blocco persiste dopo Fasi 14-15

Se dopo il fix della graffa il blocco persiste, test di isolamento:
1. Rimuovere TUTTE le 11 vanilla/ type files dal deploy → testare se il menu appare
2. Se SI: il problema e nei vanilla/ types → ricontrollare contenuto di ciascuno
3. Se NO: il problema e nei wrapper → confronto sistematico wrapper vs upstream


---

## 14. Esito Quinto Intervento — Menu Raggiunto, Crash a Nuova Partita (2026-03-17)

### Risultato

Le Fasi 14-15 hanno risolto il blocco pre-menu **(il menu principale è ora raggiungibile)**.

Esito Fase 16 (parziale):
- [x] Menu principale raggiunto ✓ (graffa sbilanciata era la causa del blocco)
- [ ] Nuova partita → CRASH prima della selezione zona geografica
- [x] error.log — 0 errori tipo GUI ✓
- [x] gui_warnings.log — template '3' risolto (spacing fix applicato) ✓

**Crash rilevato**: crash dump generato in `crashes/ck3_20260317_155725/`.

---

## 15. Diagnostica Quinto Intervento — EXCEPTION_STACK_OVERFLOW a Nuova Partita

### Dati crash dump `ck3_20260317_155725`

| Campo | Valore |
|-------|--------|
| Tipo eccezione | EXCEPTION_STACK_OVERFLOW (C00000FD) |
| Indirizzo | **0x00007FF63ABAA7A3** |
| Frame nello stack | ~73 (troncati — stack completamente esaurito) |
| Timestamp crash | 2026-03-17 15:57:28 |
| Crash dump | `crashes/ck3_20260317_155725/` |
| Triggering action | "Scelta libera governante" (Tab dopo selezione era) |
| Ultimo log debug | `Setup powerful vassals among a total of [20673] living character.` (15:57:24) |
| Crash point | 4 secondi dopo l'ultimo log — transizione da history init a GUI in-game |

> ⚠️ **STESSO INDIRIZZO del test 2 (ck3_20260317_121429)**: il crash era già presente dopo
> le Fasi 1-4 (test 2). Non è stato introdotto dalle Fasi 5-16. Era sempre lì, ma nascosto
> dal blocco pre-menu che impediva di arrivarci.

### Analisi comparativa test 2 vs test 6

| Aspetto | Test 2 (post Fasi 1-4) | Test 6 (post Fasi 14-15) | Conclusione |
|---------|----------------------|--------------------------|-------------|
| Indirizzo crash | 0x00007FF63ABAA7A3 | 0x00007FF63ABAA7A3 | Stessa funzione |
| Errori GUI | 661 | 0 | Irrilevanti per questo crash |
| Vanilla/ types | NON deployati | Tutti deployati | Irrilevanti per questo crash |
| File inline | Presenti (da 2026-03-15) | Presenti (idem) | **Comuni a entrambi** |
| OCR upstream | Attivo | Attivo | **Comune a entrambi** |

**Deduzione**: la causa è in un elemento COMUNE a entrambi i test, presente dall'inizio.
I file vanilla/ type-separated NON sono il colpevole (non erano presenti nel test 2).

### Fattori rilevanti identificati

1. **Mod di terze parti "MIV" attivo** (`miv_loyalist_enabled`, `call_allied_vassals_enabled`, etc.)
   - Errori nel log: `Failed to read key reference: miv_loyalist_enabled` (12+ istanze)
   - "MIV" = More Interesting Vassals (o simile) — mod aggiuntivo non compatibile o corrotto
   - Nel contesto "nuova partita", i mod terzi possono interferire con `on_game_start`

2. **OCR upstream — scripted_gui con ricorsione potenziale**
   - `sgui_ocr.txt:328 (special_buildings_list:effect)` → `Empty argument list provided for special_buildings_switch`
   - Se `special_buildings_switch` chiama se stesso via lista argomenti vuota: ricorsione infinita
   - Questo avviene OGNI volta che `special_buildings_list` viene valutato

3. **ARMIES_ocr.txt:1365** → `Unknown effect confirm_title` — effetto sconosciuto in OCR script

4. **hud.gui dimensioni reali**: 7167 righe (non 5959 come stimato dal subagente)
   - Contenuto principalmente OCR upstream (tipi OCR a riga 7138)
   - Brace bilanciate: 1704/1704 ✓
   - Nessun tipo circolare ✓
   - Struttura sana — prima sospettata, ora esclusa come causa strutturale

5. **Nessun tipo circolare nei file patch**: verifica sistematica confermata

### Ipotesi causa stack overflow (in ordine di probabilità)

| Priorità | Ipotesi | Evidenza | Azione richiesta |
|----------|---------|----------|-----------------|
| **H1 (Alta)** | Bug in OCR upstream `sgui_ocr.txt:328` — `special_buildings_switch` con argomenti vuoti causa ricorsione infinita durante `on_game_start` nuova partita | Stessa crash address in test con ZERO errori GUI; errore OCR loggato durante ogni sessione | Test isolamento: avviare con SOLO OCR (no nostra patch) |
| **H2 (Media)** | Mod "MIV" (terze parti) + OCR + nostra patch → catena trigger circolare durante `on_game_start` | 12+ "Failed to read key reference" per chiavi MIV; stack overflow avviene durante setup game state | Test isolamento: avviare senza MOD MIV |
| **H3 (Bassa)** | Uno dei file inline grandi (`hud.gui` 7167 righe, `window_character.gui` 5692 righe) produce istanziazione widget troppo profonda nel contesto specifico "scelta libera" | Files grandi, ma nessun tipo circolare trovato | Test hot-swap: rimpiazzo temporaneo con OCR originale |

---

## 16. Strategia Correttiva — Sesto Intervento (Fasi 17-20)

### Approccio: Isolamento a Cascata

Prima di modificare qualsiasi file, isolare la fonte del crash attraverso
test progressivi. Ogni test elimina o conferma un'ipotesi.

### Fase 17 — Test Isolamento a Cascata (3 Passi)

**Obiettivo**: Determinare quale componente causa il crash — OCR upstream, nostra patch, o MIV.

> ⚠️ I tre passi sono SEQUENZIALI: eseguire il passo successivo SOLO se il precedente non crasha.
> Non saltare passi — ogni passo elimina una variabile diversa.

---

**Passo A — SOLO OCR upstream (nessuna nostra patch, nessun MIV)**:
1. Disabilitare la mod `OCR Support Compatibility Patch` (nostra)
2. Disabilitare TUTTI i mod di terze parti (MIV e analoghi)
3. Lasciare attivo SOLO `OCR Support` (Agamidae upstream)
4. Avviare CK3 → Nuova partita → Scelta libera governante (Tab)
5. Riportare esito

| Esito Passo A | Conclusione | Azione |
|---------------|-------------|--------|
| **CRASH** | Bug in OCR upstream — non dipende da noi | **STOP → Fase 18A** |
| **NO CRASH** | OCR da solo funziona → proseguire con Passo B | Continuare |

---

**Passo B — OCR upstream + NOSTRA PATCH (senza MIV)**:
1. Mantenere MIV disabilitato
2. Riabilitare `OCR Support Compatibility Patch` (nostra)
3. Stesso test: Nuova partita → Scelta libera governante (Tab)
4. Riportare esito

| Esito Passo B | Conclusione | Azione |
|---------------|-------------|--------|
| **CRASH** | La nostra patch introduce il crash | **STOP → Fase 18B** |
| **NO CRASH** | OCR + nostra patch funzionano → proseguire con Passo C | Continuare |

---

**Passo C — Tutto attivo (OCR + nostra patch + MIV)**:
1. Riabilitare MIV e gli altri mod terze parti
2. Stesso test: Nuova partita → Scelta libera governante (Tab)
3. Riportare esito

| Esito Passo C | Conclusione | Azione |
|---------------|-------------|--------|
| **CRASH** | MIV entra in conflitto con OCR/nostra patch | **Fase 18C: rimuovere MIV dal load order** |
| **NO CRASH** | Tutto funziona (insolito — possibile bug intermittente) | Documentare e monitorare |

- [ ] Utente esegue Passo A → riporta esito
- [ ] Utente esegue Passo B se A non crasha → riporta esito
- [ ] Utente esegue Passo C se B non crasha → riporta esito

---

### Fase 18A — (SE CRASH = OCR UPSTREAM) Documentazione Limitazione Nota

Se il crash esiste in OCR upstream senza la nostra patch:

- [ ] Aggiornare `gui-conversion-progress.instructions.md` con nota "crash nuova partita = OCR upstream bug"
- [ ] Verificare se esiste fix nella community OCR (Agamidae repository issues)
- [ ] La nostra patch NON può risolvere questo crash; la funzionalità "scelta libera governante"
  è limitata finché OCR upstream non aggiorna `sgui_ocr.txt:328`

---

### Fase 18B — (SE CRASH = NOSTRA PATCH) Isolamento File Causa

Se OCR upstream da solo NON crasha, il crash è nella nostra patch.

**Azione**: test hot-swap sistematico. Rimpiazzare temporaneamente nel deploy i file
sospetti con le versioni originali OCR upstream, uno alla volta, testando dopo ciascuno.

**Lista file sospetti (in ordine di priorità)**:

| Priorità | File patch | Dimensione | Sospetto |
|----------|-----------|-----------|----------|
| 1 | `hud.gui` | 7167 righe | Più grande inline; istanziato al boot gioco |
| 2 | `window_character.gui` | 5692 righe | 2° grande inline; possibilmente pre-caricato |
| 3 | `window_army.gui` | ~6100 righe wrapper | Wrapper grandi con vanilla types complessi |
| 4 | `window_intrigue.gui` | ~3700 righe | Inline con schema complesso |
| 5 | Altri inline | < 3000 righe | Meno probabili |

**Procedura per ciascun file sospetto**:
1. Nel deploy path, rinominare `FILE.gui` → `FILE.gui.bak`
2. Copiare `OCR-upstream/FILE.gui` nel deploy path
3. Avviare CK3 → Nuova partita → Scelta libera → testare
4. Se NO CRASH: il file originale era la causa → applicare Fase 19
5. Se CRASH: ripristinare `.bak` → testare il file successivo

- [ ] Test hot-swap `hud.gui` (primo candidato)
- [ ] Test hot-swap `window_character.gui` (secondo candidato)
- [ ] Test hot-swap altri file se necessario
- [ ] File causa identificato: _______________

---

### Fase 18C — (SE CRASH = MIV + NOSTRA PATCH) Conflitto Mod Terze Parti

Se il crash avviene SOLO quando MIV è attivo insieme alla nostra patch (Passo B OK, Passo C CRASH):

- [ ] Disabilitare MIV definitivamente dal load order
- [ ] Documentare in `gui-conversion-progress.instructions.md`: "MIV mod causa conflitto di stack overflow con OCR + nostra patch"
- [ ] La nostra patch è corretta — il problema è MIV; non modificare i nostri file
- [ ] Nota all'utente: MIV non è compatibile con OCR Support in questa configurazione

---

### Fase 19 — Correzione File Isolato

Dipende dal file identificato in Fase 18B.

**Se causa = `hud.gui`**:
- Opzione A: Convertire a type-separated (v1.1) — spostare contenuto vanilla in
  `gui/vanilla/hud_patch_vanilla.gui`. Alto rischio operativo, richiede CP1 dal modder.
- Opzione B: Verificare se il dual-mode è implementato correttamente e se le sezioni
  OCR/vanilla producono ricorsione attraverso qualche widget specifico. Individuare e
  correggere il widget specifico.
- Opzione C: Rimuovere temporaneamente il contenuto vanilla da `hud.gui` lasciando
  solo la sezione OCR (regressione funzionale temporanea per diagnosi).

**Se causa = `window_character.gui`**:
- Stessa logica ma file già identificato strutturalmente sano (brace OK, nessun tipo circolare)
- Riesaminare le sezioni specifiche che vengono istanziate all'avvio in-game

**Se causa = altro file**:
- Analisi specifica sul file identificato

- [ ] Strategia scelta: _______________ (da decidere dopo Fase 18B)
- [ ] Correzione implementata
- [ ] Deploy e hash verification

---

### Fase 20 — Test Finale Sesto Intervento

- [ ] Test: avvio CK3, menu principale raggiunto ✓ (già confermato)
- [ ] Test: nuova partita → scelta libera → schermata zona geografica RAGGIUNTA
- [ ] Test: selezione zona → selezione personaggio → avvio in-game SENZA crash
- [ ] Verificare error.log — 0 errori GUI
- [ ] Verificare Shift+F11 alterna OCR ↔ Vanilla correttamente in-game

---

## 17. Note Storiche — Cose da NON Ripetere

_(Sezione permanente: aggiornare ad ogni intervento con lezioni negative)_

| Data | Cosa NON fare | Perché |
|------|--------------|--------|
| 2026-03-15 | Creare file vanilla/ type-sep senza deployarli | Il gap workspace↔deploy ha causato test falso negativo |
| 2026-03-15 | Usare `Set-Content -Encoding UTF8` in PowerShell | Aggiunge BOM silenziosamente — usare sempre `New-Object UTF8Encoding($false)` |
| 2026-03-16 | Non verificare bilanciamento brace dopo ogni modifica file | Graffa extra in army_patch_vanilla.gui ha causato hang per 2+ interventi |
| 2026-03-17 | `space = 3` invece di `spacing = 3` in widget flowcontainer | Jomini interpreta `space` come keyword template → warning "template '3' not found" |
| 2026-03-17 | Assumere che tutti i mod attivi siano compatibili | MIV (mod terze parti) può causare crash di stack overflow che mascherano bug OCR/patch |
| 2026-03-17 | Stimare dimensioni file senza verifica diretta | Il subagente ha stimato hud.gui a 5959 righe, in realtà sono 7167 (errore di misura) |

---

## 18. Diagnostica Sesto Intervento — Regressione a Blocco in Caricamento (2026-03-17 ore 18:19)

### Esito del test successivo al fix `expanded_view`

Dopo l'aggiunta del template `expanded_view` in `window_character.gui`, il comportamento
non è migliorato: il gioco va in **blocco durante il caricamento** e non genera un nuovo crash dump.

**Dato critico**: nella cartella `crashes/` NON esiste alcun dump nuovo oltre `ck3_20260317_171513`.
Quindi il problema corrente è un **hang/stall**, non un crash con eccezione catturata.

### Verifica deploy attivo

Il fix `expanded_view` è presente anche nel deploy attivo:
- `mod/ocr_support_compatibility_pach/gui/window_character.gui`
- il template è definito correttamente nel file deployato

**Conclusione**: la regressione attuale NON è spiegata dall'assenza del template `expanded_view`.
Quel fix era necessario, ma non è la causa del blocco corrente.

### Stato log live (run 18:19-18:20)

| Fonte | Esito | Conclusione |
|------|-------|-------------|
| `logs/error.log` | errori quasi identici al run precedente che arrivava oltre il menu | **non discriminante** |
| `logs/gui_warnings.log` | warning OCR preload e duplicate registrations sostanzialmente invariati | **rumore storico, non nuova regressione** |
| `logs/database_conflicts.log` | vuoto | nessun conflitto database rilevato |
| `logs/debug.log` | si ferma a `history.cpp:1380 End loading of history` | blocco **tra fine history e fase post-history** |
| `logs/game.log` | si ferma al caricamento eventi | conferma che il bootstrap non completa la transizione successiva |

### Punto esatto del blocco

L'ultimo marker utile in `debug.log` è:

`[18:20:07][D][history.cpp:1380]: End loading of history`

Mancano completamente i marker che nei run precedenti comparivano dopo:
- `Completed running through history`
- `Start running through post-history`
- `Completed running through post-history`
- `Setup powerful vassals ...`

**Deduzione**: il blocco corrente avviene DOPO il caricamento della history ma PRIMA
dell'inizializzazione post-history / transizione runtime successiva.

### Analisi incrociata con i run precedenti

| Run | Esito | Firma | Fase raggiunta |
|-----|------|-------|----------------|
| `121429` | crash | stack overflow `0x00007FF63ABAA7A3` | oltre bootstrap iniziale |
| `155725` | crash | stack overflow `0x00007FF63ABAA7A3` | fino a `Setup powerful vassals` |
| `171513` | crash | stack overflow `0x00007FF63ABAA7A3` | fino a `Setup powerful vassals` |
| run 18:19 | **hang** | nessun dump | si ferma a `End loading of history` |

**Conclusione forte**: siamo davanti a una regressione di fase, non necessariamente di causa.
Il problema attuale si manifesta PRIMA del punto in cui i crash precedenti producevano stack overflow.

### Fattori ancora aperti dopo analisi incrociata

1. **OCR upstream scripted_guis ancora difettosi**
  - `sgui_ocr.txt:328` → `special_buildings_switch = { }`
  - `ARMIES_ocr.txt:1365` → `confirm_title` sconosciuto
  - Poiché la patch NON override `common/scripted_guis/`, questi errori provengono dall'OCR originale

2. **Persistenza dati contaminata da mod disattive**
  - `pdx_persistent_reader` continua a leggere chiavi MIV/RICE/VIET anche con mod disattive
  - Questo rende il profilo utente corrente non affidabile per test di isolamento puro

3. **Warning preload OCR su template mancanti**
  - `gui/preload/00_types_OCR.gui` usa `Background_Area`, `Background_Area_Solid`, `Background_Area_Dark`, `Scrollbox_Margins`
  - I warning sono già presenti nei run precedenti, quindi NON bastano da soli a spiegare la regressione

4. **Errori GUI patch ancora presenti ma non nuovi**
  - `hud.gui` → `TAX_SLOT_OVERVIEW_WINDOW_TAX_SLOTS_WARNING`
  - `window_county_view.gui` → `tooltip_paragraph` invalido
  - Sono da correggere, ma il loro pattern era già presente anche in run che andavano più avanti

### Ipotesi aggiornate (regressione attuale)

| Priorità | Ipotesi | Evidenza | Stato |
|----------|---------|----------|-------|
| **H1 (Alta)** | Profilo utente / dati persistenti contaminati causano hang tra history e post-history | `pdx_persistent_reader` continua a leggere chiavi di mod disattive; nessun dump nuovo; blocco anticipato | nuova priorità alta |
| **H2 (Alta)** | Bug OCR upstream nei `scripted_guis` si manifesta come hang invece che crash, a seconda dello stato runtime | errori `special_buildings_switch` e `confirm_title` invariati, patch non li override | confermata come causa esterna aperta |
| **H3 (Media)** | La patch contiene ancora uno o più file che degradano la transizione post-history, ma non `expanded_view` | fix deployato presente; error signature invariata; altri file patch ancora rumorosi | richiede isolamento file |
| **H4 (Bassa)** | Warning preload OCR sono la causa primaria del blocco | warning preesistenti e non discriminanti | improbabile |

---

## 19. Strategia Correttiva — Settimo Intervento (Fasi 21-24)

### Principio guida aggiornato

Con il profilo attuale i test NON sono più puliti: i log mostrano residui persistenti di mod disattive.
Qualsiasi ulteriore modifica ai `.gui` senza isolamento del profilo rischia di produrre altri falsi positivi.

### Fase 21 — Test Clean-Room Obbligatorio (senza modifiche codice)

**Obiettivo**: escludere definitivamente la contaminazione del profilo utente corrente.

**Procedura manuale proposta al modder**:
1. Creare un profilo pulito di test, usando UNO dei due metodi:
  - Metodo A: rinominare temporaneamente la cartella utente di CK3 in Documenti
  - Metodo B: avviare CK3 con un `--user-data-path` dedicato e vuoto
2. Nel profilo pulito, attivare SOLO:
  - `OCR Support`
  - `ocr support compatibility pach`
  - eventuale traduzione italiana se indispensabile
3. Ripetere il test che ora produce il blocco
4. Conservare i nuovi log del profilo pulito

**Interpretazione**:

| Esito clean-room | Conclusione | Azione |
|------------------|-------------|--------|
| Il blocco sparisce | problema nel profilo utente corrente | Fase 22A |
| Il blocco resta | problema reale in OCR/patch | Fase 22B |

### Fase 22A — Se il blocco sparisce in clean-room

- [ ] Classificare i `pdx_persistent_reader` errors come contaminazione da dati persistenti
- [ ] Smettere di usare il profilo corrente per diagnosi dei crash GUI
- [ ] Riprendere i test solo su profilo pulito

### Fase 22B — Se il blocco resta anche in clean-room

Procedere a isolamento file mirato, ma SOLO su file che possono influire nella fase post-history.

Ordine aggiornato di sospetto:
1. `hud.gui` — caricato sempre, contiene errori `TAX_SLOT_*`
2. `window_county_view.gui` — contiene proprietà invalide (`tooltip_paragraph`)
3. `window_character.gui` — mantenere in osservazione, ma `expanded_view` è già corretto
4. `window_activity.gui` / `window_intrigue.gui` — file inline grandi, da testare dopo

### Fase 23 — Isolamento File Patch (solo se clean-room conferma problema reale)

**Metodo**: hot-swap nel deploy con la corrispondente versione OCR upstream, uno alla volta.

Per ciascun file sospetto:
1. Sostituire temporaneamente il file della patch nel deploy con la versione OCR upstream
2. Ripetere il test
3. Se il blocco sparisce: file identificato
4. Se il blocco resta: ripristinare e passare al file successivo

### Fase 24 — Regole di intervento prima di nuove modifiche codice

- [ ] NON modificare altri `.gui` finché non esiste un test clean-room riuscito o fallito con log puliti
- [ ] NON attribuire la regressione al fix `expanded_view` senza evidenza, perché il fix è presente nel deploy attivo
- [ ] Trattare `special_buildings_switch` e `confirm_title` come issue OCR upstream aperte, non come bug della patch
- [ ] Usare i log live come gate: il prossimo obiettivo minimo è superare `End loading of history` e arrivare almeno a `Completed running through post-history`
