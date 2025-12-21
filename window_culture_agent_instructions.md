# ocr-support-patch
patch di compatibilità pe rocr support, mod dedicata a crusader king 3

---
## Obiettivo
Implementare `OCR-Support/gui/window_culture.gui` in modalità duale (OCR vs normo-vedente), mantenendo checksum identico e compatibilità multiplayer. Modalità OCR: codice originale OCR Support **immutato**. Modalità vedente: UI grafica completa con 5 tab mantenendo **tutta la funzionalità e grafica** di entrambe le modalità senza compromessi.

# **Piano di Implementazione Completo: Supporto OCR Dual-Mode per window_culture.gui**

**Repository**: `Nemex81/ocr-support-patch`  
**Branch**: `main`  
**File**: `ocr-support/compatibility-pach/gui/window_culture.gui`  
**riferimenti files originali**: 
`ocr-support/compatibility-pach/gui/placeorders/window_culture_ocr_support_originale.md`  
`ocr-support/compatibility-pach/gui/placeorders/window_culture_vanilla_originale.md`  

***

## **PRINCIPI FONDAMENTALI**

### **Regola d'Oro della Separazione**
```
SE componente ha grafica/animazioni/texture → Types SEPARATI (OCR vs Vanilla)
SE componente è solo logica/dati → CONDIVISO (datacontext, datamodel, tooltip)
```

### **Architettura Dual-Mode**
- **Window principale**: Contiene datacontext, states, properties comuni
- **Widget OCR**: Rendering testuale, accessibile, lineare
- **Widget Vanilla**: Rendering grafico completo con texture, animazioni, effetti
- **Types separati**: OCR types vs Vanilla types
- **Logica condivisa**: Datamodel, tooltip, actions, scripted_gui

***

## **1. STRUTTURA WINDOW PRINCIPALE**

Il window principale funge da **container comune** per entrambe le modalità:

```gui
window name="culturewindow" {
  widgetid="culturewindow"
  layer="windows_layer"
  movable=no
  using="base_ocr_window"
  
  # === DATACONTEXT COMUNI (definiti UNA SOLA VOLTA) ===
  datacontext="CultureWindow.GetCulture()"
  datacontext="Culture.GetReformation()"
  
  # === STATES COMUNI (definiti UNA SOLA VOLTA) ===
  state name="show" {
    using="AnimationFadeInQuick"
    using="SoundWindowShowStandard"
    position={ 0 0 }
    onstart="[GetVariableSystem.Set('culture_tab', 'early')]"
    onstart="[GetVariableSystem.Set('hidebottom_left_HUD', true)]"
    onstart="[GetVariableSystem.Set('culture_view_tabs', 'overview')]"
    onstart="[CultureWindow.HideReformationMode()]"
    onfinish="[GetScriptedGui('culture_closest_county_ocr').Execute(GuiScope.SetRoot(Culture.MakeScope()).AddScope('player', GetPlayer.MakeScope()).End())]"
  }
  
  state name="hide" {
    using="AnimationFadeOutQuick"
    using="SoundWindowHideStandard"
    position={ -90 0 }
    onstart="[GetVariableSystem.Clear('hidebottom_left_HUD')]"
  }
  
  # I widget figli ereditano automaticamente datacontext e states
  # NON ridefinirli nei widget OCR o Vanilla
}
```

**❌ ERRORE da evitare**: Ridefinire datacontext/states nei widget figli  
**✅ CORRETTO**: Definire una sola volta nel parent, i figli ereditano

***

## **2. MODALITÀ NON VEDENTI (OCR MODE)**

**Condizione di visibilità**: `visible="[Not(GetVariableSystem.Exists('ocr'))]"`

### **2.1 Container OCR**

```gui
window_ocr visible="[Not(GetVariableSystem.Exists('ocr'))]" {
  
  blockoverride "ocr_header" {
    header_pattern {
      layoutpolicy_horizontal=expanding
      
      blockoverride "header_text" {
        text="CULTUREWINDOW_CULTURE"
      }
      
      blockoverride "button_close" {
        onclick="[CultureWindow.Close()]"
      }
      
      blockoverride "button_back" {
        visible="[HasViewHistory]"
        onclick="[OpenFromViewHistory()]"
        tooltip="[GetViewHistoryTooltip]"
        size={ 0 0 }  # Nascosto ma funzionante
      }
      
      blockoverride "button_me" {
        onclick="[DefaultOnCharacterClick(GetPlayer.GetID())]"
        size={ 0 0 }
      }
      
      # Titolo cultura + contesto
      flowcontainer {
        ignoreinvisible=yes
        spacing=3
        
        text_single { rawtext="CULTUREWINDOW_CULTURE, " }
        text_single { 
          visible="[Has('culture_view_tabs', 'overview')]"
          rawtext="[Culture.GetHeritage().GetNameNoTooltip()], "
        }
        text_single { 
          visible="[Not(ObjectsEqual(Culture.Self, GetPlayer.GetCulture()))]"
          rawtext="[Culture.GetAcceptance(GetPlayer.GetCulture())('0V')], "
        }
        text_single { rawtext="[Get('culture_view_tabs')] tab." }
      }
    }
  }
  
  blockoverride "ocr_content" {
    vbox {
      layoutpolicy_horizontal=expanding
      layoutpolicy_vertical=expanding
      # Contenuto OCR qui (vedi sezioni successive)
    }
  }
}
```

### **2.2 Sistema di Tabs OCR**

**5 Tabs funzionali con hotkeys Speed1-5**:

```gui
hbox name="tabs" {
  layoutpolicy_horizontal=expanding
  margintop=10
  visible="[Not(CultureWindow.IsInReformationMode())]"
  
  text_single { rawtext="Tabs:" }
  
  # Tab 1: Overview
  button_text {
    shortcut="speed1"
    blockoverride "text" { rawtext="Overview," }
    blockoverride "pre" { text_single { rawtext="1," } }
    onclick="[GetVariableSystem.Set('culture_view_tabs', 'overview')]"
    onclick="[CultureWindow.HideReformationMode()]"
  }
  
  # Tab 2: Innovations
  button_text {
    shortcut="speed2"
    name="innovations_tab_tutorial_uses_this"
    blockoverride "text" { rawtext="2, Innovations," }
    onclick="[GetVariableSystem.Set('culture_view_tabs', 'innovations')]"
    onclick="[CultureWindow.HideReformationMode()]"
  }
  
  # Tab 3: All Cultures
  button_text {
    shortcut="speed3"
    blockoverride "text" { rawtext="3, all cultures." }
    onclick="[GetVariableSystem.Set('culture_view_tabs', 'other cultures')]"
    onclick="[Click('add_culture_list', GetPlayer, Culture)]"
    onclick="[CultureWindow.HideReformationMode()]"
  }
  
  # Tab 4: Counties
  button_text {
    shortcut="speed4"
    blockoverride "text" { rawtext="4, counties." }
    onclick="[GetVariableSystem.Set('culture_view_tabs', 'counties')]"
    onclick="[Click('add_culture_counties_list', GetPlayer, Culture)]"
    onclick="[CultureWindow.HideReformationMode()]"
  }
  
  # Tab 5: Rulers
  button_text {
    shortcut="speed5"
    blockoverride "text" { rawtext="5, rulers." }
    onclick="[GetVariableSystem.Set('culture_view_tabs', 'rulers')]"
    onclick="[Click('add_culture_characters_list', GetPlayer, Culture)]"
    onclick="[CultureWindow.HideReformationMode()]"
  }
  
  expand={}
}
```

### **2.3 Tab Content OCR**

#### **A. Overview Tab**
```gui
vbox visible="[And(Not(CultureWindow.IsInReformationMode()), Has('culture_view_tabs', 'overview'))]" {
  layoutpolicy_horizontal=expanding
  
  # Closest county button
  button_text {
    layoutpolicy_horizontal=expanding
    using="prov_click"
    datacontext="Culture.MakeScope().Var('closest_county')"
    visible="[And(Scope.IsSet, Not(ObjectsEqual(Culture.Self, GetPlayer.GetCulture())))]"
    datacontext="Scope.Title.GetCountyData.GetCapital"
    datacontext="Scope.Title"
    
    blockoverride "extra" {
      text_distance_capital={}
      text_single { 
        rawtext="Closest county: [Title.GetNameNoTierNoTooltip()],"
      }
      text_single {
        visible="[Not(ObjectsEqual(Title.Self, Title.GetHolder.GetTopLiege.GetPrimaryTitle))]"
        rawtext="in [Title.GetHolder.GetTopLiege.GetPrimaryTitle.GetNameNoTierNoTooltip()]."
      }
    }
  }
  
  # Culture counties button
  button_text {
    layoutpolicy_horizontal=expanding
    shortcut="characterfinder"
    onclick="[Set('culture_view_tabs', 'counties')]"
    onclick="[Click('add_culture_counties_list', GetPlayer, Culture)]"
    
    blockoverride "extra" {
      text_single {
        rawtext="[Culture.MakeScope().ScriptValue('culture_counties')] [Culture.GetNameNoTooltip()] counties,"
      }
      text_single {
        layoutpolicy_horizontal=expanding
        rawtext="[Culture.MakeScope().ScriptValue('culture_held_by_enemies')] held by foreigners,"
      }
      text_single { rawtext="C." }
    }
  }
  
  # Wrong counties button
  button_text {
    layoutpolicy_horizontal=expanding
    shortcut="courtscene_editor_tool_set_translate"
    onclick="[GetScriptedGui('culture_holders_wrong_counties').Execute(...)]"
    onclick="[Set('culture_view_tabs', 'counties of other cultures')]"
    
    blockoverride "extra" {
      text_single {
        rawtext="[Culture.MakeScope().ScriptValue('culture_rulers')] rulers,"
      }
      text_single {
        rawtext="holding [Culture.MakeScope().ScriptValue('culture_holders_wrong_counties')] counties of other cultures"
      }
      text_single {
        visible="[GreaterThan_CFixedPoint(Culture.MakeScope().ScriptValue('culture_holders_wrong_counties'), CFixedPoint('0'))]"
        rawtext="and converting [Culture.MakeScope().ScriptValue('culture_holders_convert_counties')],"
      }
      text_single { rawtext="W." }
    }
  }
  
  # Pillars section (usa type OCR separato)
  vbox_locr_culture_desc={}
  
  # Traditions section
  # Culture head section
  # Action buttons (Reform, Diverge, Hybridize)
}
```

#### **B. Innovations Tab**
```gui
vbox visible="[GetVariableSystem.HasValue('culture_view_tabs', 'innovations')]" {
  layoutpolicy_horizontal=expanding
  layoutpolicy_vertical=expanding
  using="AnimationTabSwitch"
  
  # Era selection (usa type OCR separato)
  vbox {
    layoutpolicy_horizontal=expanding
    datamodel="[CultureWindow.GetCultureEras()]"
    visible="[Not(Is('all_eras'))]"
    
    item = {
      vbox_era_tab_ocr {  # ← Type OCR specifico
        visible="[GuiCultureEra.IsSelected()]"
      }
    }
  }
  
  # Show/Hide all eras button
  button_text {
    layoutpolicy_horizontal=expanding
    shortcut="mapmode1"
    onclick="[Toggle('all_eras')]"
    blockoverride "text" {
      rawtext="[SelectCString(Is('all_eras'), 'Hide', 'Show')] all eras, E."
    }
  }
  
  # Selected era innovations
  scrollbox {
    datacontext="CultureWindow.GetSelectedCultureEra()"
    layoutpolicy_horizontal=expanding
    layoutpolicy_vertical=expanding
    
    blockoverride "scrollbox_content" {
      vbox {
        datacontext="GuiCultureEra.GetCultureEra()"
        layoutpolicy_horizontal=expanding
        
        # Era groups con innovations (usa type OCR separato)
        vbox name="era_groups" {
          datamodel="[GuiCultureEra.GetCultureEraGroups()]"
          layoutpolicy_horizontal=expanding
          
          item = {
            vbox {
              visible="[GuiCultureEraGroup.HasInnovations()]"
              layoutpolicy_horizontal=expanding
              
              text_single {
                layoutpolicy_horizontal=expanding
                rawtext="[GuiCultureEraGroup.GetName()], [GetDataModelSize(GuiCultureEraGroup.GetInnovations())]."
              }
              
              # Innovations list (usa type OCR separato)
              dynamicgridbox {
                layoutpolicy_horizontal=expanding
                datamodel="[GuiCultureEraGroup.GetInnovations()]"
                
                item = {
                  flowcontainer_innovation {  # ← Type OCR specifico
                    visible="[Or(Is('nt_hide_discovered'), And(Is('hide_discovered'), Not(CultureInnovation.IsActive())))]"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

#### **C. Other Tabs (Cultures, Counties, Rulers)**
```gui
# Implementazione simile con fixedgridbox/dynamicgridbox
# Usa button_text OCR per ogni item
# Include sorting, filtering, pagination
```

***

## **3. MODALITÀ NORMO VEDENTI (VANILLA MODE)**

**Condizione di visibilità**: `visible="[GetVariableSystem.Exists('ocr')]"`

### **3.1 Container Vanilla**

```gui
margin_widget visible="[GetVariableSystem.Exists('ocr')]" {
  using="Window_Margins_Sidebar"
  
  header_pattern {
    layoutpolicy_horizontal=expanding
    
    blockoverride "header_text" {
      text="CULTUREWINDOW_CULTURE"
    }
    
    blockoverride "button_close" {
      onclick="[CultureWindow.Close()]"
    }
    
    blockoverride "button_back" {
      visible="[HasViewHistory]"
      onclick="[OpenFromViewHistory()]"
      tooltip="[GetViewHistoryTooltip]"
    }
    
    blockoverride "button_me" {
      onclick="[DefaultOnCharacterClick(GetPlayer.GetID())]"
    }
  }
  
  # Watch window button
  watch_window_button {
    size={ 60 40 }
    onclick="[AddWatchWindow(Culture.MakeScope())]"
  }
  
  # Acceptance widget (top-right)
  widget {
    layoutpolicy_horizontal=expanding
    size={ 0 48 }
    
    vbox name="acceptance" {
      visible="[Not(ObjectsEqual(Culture.Self, GetPlayer.GetCulture()))]"
      spacing=2
      marginleft=450
      marginright=10
      
      text_single name="acceptance_text" {
        layoutpolicy_horizontal=expanding
        text="CULTUREVIEW_ACCEPTANCE"
        align=right
        autoresize=no
        tooltip="CULTURE_ACCEPTANCE_TOOLTIP"
      }
      
      text_single {
        visible="[NotEqualTo_CFixedPoint(Culture.GetAcceptanceDiff(GetPlayer.GetCulture()), CFixedPoint('0'))]"
        layoutpolicy_horizontal=expanding
        text="CULTUREVIEW_ACCEPTANCE_DIFF"
        align=right
        autoresize=no
        tooltip="CULTURE_ACCEPTANCE_TOOLTIP"
      }
      
      expand={}
    }
  }
  
  # Who's culture text
  hbox name="whos_culture" {
    margintop=5
    
    vbox {
      layoutpolicy_vertical=expanding
      
      textlabelcenter {
        text="[Culture.GetPlayerRelationString()]"
        defaultformat="low"
      }
      
      text_single {
        text="[Culture.GetCreationString()]"
        maxwidth=490
      }
    }
  }
}
```

### **3.2 Tab System Vanilla**

```gui
hbox name="tabs" {
  layoutpolicy_horizontal=expanding
  margintop=10
  
  # Tab 1: Overview
  button_tab {
    shortcut="speed1"
    layoutpolicy_horizontal=expanding
    onclick="[GetVariableSystem.Set('culture_view_tabs', 'overview')]"
    onclick="[CultureWindow.HideReformationMode()]"
    down="[GetVariableSystem.HasValue('culture_view_tabs', 'overview')]"
    
    text_single {
      parentanchor=center
      text="CULTUREVIEW_OVERVIEW"
      maximumsize={ 400 -1 }
      defaultformat="low"
    }
  }
  
  # Tab 2: Innovations
  button_tab {
    shortcut="speed2"
    name="innovations_tab_tutorial_uses_this"
    layoutpolicy_horizontal=expanding
    onclick="[GetVariableSystem.Set('culture_view_tabs', 'innovations')]"
    onclick="[CultureWindow.HideReformationMode()]"
    down="[GetVariableSystem.HasValue('culture_view_tabs', 'innovations')]"
    
    text_single {
      parentanchor=center
      text="CULTUREVIEW_INNOVATIONS"
      maximumsize={ 400 -1 }
      defaultformat="low"
    }
  }
  
  # Tabs 3-5 non implementate in vanilla originale
}
```

### **3.3 Content Sections Vanilla**

#### **A. Overview Tab**
```gui
vbox name="traditions_and_pillars_tab_tutorial_uses_this" {
  visible="[GetVariableSystem.HasValue('culture_view_tabs', 'overview')]"
  layoutpolicy_horizontal=expanding
  layoutpolicy_vertical=expanding
  using="AnimationTabSwitch"
  
  # Ethos pillar (usa type Vanilla completo con grafica)
  containerpillaritem {  # ← Type Vanilla con highlighticon 592x130
    datacontext="Culture.GetEthos()"
    blockoverride "iconsize" {
      size={ 400 100 }
    }
  }
  
  # Reform button (se reformation mode)
  button_round {
    visible="[CultureWindow.IsInReformationMode()]"
    parentanchor=bottomright
    onclick="[Culture.OpenReplaceEthosWindow()]"
    position={ -8 -8 }
    tooltip="CULTURE_CLICK_TO_REPLACE"
  }
  
  button_change {
    alwaystransparent=yes
    parentanchor=center
  }
  
  # Pillars section
  vbox {
    layoutpolicy_horizontal=expanding
    
    textlabelleft {
      layoutpolicy_horizontal=expanding
      margin={ 10 6 }
      text="culture_pillars"
      defaultformat="low"
      align=nobaseline
    }
    
    # Cultural pillars block con icone grafiche
    hbox name="cultural_pillars_block" {
      layoutpolicy_horizontal=expanding
      layoutpolicy_vertical=expanding
      maximumsize={ 594 104 }
      
      # Column 1: Heritage + Martial
      widget name="cultural_pillars_collumn_one" {
        layoutpolicy_horizontal=expanding
        
        vbox {
          marginleft=10
          
          # Heritage con icon 44x44
          hbox name="heritage" {
            datacontext="Culture.GetHeritage()"
            layoutpolicy_horizontal=expanding
            
            hbox {
              spacing=10
              tooltipwidget={ using=culture_pillar_tooltip }
              
              icon_doctrine {
                visible="[ObjectsEqual(Culture.GetHeritage(), GetPlayer.GetCulture().GetHeritage())]"
                size={ 44 44 }
                texture="gfx/interface/icons/culture_pillars/heritage.dds"
              }
              
              icon_doctrine {
                visible="[Not(ObjectsEqual(Culture.GetHeritage(), GetPlayer.GetCulture().GetHeritage()))]"
                size={ 44 44 }
                texture="gfx/interface/icons/culture_pillars/heritage_diverge.dds"
              }
              
              textmulti {
                datacontext="Culture.GetHeritage()"
                layoutpolicy_horizontal=expanding
                maxwidth=210
                text="[CulturePillar.GetName()]"
                defaultformat="high"
              }
            }
          }
          
          # Martial custom (se DLC)
          hbox name="martial_custom" {
            datacontext="Culture.GetMartialCustom()"
            layoutpolicy_horizontal=expanding
            visible="[HasDlcFeature('dlc_fp1_feature_martial_custom')]"
            
            hbox {
              spacing=10
              tooltipwidget={ using=culture_pillar_tooltip }
              
              icon_doctrine {
                size={ 44 44 }
                texture="gfx/interface/icons/culture_pillars/martial_custom.dds"
              }
              
              textmulti {
                layoutpolicy_horizontal=expanding
                maxwidth=210
                text="[CulturePillar.GetName()]"
                defaultformat="high"
              }
            }
          }
        }
      }
      
      # Column 2: Language + Aesthetics
      widget name="cultural_pillars_collumn_two" {
        layoutpolicy_horizontal=expanding
        layoutpolicy_vertical=expanding
        
        vbox {
          marginleft=10
          
          # Language (se DLC)
          hbox name="language" {
            datacontext="Culture.GetCourtLanguage()"
            layoutpolicy_horizontal=expanding
            visible="[HasDlcFeature('dlc_fp1_feature_court_language')]"
            
            hbox {
              spacing=10
              tooltipwidget={ using=culture_pillar_tooltip }
              
              icon_culture_pillar {
                size={ 44 44 }
                texture="gfx/interface/icons/flat_icons/map_modes/court_languages.dds"
              }
              
              textmulti {
                layoutpolicy_horizontal=expanding
                maxwidth=210
                text="[CulturePillar.GetName()]"
                defaultformat="high"
              }
            }
          }
          
          # Aesthetics
          hbox name="aesthetics" {
            datacontext="Culture.GetAesthetics()"
            layoutpolicy_horizontal=expanding
            
            hbox {
              spacing=10
              tooltipwidget={ using=culture_pillar_tooltip }
              
              icon_culture_pillar {
                size={ 44 44 }
                texture="gfx/interface/icons/culture_pillars/aesthetics.dds"
              }
              
              textmulti {
                layoutpolicy_horizontal=expanding
                maxwidth=210
                text="[CulturePillar.GetName()]"
                defaultformat="high"
              }
            }
          }
        }
      }
    }
  }
  
  # Traditions section con layered icons
  textlabelleft {
    layoutpolicy_horizontal=expanding
    margin={ 10 6 }
    text="traditions"
    defaultformat="low"
    align=nobaseline
  }
  
  # Traditions grid 2x con widget_tradition_icon (5 layers)
  dynamicgridbox name="traditions_grid" {
    datamodel="[Culture.GetTraditions()]"
    datamodelwrap=2
    layoutpolicy_horizontal=expanding
    layoutpolicy_vertical=expanding
    flipdirection=yes
    
    item = {
      widget {
        layoutpolicy_horizontal=expanding
        layoutpolicy_vertical=expanding
        size={ 276 158 }
        
        background {
          using="MaskRoughEdges"
          alpha=0.9
          texture="[CultureTradition.GetLayeredIcon().GetTexture(int32('0'))]"
        }
        
        widget_tradition_icon {  # ← Type Vanilla con 5 layers grafiche
          parentanchor=center
          size={ 276 138 }
        }
        
        textlabelcenter {
          parentanchor=bottomhcenter
          marginbottom=4
          text="[CultureTradition.GetNameNoTooltip()]"
          defaultformat="high"
        }
      }
    }
  }
  
  # Action buttons
  hbox {
    layoutpolicy_horizontal=expanding
    margintop=10
    spacing=10
    
    button_standard {
      text="CULTUREWINDOW_HYBRIDIZE"
      onclick="[CultureWindow.OpenHybridizeCultureWindow()]"
      visible="[GetPlayer.GetCulture().CanHybridize()]"
    }
    
    button_standard {
      text="CULTUREWINDOW_ADD_TRADITION"
      onclick="[CultureWindow.OpenAddTraditionWindow()]"
      visible="[Culture.CanAdoptNewTradition()]"
    }
    
    button_standard {
      text="CULTUREWINDOW_REFORM"
      onclick="[CultureWindow.ShowReformationMode()]"
      visible="[Culture.CanReform()]"
    }
    
    button_standard {
      text="CULTUREWINDOW_DIVERGE"
      onclick="[CultureWindow.OpenDivergeCultureWindow()]"
      visible="[GetPlayer.GetCulture().CanDiverge()]"
    }
  }
  
  # Culture head section con portrait_shoulders + fascination
  hbox name="culture_head_block" {
    datacontext="CultureWindow.GetCulture()"
    layoutpolicy_horizontal=expanding
    margintop=10
    spacing=10
    
    portrait_shoulders {
      size={ 120 200 }
      datacontext="Culture.GetCultureHead()"
    }
    
    vbox {
      layoutpolicy_horizontal=expanding
      
      textlabelleft {
        text="CULTUREWINDOW_CULTURE_HEAD"
      }
      
      # Fascination con iconinnovation (shimmer effect)
      hbox {
        datacontext="Culture.GetFascination()"
        visible="[Culture.HasFascination()]"
        layoutpolicy_horizontal=expanding
        spacing=8
        
        iconinnovation {  # ← Type Vanilla con animazioni shimmer/glow
          size={ 90 60 }
          tooltipwidget={ using=culture_innovation_tooltip }
        }
        
        vbox {
          text_single {
            text="CULTUREWINDOW_HEAD_FASCINATION"
          }
          
          hbox {
            layoutpolicy_horizontal=expanding
            
            skilliconlabel {
              datacontext="CultureWindow.GetLearningLevel()"
            }
            
            expand={}
          }
        }
      }
    }
  }
}
```

#### **B. Innovations Tab**
```gui
vbox name="innovations_area_tutorial_uses_this" {
  widgetid="innovations_area_tutorial_uses_this"
  visible="[GetVariableSystem.HasValue('culture_view_tabs', 'innovations')]"
  layoutpolicy_horizontal=expanding
  layoutpolicy_vertical=expanding
  using="AnimationTabSwitch"
  
  vbox {
    layoutpolicy_horizontal=expanding
    margin={ 0 10 }
    
    textlabelcenter {
      text="CULTUREWINDOW_INNOVATIONS"
      using="FontSizeMedium"
    }
  }
  
  # Visual era tabs con illustrations
  hbox {
    layoutpolicy_horizontal=expanding
    margin={ 5 5 }
    background={ using="BackgroundAreaDark" }
    datamodel="[CultureWindow.GetCultureEras()]"
    
    item = {
      vbox_era_tab={}  # ← Type Vanilla con texture illustrations + animations
    }
  }
  
  # Selected era scrollbox
  scrollbox name="selected_culture_era" {
    datacontext="CultureWindow.GetSelectedCultureEra()"
    layoutpolicy_horizontal=expanding
    layoutpolicy_vertical=expanding
    
    blockoverride "scrollbox_content" {
      vbox {
        datacontext="GuiCultureEra.GetCultureEra()"
        layoutpolicy_horizontal=expanding
        spacing=10
        
        state name="culture_refresh" {
          using="AnimationRefreshFadeOut"
        }
        state {
          using="AnimationRefreshFadeIn"
        }
        
        # Era groups
        vbox name="era_groups" {
          datamodel="[GuiCultureEra.GetCultureEraGroups()]"
          layoutpolicy_horizontal=expanding
          spacing=30
          
          item = {
            vbox {
              visible="[GuiCultureEraGroup.HasInnovations()]"
              layoutpolicy_horizontal=expanding
              spacing=10
              
              textlabelleft {
                layoutpolicy_horizontal=expanding
                align=left
                margin={ 0 3 }
                text="[GuiCultureEraGroup.GetName()]"
              }
              
              # Innovations grid con iconinnovation (grafiche complete)
              dynamicgridbox {
                datamodel="[GuiCultureEraGroup.GetInnovations()]"
                datamodelwrap=2
                flipdirection=yes
                
                item = {
                  flowcontainer {
                    margintop=10
                    marginright=45
                    
                    # Widget grafico cliccabile
                    button_standard_hover {
                      visible="[And(CultureInnovation.GetCulture().IsPlayerCultureHead(), Not(CultureInnovation.IsActive()))]"
                      enabled="[CultureInnovation.CanBeFascination()]"
                      size={ 256 66 }
                      onclick="[CultureInnovation.SelectAsFascination()]"
                      
                      hbox {
                        margin={ 3 3 }
                        marginright=8
                        spacing=5
                        allowoutside=yes
                        ignoreinvisible=yes
                        
                        background={ using="BackgroundArea" }
                        
                        widget {
                          size={ 90 60 }
                          
                          iconinnovation {  # ← Type Vanilla con shimmer/glow
                            parentanchor=center
                          }
                        }
                        
                        widget {
                          size={ 150 60 }
                          alwaystransparent=yes
                          
                          vbox {
                            position={ 0 -1 }
                            ignoreinvisible=yes
                            
                            textmulti name="name_clickable" {
                              visible="[CultureInnovation.CanBeFascination()]"
                              layoutpolicy_horizontal=expanding
                              text="[CultureInnovation.GetNameNoTooltip()]"
                              align=nobaseline
                              margin={ 3 0 }
                              defaultformat="clickable"
                            }
                            
                            textmulti name="name_unlocked" {
                              visible="[CultureInnovation.IsActive()]"
                              layoutpolicy_horizontal=expanding
                              text="[CultureInnovation.GetNameNoTooltip()]"
                              maxwidth=150
                              align=nobaseline
                              margin={ 3 0 }
                              defaultformat="P"
                              alpha=0.7
                            }
                            
                            textmulti name="name_blocked" {
                              visible="[And(Not(CultureInnovation.CanBeFascination()), Not(CultureInnovation.IsActive()))]"
                              layoutpolicy_horizontal=expanding
                              text="[CultureInnovation.GetNameNoTooltip()]"
                              maxwidth=150
                              align=nobaseline
                              margin={ 3 0 }
                              defaultformat="low"
                            }
                            
                            # Progress bar grafica
                            hbox {
                              visible="[And(CultureInnovation.CanGainProgress(), Not(CultureInnovation.IsActive()))]"
                              layoutpolicy_horizontal=expanding
                              margin={ 3 0 }
                              
                              progressbar_standard {
                                value="[FixedPointToFloat(CultureInnovation.GetProgress())]"
                                layoutpolicy_horizontal=expanding
                                size={ 90 15 }
                                min=0
                                max=100
                              }
                            }
                          }
                        }
                      }
                    }
                    
                    # Gray overlay se non disponibile
                    background name="gray_overlay" {
                      visible="[GuiCultureEra.GetCultureEra().GetType().IsInvalidForPlayerGovernment()]"
                      using="BackgroundAreaBorderSolid"
                      tintcolor={ 0.5 0.5 0.5 0.3 }
                      alwaystransparent=no
                      margin={ 10 10 }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

***

## **4. TYPES: Separazione Completa OCR vs Vanilla**

### **4.1 Types OCR (Testuali)**

```gui
types OCR {
  
  # Era tab OCR - Testuale
  type vbox_era_tab_ocr = hbox {
    datacontext="GuiCultureEra.GetCultureEra()"
    layoutpolicy_horizontal=expanding
    using="tooltipse"
    
    button_text {
      layoutpolicy_horizontal=expanding
      
      state name="mouse_click" {
        onfinish="[GuiCultureEra.Select()]"
        onclick="[Clear('all_eras')]"
        onclick="[PdxGuiTriggerAllAnimations('culture_refresh')]"
      }
      
      blockoverride "pre" {
        text_single {
          rawtext="Showing"
          visible="[GuiCultureEra.IsSelected()]"
        }
      }
      
      blockoverride "text" {
        rawtext="[CultureEra.GetNameNoTooltip()]"
        align=left
      }
      
      blockoverride "extra" {
        text_single { rawtext="era," }
        text_single {
          rawtext="[CultureEra.GetNumberOfActiveInnovations()] out of [CultureEra.GetNumberOfInnovations()]"
        }
        text_single { rawtext="innovations discovered." }
        text_single { rawtext="Tooltip." }
      }
    }
    
    tooltipwidget={ using=culture_era_tooltip }
  }
  
  # Pillar OCR - Testuale
  type containerpillaritemocr = hbox {
    using="tooltipws"
    tooltipwidget={ using=culture_pillar_tooltip }
    
    hbox {
      marginbottom=5
      spacing=3
      layoutpolicy_horizontal=expanding
      
      block "reform" {}
      
      text_single name="name" {
        rawtext="[CulturePillar.GetNameNoTooltip()], ethos."
      }
      
      # Progress bar (condiviso)
      hbox {
        layoutpolicy_horizontal=expanding
        spacing=3
        visible="[And(CultureReformation.IsReformingSamePillarTypeAs(Culture.GetEthos()), Not(CultureWindow.IsInReformationMode()))]"
        tooltipwidget={ using=culture_pillar_tooltip_establishing }
        
        text_single {
          text="REFORM_ETHOS_NEW_NAME"
          align=left
        }
        text_single {
          text="REFORMATION_NEW_TRADITION_INFO"
          align=left
        }
        progressbar_reform {
          blockoverride "progressbar_reform_size" {
            size={ 200 14 }
          }
        }
      }
      
      expand={}
    }
  }
  
  # Innovation OCR - Testuale
  type flowcontainer_innovation = flowcontainer {
    datacontext="GuiCultureInnovation.GetCultureInnovation()"
    direction=horizontal
    allowoutside=yes
    using="tooltipes"
    ignoreinvisible=yes
    tooltipwidget={ using=culture_innovation_tooltip }
    
    # Widget testuale NON cliccabile per lettura
    widget {
      size={ 560 22 }
      
      hbox {
        layoutpolicy_horizontal=expanding
        layoutpolicy_vertical=expanding
        
        text_single {
          visible="[CultureInnovation.IsFascination()]"
          rawtext="Current fascination:"
        }
        
        hbox {
          layoutpolicy_vertical=expanding
          layoutpolicy_horizontal=expanding
          
          text_single {
            size={ 500 22 }
            text="[CultureInnovation.GetNameNoTooltip()]"
          }
          
          text_single name="name_unlocked" {
            visible="[CultureInnovation.IsActive()]"
            rawtext=", discovered."
          }
          
          text_single name="name_blocked" {
            visible="[And(Not(CultureInnovation.CanBeFascination()), Not(CultureInnovation.IsActive()))]"
            rawtext=", not available."
          }
          
          hbox {
            visible="[And(CultureInnovation.CanGainProgress(), Not(CultureInnovation.IsActive()))]"
            text_single {
              rawtext=", [CultureInnovation.GetProgress('1')]."
            }
          }
          
          hbox {
            text_single {
              visible="[And(And(CultureInnovation.CanBeFascination(), Not(CultureInnovation.IsFascination())), Not(CultureInnovation.IsActive()))]"
              rawtext="Click to select as fascination."
            }
          }
        }
      }
    }
    
    # Button cliccabile
    button {
      hbox {
        layoutpolicy_vertical=expanding
        layoutpolicy_horizontal=expanding
        visible="[Not(CultureInnovation.IsFascination())]"
        
        tooltipwidget={ using=culture_innovation_tooltip }
        visible="[And(And(CultureInnovation.GetCulture().IsPlayerCultureHead(), Not(CultureInnovation.IsActive())), Not(CultureInnovation.IsFascination()))]"
        enabled="[CultureInnovation.CanBeFascination()]"
        size={ 100% 100% }
        onclick="[CultureInnovation.SelectAsFascination()]"
      }
    }
  }
}
```

### **4.2 Types Vanilla (Grafici)**

```gui
types CultureWindow {
  
  # Era tab Vanilla - Visual con texture
  type vbox_era_tab = vbox {
    datacontext="GuiCultureEra.GetCultureEra()"
    layoutpolicy_horizontal=expanding
    tooltipwidget={ using=culture_era_tooltip }
    using="tooltipse"
    
    spacer {
      visible="[GuiCultureEra.IsSelected()]"
      size={ 150 0 }
      
      state name="show" {
        size={ 135 0 }
        duration=0.3
      }
      
      state name="hide" {
        size={ 0 0 }
        duration=0.3
      }
    }
    
    button {
      layoutpolicy_horizontal=expanding
      size={ 0 128 }
      onclick="[PdxGuiTriggerAllAnimations('culture_refresh')]"
      scissor=yes
      
      state name="mouse_click" {
        onfinish="[GuiCultureEra.Select()]"
      }
      
      # Illustration texture
      highlighticon {
        parentanchor=center
        size={ 248 128 }
        texture="[CultureEra.GetType().GetIllustration()]"
        using="MaskRoughEdges"
        
        modify_texture {
          texture="gfx/interface/component_masks/mask_culture_era_tab.dds"
          blendmode=alphamultiply
          alpha=0.9
        }
      }
      
      # Overlay grigio se non attiva
      highlighticon {
        visible="[Not(CultureEra.IsActive())]"
        parentanchor=center
        size={ 248 128 }
        texture="[CultureEra.GetType().GetIllustration()]"
        tintcolor={ 0 0 0 0.5 }
      }
      
      # Borders
      widget {
        parentanchor=left
        size={ 6 128 }
        background={
          using="BackgroundAreaSolid"
          spriteType=Corneredtiled
          spriteborder={ 20 20 }
          spriteborder_right=11
          margin={ 0 20 }
          marginleft=10
        }
      }
      
      widget {
        parentanchor=right
        size={ 6 128 }
        background={
          using="BackgroundAreaSolid"
          mirror=horizontal
          spriteType=Corneredtiled
          spriteborder={ 20 20 }
          spriteborder_right=11
          margin={ 0 20 }
          marginright=10
        }
      }
      
      # Nome era (fade in/out)
      textmulti {
        visible="[GuiCultureEra.IsSelected()]"
        size={ 100% 100% }
        margin={ 5 10 }
        autoresize=no
        text="[CultureEra.GetNameNoTooltip()]"
        align=tophcenter
        defaultformat="low"
        
        state name="show" {
          using="AnimationFadeInStandard"
        }
        
        state name="hide" {
          using="AnimationFadeOutStandard"
        }
      }
      
      # Innovation count
      textlabelcenter {
        visible="[Not(CultureEra.IsActive())]"
        parentanchor=bottomhcenter
        position={ 0 -8 }
        text="CULTURE_ERA_INNOVATION_COUNT"
        defaultformat="low"
      }
      
      textlabelcenter {
        visible="[CultureEra.IsActive()]"
        parentanchor=bottomhcenter
        position={ 0 -8 }
        text="CULTURE_ERA_INNOVATION_COUNT_JOIN_LEAVE"
        defaultformat="high"
      }
    }
  }
  
  # Pillar Vanilla - Graphic con highlighticon
  type containerpillaritem = container {
    using="tooltipws"
    tooltipwidget={ using=culture_pillar_tooltip }
    
    # GRANDE ICONA DECORATIVA
    highlighticon name="icon" {
      alpha=0.3
      using="vanilla"
      
      block "iconsize" {
        size={ 592 130 }
      }
      
      texture="[CulturePillar.GetIcon()]"
      using="MaskRoughEdges"
    }
    
    widget {
      size={ 100% 100% }
      
      vbox {
        marginbottom=5
        expand={}
        
        textlabelcenter name="name" {
          text="[CulturePillar.GetNameNoTooltip()]"
          defaultformat="high"
          maximumsize={ 150 44 }
          fontsize_min=12
          multiline=yes
          align=center
          using="FontSizeMedium"
        }
        
        spacer { size={ 0 5 } }
        
        # Progress bar grafica
        hbox {
          layoutpolicy_horizontal=expanding
          spacing=5
          visible="[And(CultureReformation.IsReformingSamePillarTypeAs(Culture.GetEthos()), Not(CultureWindow.IsInReformationMode()))]"
          background={ using="BackgroundAreaDark" }
          margin={ 0 5 }
          tooltipwidget={ using=culture_pillar_tooltip_establishing }
          expand={}
          
          text_single {
            text="REFORM_ETHOS_NEW_NAME"
            align=nobaseline
          }
          text_single {
            text="REFORMATION_NEW_TRADITION_INFO"
            align=nobaseline
          }
          progressbar_reform {
            blockoverride "progressbar_reform_size" {
              size={ 200 14 }
            }
          }
        }
      }
    }
  }
  
  # Innovation Vanilla - Icon con animazioni
  type iconinnovation = icon {
    size={ 90 60 }
    
    # Icona base
    icon {
      texture="[CultureInnovation.GetType().GetIcon()]"
      size={ 90 60 }
      
      # SHIMMER ANIMATION per fascination
      modify_texture name="shimmer" {
        texture="gfx/interface/component_effects/effect_shimmer.dds"
        blendmode=colordodge
        translate_uv={ 0.2 0.2 }
        
        state name="shimmer" {
          next="pause"
          trigger_on_create=yes
          duration=1.2
          trigger_when="[CultureInnovation.IsFascination()]"
          bezier={ 0 0.9 1 0.4 }
          
          modify_texture name="shimmer" {
            translate_uv={ -1 1 }
          }
        }
        
        state name="pause" {
          duration=0
          delay=5
          
          modify_texture name="shimmer" {
            translate_uv={ 1 -1 }
          }
        }
      }
    }
    
    # Frame era
    icon {
      texture="[CultureInnovation.GetType().GetCultureEraType().GetFrame()]"
      size={ 90 60 }
    }
    
    # Overlay grigio se non attiva
    icon {
      visible="[Not(CultureInnovation.IsActive())]"
      size={ 100% 100% }
      texture="[CultureInnovation.GetType().GetIcon()]"
      tintcolor={ 0 0 0 0.5 }
    }
    
    highlighticon {
      visible="[Not(CultureInnovation.CanGainProgress())]"
      size={ 100% 100% }
      texture="[CultureInnovation.GetType().GetIcon()]"
      tintcolor={ 0 0 0 0.5 }
    }
    
    # GLOW FASCINATION
    highlighticon name="fascination" {
      visible="[CultureInnovation.IsFascination()]"
      parentanchor=center
      size={ 110 78 }
      texture="gfx/interface/component_effects/innovation_glow.dds"
      tintcolor={ 1 0.8 0.6 1 }
      
      state {
        trigger_on_create=yes
        name="max_glow"
        next="min_glow"
        duration=1
        using="AnimationCurveDefault"
        alpha=0.8
      }
      
      state name="min_glow" {
        next="max_glow"
        duration=1.6
        using="AnimationCurveDefault"
        alpha=0.5
      }
    }
    
    # GLOW EXPOSURE MARKER
    highlighticon name="exposure" {
      visible="[CultureInnovation.HasExposureMarker()]"
      parentanchor=center
      size={ 110 78 }
      texture="gfx/interface/component_effects/innovation_glow.dds"
      using="ColorBlue"
      
      state name="max_glow" {
        next="min_glow"
        trigger_on_create=yes
        duration=1
        using="AnimationCurveDefault"
        alpha=0.8
      }
      
      state name="min_glow" {
        next="max_glow"
        duration=1.6
        using="AnimationCurveDefault"
        alpha=0.5
      }
    }
  }
}
```

### **4.3 Types Condivisi**

```gui
types CultureShared {
  
  # Progress bar condiviso (usato da entrambi)
  type progressbar_reform = progressbar_standard {
    block "progressbar_reform_size" {}
    min=0
    max=100
    value="[CultureReformation.GetProgress()]"
  }
  
  # Tradition icon layered (5 layers)
  type widget_tradition_icon = widget {
    icon name="background" {
      texture="[CultureTradition.GetLayeredIcon().GetTexture(int32('0'))]"
      size={ 100% 100% }
    }
    
    icon name="pattern_left" {
      texture="[CultureTradition.GetLayeredIcon().GetTexture(int32('1'))]"
      size={ 100% 100% }
      parentanchor=hcenter
    }
    
    icon name="pattern_right" {
      texture="[CultureTradition.GetLayeredIcon().GetTexture(int32('1'))]"
      size={ 100% 100% }
      parentanchor=hcenter
      mirror=horizontal
    }
    
    icon name="support" {
      texture="[CultureTradition.GetLayeredIcon().GetTexture(int32('2'))]"
      size={ 100% 100% }
    }
    
    icon name="stroke" {
      texture="[CultureTradition.GetLayeredIcon().GetTexture(int32('3'))]"
      size={ 90 90 }
      parentanchor=center
    }
    
    icon name="items" {
      texture="[CultureTradition.GetLayeredIcon().GetTexture(int32('4'))]"
      size={ 100% 100% }
      parentanchor=center
    }
  }
}
```

***

## **5. COMPONENTI CONDIVISI: Gestione Integrata**

### **5.1 Tooltip Widgets (UNA SOLA DEFINIZIONE)**

```gui
# === TOOLTIP WIDGETS CONDIVISI ===
# Definiti DOPO i types, usati da entrambe le modalità

tooltipwidget = {
  using = culture_pillar_tooltip
  # Contenuto identico per OCR (letto) e Vanilla (mostrato)
  
  vbox {
    textmulti {
      text="[CulturePillar.GetName()]"
      autoresize=yes
      maxwidth=400
    }
    
    textmulti {
      text="[CulturePillar.GetDescription()]"
      autoresize=yes
      maxwidth=400
    }
    
    # Effects, requirements, etc.
  }
}

tooltipwidget = {
  using = culture_tradition_tooltip
  # ... tooltip completo per tradizioni
}

tooltipwidget = {
  using = culture_innovation_tooltip
  # ... tooltip completo per innovazioni
}

tooltipwidget = {
  using = culture_era_tooltip
  # ... tooltip completo per ere
}
```

**Utilizzo identico**:
```gui
# OCR
button_text {
  tooltipwidget={ using=culture_pillar_tooltip }  # ← Riferimento
}

# Vanilla
containerpillaritem {
  tooltipwidget={ using=culture_pillar_tooltip }  # ← Stesso riferimento
}
```

### **5.2 Datamodel Condivisi (IDENTICI)**

```gui
# OCR Mode usa:
datamodel="[CultureWindow.GetCultureEras()]"
datamodel="[Culture.GetTraditions()]"
datamodel="[GuiCultureEraGroup.GetInnovations()]"

# Vanilla Mode usa:
datamodel="[CultureWindow.GetCultureEras()]"  # ← STESSO
datamodel="[Culture.GetTraditions()]"         # ← STESSO
datamodel="[GuiCultureEraGroup.GetInnovations()]"  # ← STESSO
```

### **5.3 Scripted GUI Condivisi**

```gui
# Entrambe le modalità chiamano gli stessi script

# OCR
onclick="[GetScriptedGui('culture_closest_county_ocr').Execute(...)]"
onclick="[GetScriptedGui('culture_map_extents').Execute(...)]"

# Vanilla (se implementato)
onclick="[GetScriptedGui('culture_closest_county_ocr').Execute(...)]"  # ← STESSO
onclick="[GetScriptedGui('culture_map_extents').Execute(...)]"         # ← STESSO
```

### **5.4 Conditional DLC Features (IDENTICI)**

```gui
# OCR
visible="[HasDlcFeature('diverge_culture')]"
enabled="[GetPlayer.GetCulture().CanDiverge()]"

# Vanilla
visible="[HasDlcFeature('diverge_culture')]"  # ← STESSA CONDIZIONE
enabled="[GetPlayer.GetCulture().CanDiverge()]"  # ← STESSA CONDIZIONE
```

***

## **6. STATI E ANIMAZIONI**

```gui
# State condiviso per refresh
state name="culture_refresh" {
  using="AnimationRefreshFadeOut"
}
state {
  using="AnimationRefreshFadeIn"
}

# State per era tabs (solo Vanilla)
state name="show" {
  size={ 135 0 }
  duration=0.3
}

state name="hide" {
  size={ 0 0 }
  duration=0.3
}

# State shimmer per innovations (solo Vanilla)
state name="shimmer" {
  next="pause"
  trigger_on_create=yes
  duration=1.2
  trigger_when="[CultureInnovation.IsFascination()]"
  bezier={ 0 0.9 1 0.4 }
  
  modify_texture name="shimmer" {
    translate_uv={ -1 1 }
  }
}

state name="pause" {
  duration=0
  delay=5
  
  modify_texture name="shimmer" {
    translate_uv={ 1 -1 }
  }
}
```

***

## **7. TEMPLATES CONDIVISI**

```gui
template agot_show_hybridize_culture = {
  visible="[And(Not(ObjectsEqual(Culture.GetHeritage(), GetPlayer.GetCulture().GetHeritage())), And(Not(GetPlayer.GetCulture().IsChildOf(Culture.Self)), Not(Culture.IsChildOf(GetPlayer.GetCulture()))))]"
}

template animation_culture_refresh = {
  state name="culture_refresh" {
    using="AnimationRefreshFadeOut"
  }
  state {
    using="AnimationRefreshFadeIn"
  }
}
```

***

## **8. STRUTTURA FILE FINALE**

```gui
###############################################
# WINDOW CULTURE - DUAL MODE (OCR + VANILLA)
###############################################
# Repository: Nemex81/ocr-support-patch
# File: ocr-support/compatibility-pach/gui/window_culture.gui
# Last Modified: 2025-12-21

### === WINDOW PRINCIPALE === ###
window name="culturewindow" {
  widgetid="culturewindow"
  layer="windows_layer"
  movable=no
  using="base_ocr_window"
  
  # DATACONTEXT COMUNI (definiti UNA SOLA VOLTA)
  datacontext="CultureWindow.GetCulture()"
  datacontext="Culture.GetReformation()"
  
  # STATES COMUNI (definiti UNA SOLA VOLTA)
  state name="show" { ... }
  state name="hide" { ... }
  
  ### === MODALITÀ OCR (Non Vedenti) === ###
  window_ocr visible="[Not(GetVariableSystem.Exists('ocr'))]" {
    blockoverride "ocr_header" { ... }
    blockoverride "ocr_content" {
      # Tabs hbox
      # Tab 1: Overview content
      # Tab 2: Innovations content
      # Tab 3: All Cultures content
      # Tab 4: Counties content
      # Tab 5: Rulers content
      # Culture head section
    }
  }
  
  ### === MODALITÀ VANILLA (Normovedenti) === ###
  margin_widget visible="[GetVariableSystem.Exists('ocr')]" {
    using="Window_Margins_Sidebar"
    # Header con watch button
    # Acceptance widget
    # Who's culture text
    # Tabs (Overview, Innovations)
    # Tab 1: Overview content (pillars grafici, traditions layered, buttons, culture head portrait)
    # Tab 2: Innovations content (era tabs visual, innovations grid grafiche)
  }
}

### === TYPES OCR-SPECIFIC === ###
types OCR {
  type vbox_era_tab_ocr = { ... }
  type containerpillaritemocr = { ... }
  type flowcontainer_innovation = { ... }
}

### === TYPES VANILLA-SPECIFIC === ###
types CultureWindow {
  type vbox_era_tab = { ... }  # Con texture illustrations + animations
  type containerpillaritem = { ... }  # Con highlighticon 592x130 + effects
  type iconinnovation = { ... }  # Con shimmer + glow animations
}

### === TYPES CONDIVISI === ###
types CultureShared {
  type progressbar_reform = { ... }
  type widget_tradition_icon = { ... }  # 5 layers grafiche
}

### === TEMPLATES CONDIVISI === ###
template agot_show_hybridize_culture = { ... }
template animation_culture_refresh = { ... }

### === TOOLTIP WIDGETS CONDIVISI === ###
# (Opzionale: possono essere in file separato)
tooltipwidget = { using = culture_pillar_tooltip }
tooltipwidget = { using = culture_tradition_tooltip }
tooltipwidget = { using = culture_innovation_tooltip }
tooltipwidget = { using = culture_era_tooltip }
```

***

## **9. CRITERI DI SUCCESSO**

### **✅ OCR Mode (Non Vedenti)**
- [ ] Tutte e 5 le tabs funzionanti con hotkeys Speed1-5
- [ ] Navigation completa tramite tastiera (Tab, Enter, hotkeys)
- [ ] Screen reader può leggere **tutto** il contenuto sequenzialmente
- [ ] Tutti i button hanno `rawtext` espliciti e descrittivi
- [ ] Sorting e filtering funzionanti con feedback vocale
- [ ] Nessuna texture/icon decorativa inutile
- [ ] Layout lineare (vbox/hbox) senza complessità visive
- [ ] Tooltip letti correttamente da screen reader

### **✅ Vanilla Mode (Normovedenti)**
- [ ] **TUTTA** la grafica originale mantenuta:
  - [ ] Pillar highlighticon 592x130px con MaskRoughEdges
  - [ ] Innovation iconinnovation 90x60px con shimmer effect
  - [ ] Tradition widget_tradition_icon con 5 layers grafiche
  - [ ] Era tab texture illustrations con fade animations
  - [ ] Portrait shoulders per culture head
  - [ ] Glow effects per fascination (alpha 0.5 ↔ 0.8)
  - [ ] Exposure markers blu
  - [ ] Progress bar grafiche
  - [ ] Coat of arms
- [ ] **TUTTE** le animazioni funzionanti:
  - [ ] Shimmer effect (UV rotation 360°, 7s loop)
  - [ ] Glow pulsing (1s + 1.6s cycle)
  - [ ] Fade in/out (AnimationFadeInStandard/FadeOut)
  - [ ] Size transitions (era tabs 135↔0)
  - [ ] State animations (culture_refresh)
- [ ] **TUTTE** le interazioni funzionanti:
  - [ ] Hover effects
  - [ ] Click areas ottimizzate
  - [ ] Tooltip grafici ricchi
  - [ ] Modal windows (reform, diverge, hybridize)
  - [ ] Visual feedback immediato

### **✅ Entrambe le Modalità**
- [ ] **Stessi datamodel** (CultureWindow.GetCultureEras(), Culture.GetTraditions(), etc.)
- [ ] **Stessi tooltip widget** (culture_pillar_tooltip, culture_innovation_tooltip, etc.)
- [ ] **Stesse funzionalità**:
  - [ ] Reform culture (se culture head + DLC)
  - [ ] Hybridize culture (se DLC + condizioni)
  - [ ] Diverge culture (se player culture + DLC)
  - [ ] Add tradition (se culture head)
  - [ ] Select fascination (se culture head)
  - [ ] Replace tradition (se reformation mode)
  - [ ] Adopt court language (se DLC royalcourt)
- [ ] **Nessun crash** o elemento mancante
- [ ] **Proper conditional visibility** per DLC features:
  - [ ] `HasDlcFeature('diverge_culture')`
  - [ ] `HasDlcFeature('hybridize_culture')`
  - [ ] `HasDlcFeature('reform_culture')`
  - [ ] `HasDlcFeature('dlc_fp1_feature_martial_custom')`
  - [ ] `HasDlcFeature('dlc_fp1_feature_court_language')`
  - [ ] `HasDlcFeature('royal_court')`
- [ ] **Stesse localization keys** (CULTUREWINDOW_CULTURE, REFORM_CULTURE_LABEL, etc.)
- [ ] **Stessi scripted_gui** (culture_closest_county_ocr, culture_map_extents, etc.)

***

## **10. ISTRUZIONI SPECIFICHE PER L'AGENTE GITHUB**

### **✅ DA FARE**

1. **Definire datacontext/states nel window principale** prima di qualsiasi widget figlio
2. **Creare types SEPARATI** per OCR e Vanilla quando rendering è diverso
3. **Creare types CONDIVISI** per componenti logici identici (progressbar_reform)
4. **Usare gli STESSI datamodel** in entrambe le modalità (no duplicazioni)
5. **Usare le STESSE localization keys** in entrambe le modalità
6. **Sincronizzare TUTTE le condizioni DLC** (visible/enabled identiche)
7. **Referenziare tooltip UNA SOLA VOLTA** tramite `using=tooltip_name`
8. **Usare blockoverride** per variazioni minime di componenti simili
9. **Mantenere GetScriptedGui IDENTICI** in entrambe le modalità
10. **Commentare CHIARAMENTE** ogni sezione (OCR vs Vanilla vs Condiviso)
11. **Preservare TUTTA la grafica Vanilla** (texture, alpha, tint, effects)
12. **Preservare TUTTE le animazioni Vanilla** (shimmer, glow, fade, transitions)
13. **Testare SEPARATAMENTE** OCR mode (senza `ocr` var) e Vanilla mode (con `ocr` var)

### **❌ DA NON FARE**

1. ❌ **NON duplicare datacontext** nei widget figli
2. ❌ **NON ridefinire lo stesso type** due volte (OCR e Vanilla devono avere nomi diversi)
3. ❌ **NON usare datamodel diversi** per gli stessi dati backend
4. ❌ **NON creare tooltip separati** se il contenuto è identico
5. ❌ **NON hardcodare valori** che dovrebbero venire dal backend
6. ❌ **NON usare localization keys diverse** per lo stesso concetto
7. ❌ **NON duplicare states/animations** identici
8. ❌ **NON creare condizioni DLC diverse** tra OCR e Vanilla
9. ❌ **NON semplificare la grafica Vanilla** per "coerenza" con OCR
10. ❌ **NON rimuovere animazioni Vanilla** perché "non necessarie"
11. ❌ **NON usare lo stesso type** per rendering completamente diversi
12. ❌ **NON mescolare logica OCR e Vanilla** nello stesso widget (separare completamente)

***

## **11. CHECKLIST FINALE PRE-COMMIT**

Prima di creare il commit, verificare:

- [ ] Window principale ha datacontext/states definiti UNA VOLTA
- [ ] OCR mode ha types separati (suffix `_ocr`)
- [ ] Vanilla mode ha types separati (no suffix o suffix vanilla-specific)
- [ ] Types condivisi sono in `types CultureShared`
- [ ] Tooltip sono definiti UNA VOLTA e referenziati da entrambi
- [ ] Datamodel sono identici in OCR e Vanilla
- [ ] Localization keys sono identiche in OCR e Vanilla
- [ ] DLC conditions sono identiche in OCR e Vanilla
- [ ] Scripted_gui calls sono identici in OCR e Vanilla
- [ ] OCR mode è completamente funzionale senza `ocr` var
- [ ] Vanilla mode è completamente funzionale con `ocr` var
- [ ] Tutte le texture Vanilla sono presenti
- [ ] Tutte le animazioni Vanilla funzionano
- [ ] Tutti i tooltip sono accessibili
- [ ] Nessun elemento duplicato inutilmente
- [ ] File è commentato chiaramente
- [ ] Codice è validato sintatticamente

***

Questo piano completo e dettagliato fornisce all'agente GitHub **tutte le informazioni necessarie** per implementare un sistema dual-mode perfetto, garantendo che:

1. **OCR mode** sia completamente accessibile per non vedenti
2. **Vanilla mode** mantenga tutta la grafica e animazioni originali
3. **Componenti condivisi** siano gestiti in modo DRY (Don't Repeat Yourself)
4. **Nessun compromesso** venga fatto su nessuna delle due modalità