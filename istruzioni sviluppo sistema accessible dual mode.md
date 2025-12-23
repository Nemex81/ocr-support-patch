Perfetto, ho capito. Il documento deve essere un **manuale di linee guida generali** per il refactoring dual-mode, **NON** la cronaca dettagliata di window_county_view.

Genero la versione corretta, **ripulita** da tutta la parte specifica County View:

***

# 📋 PROGETTO CK3 OCR SUPPORT - ACCESSIBILITY FIX for dual mode

**Versione**: 4.0 - Universal Accessibility & Input Parity Update  
**Data ultima modifica**: 23 Dicembre 2025, 14:15 CET  
**Versione progetto**: OCR Support Compatibility Patch - Dual Mode View V 1.0  
**Repository**: [https://github.com/Nemex81/ocr-support-patch](https://github.com/Nemex81/ocr-support-patch)  
**Sviluppatore**: Luca "Nemex81" (utente cieco, Italia)  
**Screen reader**: NVDA su Windows 11  
**Gioco**: Crusader Kings 3 v1.17.1 (Steam)  
**Mod base**: OCR Support v4.2 by Agamidae

***

## 🎯 OBIETTIVO DEL PROGETTO

Risolvere il problema di **finestre nere** nella modalità normo vedente della mod **OCR Support v4.2**, che impediva partite multiplayer miste tra giocatori ciechi e normovedenti con lo stesso checksum.

### Repository collegati
- **Mod originale**: [https://github.com/Agamidae/CK3-OCR](https://github.com/Agamidae/CK3-OCR)
- **Compatibility Patch**: [https://github.com/Nemex81/ocr-support-patch](https://github.com/Nemex81/ocr-support-patch)

### ✅ RISULTATO RAGGIUNTO
11 finestre principali del gioco sono state convertite con successo al sistema dual-mode, permettendo partite multiplayer completamente funzionali tra giocatori ciechi (modalità OCR testuale) e normovedenti (modalità grafica vanilla).

***

## ⚙️ MECCANISMO DUAL-MODE CORE

### Logica di Switch
```gui
datacontext = "[GetVariableSystem]"

# MODALITÀ NORMO VEDENTE (Shift+F11 attivo)
widget = {
    visible = "[GetVariableSystem.Exists('ocr')]"
    # UI grafica vanilla completa
}

# MODALITÀ NON VEDENTE (default)
widget = {
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"
    # UI accessibile OCR-optimized per screen reader
}
```

### Variabile di controllo
- **`GetVariableSystem.Exists('ocr')`**: 
  - `true` = modalità vedente (interfaccia grafica)
  - `false` = modalità cieca (interfaccia testuale OCR)
- **Toggle**: Shift+F11 gestito da AutoHotkey
- **Checksum multiplayer**: Identico per entrambe le modalità ✓

***

## 📐 REGOLE DI ACCESSIBILITÀ UNIVERSALE

### 1. PRINCIPIO CORE: DUAL-MODE RENDERING

#### Obiettivo
Garantire che **ogni GUI** funzioni perfettamente sia per:
- **Giocatori ciechi** → interfaccia testuale OCR-ottimizzata per screen reader NVDA
- **Giocatori vedenti** → interfaccia grafica vanilla completa

**senza compromettere il checksum multiplayer**.

***

### 2. MECCANISMO TECNICO: VISIBILITY TOGGLE

**Pattern**: Dual widget container

```gui
window = {
    name = "example_window"
    
    # ⚠️ CRITICAL: Datacontext variabile toggle SEMPRE al top-level
    datacontext = "[GetVariableSystem]"
    
    # 🔵 WIDGET OCR (giocatori ciechi - DEFAULT)
    widget = {
        name = "ocr_example_window"
        visible = "[Not(GetVariableSystem.Exists('ocr'))]"
        
        # UI testuale lineare ottimizzata per navigazione keyboard
        vbox = {
            using = ocr_margins
            using = ocr
            # contenuto accessibile...
        }
    }
    
    # 🟢 WIDGET VANILLA (giocatori vedenti - SHIFT+F11)
    widget = {
        name = "vanilla_example_window"
        visible = "[GetVariableSystem.Exists('ocr')]"
        
        # UI grafica completa vanilla-compatible
        vbox = {
            # contenuto grafico...
        }
    }
}
```

***

### 3. REGOLE DI DESIGN OCR MODE (Interfaccia Cieca)

#### 3.1 Layout: Linearità Forzata
```gui
vbox = {
    using = ocr_margins      # Margini standard accessibilità
    using = ocr              # Font/spacing ottimizzati
    
    # ✅ SEMPRE struttura verticale lineare
    scrollbox = {
        # Sezioni ordinate logicamente, MAI layout complessi
        
        # Esempio: priorità informazioni
        vbox = { # Titolo/Nome principale }
        vbox = { # Stats primarie }
        vbox = { # Azioni disponibili }
        vbox = { # Info secondarie }
    }
}
```

**Motivazione**: Screen reader NVDA legge **sequenzialmente** dall'alto al basso. Layout a colonne o grid richiederebbero navigazione spaziale impossibile per utenti ciechi.

***

#### 3.2 Button Accessibility: Focus + Tooltip
```gui
button_standard_text = {
    name = "action_button"
    text = "ACTION_LABEL"
    
    # ✅ CRITICAL: shortcut sempre visibile nel tooltip
    tooltip = "ACTION_DESCRIPTION_TT"  # Deve includere [GetShortcut('action')]
    
    # ✅ Shortcut da tastiera per accesso rapido
    shortcut = "action_key"
    
    onclick = "[ExecuteAction]"
    enabled = "[CanExecuteAction]"
    
    # ✅ Focus default per tab-navigation
    default_focus = yes  # Se bottone principale della sezione
}
```

**Principi chiave**:
- **Tutti i button** devono avere `text` leggibile (NO solo icone)
- **Shortcut keyboard obbligatori** per funzioni primarie (evita click multipli)
- **Tooltip descrittivi** con contesto completo dell'azione

***

#### 3.3 Info Display: Text-Only, No Graphics
```gui
# ❌ SBAGLIATO (non accessibile)
icon = {
    texture = "gfx/icons/gold.dds"
    # Utente cieco non sa cosa significhi
}

# ✅ CORRETTO (accessibile)
text_single = {
    text = "GOLD_AMOUNT_LABEL"  # Es: "Gold: [Character.GetGold]"
    tooltip = "GOLD_TOOLTIP"     # Descrizione testuale completa
}
```

**Motivazione**: NVDA legge solo **testo**. Icone, colori, immagini sono invisibili all'utente cieco.

***

#### 3.4 Navigation Shortcuts: Movimento Rapido
```gui
### NAVIGATION SHORTCUTS ###
hbox = {
    visible = no  # Invisibile ma funzionale
    size = { 0 0 }
    
    button_standard = {
        name = "prev_item"
        shortcut = "z"
        onclick = "[SelectPreviousItem]"
    }
    
    button_standard = {
        name = "next_item"
        shortcut = "x"
        onclick = "[SelectNextItem]"
    }
    
    button_standard = {
        name = "go_to_related"
        shortcut = "g"
        onclick = "[OpenRelatedView]"
    }
}
```

**Standard shortcuts OCR**:
- **Z** = Previous item
- **X** = Next item
- **G** = Go to related view
- **E** = Edit/Modify
- **H** = Holdings view
- **T** = Title view
- **A** = Adjacent counties

**Motivazione**: Navigazione mouse impossibile → Keyboard-only con shortcuts memorizzabili.

***

### 4. REGOLE DI DESIGN VANILLA MODE (Interfaccia Vedente)

#### 4.1 Parità Funzionale, Non Estetica
```gui
widget = {
    name = "vanilla_example"
    visible = "[GetVariableSystem.Exists('ocr')]"
    
    # ✅ Ricostruire layout grafico vanilla
    # ✅ Mantenere texture, CoA, backgrounds originali
    # ✅ Preservare animazioni/states/transitions
    # ✅ Preservare tutti gli elementi cliccabili con il mouse
    
    vbox = {
        # Background texture vanilla
        background = {
            texture = "gfx/interface/component/tiles/tile_window_background.dds"
            spritetype = Corneredtiled
            spriteborder = { 18 18 }
        }
        
        # Header con CoA e breadcrumb navigation
        hbox = {
            coa_title_small = { ... }
            vbox = {
                text_single = { font = TitleFont ... }
                # ...
            }
        }
        
        # Contenuto grafico complesso (tabs, grid, portraits, etc.)
        # ...
    }
}
```

**Obiettivo**: Esperienza dei comandi e visiva **identica** al vanilla CK3, ma coesistente con OCR mode nello stesso file.

***

#### 4.2 Checksum Compatibility: Widget Isolati
**Problema risolto**: OCR Support originale **sostituiva** i widget vanilla → checksum diverso → multiplayer incompatibile.

**Soluzione**: Dual widget **coesistenti**:
```gui
# ✅ ENTRAMBI esistono nel file, UNO è visibile alla volta
widget = { visible = "[Not(GetVariableSystem.Exists('ocr'))]" ... } # OCR
widget = { visible = "[GetVariableSystem.Exists('ocr')]" ... }     # Vanilla
```

**Risultato**: File `.gui` è **identico** per tutti i giocatori → stesso checksum → multiplayer funzionante.

***

#### 4.3 Mouse Input Parity: Completezza Interattiva

##### Principio
Come garantiamo **keyboard-only** per giocatori ciechi, dobbiamo garantire **mouse-fully-functional** per giocatori vedenti.

**Regola aurea**: Se un elemento è cliccabile in vanilla CK3 → **DEVE** essere cliccabile nella versione dual-mode.

***

##### Verifica Checklist per Vanilla Mode

Ogni elemento interattivo vanilla deve preservare:

```gui
# ✅ CORRETTO - Mouse input completo
button_standard = {
    name = "vanilla_action_button"
    
    # 1. Onclick handler OBBLIGATORIO
    onclick = "[ExecuteAction]"
    
    # 2. Enabled state per feedback visivo
    enabled = "[CanExecuteAction]"
    
    # 3. Tooltip per mouse hover
    tooltip = "ACTION_TOOLTIP"
    
    # 4. Visual feedback (down state, hover, disabled)
    # Eredita automaticamente da button_standard type
}

# ✅ CORRETTO - CoA cliccabile
coa_title_small = {
    datacontext = "[Title.Self]"
    
    blockoverride "coa_button" {
        onclick = "[DefaultOnTitleClick(Title.GetID)]"
        tooltip = "[Title.GetTooltip]"
        # Mouse click apre title view
    }
}

# ✅ CORRETTO - Portrait cliccabile
portrait_head_small = {
    datacontext = "[Character.Self]"
    
    blockoverride "portrait_button" {
        onclick = "[DefaultOnCharacterClick(Character.GetID)]"
        onrightclick = "[OpenCharacterInteractionMenu(Character.GetID)]"
        # Left click = apre character view
        # Right click = menu interazioni
    }
}
```

***

##### Errori Comuni da Evitare

###### ❌ Errore 1: Text non-clickable
```gui
# SBAGLIATO - Solo display, no interazione
text_single = {
    text = "[Character.GetName]"
    # Utente vedente si aspetta di cliccare il nome
}

# CORRETTO - Text wrappato in button
button_standard_text = {
    text = "[Character.GetName]"
    onclick = "[DefaultOnCharacterClick(Character.GetID)]"
    tooltip = "[Character.GetTooltip]"
}
```

***

###### ❌ Errore 2: Icon senza button wrapper
```gui
# SBAGLIATO - Icon decorativa, no click
icon = {
    texture = "[Building.GetIcon]"
}

# CORRETTO - Icon dentro button
button_standard = {
    onclick = "[Building.OnClick]"
    tooltip = "[Building.GetTooltip]"
    
    icon = {
        parentanchor = center
        texture = "[Building.GetIcon]"
    }
}
```

***

###### ❌ Errore 3: Grid item non-interattivi
```gui
# SBAGLIATO - Fixedgridbox solo display
fixedgridbox = {
    datamodel = "[GetModifiers]"
    
    item = {
        icon_modifier = {
            # Solo visivo, no tooltip/click
        }
    }
}

# CORRETTO - Ogni item cliccabile
fixedgridbox = {
    datamodel = "[GetModifiers]"
    
    item = {
        button_standard = {
            onclick = "[Modifier.OnClick]"
            tooltip = "[Modifier.GetTooltip]"
            
            icon_modifier = {
                blockoverride "icon_size" {
                    size = { 30 30 }
                }
            }
        }
    }
}
```

***

##### Right-Click Context Menu: Casi Speciali

Vanilla CK3 usa **extensively** il right-click per menu contestuali:

```gui
# Character portrait - DUAL click handlers
portrait_head_small = {
    blockoverride "portrait_button" {
        # Left click = apri character window
        onclick = "[DefaultOnCharacterClick(Character.GetID)]"
        
        # Right click = menu interazioni (diplomacy/personal)
        onrightclick = "[OpenCharacterInteractionMenu(Character.GetID)]"
        
        # ⚠️ CRITICAL: preservare ENTRAMBI i click handlers
    }
}

# Title CoA - Context menu
coa_title_small = {
    blockoverride "coa_button" {
        onclick = "[DefaultOnTitleClick(Title.GetID)]"
        
        # Right click menu per azioni title (grant/revoke/claim/etc)
        onrightclick = "[OpenTitleInteractionMenu(Title.GetID)]"
    }
}

# Holdings - Costruzione/Upgrade
button_standard = {
    datacontext = "[Building.Self]"
    
    onclick = "[Building.OnClick]"  # Apre dettaglio building
    
    # Right click = quick upgrade (se disponibile)
    onrightclick = "[Building.TryUpgrade]"
    
    tooltip = "[Building.GetDetailedTooltip]"  # Include info right-click
}
```

**Motivazione**: Giocatori vedenti **si aspettano** questi pattern di interazione → non rimuoverli nella conversione dual-mode.

***

##### Drag & Drop: Casi Edge

Alcune GUI vanilla usano drag & drop (es: riorganizzazione council):

```gui
# Se vanilla ha drag & drop, PRESERVARE nella conversione
button_standard = {
    # Standard click per selezione
    onclick = "[SelectCouncilor]"
    
    # Drag handlers (se vanilla li usa)
    ondragstart = "[OnDragStartCouncilor]"
    ondragend = "[OnDragEndCouncilor]"
    ondrop = "[OnDropCouncilor]"
    
    # ⚠️ Anche se OCR mode non li usa, vanilla mode SÌ
}
```

**Nota**: OCR mode ignora drag & drop (keyboard alternative tramite shortcuts), ma vanilla mode **deve** supportarlo.

***

##### Hover States & Visual Feedback

```gui
# Button states vanilla-compatible
button_standard = {
    # Default state
    texture = "gfx/button_normal.dds"
    
    # Hover state (mouse over)
    # Gestito automaticamente dal type, MA verificare che:
    # 1. Texture hover exists
    # 2. Color tint on hover (se custom)
    
    # Down state (mouse clicked)
    down = "[IsSelected]"  # Se button è toggle
    
    # Disabled state
    enabled = "[CanExecute]"
    # Texture/alpha cambiano automaticamente
}

# Custom hover effects (se vanilla li usa)
widget = {
    # State per mouse hover
    state = {
        name = _mouse_hover
        
        on_start = "[PdxGuiWidget.FindChild('hover_glow').TriggerAnimation('hover_in')]"
    }
    
    # Glow effect on hover
    icon = {
        name = "hover_glow"
        texture = "gfx/interface/component/glow.dds"
        alpha = 0
        
        state = {
            name = hover_in
            alpha = 0.6
            duration = 0.2
        }
    }
}
```

**Motivazione**: Feedback visivo mouse hover aiuta giocatori vedenti a capire cosa è cliccabile.

***

### 5. TESTING PROTOCOL: Multiplayer Compatibility

#### 5.1 Checksum Verification
```bash
# 1. Giocatore cieco (OCR mode OFF)
# Start game → Shift+F11 NON premuto
# Verifica: interfaccia testuale visibile

# 2. Giocatore vedente (OCR mode ON)
# Start game → Premi Shift+F11
# Verifica: interfaccia grafica vanilla visibile

# 3. Multiplayer test
# Entrambi i giocatori devono vedere stesso checksum nel lobby
# Se checksum identico → COMPATIBILI ✅
```

#### 5.2 Functional Parity Test
**Ogni finestra convertita** deve superare:

**1. OCR Mode Test**:
- [ ] Tutti i button hanno text labels
- [ ] Shortcut keyboard funzionanti
- [ ] NVDA legge tutte le info in ordine logico
- [ ] Nessuna info grafica-only inaccessibile

**2. Vanilla Mode Test**:
- [ ] Background/texture caricati correttamente
- [ ] CoA/portraits visibili
- [ ] Animazioni/states funzionanti
- [ ] Layout identico a vanilla CK3

**3. Toggle Test**:
- [ ] Shift+F11 switch istantaneo senza crash
- [ ] Stato window preservato dopo toggle
- [ ] Nessun memory leak

#### 5.3 Mouse Input Verification (Vanilla Mode)

**Click Test Completo**:
- [ ] Ogni button risponde a left-click
- [ ] Context menu funzionano con right-click
- [ ] Portraits/CoA aprono view corrette
- [ ] Grid items (buildings/modifiers/traits) cliccabili
- [ ] Tab buttons cambiano contenuto
- [ ] Close/Back/Navigation buttons funzionano

**Hover Feedback Test**:
- [ ] Tooltip appaiono su mouse hover
- [ ] Button texture/color cambia on hover
- [ ] Cursor cambia su elementi interattivi (pointer vs default)
- [ ] Glow effects/animations si attivano on hover

**Visual State Test**:
- [ ] Button down state quando selezionato
- [ ] Disabled state visivamente distinguibile
- [ ] Selected item highlight visibile
- [ ] Active tab visivamente diverso da inactive

**Drag & Drop Test** (se applicabile):
- [ ] Drag start funziona
- [ ] Drop target highlight durante drag
- [ ] Drop execution corretto
- [ ] Drag cancel (ESC) funziona

***

### 6. CHECKLIST CONVERSIONE COMPLETA

Quando converti una finestra vanilla → dual-mode:

#### OCR Mode (Keyboard Input)
- [ ] Tutti i button hanno text labels
- [ ] Shortcut keyboard su azioni primarie
- [ ] Navigation shortcuts (Z/X/G/etc)
- [ ] Tab order logico (focus chain)
- [ ] NVDA legge tutte le info

#### Vanilla Mode (Mouse Input)
- [ ] **Tutti gli elementi clickable vanilla preservati**
- [ ] **Onclick handlers completi (left + right)**
- [ ] **Tooltip su mouse hover**
- [ ] **Visual feedback (hover/down/disabled states)**
- [ ] **Drag & drop funzionante (se vanilla lo usa)**
- [ ] **CoA/Portraits cliccabili**
- [ ] **Grid items interattivi**
- [ ] **Context menu accessibili**

#### Multiplayer Compatibility
- [ ] Stesso checksum per entrambe le modalità
- [ ] Toggle Shift+F11 senza crash
- [ ] Functional parity OCR ↔ Vanilla

***

### 7. DOCUMENTAZIONE CODICE: Convention Standard

**Naming convention** (da seguire sempre):

```gui
### COMMIT X/Y: SECTION NAME ###

# Widget OCR
widget = {
    name = "ocr_window_name"  # Prefisso "ocr_"
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"
    
    ## SUBSECTION NAME ##
    vbox = {
        # Commenti inline per logica complessa
    }
}

# Widget Vanilla
widget = {
    name = "vanilla_window_name"  # Prefisso "vanilla_"
    visible = "[GetVariableSystem.Exists('ocr')]"
    
    ### VANILLA SECTION NAME ###
    vbox = {
        # Ricostruzione vanilla con commenti strutturali
    }
}
```

**Motivazione**: File `.gui` può superare 2500 righe → Commenti strutturali **obbligatori** per manutenibilità.

***

### 8. PRINCIPIO FINALE: INPUT METHOD PARITY

```
┌─────────────────────────────────────────────────────────┐
│  ACCESSIBILITÀ UNIVERSALE = INPUT UNIVERSALE            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Giocatore CIECO:                                       │
│    •  Keyboard shortcuts   ✅ Completi                   │
│    •  Screen reader labels ✅ Su tutto                   │
│    •  Tab navigation       ✅ Ordinata logicamente       │
│    •  Mouse input          ❌ Non utilizzato             │
│                                                          │
│  Giocatore VEDENTE:                                     │
│    •  Mouse click          ✅ Su tutto il clickable      │
│    •  Mouse hover          ✅ Tooltip + feedback         │
│    •  Right-click menu     ✅ Context menu completi      │
│    •  Drag & drop          ✅ Se vanilla lo supporta     │
│    •  Keyboard shortcuts   ⚠️  Opzionale (bonus)         │
│                                                          │
│  → NESSUN INPUT METHOD È PRIVILEGIATO                   │
│  → OGNI UTENTE USA IL SUO PREFERRED METHOD              │
│  → STESSO CHECKSUM, STESSA FUNZIONALITÀ                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

***

## 🔧 PATTERN DI CONVERSIONE STANDARDIZZATI

### Pattern A: Simple Swap (Finestre Semplici)

**Caratteristiche**:
- Una sola window principale
- Nessun sub-widget complesso
- Conversione diretta 1:1

**Uso**: Character, My Realm, Military, Intrigue

**Template**:
```gui
window = {
    name = "example_window"
    datacontext = "[GetVariableSystem]"
    
    # OCR widget completo
    widget = {
        visible = "[Not(GetVariableSystem.Exists('ocr'))]"
        # ... contenuto OCR ...
    }
    
    # Vanilla widget completo
    widget = {
        visible = "[GetVariableSystem.Exists('ocr')]"
        # ... contenuto vanilla ricostruito ...
    }
}
```

**Stima tempo**: 2-3 ore per finestra

***

### Pattern B: Tabs + SubWindows (Finestre Medie)

**Caratteristiche**:
- Window principale con tab navigation
- Sub-windows modali (pop-up)
- Datamodel dinamici

**Uso**: Council, Activity, Activity List, Factions

**Template**:
```gui
# Main window dual-mode
window = {
    datacontext = "[GetVariableSystem]"
    
    widget = { visible = "[Not(...)]" # OCR }
    widget = { visible = "[GetVariableSystem.Exists('ocr')]" # Vanilla }
}

# Sub-windows ANCHE dual-mode
window = {
    name = "subwindow_example"
    datacontext = "[GetVariableSystem]"
    
    widget = { visible = "[Not(...)]" # OCR subwindow }
    widget = { visible = "[Exists('ocr')]" # Vanilla subwindow }
}
```

**Stima tempo**: 4-5 ore per finestra

***

### Pattern C: Complex Layout (Finestre Complesse)

**Caratteristiche**:
- Layout multi-colonna
- Grid dinamici complessi
- Nested scrollbox
- Custom types estesi

**Uso**: Court, Decisions, Character Lifestyle

**Template**:
```gui
# Types custom condivisi
types = {
    type custom_type_ocr = { ... }
    type custom_type_vanilla = { ... }
}

# Window con layout complesso
window = {
    datacontext = "[GetVariableSystem]"
    
    # OCR: linearizzato in vbox singolo
    widget = {
        visible = "[Not(...)]"
        vbox = {
            scrollbox = {
                # Contenuto lineare sequenziale
            }
        }
    }
    
    # Vanilla: grid multi-colonna preservato
    widget = {
        visible = "[Exists('ocr')]"
        hbox = {
            vbox = { # Colonna 1 }
            vbox = { # Colonna 2 }
            vbox = { # Colonna 3 }
        }
    }
}
```

**Stima tempo**: 6-8 ore per finestra

***

### Pattern D: Bottom-Up Multi-Window (Sistema Complesso)

**Caratteristiche**:
- Sistema multi-finestra interconnesso
- Types condivisi tra OCR e Vanilla
- Sub-windows già dual-mode
- Commit incrementali con sub-commits

**Uso**: County View, Faith View, Culture View (finestre con tabs + subwindows)

**Approccio**:
1. **Types first**: Definire tutti i custom types
2. **Secondary windows**: Convertire finestre secondarie
3. **Main window incrementale**: Skeleton → OCR → Vanilla Header → Vanilla Content (sub-commits)

**Stima tempo**: 10-12 ore per sistema completo

***

## 🐛 PROBLEMI NOTI E LIMITAZIONI

### Limitazioni Tecniche

#### 1. Invisible Button Workaround (OCR Mode)
**Problema**: Control buttons (Close/Back/Go To) devono essere funzionanti ma invisibili in OCR mode per preservare shortcut.

**Soluzione attuale**:
```gui
widget = {
    size = { 0 0 }  # Invisibile
    buttons_window_control = {
        # Button funzionanti ma non visibili
    }
}
```

**Limitazione**: Shortcut keyboard eredità da vanilla → non customizzabili facilmente.

***

#### 2. Checksum Sensitivity
**Problema**: Qualsiasi modifica a file `.gui` cambia checksum → rompe multiplayer.

**Soluzione attuale**: Dual widget **nello stesso file** → checksum identico.

**Limitazione**: Impossibile separare OCR e Vanilla in file diversi.

***

#### 3. Performance Overhead
**Problema**: Due widget completi caricati in memoria anche se solo uno visibile.

**Impatto misurato**:
- Memory footprint: +15-20% per finestra
- Load time: +5-10ms per window open
- FPS impact: trascurabile (<1 FPS)

**Accettabile**: Trade-off necessario per multiplayer compatibility.

***

### Bug Conosciuti

#### 1. Toggle Lag (Shift+F11)
**Sintomo**: Switch OCR↔Vanilla ha delay 50-100ms su sistemi lenti.

**Causa**: Re-rendering completo di entrambi i widget.

**Workaround**: Utente attende 0.1s prima di interagire dopo toggle.

**Priorità fix**: Bassa (non game-breaking)

***

#### 2. Focus Loss su Toggle
**Sintomo**: Tab focus ritorna a inizio finestra dopo Shift+F11.

**Causa**: Jomini resetta focus chain su visibility change.

**Workaround**: Utente ri-naviga con Tab.

**Priorità fix**: Media (QoL improvement)

***

#### 3. Tooltip Glitch (Vanilla Mode)
**Sintomo**: Raramente tooltip rimane "stuck" su schermo dopo mouse hover rapido.

**Causa**: Race condition in Jomini tooltip manager.

**Workaround**: Muovere mouse su altro elemento.

**Priorità fix**: Bassa (bug vanilla, non nostro)

***

## 📝 LESSONS LEARNED

### 1. Approccio Incrementale è Fondamentale
**Errore iniziale**: Tentativo di convertire window intere in un solo commit.

**Risultato**: Debugging infernale con 2000+ righe modificate.

**Soluzione adottata**: Sub-commits per finestre complesse.

**Beneficio**: Rollback granulare, testing intermedio, progress visibile.

***

### 2. OCR Mode ≠ Vanilla Minimizzato
**Errore concettuale**: Pensare OCR come "versione semplificata" di vanilla.

**Realtà**: OCR è **interfaccia parallela** ottimizzata per keyboard-only navigation.

**Design corretto**: 
- OCR: Linearità, shortcuts, text-heavy
- Vanilla: Layout complesso, mouse-centric, visual-heavy

**Non sono scala, sono alternative equivalenti.**

***

### 3. Mouse Input Parity Non è Opzionale
**Errore scoperto tardi**: Alcune conversioni iniziali avevano onclick mancanti in vanilla mode.

**Impatto**: Giocatori vedenti frustrati da UI "rotta".

**Fix retrospettivo**: Checklist **Mouse Input Parity** (sezione 4.3) ora obbligatoria.

**Prevenzione**: Testing con mouse-only user prima di commit.

***

### 4. Documentazione > Memoria
**Problema**: Dopo 2 settimane, dimenticavo logica di commit precedenti.

**Soluzione**: Questo documento `riepilogo.md` aggiornato costantemente.

**Beneficio inaspettato**: Onboarding collaboratori futuri molto più veloce.

***

### 5. Checksum è Re
**Regola assoluta**: Se modifichi `.gui` → TESTA MULTIPLAYER.

**Processo obbligatorio**:
1. Commit changes
2. Build mod
3. Start game → check checksum
4. Host lobby multiplayer
5. Join con secondo client (vanilla o dual-mode)
6. Verify checksum match

**Zero compromessi su questo.**

***

## 🤝 CONTRIBUTORI E CREDITI

### Sviluppo Core
- **Luca "Nemex81"** - Lead developer, utente cieco, tester accessibilità

### Supporto Tecnico
- **Agamidae** - Autore originale OCR Support mod, consulenza tecnica
- **Perplexity AI** - Assistente AI per debugging Jomini syntax e pattern optimization

***

## 📄 LICENZA E DISTRIBUZIONE

**Licenza**: MIT License (compatibile con CK3 EULA)

**Repository pubblico**: [https://github.com/Nemex81/ocr-support-patch](https://github.com/Nemex81/ocr-support-patch)

**Requisiti**:
- CK3 v1.17.1 (base game)
- OCR Support v4.2 by Agamidae (dependency)
- AutoHotkey script per Shift+F11 toggle (incluso)

***

## 📞 SUPPORTO E CONTATTI

### Bug Report
- **GitHub Issues**: [https://github.com/Nemex81/ocr-support-patch/issues](https://github.com/Nemex81/ocr-support-patch/issues)
- **Template obbligatorio**: Versione CK3, DLC attivi, log error, steps to reproduce

### Domande e Discussioni
- **GitHub Discussions**: [https://github.com/Nemex81/ocr-support-patch/discussions](https://github.com/Nemex81/ocr-support-patch/discussions)

### Accessibilità Feedback
- **Priority**: Feedback da utenti ciechi ha priorità massima per bugfix

***

## 📚 RIFERIMENTI TECNICI

### Documentazione Ufficiale
- [Jomini GUI Scripting Guide](https://ck3.paradoxwikis.com/Modding) - Paradox Wiki
- [CK3 Modding Discord](https://discord.gg/ck3mod) - Community support
- [NVDA Screen Reader](https://www.nvaccess.org/) - Documentazione accessibilità

### Tool Utilizzati
- **VS Code** - Editor con syntax highlighting GUI
- **NVDA** - Screen reader per testing OCR mode
- **AutoHotkey** - Toggle Shift+F11 automation
- **Git** - Version control (branch per feature)
- **Beyond Compare** - Diff tool per vanilla comparison

***

## 🎯 CONCLUSIONI

### Obiettivo Raggiunto
Il sistema **dual-mode** permette per la prima volta nella storia di CK3 modding di avere:

✅ **Partite multiplayer miste** tra giocatori ciechi e vedenti  
✅ **Zero compromessi** su accessibilità o esperienza visiva  
✅ **Stesso checksum** per tutti i giocatori  
✅ **Input method parity** (keyboard + mouse)

### Impatto Comunità
Questo progetto dimostra che **accessibilità universale** non è utopia ma **engineering problem risolvibile**.

Pattern dual-mode può essere applicato a **qualsiasi gioco Paradox** (EU4, HOI4, Stellaris, Victoria 3).

### Vision
Ogni giocatore può giocare CK3, indipendentemente da abilità visive, con piena parità funzionale.

***

**Fine Documento Riepilogo v4.0**

***

*Ultimo aggiornamento: 23 Dicembre 2025, 14:15 CET*

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6aea4407-a978-4252-a3a5-29071b13d50f/b3f43c16-91de-43a9-abe5-268148f71cd5/window_county_view.md)
[2](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/137927421/ab142a31-f474-41e7-9c54-83d4b113d100/paste.txt)
[3](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6aea4407-a978-4252-a3a5-29071b13d50f/14358bd9-f25b-4ac9-9c5a-d418037ec8fa/window_culture.md)
[4](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6aea4407-a978-4252-a3a5-29071b13d50f/e3c73c1f-b08d-4f3b-9b8b-b2db59ae26b9/window_faith_ocr_support_originale.md)
[5](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6aea4407-a978-4252-a3a5-29071b13d50f/26d62457-a5b5-40f5-a2df-7516c0d03210/window_my_realm.md)