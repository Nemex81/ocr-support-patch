# Dependency Map — Type/Template Cross-File nella Patch

Generata: 2026-03-20 | Framework Fase C4
Scopo: identificare dipendenze tra file .gui della patch per ordinare revisioni e prevenire rotture.

---

## Grafo Dipendenze Cross-File

```
window_county_view.gui ──[type: adjacent_county_button]──▸ window_army.gui
window_army.gui ──[template: send_army_click]──▸ window_combat.gui
hud.gui ──[template: close_character]──▸ window_my_realm.gui
```

Catena più lunga: `window_county_view.gui → window_army.gui → window_combat.gui` (2 hop).

---

## Dettaglio Dipendenze

| File consumatore | Risorsa usata | Tipo | File fornitore | Note |
|-----------------|---------------|------|----------------|------|
| `window_army.gui` | `adjacent_county_button` | type | `window_county_view.gui` | Ereditarietà type per pulsante contea adiacente |
| `window_combat.gui` | `send_army_click` | template | `window_army.gui` | Usato 3 volte nel file combattimento |
| `window_my_realm.gui` | `close_character` | template | `hud.gui` | Chiusura finestra personaggio |

---

## Impatto Operativo

Quando si revisiona un file **fornitore**, verificare che i file **consumatori** non vengano rotti:

| Se modifichi... | Controlla anche... |
|-----------------|-------------------|
| `window_county_view.gui` (type `adjacent_county_button`) | `window_army.gui` |
| `window_army.gui` (template `send_army_click`) | `window_combat.gui` |
| `hud.gui` (template `close_character`) | `window_my_realm.gui` |

---

## File Autosufficienti (19/22)

Nessuna dipendenza cross-file interna alla patch. Possono essere revisionati indipendentemente:

`interaction_blackmail.gui`, `interaction_interfere_in_war_notification.gui`,
`interaction_menu_window.gui`, `window_activity.gui`, `window_activity_list.gui`,
`window_character.gui`, `window_character_lifestyle.gui`, `window_council.gui`,
`window_court.gui`, `window_culture.gui`, `window_decisions.gui`,
`window_dynasty_house.gui`, `window_factions.gui`, `window_faith.gui`,
`window_intrigue.gui`, `window_inventory.gui`, `window_military.gui`,
`window_county_view.gui`¹, `hud.gui`¹

> ¹ Questi file **forniscono** risorse ad altri file ma non **consumano** — sono autosufficienti
> per la propria revisione, ma modifiche ai type/template esportati richiedono verifica downstream.
