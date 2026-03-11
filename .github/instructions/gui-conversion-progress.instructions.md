---
applyTo: ".github/**"
---

# Stato Conversioni GUI — CK3 1.17.1

Registro delle finestre già convertite e da convertire.
Consultare prima di iniziare qualsiasi nuova conversione.

Ultimo aggiornamento: 2026-03-10

---

## Già Convertite

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

---

## Da Convertire

### Priorità ALTA

| File | Motivazione |
|------|-------------|
| `window_army.gui` | Gestione eserciti, uso frequente |
| `window_war.gui` | Interfaccia guerra |
| `window_title.gui` | Gestione titoli |
| `window_government.gui` | Governo/leggi |

### Priorità MEDIA

| File | Motivazione |
|------|-------------|
| `window_vassal_contracts.gui` | Contratti vassalli |
| `window_schemes.gui` | Schema dettaglio |
| `window_hook.gui` | Ganci/segreti |
| `window_travel.gui` | Viaggio |

### Priorità BASSA

| File | Motivazione |
|------|-------------|
| `window_struggle.gui` | Conflitti regionali |

---

## Workflow per Nuova Conversione

0. **[Pre-analisi]** `python tools/tri_diff.py --window nome_file` — report strutturale tra i 3 repo
1. Aprire il file vanilla da `../CK3 ORIGINAL VERSION/ck3origin/game/gui/`
2. Aprire il file OCR upstream da `../CK3-OCR/OCR-Support/gui/`
3. Identificare struttura widget vanilla (tipo, nome, gerarchia)
4. Costruire il container OCR rispettando la stessa gerarchia informativa
5. Incapsulare il vanilla nel container vanilla **senza modifiche**
6. Verificare che le due visibility siano mutuamente esclusive
7. `python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/nome_file.gui` — aggiornare whitelist se necessario
8. `python tools/gui_validator.py --file ocr_support_compatibility_pach/gui/nome_file.gui` — risolvere tutti i CRITICO prima di committare
9. Eseguire la checklist pre-commit in `gui-jomini.instructions.md`
10. Aggiornare questo file spostando la voce in "Già Convertite"
