# Priority List — Finestre da Convertire

Stato aggiornato al: 2026-03-10
Criterio priorità: frequenza d'uso in-game + complessità strutturale

## ✅ Già Convertite

| File | Dimensione | Note |
|------|-----------|------|
| `window_character.gui` | 187KB | Multi-tab, complessa |
| `window_council.gui` | 117KB | Tab task/skills |
| `window_culture.gui` | 99KB | Alberi cultura |
| `window_faith.gui` | 137KB | Tab dottrine/siti |
| `window_combat.gui` | 123KB | Dati militari |
| `window_intrigue.gui` | 90KB | Schemi/agenti |
| `window_inventory.gui` | 82KB | Artefatti |
| `window_military.gui` | 91KB | Tab eserciti |
| `window_my_realm.gui` | 85KB | Tab regno |
| `window_dynasty_house.gui` | 90KB | Dinastia/casata |
| `window_county_view.gui` | 269KB | Vista contea |
| `window_court.gui` | 38KB | Corte |
| `window_decisions.gui` | 26KB | Decisioni |
| `window_activity.gui` | 44KB | Attività |
| `window_activity_list.gui` | 30KB | Lista attività |
| `window_character_lifestyle.gui` | 73KB | Stile di vita |
| `window_factions.gui` | 39KB | Fazioni |
| `hud.gui` | 177KB | HUD principale |
| `interaction_blackmail.gui` | 13KB | Interazione |
| `interaction_menu_window.gui` | 9KB | Menu interazioni |
| `interaction_interfere_in_war_notification.gui` | 2KB | Notifica guerra |

## 🔄 Da Convertire (alta priorità)

| File | Priorità | Motivazione |
|------|----------|-------------|
| `window_army.gui` | ALTA | Gestione eserciti, uso frequente |
| `window_war.gui` | ALTA | Interfaccia guerra |
| `window_title.gui` | ALTA | Gestione titoli |
| `window_government.gui` | ALTA | Governo/leggi |
| `window_vassal_contracts.gui` | MEDIA | Contratti vassalli |
| `window_schemes.gui` | MEDIA | Schema dettaglio |
| `window_hook.gui` | MEDIA | Ganci/segreti |
| `window_travel.gui` | MEDIA | Viaggio |
| `window_struggle.gui` | BASSA | Conflitti regionali |

## Note Operative

Per iniziare una nuova conversione, usare il prompt:
`.github/prompts/converti-finestra-dual-mode.prompt.md`

Per verificare una finestra già convertita:
`.github/prompts/verifica-dual-mode.prompt.md`
