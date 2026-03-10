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
# Visibilità OCR attiva
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('yes')]"
# Visibilità vanilla attiva
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('no')]"
```

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
Ultimo aggiornamento: 2026-03-10
