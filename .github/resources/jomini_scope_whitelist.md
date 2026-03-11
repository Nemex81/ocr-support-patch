# Jomini Scope Whitelist — CK3 1.17.1

Scope e binding verificati nei file vanilla di CK3 1.17.1.
Copilot NON deve usare scope non presenti qui senza verifica esplicita nel vanilla.

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
Ultimo aggiornamento: 2026-03-11

---

## Scope e binding — window_faith.gui

Verificati direttamente in `../CK3 ORIGINAL VERSION/ck3origin/game/gui/window_faith.gui`.

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
