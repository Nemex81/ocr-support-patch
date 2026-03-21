# Jomini Scope Whitelist — CK3 1.17.1

Scope e binding verificati nei file vanilla di CK3 1.17.1.
Copilot NON deve usare scope non presenti qui senza verifica esplicita nel vanilla.

## Policy di tracciabilità (dal 2026-03-20)

Ogni nuova sezione di binding DEVE indicare:
- **Fonte vanilla**: percorso completo del file CK3 originale dove il binding è stato verificato
- **Data di verifica**: data dell'ultimo controllo
- **Aggiunto da**: chi ha aggiunto la sezione (Implementatore Patch / scope_extractor.py)

Le sezioni precedenti al 2026-03-20 mantengono il formato originale.
Le sezioni dal 2026-03-20 in poi seguono il nuovo formato con tracciabilità.

## Scope GUI principali verificati

| Scope | Contesto | Note |
| ------- | --------- | ------ |
| `GetPlayer` | globale | personaggio del giocatore |
| `GetCharacter` | contesto personaggio | richiede scope parent corretto |
| `GetTitle` | contesto titolo | metodi verificati: `GetNameNoTooltip`, `GetNameNoTierNoTooltip`, `GetHolder` |
| `GetFaith` | contesto fede | richiede scope parent corretto |
| `GetCulture` | contesto cultura | richiede scope parent corretto |
| `GetDynasty` | contesto dinastia | richiede scope parent corretto |
| `GetHouse` | contesto casata | richiede scope parent corretto |
| `GetArmy` | contesto esercito | richiede scope parent corretto |
| `GetWar` | contesto guerra | richiede scope parent corretto |
| `GetFaction` | contesto fazione | richiede scope parent corretto |
| `GameRules` | globale | accesso alle game rules |
| `ActivityWindow` | contesto finestra attività | metodi: `GetActivity`, `HasActiveEvent`, `GetCharacters`, `GetEventWindowInsert`, `GetCurrentPhaseGuestSubset`, `GetLastWeeklyPulseEffectData`, `GetIntentTooltip`, `Close` |
| `Activity` | contesto attività | metodi: `IsComplete`, `GetType`, `GetCurrentPhase`, `GetTimeline`, `IsParticipant`, `GetLastWeeklyPulseAction`, `MakeScope` |
| `ActivityType` | contesto tipo attività | metodi: `GetHeaderIcon`, `GetKey` |
| `ActivityPhase` | contesto fase attività | metodi: `GetKey`, `GetName`, `GetProgress`, `GetLocation`, `GetPhase` |
| `Character` | contesto personaggio attivo | metodi: `Self`, `GetInvolvedActivityIntent`, `GetCompletedIntents` |
| `ActivityWindowCharacter` | contesto elenco personaggi | metodi: `GetCharacter`, `GetLabel` |
| `ActivityIntent` | contesto intent attività | metodi: `GetName`, `GetType`, `GetIcon` |
| `GetVariableSystem` | contesto variabili GUI | metodi: `Exists`, `Toggle` |
| `EventWindowViewInsert` | contesto header evento attività | metodi: `GetOpenEvent`, `HasOpenEvent`, `OnMouseEnterOption`, `OnMouseLeaveOption` |
| `EventWindowData` | contesto dati evento attività | metodi: `GetDescription`, `GetOptions` |
| `EventOption` | contesto opzioni evento | metodi: `GetText`, `GetTooltip`, `Select`, `IsValid`, `GetClickSound`, `OnEnter`, `OnLeave` |
| `Province` | contesto provincia/location attività | metodi: `GetTitle`, `GetCounty`, `GetNameNoTooltip`, `PanCameraTo` |
| `Holding` | contesto holding/location attività | metodi: `GetSpecialBuildingType` |
| `SpecialBuildingType` | contesto edificio speciale | metodi: `GetTypeIcon` |
| `PdxGuiWidget` | contesto widget GUI | metodo: `AccessSelf` |
| `ActivityPulseEffect` | contesto popup weekly pulse attività | metodi: `IsValid`, `GetTitle`, `GetEffectText` |

## Funzioni GUI verificate

```jomini
onclick = "[ToggleGameViewData( 'activity_log', Activity.Self )]"
down = "[IsGameViewDataShown( 'activity_log', Activity.Self )]"
visible = "[DataModelHasItems( ActivityWindow.GetCurrentPhaseGuestSubset( 'charioteers' ) )]"
onclick = "[AddWatchWindow( Activity.MakeScope )]"
```

## Note specifiche verificate in window_activity.gui

- `Activity.GetCurrentPhase.GetLocation.PanCameraTo` usato dal pulsante go-to del vanilla.
- `Activity.GetCurrentPhase.GetLocation.GetHolding.GetSpecialBuildingType.GetTypeIcon` usato nel widget journey skill text del vanilla.

## Binding Dual Mode (obbligatori, non modificare)

```jomini
# Container OCR attivo — modalità non vedente (variabile ocr assente)
visible = "[Not(GetVariableSystem.Exists('ocr'))]"
# Container vanilla attivo — modalità normo-vedente (variabile ocr presente)
visible = "[GetVariableSystem.Exists('ocr')]"
```

> ⚠️ `GameRules.GetRule('ocr_accessibility_mode')` è **deprecato** — non usarlo nelle nuove conversioni.

## Pattern binding dati comuni verificati

```jomini
# Oro del giocatore
text = "[GetPlayer.GetTreasury|0]"
# Pietà
text = "[GetPlayer.GetPiety|0]"
# Prestigio
text = "[GetPlayer.GetPrestige|0]"
# Nome UI senza tooltip
text = "[GetPlayer.GetUINameNoTooltip]"
# Data corrente
text = "[GetDate]"
```

## Note operative

- Il modificatore `|0` formatta i numeri — usarlo sempre per valori numerici
- I scope dipendono dal contesto widget parent — verificare sempre la gerarchia
- In caso di dubbio: aprire il file vanilla corrispondente e copiare il binding esatto
- Se un scope non è in questa lista: aggiungerlo solo dopo verifica manuale nel vanilla

**Aggiornare questo file ogni volta che si verifica un nuovo scope nel vanilla.**
Ultimo aggiornamento: 2026-03-20

> **Formato nuove sezioni (dal 2026-03-20)**:
> ```
> ## Scope e binding — nome_file.gui
> Fonte vanilla: `C:/.../game/gui/nome_file.gui`
> Data verifica: YYYY-MM-DD | Aggiunto da: Implementatore Patch / scope_extractor.py
> ```

---

## Scope e binding — interaction_menu_window.gui

Verificati direttamente in `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/interaction_menu_window.gui`
e in `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/interaction_templates.gui`.

### Scope finestra e controller

| Scope / Binding | Contesto | Note |
|---|---|---|
| `CharacterInteractionMenuWindow` | interaction_menu_window.gui — scope finestra interazioni | metodi: `GetCharacter`, `Close`, `OutsideDiplomaticRange`, `IsFiltered`, `GetFilterDescription`, `GetCategoryItems`, `GetMoreInteractions`, `AreMoreInteractionsVisisble` |
| `CharacterInteractionMenuWindow.AreMoreInteractionsVisisble` | interaction_menu_window.gui | ⚠️ refuso storico nel nome — usare ESATTAMENTE così, non correggere |

### Metodi Character verificati in interaction_menu_window.gui

| Scope / Binding | Contesto | Note |
|---|---|---|
| `Character.IsLocalPlayer` | interaction_menu_window.gui — check giocatore locale | usato nel header OCR e vanilla |
| `Character.GetNameNoTooltip` | interaction_menu_window.gui — nome vanilla senza tooltip | con modificatore `\|U` per uppercase |
| `Character.GetUINameNoTooltip` | interaction_menu_window.gui — nome UI completo senza tooltip | più completo di GetNameNoTooltip |
| `Character.IsPinned` | interaction_menu_window.gui — stato pin outliner | usato per toggle testuale OCR |
| `Character.ToggleCharacterPinned` | interaction_menu_window.gui — toggle pin outliner | onclick del pulsante pin vanilla e OCR |
| `Character.CanCustomizePortrait` | interaction_menu_window.gui — guard apertura barbiere | visibilità pulsante barbiere vanilla e OCR |
| `Character.OnCustomizePortrait` | interaction_menu_window.gui — apertura barbiere | onclick del pulsante barbiere |
| `Character.CanCharacterBeRenamed` | interaction_menu_window.gui — guard rinomina | visibilità pulsante rename vanilla e OCR |
| `Character.PanCameraTo` | interaction_menu_window.gui — centra camera sul personaggio | onclick del pulsante go-to vanilla e OCR |

### Scope categorie e interazioni

| Scope / Binding | Contesto | Note |
|---|---|---|
| `InteractionCategoryItem` | interaction_templates.gui — scope categoria interazioni | metodi: `IsVisible`, `GetName`, `GetInteractions`, `ShowMoreInteractions` |
| `InteractionItem` | interaction_templates.gui — scope singola riga interazione | metodi: `GetName`, `GetTooltip`, `IsValid`, `OnClick`, `ToggleFavorite`, `IsFavorite`, `IsMarriageSetting`, `OnClickCheckbox`, `CheckboxEnabled`, `GetCheckboxFrame`, `GetCheckboxTooltip`, `HasWarningIcon`, `GetWarningTooltipDesc`, `HasPreviewSchemeOdds`, `GetPreviewSchemeOdds`, `IsPotentialAccept`, `IsMore`, `IsCharacterInteraction`, `IsHighlighted`, `ShouldUseExtraIcon`, `GetExtraIcon`, `GetCharacterInteraction` |

### Funzioni GUI verificate in interaction_menu_window.gui

| Funzione | Contesto | Note |
|---|---|---|
| `GetDataModelSize()` | interaction_templates.gui — conteggio interazioni per categoria | es. `GetDataModelSize(InteractionCategoryItem.GetInteractions)` |
| `EqualTo_int32()` | interaction_templates.gui — confronto checkbox frame | es. `EqualTo_int32(InteractionItem.GetCheckboxFrame, '(int32)2')` |
| `LessThanOrEqualTo_CFixedPoint()` | interaction_templates.gui — check acceptance value | es. per "won't accept" nel riepilogo OCR upstream |
| `Select_CString()` | interaction_menu_window.gui — testi condizionali | es. `Select_CString(Character.IsPinned, 'Rimuovi dall outliner.', 'Aggiungi all outliner.')` |

### ScriptedGui rename verificato

| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetScriptedGui('rename_character_after_birth')` | interaction_menu_window.gui — GUI scriptata rinomina | binding verificato in vanilla; `datacontext` sulla stessa riga non sovrascrive Character scope dal parent |
| `ScriptedGui.Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('child', Character.MakeScope).End)` | interaction_menu_window.gui — esecuzione rename | pattern GuiScope con AddScope 'child' verificato nel vanilla |

---

## Scope e binding — window_faith.gui

Verificati direttamente in `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/window_faith.gui`.

| Scope / Binding | Contesto | Note |
|---|---|---|
| `FaithWindow` | window_faith.gui — contesto finestra fede | metodi: `GetFaith`, `GetHolySites`, `GetGroupingHelper()`, `GetSins`, `GetVirtues`, `Close`, `ToggleReligionWindow` |
| `FaithDoctrine` | window_faith.gui — scope dottrina | metodi: `GetNameNoTooltip(Faith)`, `GetIcon`, `GetGroup`, `GetNameNoTooltip(Faith.Self)`, `GetBaseName` |
| `Faith` | window_faith.gui — scope fede diretto (non solo via `GetFaith`) | metodi: `GetReligion`, `IsUnreformed`, `GetAdherentNamePlural`, `GetNameNoTooltip`, `MakeScope`, `GetID`, `Self` |
| `HolySite` | window_faith.gui — scope sito sacro | metodi: `GetBarony`, `GetName`, `GetBarony.GetProvince` |
| `GuiFaithDoctrineItem` | window_faith.gui — item datamodel dottrine | metodi: `GetDoctrine`, `GetFaith` |
| `GuiHolySiteItem` | window_faith.gui — item datamodel siti sacri | metodi: `GetHolySite`, `IsHeldByFaith` |
| `GuiVirtueOrSinItem` | window_faith.gui — item datamodel virtù/peccati | metodo: `GetTrait` |
| `Title` | window_faith.gui — scope titolo diretto (non solo via `GetTitle`) | metodi: `GetHolder`, `GetNameNoTierNoTooltip`, `GetDeJureLiege`, `GetTopLiege`, `Self` |
| `Trait` | window_faith.gui — scope tratto | metodi: `GetNameNoTooltip(GetPlayer)`, `GetIcon(GetPlayer)` |
| `ScriptedGui` | window_faith.gui — binding GUI scriptata | metodi: `IsValid()`, `Execute()`, `BuildTooltip()`, `IsShown()` |
| `ReligionWindow` | window_faith.gui — contesto finestra religione | metodi: `GetReligion`, `GetFaiths`, `ShowOnlyReligionFaiths`, `Close` |

## Funzioni GUI — window_faith.gui

| Funzione | Contesto | Note |
|---|---|---|
| `EqualTo_string()` | window_faith.gui — comparazione stringa | es. `EqualTo_string(Var.GetFlagName, 'piety')` |
| `EqualTo_int32()` | window_faith.gui — comparazione int32 | es. `EqualTo_int32(GetDataModelSize(...), (int32)1)` |
| `GreaterThan_int32()` | window_faith.gui — comparazione int > | es. `GreaterThan_int32(GetDataModelSize(...), (int32)1)` |
| `GreaterThan_CFixedPoint()` | window_faith.gui — comparazione fixed point > | es. `GreaterThan_CFixedPoint(Faith.MakeScope.ScriptValue('faith_holy_sites_held'), CFixedPoint('0'))` |
| `NotEqualTo_uint32()` | window_faith.gui — comparazione uint != | es. `NotEqualTo_uint32(Faith.GetID, GetPlayer.GetFaith.GetID)` |
| `ObjectsEqual()` | window_faith.gui — comparazione oggetti ⚠️ verificare in vanilla | es. `ObjectsEqual(GetPlayer.GetFaith, Faith.Self)` |
| `Select_CString()` | window_faith.gui — funzione ternaria stringa | es. `Select_CString(GetVariableSystem.Exists('holy_site_effects'), 'Show', 'Hide')` |
| `AddTextIf()` | window_faith.gui — testo condizionale | es. `AddTextIf(GetPlayer.MakeScope.Var('faith_counties_filter').IsSet, ' held by non-believers')` |
| `MakeScopeFlag()` | window_faith.gui — flag da scope | es. `MakeScopeFlag(Scope.GetFlagName)` |
| `GetGlobalList()` | window_faith.gui — lista globale | es. `GetGlobalList('faith_followers_sort')` |
| `GetDoctrine()` | window_faith.gui — accesso dottrina globale | es. `GetDoctrine('doctrine_spiritual_head')` |
| `GetFaithDoctrine()` | window_faith.gui — accesso dottrina faith | es. `GetFaithDoctrine('unreformed_faith_doctrine').GetBaseName` |
| `GetDataModelSize()` | window_faith.gui — conteggio elementi datamodel | es. `GetDataModelSize(Faith.GetReligion.GetFaiths)` |
| `CFixedPoint()` | window_faith.gui — costruttore tipo fixed point | es. `CFixedPoint('0')` per confronti numerici |
| `GetNumberOfValidInteractionsWithFilter` | window_faith.gui — conteggio interazioni filtrate | verificato in vanilla window_faith.gui:730 |
| `GetPietyLevelName` | window_faith.gui (OCR) — nome livello pietà | NON in vanilla GUI — binding OCR upstream, presente in data_binding/ |
| `GetDataModelSize` | window_faith.gui — alias path-dotted di `GetDataModelSize()` | verificato in vanilla frontend_bookmarks.gui:1623 |
| `GetDoctrine` | window_faith.gui — alias path-dotted di `GetDoctrine()` | verificato in vanilla window_faith.gui:769 |
| `GetFaithDoctrine` | window_faith.gui — alias path-dotted di `GetFaithDoctrine()` | NON in vanilla GUI — binding OCR upstream |
| `GetScriptedGui` | window_faith.gui — alias path-dotted | verificato in vanilla window_faith.gui:878 |
| `AddWatchWindow` | window_faith.gui — aggiunge finestra watch | verificato in vanilla window_faith.gui:97 |
| `AddTextIf` | window_faith.gui — alias path-dotted di `AddTextIf()` | verificato in vanilla (già whitelistato come `AddTextIf()`) |
| `OrderFaithOption.GetName` | window_faith.gui — nome opzione sort faith | verificato in vanilla window_faith.gui:1210 |
| `Select_float` | window_faith.gui — funzione ternaria float | verificato in vanilla window_faith.gui:1276 |
| `Select_CString` | window_faith.gui — alias path-dotted di `Select_CString()` | già whitelistato come `Select_CString()` |
| `EqualTo_int32` | window_faith.gui — alias path-dotted | già whitelistato come `EqualTo_int32()` |
| `EqualTo_string` | window_faith.gui — alias path-dotted | già whitelistato come `EqualTo_string()` |
| `GreaterThan_int32` | window_faith.gui — alias path-dotted | già whitelistato come `GreaterThan_int32()` |
| `GreaterThan_CFixedPoint` | window_faith.gui — alias path-dotted | già whitelistato come `GreaterThan_CFixedPoint()` |
| `NotEqualTo_uint32` | window_faith.gui — alias path-dotted | già whitelistato come `NotEqualTo_uint32()` |
| `GetVariableSystem.Exists` | globale Dual Mode — controlla esistenza variabile | verificato in vanilla window_faith.gui:229 |
| `GetVariableSystem.Set` | globale Dual Mode — imposta variabile | verificato in vanilla window_faith.gui:19 |
| `GetVariableSystem.Clear` | globale Dual Mode — cancella variabile | verificato in vanilla window_faith.gui:29 |
| `GetVariableSystem.HasValue` | globale Dual Mode — controlla valore variabile | verificato in vanilla window_faith.gui:229 |
| `GetVariableSystem.Toggle` | globale Dual Mode — inverte variabile | presente in patch, compatibile con GetVariableSystem vanilla |
| `GetPlayer.MakeScope.Var` | window_faith.gui (OCR) — variabile scope player | verificato in vanilla hud.gui:157 |
| `Has` | window_faith.gui (OCR) — shorthand OCR per GetVariableSystem.HasValue | binding OCR mod (data_binding/OCR_bindings.txt) — NON in vanilla nativo |
| `Scope.Faith` | window_faith.gui (OCR) — scope faith in catena GuiScope | binding Jomini scope accessor — `GuiScope.SetRoot(...).AddScope('faith', ...)` |
| `Scope.GetCharacter` | window_faith.gui (OCR) — scope character in catena GuiScope | binding Jomini scope accessor |
| `Scope.GetFlagName` | window_faith.gui (OCR) — flag name da scope | NON in vanilla GUI — binding OCR upstream / Jomini interno |
| `Scope.Title` | window_faith.gui (OCR) — scope title in catena GuiScope | binding Jomini scope accessor |
| `Scope.Title.GetCountyData.GetCapital` | window_faith.gui (OCR) — capitale contea del titolo | binding OCR specifico — catena scope |
| `Scope.Var` | window_faith.gui (OCR) — variabile su scope | compatibile con GetPlayer.MakeScope.Var() verificato in vanilla hud.gui |

---

## Scope e binding — window_my_realm.gui

Verificati direttamente in `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/window_my_realm.gui`.

| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPlayer.GetPrimaryTitle.GetNameNoTooltip` | window_my_realm.gui — header realm | verificato in vanilla window_my_realm.gui:485 |
| `GetPlayer.GetActiveLawInGroupWithFlag` | window_my_realm.gui — subtitle authority / realm law | verificato in vanilla window_my_realm.gui:525 |
| `GetPlayer.HasSuzerain` | window_my_realm.gui — label liege/suzerain | verificato in vanilla window_my_realm.gui:587 |
| `GetPlayer.HasLiege` | window_my_realm.gui — label liege | verificato in vanilla window_my_realm.gui:594 |
| `SelectLocalization` | window_my_realm.gui — testo condizionale liege/suzerain | verificato in vanilla window_my_realm.gui:988 |
| `GetPlayer.GetDreadBreakdown` | window_my_realm.gui — tooltip dread | verificato in vanilla window_my_realm.gui:3222 |
| `GetPlayer.GetDread` | window_my_realm.gui — valore dread | verificato in vanilla window_my_realm.gui:3232 |
| `NotEqualTo_int32` | window_my_realm.gui — filtro conteggio stance vassalli | verificato in vanilla window_my_realm.gui:3283 |
---
## Scope e binding -- hud.gui
Verificati direttamente in `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/hud.gui`
e in altri file vanilla (citati nelle note).
### Funzioni matematiche/comparazione -- verificate in vanilla hud.gui
| Scope / Binding | Contesto | Note |
|---|---|---|
| `GreaterThanOrEqualTo_CFixedPoint` | hud.gui -- comparazione >= fixed point | verificato in vanilla hud.gui:5124 |
| `GreaterThanOrEqualTo_int32` | hud.gui -- comparazione >= int32 | verificato in vanilla hud.gui:1442 |
| `LessThan_CFixedPoint` | hud.gui -- comparazione < fixed point | verificato in vanilla hud.gui:5279 |
| `LessThan_int32` | hud.gui -- comparazione < int32 | verificato in vanilla hud.gui:5976 |
| `Add_int32` | hud.gui -- somma int32 | verificato in vanilla map_icon_layer.gui:847, window_activity_planner.gui:1705 |
| `EqualTo_CFixedPoint` | hud.gui -- uguaglianza fixed point | verificato in vanilla interaction_declare_war.gui:857 |
### Binding GetPlayer -- verificati in vanilla hud.gui
| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPlayer.GetPiety` | hud.gui -- pieta del giocatore | verificato in vanilla hud.gui (usato come value, comune in tutti i file) |
| `GetPlayer.GetPrestige` | hud.gui -- prestigio del giocatore | verificato in vanilla hud.gui (usato come value, comune in tutti i file) |
| `GetPlayer.GetAcceptedTaskContracts` | hud.gui -- contratti accettati | verificato in vanilla hud.gui:3355 |
| `GetPlayer.GetCulture` | hud.gui -- cultura del giocatore | verificato in vanilla hud.gui:1623 |
| `GetPlayer.GetDomicile` | hud.gui -- domicilio | verificato in vanilla hud.gui:5451 |
| `GetPlayer.GetDynasty.GetDynastyPrestigeLevelTexture` | hud.gui -- texture livello prestigio dinasta | verificato in vanilla hud.gui:5648 |
| `GetPlayer.GetDynasty.GetPrestige` | hud.gui -- prestigio dinastia | verificato in vanilla hud.gui:5667 |
| `GetPlayer.GetFaith` | hud.gui -- fede del giocatore | verificato in vanilla hud.gui:1649 |
| `GetPlayer.GetFaith.GetDefensiveGreatHolyWars` | hud.gui -- guerre sante difensive | verificato in vanilla hud.gui:3432 |
| `GetPlayer.GetFaith.GetGreatHolyWar` | hud.gui -- guerra santa in corso | verificato in vanilla hud.gui:3452 |
| `GetPlayer.GetFaith.HasOffensiveGreatHolyWar` | hud.gui -- ha guerra santa offensiva | verificato in vanilla hud.gui:3453 |
| `GetPlayer.GetFocus.GetIcon` | hud.gui -- icona focus corrente | verificato in vanilla hud.gui:2355 |
| `GetPlayer.GetGold` | hud.gui -- oro del giocatore | verificato in vanilla hud.gui:5271 |
| `GetPlayer.GetGovernment.HasRule` | hud.gui -- regola governo | verificato in vanilla hud.gui:5556 |
| `GetPlayer.GetGovernment.IsType` | hud.gui -- tipo di governo | verificato in vanilla hud.gui:342 |
| `GetPlayer.GetHostileRaiders` | hud.gui -- razziatori ostili | verificato in vanilla hud.gui:3467 |
| `GetPlayer.GetHouse` | hud.gui -- casata del giocatore | verificato in vanilla hud.gui:1677 |
| `GetPlayer.GetInfluence` | hud.gui -- influenza corrente | verificato in vanilla hud.gui:5595 |
| `GetPlayer.GetInfluenceLevelTexture` | hud.gui -- texture livello influenza | verificato in vanilla hud.gui:5585 |
| `GetPlayer.GetInterloperStruggles` | hud.gui -- lotte come interlopere | verificato in vanilla hud.gui:3531 |
| `GetPlayer.GetInvolvedSituations` | hud.gui -- situazioni coinvolte | verificato in vanilla hud.gui:3505 |
| `GetPlayer.GetInvolvedStruggles` | hud.gui -- lotte come partecipante | verificato in vanilla hud.gui:3518 |
| `GetPlayer.GetLifestyle` | hud.gui -- stile di vita | verificato in vanilla hud.gui:2366 |
| `GetPlayer.GetPietyLevelTexture` | hud.gui -- texture livello pieta | verificato in vanilla hud.gui:5412 |
| `GetPlayer.GetPrestigeLevelTexture` | hud.gui -- texture livello prestigio | verificato in vanilla hud.gui:5348 |
| `GetPlayer.GetRaidHostilityEnd` | hud.gui -- fine ostilita raid | verificato in vanilla hud.gui:4834 |
| `GetPlayer.GetRaidTargets` | hud.gui -- bersagli raid | verificato in vanilla hud.gui:3480 |
| `GetPlayer.GetSponsoredInspirations` | hud.gui -- ispirazioni sponsorizzate | verificato in vanilla hud.gui:2890 |
| `GetPlayer.GetStressProgress` | hud.gui -- progresso stress | verificato in vanilla hud.gui:1965 |
| `GetPlayer.GetTopLiege.GetGovernment.HasRule` | hud.gui -- regola governo del liege supremo | verificato in vanilla hud.gui:556 |
| `GetPlayer.HasActiveCompanionAISetting` | hud.gui -- AI compagno attivo | verificato in vanilla hud.gui:3372 |
| `GetPlayer.IsAdult` | hud.gui -- e adulto | verificato in vanilla hud.gui:2336 |
| `GetPlayer.IsDynast` | hud.gui -- e dinasta | verificato in vanilla hud.gui:5647 |
| `GetPlayer.IsValid` | hud.gui -- e valido (check null-safety) | verificato in vanilla hud.gui:1461 |
### Binding GetPlayer -- analoghi a Character.X verificati nel vanilla
| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPlayer.GetNumPendingCourtEvents` | hud.gui -- eventi corte in attesa | analogo a `Character.GetNumPendingCourtEvents` verificato in vanilla hud.gui:423 |
| `GetPlayer.GetShortUINameNotMeNoTooltip` | hud.gui -- nome breve UI | analogo a `Character.GetShortUINameNotMeNoTooltip` verificato in vanilla window_barbershop.gui:1447 |
| `GetPlayer.HasRaisedRegiments` | hud.gui -- ha reggimenti alzati | analogo a `Character.HasRaisedRegiments` presente (come commento) in vanilla window_military.gui:115 |
| `GetPlayer.GetTopLiege.MakeScope.ScriptValue` | hud.gui -- script value su scope liege supremo | pattern `MakeScope.ScriptValue` verificato in vanilla window_domicile.gui:3011 |
### Binding OCR upstream -- da OCR-Support/gui/hud.gui (non nel vanilla nativo)
| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPrestigeLevelName` | hud.gui OCR -- nome testuale livello prestigio | binding OCR upstream hud.gui:1714; NON nel vanilla GUI; compatibile con data_binding OCR |
| `GetDynastyPrestigeLevelName` | hud.gui OCR -- nome livello prestigio dinastia | binding OCR upstream hud.gui:1891; NON nel vanilla GUI; compatibile con data_binding OCR |
| `GetPlayer.GetCurrentLocation` | hud.gui OCR -- posizione corrente giocatore | binding OCR (OCR_bindings.txt:92 come replace_with); NON nel vanilla GUI nativo |
---
## Scope e binding -- window_county_view.gui
Verificati in `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/window_county_view.gui`
e in altri file vanilla (citati nelle note).
### Funzioni sistema/confronto -- verificate nel vanilla
| Scope / Binding | Contesto | Note |
|---|---|---|
| `EqualTo_uint32` | window_county_view.gui -- confronto uint uguale | verificato in vanilla window_culture.gui:1228 |
| `GetCommandDesc` | window_county_view.gui -- descrizione comando | verificato in vanilla window_court_positions.gui:82 |
| `IsDataModelEmpty` | window_county_view.gui -- datamodel vuoto | verificato in vanilla window_county_view.gui:2643 |
| `IsValidCommand` | window_county_view.gui -- comando valido | verificato in vanilla window_court_positions.gui:144 |
| `GetVariableSystem.ClearIf` | window_county_view.gui -- cancella var se condizione | verificato in vanilla window_my_realm.gui:49 |
### Binding GetPlayer -- verificati o dedotti dal vanilla
| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPlayer.GetCulture.GetNameNoTooltip` | window_county_view.gui -- nome cultura | `GetPlayer.GetCulture` verificato in vanilla hud.gui:1623; `GetCulture.GetNameNoTooltip` verificato in vanilla window_character_filter.gui:439 |
| `GetPlayer.GetPrimaryTitle.GetNameNoTierNoTooltip` | window_county_view.gui -- nome titolo senza tier | `Title.GetNameNoTierNoTooltip` gia in whitelist (window_faith.gui); `GetPlayer.GetPrimaryTitle` verificato in vanilla window_my_realm.gui:485 |
### Binding OCR upstream -- da OCR-Support/gui/window_county_view.gui
| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPlayer.GetCouncillor` | window_county_view.gui OCR -- consigliere per ruolo | binding OCR upstream (county_view:2623), NON nel vanilla GUI ; `GetPlayer.GetCouncillor('councillor_name')` |
| `GetPlayer.GetFirstNamePossessiveOrMy` | window_county_view.gui OCR -- primo nome possessivo | binding OCR upstream (county_view:387), NON nel vanilla GUI |
| `GetPlayer.HasDomicile` | window_county_view.gui OCR -- ha domicilio | binding OCR upstream (county_view:376), NON nel vanilla GUI |
| `GetPlayer.MakeScope.GetList` | window_county_view.gui OCR -- lista da scope player | pattern Jomini scope; analogo a `Province.MakeScope.GetList` in OCR upstream (county_view:326) |
| `Is` | window_county_view.gui OCR -- shorthand per GetVariableSystem.Exists | shorthand OCR mod; equivalente a `GetVariableSystem.Exists('key')` |
| `Isnt` | window_county_view.gui OCR -- shorthand per Not(GetVariableSystem.Exists) | shorthand OCR mod; equivalente a `Not(GetVariableSystem.Exists('key'))` |
| `Scope.GetProvince` | window_county_view.gui OCR -- scope provincia corrente | pattern Jomini scope accessor in item block di datamodel; NON nel vanilla GUI direttamente |
| `Scope.GetProvince.GetCounty.GetCount.GetTopLiege.GetPrimaryTitle.GetNameNoTooltip` | window_county_view.gui OCR -- catena scope title liege supremo | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.GetCounty.GetName` | window_county_view.gui OCR -- nome contea | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.GetCounty.GetTitle` | window_county_view.gui OCR -- titolo contea | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.GetCounty.GetTitle.GetHolder.GetTopLiege` | window_county_view.gui OCR -- liege supremo | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.GetHolding` | window_county_view.gui OCR -- holding di provincia | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.GetHolding.GetLesseeOrHolder.IsLocalPlayer` | window_county_view.gui OCR -- e local player | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.GetName` | window_county_view.gui OCR -- nome provincia | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.GetTerrain.GetName` | window_county_view.gui OCR -- nome terreno | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.MakeScope.ScriptValue` | window_county_view.gui OCR -- script value su provincia | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.MakeScope.Var` | window_county_view.gui OCR -- variabile scope su provincia | catena OCR su Scope.GetProvince |
| `Scope.GetProvince.PanCameraTo` | window_county_view.gui OCR -- centra camera su provincia | catena OCR su Scope.GetProvince |
| `Scope.Province.MakeScope.GetList` | window_county_view.gui OCR -- lista da scope provincia | pattern Jomini scope; analogo a `Province.MakeScope.GetList` nell OCR |
| `Scope.Title.Custom` | window_county_view.gui OCR -- custom text su scope title | pattern OCR upstream; `Custom` accessor Jomini su scope |
| `Scope.Title.GetHolder.GetTopLiege.RealmSize` | window_county_view.gui OCR -- realm size liege supremo | catena OCR su Scope.Title |
---
## Scope e binding -- window_my_realm.gui (aggiornamento)
Binding verificati dopo l aggiornamento iniziale della sezione window_my_realm.gui.
### Binding GetPlayer -- analoghi a Character.X verificati nel vanilla
| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPlayer.HasOverlord` | window_my_realm.gui -- ha un overlord | analogo a `Character.HasOverlord` verificato in vanilla window_my_realm.gui:324 |
| `GetPlayer.GetDomainLimitTooltip` | window_my_realm.gui -- tooltip limite dominio | analogo a `Character.GetDomainLimitTooltip` verificato in vanilla window_my_realm.gui:829 |
| `GetPlayer.GetOverlord` | window_my_realm.gui -- overlord del giocatore | analogo a `Character.GetOverlord` verificato in vanilla window_my_realm.gui:1000 |
| `GetPlayer.HasVassals` | window_my_realm.gui -- ha vassalli | analogo a `Character.HasVassals` verificato in vanilla hud.gui:6701 |
| `GetPlayer.MakeScope.ScriptValue` | window_my_realm.gui -- script value su scope player | pattern `MakeScope.ScriptValue` verificato in vanilla window_domicile.gui:3011 |
| `LessThan_float` | window_my_realm.gui -- comparazione < float | verificato in vanilla window_ghw.gui:604 e window_war_overview.gui |
### Binding OCR upstream -- da OCR-Support/gui/window_my_realm.gui
| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPlayer.RealmSize` | window_my_realm.gui OCR -- dimensione regno in contee | binding OCR upstream (window_my_realm.gui:183); NON nel vanilla GUI |
| `GetPlayer.UsesObedience` | window_my_realm.gui OCR -- usa sistema obbedienza | binding OCR upstream (window_my_realm.gui:637); NON nel vanilla GUI |
| `Add_CFixedPoint` | window_my_realm.gui OCR -- somma CFixedPoint | binding OCR upstream (window_my_realm.gui:1388); es. `Add_CFixedPoint(Var.GetValue, '(CFixedPoint)1')` |
| `GetVariableSystem.Get` | window_my_realm.gui OCR -- legge valore variabile | binding OCR upstream (window_my_realm.gui:2524); es. `GetVariableSystem.Get('macrobuilder')` |
| `Scope.Title.GetProvince` | window_my_realm.gui OCR -- provincia del titolo in scope | binding OCR upstream (window_my_realm.gui:2699); pattern Scope accessor |
---
## Binding verificati su piu file -- window_military, window_intrigue, window_inventory, window_court, window_character_lifestyle, window_activity_list
### Funzioni confronto/sistema -- verificate nel vanilla
| Scope / Binding | File patch | Note |
|---|---|---|
| `NotEqualTo_CFixedPoint` | window_military.gui | verificato in 19 file vanilla (es. ComplexBarItem context) |
| `LessThanOrEqualTo_CFixedPoint` | window_intrigue.gui | verificato in vanilla window_war_overview.gui:3576 |
| `LessThanOrEqualTo_int32` | window_court.gui | verificato in vanilla window_struggle.gui:570 |
| `Select_int32` | window_intrigue.gui | verificato in vanilla window_succession_event.gui:643 |
| `Select_CVector2f` | window_activity_list.gui | verificato in vanilla window_decisions.gui:204 |
| `GetNumberAbove_int32` | window_intrigue.gui | verificato in vanilla window_character.gui:1492 |
| `IsDateAfter` | window_activity_list.gui | verificato in vanilla window_travel_planner.gui:190 |
| `IsGameViewDataShown` | window_activity_list.gui | verificato in vanilla window_activity.gui:628 |
| `GetCourtPositionType` | window_inventory.gui | verificato in vanilla window_travel_planner.gui:762; es. `GetCourtPositionType('role_name').GetName()` |
### Binding GetPlayer -- verificati nel vanilla
| Scope / Binding | File patch | Note |
|---|---|---|
| `GetPlayer.HasCompanionAI` | window_military.gui | verificato in vanilla window_army_automation_options.gui:170 |
| `GetPlayer.IsIndependentRuler` | window_military.gui | verificato in vanilla window_council.gui:78 |
| `GetPlayer.GetLifestyle.IsValid` | window_character_lifestyle.gui | verificato in vanilla window_character_lifestyle.gui:617 |
### Funzioni UI army detail -- verificate in vanilla window_military.gui
| Scope / Binding | File patch | Note |
|---|---|---|
| `IsAdministrativeArmyDetailViewShown` | window_military.gui | verificato in vanilla window_military.gui:1936 |
| `IsHireableRulerDetailViewShown` | window_military.gui | verificato in vanilla window_military.gui:2422 |
| `IsHolyOrderDetailViewShown` | window_military.gui | verificato in vanilla window_military.gui:3403 |
| `IsMercenaryCompanyDetailViewShown` | window_military.gui | verificato in vanilla window_military.gui:3121 |
### Binding OCR upstream -- non nel vanilla GUI nativo
| Scope / Binding | File patch | Note |
|---|---|---|
| `Scope.War` | window_military.gui OCR | binding OCR upstream (window_military.gui:1431); pattern Scope accessor per War |
| `Scope.Artifact` | window_inventory.gui OCR | binding OCR upstream (window_inventory.gui:891); pattern Scope accessor per Artifact |
| `Scope.Artifact.GetOwner` | window_inventory.gui OCR | binding OCR upstream (window_inventory.gui:903); catena su Scope.Artifact |
| `GetVariableSystem.SetOrToggle` | window_intrigue.gui OCR | variante con prefisso Get di `VariableSystem.SetOrToggle` verificato in vanilla window_royal_court.gui:1087 |
> Nota: `GetIndexString` non e un binding Jomini -- e un custom widget type definito nel patch (`type GetIndexString = text_single`). Lo scope extractor lo rileva per falso positivo. Aggiunto in whitelist solo per silenziare il warning.

| `GetIndexString` | window_character_lifestyle.gui -- custom widget type OCR | NON un binding Jomini; e un `type GetIndexString = text_single` definito nel patch; lo scope extractor lo segnala per falso positivo |

---

## Scope e binding -- window_army.gui

Verificati in `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/window_army.gui` e
in `../CK3-OCR/OCR-Support/gui/window_army.gui`.

### Binding GetPlayer -- verificati in vanilla window_army.gui

| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPlayer.CanRaid` | window_army.gui -- controllo permesso raid | verificato in vanilla window_army.gui (1 occorrenza) |

### Binding SelectedUnitItem -- verificati in vanilla window_army.gui

| Scope / Binding | Contesto | Note |
|---|---|---|
| `SelectedUnitItem.IsGatheringArmy` | window_army.gui -- esercito in raccolta | verificato in vanilla window_army.gui (4 occorrenze) |
| `SelectedUnitItem.GetArmy.IsEmbarked` | window_army.gui -- esercito imbarcato | verificato in vanilla window_army.gui (4 occorrenze) |
| `SelectedUnitItem.GetArmy.GetSoldierCount` | window_army.gui -- conteggio soldati | verificato in vanilla window_army.gui (dal count di GetSoldierCount: 7 occorrenze) |
| `SelectedUnitItem.GetTooltip` | window_army.gui -- tooltip item unita' | in vanilla window_army.gui (usato come valore tooltip) |
| `SelectedUnitItem.IsShown` | window_army.gui -- item visibile/selezionato | verificato in vanilla window_army.gui |
| `SelectedUnitItem.OnClick` | window_army.gui -- click su item unita' | verificato in vanilla window_army.gui |
| `SelectedUnitItem.OnRightClick` | window_army.gui -- click destro su item unita' | verificato in vanilla window_army.gui |

### Binding Scope.GetProvince -- verificati in vanilla window_army.gui

| Scope / Binding | Contesto | Note |
|---|---|---|
| `Scope.GetProvince.GetRaidLoot` | window_army.gui -- bottino raid della provincia | vanilla window_army.gui (2 occorrenze come GetRaidLoot) |
| `Scope.GetProvince.GetTitle` | window_army.gui -- titolo diretto della provincia | catena OCR; `Province.GetTitle` presente in vanilla come pattern generale |

### Binding OCR upstream -- da OCR-Support/gui/window_army.gui (non nel vanilla nativo)

| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetPlayer.IsAtWar` | window_army.gui OCR -- giocatore in guerra | NON in vanilla window_army.gui; binding OCR upstream |
| `GetPlayer.GetCapitalLocation` | window_army.gui OCR -- posizione capitale | NON in vanilla window_army.gui; binding OCR upstream |
| `GetPlayer.Custom` | window_army.gui OCR -- testo custom su scope player | binding Jomini custom text accessor; NON in window_army.gui vanilla |
| `Scope.Army.GetLocation` | window_army.gui OCR -- location dell'esercito in scope | catena OCR scope accessor su Army |
| `Scope.GetProvince.GetEndOfRecentlyLooted.GetString` | window_army.gui OCR -- fine periodo saccheggio | NON in vanilla window_army.gui; binding OCR upstream |
| `Scope.GetProvince.GetHolding.GetCurrentGarrisonSize` | window_army.gui OCR -- dimensione guarnigione holding | NON in vanilla window_army.gui; binding OCR upstream |
| `Scope.GetProvince.IsRecentlyLooted` | window_army.gui OCR -- provincia recentemente saccheggiata | NON in vanilla window_army.gui; binding OCR upstream |
| `Scope.Province` | window_army.gui OCR -- scope provincia in item block datamodel | pattern OCR scope accessor; analogo a `Scope.GetProvince` gia whitelistato |

### Binding pre-popolati per finestre prossime (B6 — 2026-03-20)

> Pre-popolamento automatico via `scope_extractor.py` su file vanilla.
> Fonte: installazione CK3 1.17.1 locale. Aggiunto da: framework (Fase B6).

| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetIllustration` | window_title.gui -- illustrazione titolo | verificato in vanilla CK3 1.17.1 |
| `IsAdminVassalDetailViewShown` | window_government_administration.gui -- vista dettaglio vassallo admin | verificato in vanilla CK3 1.17.1 |
| `IsAdministrativeRuler` | window_government_administration.gui -- sovrano amministrativo | verificato in vanilla CK3 1.17.1 |

### Binding auto-aggiunti da window_activity.gui (2026-03-20)

| Scope / Binding | Contesto | Note |
|---|---|---|
| `GetTicksSinceLastProgress` | window_activity.gui | verificato in vanilla CK3 1.17.1 |
