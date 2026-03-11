# Piano di Implementazione — Shortcut Icone Bottom-Left (OCR)

**Data:** 2026-03-11
**Versione target:** CK3 1.17.1 + OCR Support Patch
**Obiettivo:** Assegnare scorciatoie tastiera `alt+1` … `alt+5` alle 5 icone
laterali bottom-left, escludendo il ritratto grande del personaggio
(già gestito da `F1` / `character_window` nel vanilla).

---

## Contesto e Motivazione

Le 5 icone laterali in basso a sinistra (inventario, stile di vita, fede,
cultura, casata) sono attualmente **accessibili solo con il mouse**.
Per i giocatori non vedenti che usano OCR Support, servono scorciatoie
da tastiera dedicate. Il modificatore scelto è `alt` perché è
**completamente libero** nel vanilla CK3 1.17.1 e in OCR Support:
nessun binding attuale usa `alt+`. Le combinazioni `ctrl+` e `shift+`
sono invece già affollate da azioni di mappa, velocità e screenshot.

---

## File Coinvolti

| File | Operazione |
|------|-----------|
| `ocr_support_compatibility_pach/gui/hud.gui` | Aggiunta bottoni invisibili `size { 0 0 }` con `shortcut` nei 5 widget |
| `ocr_support_compatibility_pach/shortcuts/ocr_support.shortcuts` | Dichiarazione delle 5 nuove azioni shortcut (da verificare se esiste) |

> **Nota:** Se `ocr_support.shortcuts` non esiste nella mod, i binding
> vanno inseriti direttamente come stringa letterale (`shortcut = "alt+1"`)
> senza dichiarazione preventiva — Jomini accetta entrambe le forme.

---

## Mapping Shortcut Definito

| Tasto | Icona | Funzione | Nome bottone attuale |
|-------|-------|----------|----------------------|
| `alt+1` | Inventario | Apre inventario artefatti | `open_inventory_button` |
| `alt+2` | Stile di vita | `OpenGameViewData('lifestyle', ...)` | `lifestyle_button` |
| `alt+3` | Fede | `OpenGameViewData('faith', ...)` | `faith_button_manual` |
| `alt+4` | Cultura | `OpenGameViewData('culture_window', ...)` | `culture_button_manual` |
| `alt+5` | Casata | `DefaultOnHouseCoatOfArmsClick(...)` | `house_button_manual` |

L'ordine numerico coincide con l'ordine visivo dall'alto verso il basso
nella colonna di icone (posizioni Y crescenti nel codice attuale).

---

## Strategia di Implementazione in hud.gui

Per ogni icona si aggiunge un `button` invisibile **dentro il widget
contenitore** esistente, in coda agli elementi già presenti.
Il pattern è identico per tutte e 5:

```
button = {
    size = { 0 0 }
    shortcut = "alt+N"
    onclick = [ ... stessa onclick del bottone visibile ... ]
}
```

### Dettaglio per ciascuna icona

---

### 1. Inventario — `alt+1`

**Widget contenitore:** primo `widget` dentro `bottom_left_icons_container_final`,
`position = { 5 5 }`.

```
# Aggiungere in coda al widget position { 5 5 }
button = {
    size = { 0 0 }
    shortcut = "alt+1"
    onclick = "[ToggleGameView('inventory')]"
    # Nota: verificare l'onclick esatta di button_open_inventory
    # nel template vanilla — potrebbe essere OpenGameViewData o ToggleGameView
}
```

> **Attenzione:** `button_open_inventory` è un template (type), non un
> button_normal. La `onclick` esatta va verificata nel file
> `CK3-ORIGINAL-VERSION/gui/buttons.gui` prima di scrivere il codice.
> Fase 0 del lavoro.

---

### 2. Stile di vita — `alt+2`

**Widget contenitore:** secondo `widget` dentro `bottom_left_icons_container_final`,
`position = { 5 50 }`.

```
# Aggiungere in coda al widget position { 5 50 }
button = {
    size = { 0 0 }
    shortcut = "alt+2"
    visible = "[GetPlayer.IsAdult]"
    onclick = "[OpenGameViewData( 'lifestyle', GetPlayer.GetID )]"
}
```

> `visible = "[GetPlayer.IsAdult]"` è obbligatorio: se il personaggio
> è minorenne non ha lifestyle e il tasto non deve fare nulla.
> Stesso guard del bottone visibile soprastante.

---

### 3. Fede — `alt+3`

**Widget contenitore:** `hud_icon_faith_standalone`,
`position = { 10 -150 }`.

```
# Aggiungere in coda al widget hud_icon_faith_standalone
button = {
    size = { 0 0 }
    shortcut = "alt+3"
    onclick = "[OpenGameViewData( 'faith', GetPlayer.GetFaith.GetID )]"
}
```

---

### 4. Cultura — `alt+4`

**Widget contenitore:** `hud_icon_culture_standalone`,
`position = { 10 -200 }`.

```
# Aggiungere in coda al widget hud_icon_culture_standalone
button = {
    size = { 0 0 }
    shortcut = "alt+4"
    onclick = "[OpenGameViewData( 'culture_window', GetPlayer.GetCulture.GetID )]"
}
```

---

### 5. Casata — `alt+5`

**Widget contenitore:** `hud_icon_house_standalone`,
`position = { 10 -250 }`.

```
# Aggiungere in coda al widget hud_icon_house_standalone
button = {
    size = { 0 0 }
    shortcut = "alt+5"
    onclick = "[DefaultOnHouseCoatOfArmsClick(GetPlayer.GetHouse.GetID)]"
}
```

---

## Fasi di Lavoro (Ordine Esecutivo)

### Fase 0 — Verifica onclick inventario
- Aprire `CK3-ORIGINAL-VERSION/gui/` e cercare la definizione del type
  `button_open_inventory` per ricavare la `onclick` corretta.
- Confermare se usa `ToggleGameView('inventory')` o altra variante.

### Fase 1 — Modifica hud.gui
- Aggiungere i 5 bottoni invisibili nei rispettivi widget.
- Commit descrittivo: `feat: shortcut alt+1..5 per icone bottom-left OCR`.

### Fase 2 — Test in gioco
- Avviare CK3 con la patch attiva.
- Premere `alt+1` … `alt+5` in sequenza e verificare che si apra
  la finestra corretta.
- Verificare che `alt+2` non risponda se il personaggio è minorenne.
- Verificare che nessun binding entri in conflitto con scorciatoie
  di sistema di Windows/Linux (alt+F4, alt+Tab — questi non passano
  mai al gioco, sono intercettati dall'OS, quindi non sono un problema).

### Fase 3 — Documentazione
- Aggiornare `README.md` della patch con la lista delle nuove shortcut.

---

## Rischi e Note

| Rischio | Probabilità | Mitigazione |
|---------|-------------|-------------|
| `onclick` inventario sbagliata | Media | Verificare type in Fase 0 prima di ogni commit |
| `alt+N` in conflitto con DLC futuri | Bassa | Monitorare changelog Paradox; `alt+` è libero in 1.17.1 |
| Bottone visibile e invisibile doppione audio | Nulla | Il bottone `size {0 0}` non ha `clicksound` dichiarato |
| Lifestyle shortcut su personaggio minorenne | Reale | Guard `visible = "[GetPlayer.IsAdult]"` in Fase 1 |

---

## Riferimento Posizioni Attuali in hud.gui

```
bottom_left_icons_container_final
├── widget position { 5   5  }   → inventario    → alt+1
├── widget position { 5  50  }   → lifestyle     → alt+2
├── hud_icon_faith_standalone    → fede          → alt+3  (position { 10 -150 })
├── hud_icon_culture_standalone  → cultura       → alt+4  (position { 10 -200 })
└── hud_icon_house_standalone    → casata        → alt+5  (position { 10 -250 })
```

---

*Piano generato nel contesto dello Space CK3 OCR Support Fix.*
*Prossimo passo: Fase 0 — verifica onclick di button_open_inventory.*
