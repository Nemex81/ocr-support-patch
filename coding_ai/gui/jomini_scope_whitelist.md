# Jomini Scope Whitelist — CK3 1.17.1

Questo file elenca i scope e i datatype Jomini verificati nei file vanilla di CK3 1.17.1.
Copilot NON deve usare scope non presenti in questa lista senza verifica esplicita.

## Scope GUI principali

- `GetPlayer` — personaggio del giocatore
- `GetCharacter` — personaggio generico (richiede contesto)
- `GetTitle` — titolo (richiede contesto)
- `GetFaith` — fede (richiede contesto)
- `GetCulture` — cultura (richiede contesto)
- `GetDynasty` — dinastia (richiede contesto)
- `GetHouse` — casata (richiede contesto)
- `GetArmy` — esercito (richiede contesto)
- `GetWar` — guerra (richiede contesto)
- `GetFaction` — fazione (richiede contesto)
- `GameRules` — regole di gioco (accesso globale)
- `GetGameRules` — alias per GameRules

## Binding game_rule OCR

```
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('yes')]"
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('no')]"
```

## Pattern binding dati comuni

```
# Oro
text = "[GetPlayer.GetTreasury|0]"
# Pietà
text = "[GetPlayer.GetPiety|0]"
# Prestigio
text = "[GetPlayer.GetPrestige|0]"
# Nome personaggio
text = "[GetPlayer.GetUINameNoTooltip]"
# Data
text = "[GetDate]"
```

## Note critiche

- I binding con `|0` indicano formattazione numerica — usare sempre per valori numerici
- I scope dipendono dal contesto del widget parent — verificare sempre la gerarchia
- In caso di dubbio, aprire il file vanilla corrispondente e copiare il binding esatto

## Aggiornamenti

Aggiornare questo file ogni volta che si verifica un nuovo scope nei file vanilla.
Data ultimo aggiornamento: 2026-03-10
