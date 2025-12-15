# 📋 DOCUMENTO DI RIEPILOGO PROGETTO CK3 OCR SUPPORT - ACCESSIBILITY FIX

**Versione**: 3.3 - County View System Commit 4A/4 Completato  
**Data ultima modifica**: 15 Dicembre 2025, 01:22 CET  
**Versione progetto**: OCR Support Compatibility Patch - Dual Mode View + County System  
**Repository**: [https://github.com/Nemex81/ocr-support-patch](https://github.com/Nemex81/ocr-support-patch)  
**Sviluppatore**: Luca "Nemex81" (utente cieco, Italia)  
**Screen reader**: NVDA su Windows 10  
**Gioco**: Crusader Kings 3 v1.17.1 (Steam)  
**Mod base**: OCR Support v4.2 by Agamidae

---

## 🎯 OBIETTIVO DEL PROGETTO

Risolvere il problema di **finestre nere** nella modalità normo vedente della mod **OCR Support v4.2**, che impediva partite multiplayer miste tra giocatori ciechi e normovedenti con lo stesso checksum.

### Repository collegati
- **Mod originale**: [https://github.com/Agamidae/CK3-OCR](https://github.com/Agamidae/CK3-OCR)
- **Compatibility Patch**: [https://github.com/Nemex81/ocr-support-patch](https://github.com/Nemex81/ocr-support-patch)

### ✅ OBIETTIVO FASE 1 RAGGIUNTO
Tutte le 11 finestre principali del gioco sono state convertite con successo al sistema dual-mode, permettendo partite multiplayer completamente funzionali tra giocatori ciechi (modalità OCR testuale) e normovedenti (modalità grafica vanilla).

### 🔨 OBIETTIVO FASE 2 IN CORSO - 25% COMPLETATO
Conversione del sistema County View (window_county_view.gui) con approccio bottom-up incrementale in 4 SUB-COMMIT (4A, 4B, 4C, 4D).
**Progress**: 1/4 sub-commit completati (Commit 4A/4 ✅) - 3 sub-commit rimanenti.

---

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

---

## 🏛️ PATTERN D: County View Bottom-Up (Sistema Complesso Multi-Window)

**Uso**: window_county_view.gui (Vista Contea + Costruzione Holdings)  
**Caratteristiche**:
- Sistema multi-finestra interconnesso (holding_view + holding_tracks_view + holding_type_selection_view)
- Approccio incrementale bottom-up in 4 commit principali
- Commit 4/4 suddiviso in 4 SUB-COMMIT (4A, 4B, 4C, 4D)
- Types definitions condivisi tra OCR e Vanilla
- Finestre secondarie già dual-mode
- Window principale con widget duale molto esteso (~2500 righe vanilla)

### Strategia di Ricostruzione: BOTTOM-UP INCREMENTAL

**Fase 1: ✅ Types Definitions (Completata)**
- 16 types totali: 11 OCR specifici + 5 Vanilla condivisi
- Types OCR: button_*, text_*, flow_* per interfaccia accessibile
- Types Vanilla: building_in_vassal_warning_hbox per logica condivisa

**Fase 2: ✅ Secondary Windows (Completata)**
- `holding_tracks_view`: Finestra costruzione nuovi edifici (dual-mode completo)
- `holding_type_selection_view`: Selezione tipo holding (Castle/City/Temple) (dual-mode completo)

**Fase 3: 🔨 Main Window - 25% COMPLETATO (holding_view dual-mode)**

Approccio incrementale in **4 COMMIT PRINCIPALI + 4 SUB-COMMIT**:

---

#### COMMIT 1/4: ✅ Skeleton and States (Completato - 14 Dic 2025)

**Obiettivo**: Creare la struttura base della finestra con stati di animazione comuni

**Implementazione**:
```gui
window = {
    name = "holding_view"
    widgetid = "holding_view"
    parentanchor = bottom|left
    size = { 700 100% }
    
    # Datacontexts comuni
    datacontext = "[GetVariableSystem]"  # ← CRITICAL: Toggle variable
    datacontext = "[HoldingView.GetProvince]"
    datacontext = "[HoldingView.GetHolding]"
    datacontext = "[HoldingView.GetHolder]"
    datacontext = "[Province.GetCounty]"
    
    # States comuni (animazioni)
    state = { name = _show ... }
    state = { name = _hide ... }
    state = { name = pan_to_previous_county ... }
    state = { name = adjacent_counties ... }
    
    # Widget OCR (placeholder)
    widget = {
        name = "ocr_holding_view"
        visible = "[Not(GetVariableSystem.Exists('ocr'))]"
        vbox = { } # Placeholder
    }
    
    # Widget Vanilla (placeholder)
    widget = {
        name = "vanilla_holding_view"
        visible = "[GetVariableSystem.Exists('ocr')]"
        vbox = { } # Placeholder
    }
}
```

**Risultato**: Struttura container pronta per ospitare entrambe le modalità

---

#### COMMIT 2/4: ✅ OCR Widget Content (Completato - 14 Dic 2025)

**Commit SHA**: `6842a77b12627370926e34d968ee6d0b52ac45f9`  
**File size**: 40.8 KB (~900 righe di contenuto OCR)

**Contenuto implementato**:

```gui
widget = {
    name = "ocr_holding_view"
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"
    size = { 100% 100% }
    
    ## WINDOW CONTROL BUTTONS (invisible but functional)
    widget = {
        size = { 0 0 }
        buttons_window_control = {
            blockoverride "button_go_to" { ... }
            blockoverride "button_back" { ... }
            blockoverride "button_close" { ... }
        }
    }
    
    ## MAIN OCR CONTENT VBOX
    vbox = {
        using = ocr_margins
        using = ocr
        background = { using = Background_Area_Border_Solid }
        
        error_button = { }
        
        scrollbox = {
            # 8 SEZIONI PRINCIPALI:
            # 1. Province and County Titles
            # 2. Current Holding Info
            # 3. Domicile Info
            # 4. County Title Info
            # 5. Occupation/Siege/Raid
            # 6. Realm and Military Info
            # 7. Adjacent Counties
            # 8. Holding Details
        }
    }
}
```

**Funzionalità OCR implementate**:
- ✅ Navigazione testuale completa tra holdings
- ✅ Info provincia/contea con coordinate X/Y
- ✅ Gestione domicilio per giocatori landless
- ✅ Task system (Chancellor, Steward, etc.)
- ✅ Informazioni siege/raid/occupation
- ✅ Adjacent counties navigation (Z/X prev/next)
- ✅ Buildings count e stats (tax/levies)
- ✅ Grant holding functionality
- ✅ Tutti gli shortcut keyboard (E, H, T, A, etc.)

**Risultato**: Interfaccia OCR 100% funzionale e accessibile via screen reader NVDA

---

#### COMMIT 3/4: ✅ Vanilla Widget Header (Completato - 14 Dic 2025 23:52)

**Commit SHA**: `675ad4656cb9f8c3d62d6acfa8e1d7dbcd0e0ce5`  
**File size**: 9.3 KB (~230 righe vanilla header)  
**Link commit**: [View on GitHub](https://github.com/Nemex81/ocr-support-patch/commit/675ad4656cb9f8c3d62d6acfa8e1d7dbcd0e0ce5)

**Obiettivo**: Aggiungere header grafico completo con background, CoA, breadcrumb navigation, e control buttons

**Contenuto implementato**:

```gui
widget = {
    name = "vanilla_holding_view"
    visible = "[GetVariableSystem.Exists('ocr')]"
    size = { 605 750 }
    parentanchor = bottom|left
    alwaystransparent = yes
    
    vbox = {
        ### MAIN CONTENT VBOX ###
        vbox = {
            name = "window_content"
            margin_right = 40
            margin_top = 35
            
            ### WINDOW BACKGROUND ###
            background = {
                texture = "gfx/interface/component/tiles/tile_window_background_subwindow.dds"
                spritetype = Corneredtiled
                spriteborder = { 18 18 }
                
                modify_texture = {
                    name = "overlay"
                    texture = "gfx/interface/component/overlay/overlay_effect.dds"
                    blendmode = overlay
                }
            }
            
            ### COUNTY HEADER SECTION ###
            hbox = {
                name = "county_header"
                
                background = {
                    using = Background_Area_Dark
                }
                
                # Coat of Arms
                coa_title_small = {
                    datacontext = "[HoldingView.GetCountyTitle]"
                }
                
                # County Name and Info
                vbox = {
                    # County name with edit button
                    hbox = {
                        text_single = {
                            text = "[HoldingView.GetCountyTitle.GetNameNoTooltipU]"
                            using = Font_Size_Big
                            font = TitleFont
                        }
                        
                        button_edit_text = {
                            visible = "[HoldingView.GetCountyTitle.CanPlayerCustomizeTitle]"
                            onclick = "[OpenTitleCustomizationWindow(HoldingView.GetCountyTitle)]"
                        }
                    }
                    
                    # Holder status (Your/Realm/Foreign county)
                    vbox = {
                        text_single = { # Your county
                            visible = "[ObjectsEqual( Character.Self, GetPlayer )]"
                            text = "HOLDING_VIEW_YOUR_COUNTY"
                        }
                        
                        text_single = { # Top realm county
                            visible = "[Character.IsOtherLiegeOrAbove( GetPlayer )]"
                            text = "HOLDING_VIEW_TOP_REALM_COUNTY"
                        }
                        
                        text_single = { # Foreign county
                            visible = "[Not(Or(...))]"
                            text = "HOLDING_VIEW_FOREIGN_COUNTY"
                        }
                    }
                }
            }
            
            ### WINDOW CONTROL BUTTONS ###
            buttons_window_control = {
                blockoverride "button_go_to" {
                    onclick = "[HoldingView.PanToCountyCapital]"
                    tooltip = "GO_TO_PROVINCE_TT"
                }
                
                blockoverride "button_back" {
                    visible = "[HasViewHistory]"
                    onclick = "[OpenFromViewHistory]"
                }
                
                blockoverride "button_close" {
                    onclick = "[HoldingView.Close]"
                }
            }
            
            ### PLACEHOLDER FOR TAB CONTENT (COMMIT 4/4) ###
            # Tab navigation and content will be added next
        }
    }
}
```

**Elementi grafici implementati**:
- ✅ **Background texture**: Window subwindow con overlay effect
- ✅ **County Header**: Background area dark con spacing corretto
- ✅ **Coat of Arms**: coa_title_small della contea
- ✅ **County Name**: Font TitleFont size Big con maxwidth 380
- ✅ **Edit Title Button**: Per customizzazione nome contea
- ✅ **Holder Status**: 3 stati (Your/Top Realm/Foreign County)
- ✅ **Window Controls**: Close/Back/Go To buttons funzionanti

**Test in-game effettuati**:
- ✅ Click su provincia → Finestra OCR mode (default)
- ✅ Shift+F11 → Modalità vedente con header grafico
- ✅ Background caricato correttamente
- ✅ CoA contea visibile e cliccabile
- ✅ County name con font customizzato
- ✅ Pulsanti Close/Back/Go funzionanti
- ✅ Holder status corretto (Your/Realm/Foreign)

**Risultato**: Header grafico completo e funzionale - pronto per contenuto tab

---

#### COMMIT 4/4: 🔨 Vanilla Widget Tabs (SUDDIVISO IN 4A-4D) - 25% COMPLETATO

**Obiettivo**: Completare widget vanilla con tab navigation e tutto il contenuto grafico  
**Stima righe totali**: ~1800 righe vanilla (la sezione più grande)  
**File finale previsto**: ~2500 righe totali (~60 KB)

**Strategia**: Suddivisione in 4 SUB-COMMIT incrementali testabili

---

### 📋 COMMIT 4A/4: ✅ COUNTY INFO TAB (COMPLETATO - 15 Dic 2025 01:20)

**Commit SHA**: `7154a1617e0d3d8e5686964b7538a810963ea8f9`  
**File size**: 12.9 KB (~150 righe aggiunte)  
**Link commit**: [View on GitHub](https://github.com/Nemex81/ocr-support-patch/commit/7154a1617e0d3d8e5686964b7538a810963ea8f9)

**Obiettivo**: Aggiungere prima sezione tab content con info contea

**Contenuto implementato**:

```gui
### COMMIT 4A/4: COUNTY INFO TAB ###

vbox = {
    layoutpolicy_horizontal = expanding
    margin = { 10 5 }
    spacing = 5
    
    ### DE JURE HIERARCHY ###
    vbox = {
        datacontext = "[HoldingView.GetCountyTitle]"
        
        fixedgridbox = {
            name = "dejure_hierarchy"
            datamodel = "[Title.GetDeJureLieges]"
            flipdirection = yes
            addcolumn = 40
            addrow = 40
            maxverticalslots = 1
            
            item = {
                coa_title_tiny_crown = {}
            }
        }
    }
    
    ### COUNTY MODIFIERS ROW ###
    hbox = {
        fixedgridbox = {
            name = "county_modifiers"
            datacontext = "[HoldingView.GetCountyTitle]"
            datamodel = "[Title.GetModifiers]"
            flipdirection = yes
            addcolumn = 30
            addrow = 30
            maxverticalslots = 1
            
            item = {
                icon_modifier = {
                    blockoverride "icon_size" {
                        size = { 30 30 }
                    }
                }
            }
        }
        
        expand = {}
        
        ### MOVE DOMICILE BUTTON ###
        button_standard = {
            name = "move_domicile_button"
            datacontext = "[GetPlayer]"
            visible = "[And(And(Character.IsDomicileInProvince(Province.Self), Not(Province.IsCapitalBarony)), Character.CanMoveDomicile)]"
            size = { 180 30 }
            text = "HOLDING_VIEW_MOVE_DOMICILE"
            onclick = "[Character.MoveDomicile(Province.Self)]"
        }
    }
    
    ### COUNTY FERTILITY BAR ###
    vbox = {
        name = "fertility_bar_section"
        spacing = 3
        
        text_label_center = {
            text = "COUNTY_FERTILITY_LABEL"
        }
        
        widget = {
            size = { 100% 20 }
            
            progressbar_standard = {
                name = "fertility_bar"
                size = { 100% 100% }
                
                blockoverride "values" {
                    value = "[FixedPointToFloat(Province.GetFertility)]"
                    min = 0
                    max = 100
                }
                
                blockoverride "color" {
                    tintcolor = { 0.4 0.8 0.3 1.0 }
                }
            }
            
            text_single = {
                parentanchor = center
                text = "[Province.GetFertility|0]"
                default_format = "#high"
            }
        }
        
        ### SEASONAL INFO ###
        text_multi = {
            name = "seasonal_info"
            autoresize = yes
            max_width = 550
            text = "COUNTY_FERTILITY_SEASONAL_DESC"
        }
    }
    
    ### OCCUPATION OVERLAY ###
    widget = {
        visible = "[HoldingView.GetCountyTitle.IsOccupied]"
        size = { 100% 40 }
        
        background = {
            using = Background_Area_Dark
            tintcolor = { 0.8 0.2 0.2 0.5 }
        }
        
        text_label_center = {
            parentanchor = center
            text = "COUNTY_OCCUPIED"
            default_format = "#high"
        }
    }
}
```

**Elementi implementati**:
- ✅ **De Jure Hierarchy**: Catena lieges con CoA tiny crown
- ✅ **County Modifiers**: Fixedgridbox con icons 30x30
- ✅ **Move Domicile Button**: Conditional visibility per landless players
- ✅ **Fertility Bar**: Progressbar 0-100 con colore verde customizzato
- ✅ **Seasonal Info**: Text multi con descrizione variazioni stagionali
- ✅ **Occupation Overlay**: Warning rosso se contea occupata

**Test in-game effettuati**:
- ✅ De jure hierarchy mostra impero/regno/ducato correttamente
- ✅ County modifiers icons visibili e con tooltip
- ✅ Move domicile button appare solo quando necessario
- ✅ Fertility bar con valore corretto (0-100)
- ✅ Seasonal info text leggibile
- ✅ Occupation overlay appare se contea occupata

**Risultato**: Prima sezione county info completa e funzionale

---

### 📋 COMMIT 4B/4: ⏳ COUNTY STATS & HOLDER (PROSSIMO)

**Obiettivo**: Aggiungere stats contea e portrait holder  
**Stima righe**: ~500 righe  
**Posizione**: Dopo County Info Tab, prima delle tab buttons

**Da implementare**:

#### SEZIONE 1: Holder Portrait Section

```gui
### HOLDER PORTRAIT SECTION ###
vbox = {
    name = "holder_section"
    layoutpolicy_horizontal = expanding
    margin = { 10 5 }
    spacing = 5
    
    background = {
        using = Background_Area
    }
    
    ### HOLDER INFO HBOX ###
    hbox = {
        datacontext = "[HoldingView.GetCountyTitle.GetHolder]"
        spacing = 10
        
        ### PORTRAIT ###
        portrait_head_small = {
            datacontext = "[HoldingView.GetCountyTitle.GetHolder]"
            
            blockoverride "portrait_button" {
                onclick = "[DefaultOnCharacterClick(Character.GetID)]"
            }
        }
        
        ### HOLDER NAME AND TITLE ###
        vbox = {
            layoutpolicy_horizontal = expanding
            
            text_single = {
                text = "[Character.GetUINameNoTooltip]"
                using = Font_Size_Medium
                fontsize_min = 14
            }
            
            text_single = {
                text = "[Character.GetPrimaryTitle.GetNameNoTooltip]"
                using = Font_Size_Small
                fontsize_min = 10
            }
            
            expand = {}
        }
    }
    
    divider_light = { layoutpolicy_horizontal = expanding }
}
```

#### SEZIONE 2: County Stats Bars

```gui
### COUNTY STATS ###
vbox = {
    name = "county_stats"
    layoutpolicy_horizontal = expanding
    margin = { 10 5 }
    spacing = 5
    
    ### CONTROL LEVEL ###
    vbox = {
        text_label_left = {
            text = "COUNTY_CONTROL_LABEL"
        }
        
        progressbar_standard = {
            name = "control_bar"
            size = { 100% 25 }
            
            blockoverride "values" {
                value = "[FixedPointToFloat(County.GetControl)]"
                min = 0
                max = 100
            }
            
            text_single = {
                parentanchor = center
                text = "[County.GetControl|0]%"
            }
        }
        
        text_multi = {
            text = "COUNTY_CONTROL_DESC"
            autoresize = yes
            max_width = 550
        }
    }
    
    ### DEVELOPMENT LEVEL ###
    vbox = {
        text_label_left = {
            text = "COUNTY_DEVELOPMENT_LABEL"
        }
        
        hbox = {
            progressbar_standard = {
                name = "development_bar"
                size = { 450 25 }
                
                blockoverride "values" {
                    value = "[FixedPointToFloat(County.GetDevelopmentLevel)]"
                    min = 0
                    max = 100
                }
                
                text_single = {
                    parentanchor = center
                    text = "[County.GetDevelopmentLevel|0]"
                }
            }
            
            # Monthly progress indicator
            text_single = {
                text = "DEVELOPMENT_MONTHLY_PROGRESS"
                tooltip = "DEVELOPMENT_MONTHLY_TOOLTIP"
            }
        }
        
        text_multi = {
            text = "COUNTY_DEVELOPMENT_DESC"
            autoresize = yes
            max_width = 550
        }
    }
    
    divider_light = { layoutpolicy_horizontal = expanding }
}
```

#### SEZIONE 3: County Opinion

```gui
### COUNTY OPINION ###
vbox = {
    name = "county_opinion_section"
    layoutpolicy_horizontal = expanding
    margin = { 10 5 }
    spacing = 5
    
    hbox = {
        icon = {
            size = { 30 30 }
            texture = "gfx/interface/icons/icon_opinion.dds"
        }
        
        text_single = {
            text = "COUNTY_OPINION_LABEL"
        }
        
        text_single = {
            text = "[County.GetOpinion|+]"
            default_format = "#high"
        }
        
        expand = {}
        
        # Faction icon (if in faction)
        icon = {
            visible = "[County.IsInFaction]"
            size = { 30 30 }
            texture = "gfx/interface/icons/icon_faction.dds"
            tooltip = "COUNTY_IN_FACTION_TOOLTIP"
        }
    }
    
    divider_light = { layoutpolicy_horizontal = expanding }
}
```

#### SEZIONE 4: Culture & Faith

```gui
### CULTURE & FAITH ###
hbox = {
    name = "culture_faith_section"
    layoutpolicy_horizontal = expanding
    margin = { 10 5 }
    spacing = 10
    
    ### CULTURE ###
    vbox = {
        layoutpolicy_horizontal = expanding
        
        hbox = {
            icon = {
                size = { 40 40 }
                texture = "[County.GetCulture.GetIcon]"
            }
            
            vbox = {
                text_single = {
                    text = "[County.GetCulture.GetNameNoTooltip]"
                    using = Font_Size_Medium
                }
                
                text_single = {
                    text = "CULTURE_ACCEPTANCE"
                    using = Font_Size_Small
                }
            }
        }
        
        progressbar_standard = {
            size = { 100% 20 }
            
            blockoverride "values" {
                value = "[FixedPointToFloat(County.GetCultureAcceptance)]"
                min = 0
                max = 100
            }
            
            text_single = {
                parentanchor = center
                text = "[County.GetCultureAcceptance|0]%"
            }
        }
    }
    
    ### FAITH ###
    vbox = {
        layoutpolicy_horizontal = expanding
        
        hbox = {
            icon = {
                size = { 40 40 }
                texture = "[County.GetFaith.GetIcon]"
            }
            
            vbox = {
                text_single = {
                    text = "[County.GetFaith.GetNameNoTooltip]"
                    using = Font_Size_Medium
                }
                
                text_single = {
                    text = "FAITH_LABEL"
                    using = Font_Size_Small
                }
            }
        }
    }
}
```

**Checklist Commit 4B/4**:
- [ ] Portrait holder con onclick
- [ ] Holder name e primary title
- [ ] Control bar (0-100%)
- [ ] Development bar con monthly progress
- [ ] County opinion con faction icon
- [ ] Culture icon e acceptance bar
- [ ] Faith icon e name
- [ ] Dividers tra sezioni
- [ ] Tooltips su tutti gli elementi
- [ ] Test in-game con contee diverse (your/realm/foreign)
- [ ] Verifica valori corretti (control/development/opinion)

**Stima tempo**: ~30 minuti implementazione + 10 minuti testing

---

### 📋 COMMIT 4C/4: ⏳ HOLDINGS NAVIGATION (DA FARE)

**Obiettivo**: Sistema navigazione holdings con tab buttons  
**Stima righe**: ~300 righe  
**Posizione**: Dopo County Stats, prima del contenuto holding

**Da implementare**:

#### SEZIONE 1: Holdings Tab Buttons

```gui
### HOLDINGS TAB BUTTONS ###
fixedgridbox = {
    name = "holdings_tab_buttons"
    datamodel = "[County.GetHoldings]"
    flipdirection = yes
    addcolumn = 70
    addrow = 70
    maxverticalslots = 1
    
    item = {
        button_tab = {
            name = "holding_tab_button"
            size = { 60 60 }
            onclick = "[HoldingView.SelectHolding(Holding.Self)]"
            down = "[ObjectsEqual(Holding.Self, HoldingView.GetHolding)]"
            tooltip = "[Holding.GetNameNoTooltip]"
            
            ### HOLDING ICON ###
            icon = {
                parentanchor = center
                size = { 50 50 }
                texture = "[Holding.GetType.GetIcon]"
            }
            
            ### COUNTY CAPITAL INDICATOR ###
            icon = {
                visible = "[Holding.IsCountyCapital]"
                parentanchor = top|right
                size = { 20 20 }
                texture = "gfx/interface/icons/symbols/icon_county_capital.dds"
            }
            
            ### REALM CAPITAL INDICATOR ###
            icon = {
                visible = "[Holding.IsRealmCapital]"
                parentanchor = top|left
                size = { 20 20 }
                texture = "gfx/interface/icons/symbols/icon_realm_capital.dds"
            }
        }
    }
}
```

**Checklist Commit 4C/4**:
- [ ] Holdings tab buttons fixedgridbox
- [ ] Holding icons (Castle/City/Temple/Tribal)
- [ ] County capital indicator (top-right)
- [ ] Realm capital indicator (top-left)
- [ ] Down state per holding selezionato
- [ ] Onclick seleziona holding
- [ ] Tooltip con nome holding
- [ ] Test cambio holding runtime
- [ ] Verifica indicatori capital corretti

**Stima tempo**: ~20 minuti implementazione + 5 minuti testing

---

### 📋 COMMIT 4D/4: ⏳ HOLDING INFO & BUILDINGS (FINALE - DA FARE)

**Obiettivo**: Info holding corrente + griglia edifici  
**Stima righe**: ~800 righe  
**Posizione**: Dopo holdings tabs, fino a fine widget

**Da implementare**:

#### SEZIONE 1: Holding Info

```gui
### HOLDING INFO SECTION ###
vbox = {
    name = "holding_info"
    datacontext = "[HoldingView.GetHolding]"
    visible = "[HoldingView.HasHolding]"
    layoutpolicy_horizontal = expanding
    margin = { 10 5 }
    spacing = 5
    
    ### HOLDING ILLUSTRATION ###
    widget = {
        size = { 100% 200 }
        
        background = {
            texture = "[Holding.GetIllustration]"
            fittype = centercrop
            
            modify_texture = {
                name = "mask"
                texture = "gfx/interface/component/masks/mask_fade_vertical.dds"
                blend_mode = alphamultiply
            }
        }
    }
    
    ### HOLDING NAME AND TYPE ###
    hbox = {
        spacing = 10
        
        icon = {
            size = { 60 60 }
            texture = "[Holding.GetType.GetIcon]"
        }
        
        vbox = {
            text_single = {
                text = "[Holding.GetNameNoTooltip]"
                using = Font_Size_Big
            }
            
            text_single = {
                text = "[Holding.GetTypeName]"
                using = Font_Size_Small
            }
        }
        
        expand = {}
        
        ### MOVE REALM CAPITAL BUTTON ###
        button_standard = {
            visible = "[And(Holding.IsCountyCapital, Holding.CanMoveRealmCapital)]"
            text = "MOVE_REALM_CAPITAL"
            onclick = "[Holding.MoveRealmCapital]"
            tooltip = "MOVE_REALM_CAPITAL_TOOLTIP"
        }
    }
    
    divider_light = { layoutpolicy_horizontal = expanding }
}
```

#### SEZIONE 2: Holding Stats

```gui
### HOLDING STATS ###
hbox = {
    name = "holding_stats"
    layoutpolicy_horizontal = expanding
    spacing = 10
    
    ### TAX ###
    vbox = {
        icon = {
            size = { 40 40 }
            texture = "gfx/interface/icons/icon_gold.dds"
        }
        
        text_single = {
            text = "[Holding.GetIncome|1]"
            default_format = "#high"
        }
        
        text_single = {
            text = "TAX_LABEL"
            using = Font_Size_Small
        }
    }
    
    ### LEVIES ###
    vbox = {
        visible = "[Not(Holding.GetType.HasParameter('no_levies'))]"
        
        icon = {
            size = { 40 40 }
            texture = "gfx/interface/icons/icon_soldier.dds"
        }
        
        text_single = {
            text = "[Holding.GetMaxLevySize|0]"
            default_format = "#high"
        }
        
        text_single = {
            text = "LEVIES_LABEL"
            using = Font_Size_Small
        }
    }
    
    ### GARRISON ###
    vbox = {
        icon = {
            size = { 40 40 }
            texture = "gfx/interface/icons/icon_garrison.dds"
        }
        
        text_single = {
            text = "[Holding.GetGarrisonSize|0]"
            default_format = "#high"
        }
        
        text_single = {
            text = "GARRISON_LABEL"
            using = Font_Size_Small
        }
    }
    
    ### SUPPLY LIMIT ###
    vbox = {
        icon = {
            size = { 40 40 }
            texture = "gfx/interface/icons/icon_supply.dds"
        }
        
        text_single = {
            text = "[Holding.GetSupplyLimit|0]"
            default_format = "#high"
        }
        
        text_single = {
            text = "SUPPLY_LABEL"
            using = Font_Size_Small
        }
    }
}
```

#### SEZIONE 3: Special Buildings Slots

```gui
### SPECIAL BUILDINGS ###
hbox = {
    name = "special_buildings"
    visible = "[Or(HoldingView.GetGUIDuchyCapitalBuilding.HasLevel, HoldingView.GetGUISpecialBuilding.HasLevel)]"
    layoutpolicy_horizontal = expanding
    spacing = 10
    margin = { 10 5 }
    
    ### DUCHY CAPITAL BUILDING ###
    button_standard = {
        visible = "[HoldingView.GetGUIDuchyCapitalBuilding.HasLevel]"
        datacontext = "[HoldingView.GetGUIDuchyCapitalBuilding]"
        size = { 80 80 }
        onclick = "[Building.OnClick]"
        tooltip = "[Building.GetTooltip]"
        
        icon = {
            parentanchor = center
            size = { 70 70 }
            texture = "[Building.GetType.GetIcon]"
        }
        
        text_single = {
            parentanchor = bottom|right
            text = "[Building.GetLevel]"
            default_format = "#high"
        }
    }
    
    ### SPECIAL BUILDING ###
    button_standard = {
        visible = "[HoldingView.GetGUISpecialBuilding.HasLevel]"
        datacontext = "[HoldingView.GetGUISpecialBuilding]"
        size = { 80 80 }
        onclick = "[Building.OnClick]"
        tooltip = "[Building.GetTooltip]"
        
        icon = {
            parentanchor = center
            size = { 70 70 }
            texture = "[Building.GetType.GetIcon]"
        }
        
        text_single = {
            parentanchor = bottom|right
            text = "[Building.GetLevel]"
            default_format = "#high"
        }
    }
}
```

#### SEZIONE 4: Buildings Grid

```gui
### BUILDINGS GRID ###
vbox = {
    name = "buildings_grid_section"
    layoutpolicy_horizontal = expanding
    margin = { 10 5 }
    spacing = 5
    
    text_label_center = {
        text = "BUILDINGS_LABEL"
    }
    
    ### GRID 4x2 ###
    gridbox = {
        name = "buildings_grid"
        datamodel = "[HoldingView.GetBuildings]"
        layoutpolicy_horizontal = expanding
        addrow = 90
        addcolumn = 90
        maxverticalslots = 2
        maxhorizontalslots = 4
        
        item = {
            ### BUILDING SLOT ###
            button_standard = {
                size = { 80 80 }
                onclick = "[Building.OnClick]"
                enabled = "[Building.HasLevel]"
                tooltip = "[Building.GetTooltip]"
                
                ### BUILDING ICON ###
                icon = {
                    visible = "[Building.HasLevel]"
                    parentanchor = center
                    size = { 70 70 }
                    texture = "[Building.GetType.GetIcon]"
                }
                
                ### EMPTY SLOT INDICATOR ###
                icon = {
                    visible = "[Not(Building.HasLevel)]"
                    parentanchor = center
                    size = { 70 70 }
                    texture = "gfx/interface/icons/buildings/icon_building_empty.dds"
                    alpha = 0.3
                }
                
                ### LEVEL INDICATOR ###
                text_single = {
                    visible = "[Building.HasLevel]"
                    parentanchor = bottom|right
                    position = { -5 -5 }
                    text = "[Building.GetLevel]"
                    default_format = "#high"
                    fontsize = 18
                }
                
                ### UPGRADE AVAILABLE ###
                icon = {
                    visible = "[Building.CanUpgrade]"
                    parentanchor = top|right
                    size = { 25 25 }
                    texture = "gfx/interface/icons/symbols/icon_upgrade.dds"
                }
                
                ### CONSTRUCTION IN PROGRESS ###
                widget = {
                    visible = "[Building.IsUnderConstruction]"
                    size = { 100% 100% }
                    
                    progressbar_standard = {
                        parentanchor = bottom|hcenter
                        position = { 0 -5 }
                        size = { 70 10 }
                        
                        blockoverride "values" {
                            value = "[FixedPointToFloat(Building.GetConstructionProgress)]"
                            min = 0
                            max = 100
                        }
                    }
                }
            }
        }
    }
    
    divider_light = { layoutpolicy_horizontal = expanding }
    
    ### CONSTRUCT NEW BUILDING BUTTON ###
    button_primary = {
        name = "construct_new_building"
        layoutpolicy_horizontal = expanding
        text = "CONSTRUCT_NEW_BUILDING"
        visible = "[HoldingView.HasEmptyBuildingSlot]"
        enabled = "[HoldingView.CanConstructNewBuilding]"
        onclick = "[HoldingView.OpenConstructionView]"
        tooltip = "[HoldingView.GetConstructionTooltip]"
    }
}
```

#### SEZIONE 5: Siege/Raid Overlays

```gui
### SIEGE OVERLAY ###
widget = {
    name = "siege_overlay"
    visible = "[Province.HasActiveSiege]"
    parentanchor = bottom|hcenter
    position = { 0 -100 }
    size = { 250 100 }
    
    background = {
        using = Background_Area_Dark
        margin = { 5 5 }
    }
    
    vbox = {
        datacontext = "[Province.GetSiege]"
        margin = { 10 10 }
        spacing = 5
        
        text_label_center = {
            text = "SIEGE_IN_PROGRESS"
        }
        
        progressbar_standard = {
            size = { 200 25 }
            
            blockoverride "values" {
                value = "[FixedPointToFloat(Siege.GetProgress)]"
                min = 0
                max = 100
            }
            
            text_single = {
                parentanchor = center
                text = "[Siege.GetProgress|0]%"
            }
        }
        
        text_single = {
            text = "SIEGE_ATTACKER_LABEL"
        }
        
        button_tertiary = {
            text = "GO_TO_SIEGE"
            onclick = "[Siege.GoToSiege]"
        }
    }
}

### RAID OVERLAY ###
widget = {
    name = "raid_overlay"
    visible = "[Province.HasActiveRaid]"
    parentanchor = bottom|hcenter
    position = { 0 -100 }
    size = { 250 80 }
    
    background = {
        using = Background_Area_Dark
        margin = { 5 5 }
    }
    
    vbox = {
        datacontext = "[Province.GetRaid]"
        margin = { 10 10 }
        spacing = 5
        
        text_label_center = {
            text = "RAID_IN_PROGRESS"
        }
        
        hbox = {
            icon = {
                size = { 30 30 }
                texture = "gfx/interface/icons/icon_gold.dds"
            }
            
            text_single = {
                text = "[Raid.GetLootAmount|0]"
                default_format = "#high"
            }
        }
        
        button_tertiary = {
            text = "GO_TO_RAID"
            onclick = "[Raid.GoToRaid]"
        }
    }
}
```

**Checklist Commit 4D/4** (FINALE):
- [ ] Holding illustration background
- [ ] Holding name e type icon
- [ ] Move realm capital button (conditional)
- [ ] Stats icons (Tax/Levies/Garrison/Supply)
- [ ] Special buildings slots (Duchy + Special)
- [ ] Buildings grid 4x2 (8 slots max)
- [ ] Building level indicators
- [ ] Upgrade available icons
- [ ] Construction progress bars
- [ ] Empty slot indicators (alpha 0.3)
- [ ] "Construct New Building" button
- [ ] Siege overlay widget
- [ ] Raid overlay widget
- [ ] Test tutti gli holding types (Castle/City/Temple/Tribal)
- [ ] Test construction system
- [ ] Test upgrade buildings
- [ ] Test siege/raid overlays
- [ ] Verifica chiusura parentesi
- [ ] Test finale multiplayer checksum

**Stima tempo**: ~60 minuti implementazione + 20 minuti testing completo

---

## ✅ STATO COMPLETAMENTO

### Fase 1: Main Windows (11/11) - ✅ 100% COMPLETATO

| # | Finestra | Tasto | File | Pattern | Stato | Data |
|---|----------|-------|------|---------|-------|------|
| 1 | Character | F1 | `window_character.gui` | **A** | ✅ Completato | 04 Dic 2025 |
| 2 | My Realm | F2 | `window_my_realm.gui` | **A** | ✅ Completato | 04 Dic 2025 |
| 3 | Military | F3 | `window_military.gui` | **A** | ✅ Completato | 05 Dic 2025 |
| 4 | Council | F4 | `window_council.gui` | **B** | ✅ Completato | 06 Dic 2025 |
| 5 | Court | F5 | `window_court.gui` | **C** | ✅ Completato | 07 Dic 2025 |
| 6 | Intrigue | F6 | `window_intrigue.gui` | **A** | ✅ Completato | 08 Dic 2025 |
| 7 | Activity | - | `window_activity.gui` | **B** | ✅ Completato | 09 Dic 2025 |
| 8 | Activity List | F9 | `window_activity_list.gui` | **B** | ✅ Completato | 10 Dic 2025 |
| 9 | Decisions | - | `window_decisions.gui` | **C** | ✅ Completato | 10 Dic 2025 |
| 10 | Factions | - | `window_factions.gui` | **B** | ✅ Completato | 11 Dic 2025 |
| 11 | Character Lifestyle | - | `window_character_lifestyle.gui` | **C** | ✅ Completato | 12 Dic 2025 |

### Fase 2: County View System (SUB-COMMITS 4A-4D) - 🔨 25% COMPLETATO

| Step | Descrizione | Stato | Commit SHA | Data |
|------|-------------|-------|------------|------|
| **Phase 1** | Types Definitions (16 types) | ✅ Completato | - | Pre-esistente |
| **Phase 2** | Secondary Windows (2 finestre) | ✅ Completato | - | Pre-esistente |
| **Phase 3** | **Main Window holding_view** | 🔨 **25%** | - | **In corso** |
| ├─ Commit 1/4 | Skeleton and States | ✅ Completato | `deeee...` | 14 Dic 2025 |
| ├─ Commit 2/4 | OCR Widget Content | ✅ Completato | `6842a77` | 14 Dic 2025 |
| ├─ Commit 3/4 | Vanilla Widget Header | ✅ Completato | `675ad46` | 14 Dic 2025 23:52 |
| └─ **Commit 4/4** | **Vanilla Widget Tabs** | 🔨 **25%** | - | **In corso** |
|    ├─ **4A/4** | **County Info Tab** | ✅ **COMPLETATO** | **`7154a16`** | **15 Dic 2025 01:20** |
|    ├─ **4B/4** | **County Stats & Holder** | ⏳ **PROSSIMO** | - | - |
|    ├─ **4C/4** | **Holdings Navigation** | ⏳ Pianificato | - | - |
|    └─ **4D/4** | **Holding Info & Buildings** | ⏳ Pianificato | - | - |

**Progress**: **1/4 sub-commit completati (25%)** - **3 sub-commit rimanenti**

---

## 📊 STATISTICHE PROGETTO (Aggiornate)

| Metrica | Fase 1 | Fase 2 (in corso) | Totale Progetto |
|---------|--------|-------------------|------------------|
| **Finestre completate** | 11/11 (100%) ✅ | Sub 1/4 (25%) 🔨 | In progress |
| **Pattern standardizzati** | 3 (A, B, C) | 1 (D) | 4 |
| **Righe di codice** | ~550,000 | ~13,000 | ~563,000 |
| **File GUI modificati** | 11 | 1 (25% sub-commits) | 12 |
| **Giorni sviluppo** | 9 giorni | 1 giorno | 10 giorni |
| **Ore lavoro stimate** | 40+ ore | 8+ ore | **48+ ore** |
| **Commit totali** | 11 | 4 (+ 1 sub) | **15 + 1 sub** |
| **Repository GitHub** | 1 attivo | 1 attivo | 1 |
| **Data inizio** | 04 Dic 2025 | 14 Dic 2025 | 04 Dic 2025 |
| **Data completamento** | 12 Dic 2025 | **In corso** | **In corso** |
| **Progress totale** | 100% | **25% (sub)** | **In progress** |

---

## 🚀 GUIDA RAPIDA PER NUOVE SESSIONI

### Incollare in nuova chat
```
Ciao! Riprendo il progetto OCR Support Fix per Crusader Kings 3.

Stato attuale:
- Fase 1: 11/11 finestre completate (100% ✅)
- Fase 2: County View System (25% sub-commits completato)
  - Phase 1: Types ✅
  - Phase 2: Secondary Windows ✅
  - Phase 3: Main Window 🔨 (Commit 4/4 suddiviso in 4A-4D)
    - Commit 1/4: Skeleton ✅
    - Commit 2/4: OCR Widget ✅
    - Commit 3/4: Vanilla Header ✅
    - Commit 4A/4: County Info Tab ✅ (appena completato 15 Dic 01:20)
    - Commit 4B/4: County Stats & Holder ⏳ (PROSSIMO)
    - Commit 4C/4: Holdings Navigation ⏳
    - Commit 4D/4: Holding Info & Buildings ⏳ (FINALE)

Repository: https://github.com/Nemex81/ocr-support-patch
Compatibile: CK3 v1.17.1, OCR Support v4.2

[Incolla QUESTO DOCUMENTO completo]

Prossimo step: Commit 4B/4 - County Stats & Holder Portrait
Accedi al file window_county_view.gui e aggiungi:
- Holder portrait section
- Control level bar
- Development level bar
- County opinion
- Culture & Faith section

File corrente: ~13 KB (~150 righe da Commit 4A/4)
Target Commit 4B/4: ~18 KB (~500 righe aggiunte)
```

### Informazioni critiche da fornire sempre
1. **Nome finestra** (es. `window_county_view.gui`)
2. **Sub-commit corrente** ("Commit 4B/4 - County Stats & Holder")
3. **Pattern identificato** (D - County View Bottom-Up)
4. **Comportamento** (aggiungere stats e portrait holder)
5. **SHA file corrente** (`0a243fde4e859095b9c2cf0dd3bcad5ad36ae030`)
6. **Checklist implementazione** (vedi sezione pianificazione Commit 4B/4 sopra)

---

## 🔗 RISORSE UTILI

| Risorsa | Link |
|---------|------|
| **Mod OCR Support** | https://github.com/Agamidae/CK3-OCR |
| **Compatibility Patch** | https://github.com/Nemex81/ocr-support-patch |
| **File County View (OCR)** | https://github.com/Agamidae/CK3-OCR/blob/main/OCR-Support/gui/window_county_view.gui |
| **Commit 4A/4 su GitHub** | https://github.com/Nemex81/ocr-support-patch/commit/7154a1617e0d3d8e5686964b7538a810963ea8f9 |
| **CK3 Modding Wiki** | https://ck3.paradoxwikis.com/Modding |
| **NVDA Screen Reader** | https://www.nvaccess.org/ |
| **AutoHotkey** | https://www.autohotkey.com/docs/ |
| **Steam Workshop OCR Support** | https://steamcommunity.com/sharedfiles/filedetails/?id=2848213069 |

---

## ✨ CONCLUSIONE

Questo progetto rappresenta un importante passo avanti nell'accessibilità dei videogiochi strategy. 

**Il sistema dual-mode consente**:
- ✅ Giocatori ciechi di giocare con interfaccia testuale ottimizzata per screen reader
- ✅ Giocatori vedenti di giocare con interfaccia grafica vanilla completa
- ✅ Multiplayer misto con checksum identico
- ✅ Switch runtime senza restart del gioco
- ✅ Compatibilità totale con il resto della mod OCR Support

**I 4 pattern standardizzati** (A, B, C, D) forniscono un framework riutilizzabile per futuri fix o espansioni della mod.

**Fase 2 County View** introduce:
- ✅ Approccio bottom-up per sistemi complessi
- ✅ Sviluppo incrementale testabile con sub-commits
- ✅ Separazione Types/Secondary/Main Windows
- ✅ 4-sub-commit strategy per completare vanilla tabs (~1800 righe)
- 🔨 **25% completato (Commit 4A/4) - 3 sub-commit rimanenti**

---

**Documento compilato da**: Luca "Nemex81"  
**Ultima modifica**: 15 Dicembre 2025, 01:22 CET  
**Versione**: 3.3 - FASE 2 SUB-COMMIT 4A/4 COMPLETATO  
**Status**: 🔨 IN DEVELOPMENT - **COMMIT 4B/4 NEXT (County Stats & Holder)**