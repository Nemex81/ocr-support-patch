# ocr-support-patch
patch di compatibilità pe rocr support, mod dedicata a crusader king 3

---
## Obiettivo
Implementare `OCR-Support/gui/window_culture.gui` in modalità duale (OCR vs normo-vedente), mantenendo checksum identico e compatibilità multiplayer. Modalità OCR: codice originale OCR Support **immutato**. Modalità vedente: UI grafica completa con 5 tab come da specifica.

## Repository e riferimenti
- Repo target: `Nemex81/test-CK3-OCR`
- Percorso file: `OCR-Support/gui/window_culture.gui`
- Riferimenti vanilla/stile: cartella `gui/placeholders` del repo (es. `window_dynasty_house_vanilla_originale.md`) per pattern sidebar e animazioni.
- Pattern dual-mode già in uso: vedi `window_county_view.gui` (commit 4A/4) per struttura `GetVariableSystem.Exists('ocr')`.

## Vincoli e salvaguardie OCR
1) **Baseline OCR originale**: usa il `window_culture.gui` originale dell’OCR Support (Agamidae/CK3-OCR) come sorgente per il blocco OCR.  
2) **Blocco OCR intatto**: nel ramo `window_ocr { visible = "[Not(GetVariableSystem.Exists('ocr'))]" }` non modificare logica, widgetid, name, types. Solo wrapping e indentazione ammessi.  
3) **Datacontext e state invariati**: mantieni `datacontext` (GetVariableSystem, CultureWindow.GetCulture, Culture.GetReformation) e gli state/animazioni originali.  
4) **Types/widgetid**: non rinominare nulla del blocco OCR; non aggiungere asset al blocco OCR.  
5) **Scripted GUI/values**: non alterare `common/scripted_guis` o `common/script_values` esistenti (culture_list, culture_counties_list, culture_characters_list, etc.).  
6) **Hotkey/shortcut**: conserva gli shortcut originali (tab 1–5 / speed 1–5).  
7) **Diff check finale**: confronta il blocco OCR risultante con l’originale per verificare che sia identico (eccetto wrapper/indentazione).

## Architettura finestra (wrapper dual-mode)
- `using = Window_Size_Sidebar`, `using = Window_Background_Sidebar`, `layer = middle`.
- Animazione slide laterale (position 0 → -90) su `_show/_hide`.
- Datacontext (ordine): `[GetVariableSystem]`, `[CultureWindow.GetCulture]`, `[Culture.GetReformation]`.
- State: `_show`, `_hide`.

### Struttura
```gui
window {
  ...
  window_ocr {
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"
    // codice OCR originale, invariato
  }
  marginwidget {
    visible = "[GetVariableSystem.Exists('ocr')]"
    using = Window_Margins_Sidebar
    // UI grafica (5 tab)
  }
}
```

## Contenuti modalità vedente (5 tab)

### Tab 1: Overview (replica vanilla + header)
- Header: `header_pattern` con `button_close`, `button_back`, `watch_window_button`.
- Widget acceptance top-right (~margin_left 450) con % + delta annuale.
- Ethos monumentale: `container_pillar_item` {400 100}, `highlight_icon` + `Mask_Rough_Edges`, gradient/modify_texture, button_round per reformation mode.
- Cultural Pillars grid 2 colonne:
  - Col1: Heritage + Martial Custom (gating DLC).
  - Col2: Language + Aesthetics.
  - Icone: `icon_doctrine` 44x44 (Heritage/Martial), `icon_culture_pillar` (Language/Aesthetics); icone diverge se culture diverse; bottone “Adopt Court Language” se Royal Court DLC.
- Traditions grid: `fixedgridbox` wrap=2; item `widget_tradition_icon` size {276 138} con 5 layer (bg, pattern L/R, support, stroke 90%, items); nome sotto; counter “x/9” in alto dx.
- Bottom buttons: Hybridize, Add Tradition, Reform, Diverge con `icon_cross` se disabled.
- Culture Head section: `portrait_shoulders`; Fascination widget `icon_innovation` 90x60; learning level icon.

### Tab 2: Innovations (replica vanilla + effetti)
- Era tabs orizzontali: `vbox_era_tab` {135 128}, `highlight_icon` (GetIllustration), `mask_culture_era_tab.dds` alphamultiply, overlay scuro per non attive, frayed edges, anim size expand on select.
- Era progress bar se non attiva: `progressbar_standard` + testo “Ready in X years”.
- Innovation grid: `dynamicgridbox` wrap=2, gruppi per categoria.
- Effetti animati su `icon_innovation` (90x60):
  - Shimmer (effect_shimmer.dds, colordodge, translate_uv anim) quando `IsFascination`.
  - Glow oro per fascination (`innovation_glow.dds`, tint oro pulsante).
  - Glow blu per exposure (`HasExposureMarker`).
  - Overlay scuro per non attive; progressbar 90x15 per in-progress.
- Click selezione fascination solo se culture head; altrimenti statico. Tooltip “INNOVATION_CLICK_TO_SELECT_FASCINATION”.

### Tab 3: All Cultures (enhanced, cards)
- Header con stats: background gradient; icona `icon_culture` + “[GetDataModelSize] cultures”; filtri heritage (button_tab).
- Culture cards grid (2 colonne): CoA medio, nome, heritage, bar di acceptance con gradient dinamico (verde/giallo/rosso), icona relazione (parent/child/hybrid). Onclick apre cultura. Sorting: Name, Acceptance, Counties, Rulers con indicatori direzione.

### Tab 4: Counties (enhanced, cards)
- Header con mappa preview (se fattibile) o illustrazione.
- Stats bar: total counties, foreign-held, converting (icone + tint dinamico).
- County cards (2 colonne): CoA grande, nome titolo, portrait holder, warning se foreign culture, progress bar conversion se attiva, dev indicator, onclick GoToLocation.
- Filtri toggle: foreign-held only, converting only, tipo provincia.

### Tab 5: Rulers (enhanced, cards)
- Stats summary: #rulers, realm size, avg prestige (icone).
- Ruler cards (1 colonna ampia): portrait body, rank icon, nome+età, primary title CoA, realm size icon, skill bar (5), top 3 traits, prestige/piety. Onclick `DefaultOnCharacterClick`.
- Sorting: Tier, Realm Size, Age, Prestige; filtri Tier/Gender/Dynasty.

## Elementi tecnici trasversali
- Tab switch: fade in/out.
- Tooltip ricchi: `culture_pillar_tooltip`, `culture_tradition_tooltip`, `culture_innovation_tooltip`, `culture_era_tooltip`.
- Datamodel riuso: `culture_list`, `culture_counties_list`, `culture_characters_list`.
- Hotkeys: mantieni shortcut Speed 1–5 sui 5 tab.
- Reformation mode: overlay/disabilitazioni coerenti (icone cross/tint).
- DLC gating: Martial Custom, Hybrid/Diverge/Reform, Court Language solo se DLC; fallback hidden.
- Asset fallback: se mancano `innovation_glow.dds`, `mask_culture_era_tab.dds`, `effect_shimmer.dds`, imposta visible/alpha 0 per evitare errori.
- Performance: effetti shimmer/glow solo su fascination/exposure attivi.

## Checklist finale per l’agente
- [ ] Blocchi OCR: copiati pari all’originale, solo wrappati nel dual-mode; nessun rename widgetid/name/type.
- [ ] Datacontext/state invariati; layer/sidebar/anim ok.
- [ ] 5 tab grafici implementati secondo specifica sopra.
- [ ] Hotkeys 1–5 preservate.
- [ ] Gating DLC corretto; fascination cliccabile solo per culture head.
- [ ] Asset mancanti gestiti con fallback safe (no crash).
- [ ] Nessuna modifica a scripted_guis/script_values.
- [ ] Diff OCR vs originale: identico a parte wrapper/indentazione.
- [ ] Build GUI senza errori; checksum inalterato.

## File da toccare
- `OCR-Support/gui/window_culture.gui` (nuovo/aggiornato con dual-mode).
- Consultazione stile: `gui/placeholders/window_culture_vanilla_originale.md e gui/placeholders/window_culture_ocr_support_originale.md` (pattern sidebar, animazioni).
---