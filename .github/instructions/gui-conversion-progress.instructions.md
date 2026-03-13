---
applyTo: "**"
---

# Stato Conversioni GUI — CK3 1.17.1

Registro delle finestre del progetto. Consultare prima di iniziare qualsiasi nuova conversione.

Ultimo aggiornamento: 2026-03-12 (Fase 4 — taratura dopo gate rafforzato)

## Convenzione stati

Ogni finestra ha due stati distinti e indipendenti:

- **Convertita**: il file in `ocr_support_compatibility_pach/gui/` contiene entrambi i container OCR e vanilla con visible mutuamente esclusivi.
- **Validata**: l'ultima esecuzione di `python tools/audit.py` ha prodotto esito OK (0 critici, 0 binding assenti, 0 avvertenze non accettate).

Un file può essere convertito ma non validato (avvertenze o critici aperti).
Un file non ancora nella cartella patch si trova nella sezione "Da Convertire".

---

## Convertite — Validate (audit OK)

| File | Dim. | Note | Ultimo audit | Critici | Avv. |
|------|------|------|-------------|---------|------|
| `hud.gui` | 177KB | HUD principale | 2026-03-12 | 0 | 0 |
| `interaction_interfere_in_war_notification.gui` | 2KB | Notifica guerra | 2026-03-12 | 0 | 0 |

---

## Convertite — Revisione Necessaria (CON AVVERTENZE)

Dual-mode presente, nessun critico, ma avvertenze aperte. Verificare prima di dichiarare validata.

| File | Dim. | Note | Ultimo audit | Critici | Avv. | Binding assenti |
|------|------|------|-------------|---------|------|-----------------|
| `interaction_blackmail.gui` | 13KB | Interazione | 2026-03-12 | 0 | 2 | 0 |
| `interaction_menu_window.gui` | 9KB | Menu interazioni | 2026-03-12 | 0 | 4 | 0 |
| `window_activity.gui` | 44KB | Attività | 2026-03-12 | 0 | 6 | 1 |
| `window_army.gui` | ~130KB | Gestione eserciti | 2026-03-12 | 0 | 55 | 0 |
| `window_character.gui` | 187KB | Multi-tab, complessa | 2026-03-12 | 0 | 64 | 2 |
| `window_combat.gui` | 123KB | Dati militari | 2026-03-12 | 0 | 16 | 2 |
| `window_council.gui` | 117KB | Tab task/skills | 2026-03-12 | 0 | 7 | 1 |
| `window_culture.gui` | 99KB | Alberi cultura | 2026-03-12 | 0 | 16 | 2 |
| `window_decisions.gui` | 26KB | Decisioni | 2026-03-12 | 0 | 6 | 0 |
| `window_dynasty_house.gui` | 90KB | Dinastia/casata | 2026-03-12 | 0 | 26 | 0 |
| `window_factions.gui` | 39KB | Fazioni | 2026-03-12 | 0 | 14 | 3 |
| `window_faith.gui` | 137KB | Tab dottrine/siti | 2026-03-12 | 0 | 32 | 0 |

> Nota: `window_army.gui` era erroneamente classificata come "Da Convertire". Il file è presente nella patch con dual-mode funzionante. Spostata qui il 2026-03-12.

---

## Convertite — Bloccanti (critici aperti, fix richiesti)

Dual-mode presente ma con almeno un CRITICO rilevato da `audit.py`. Non dichiarare validata prima della correzione.

| File | Dim. | Note | Ultimo audit | Critici | Avv. |
|------|------|------|-------------|---------|------|
| `window_activity_list.gui` | 30KB | Lista attività | 2026-03-12 | 1 | 7 |
| `window_character_lifestyle.gui` | 73KB | Stile di vita | 2026-03-12 | 3 | 22 |
| `window_county_view.gui` | 269KB | Vista contea | 2026-03-12 | 4 | 45 |
| `window_court.gui` | 38KB | Corte | 2026-03-12 | 1 | 5 |
| `window_intrigue.gui` | 90KB | Schemi/agenti | 2026-03-12 | 1 | 34 |
| `window_inventory.gui` | 82KB | Artefatti | 2026-03-12 | 1 | 15 |
| `window_military.gui` | 91KB | Tab eserciti | 2026-03-12 | 2 | 34 |
| `window_my_realm.gui` | 85KB | Tab regno | 2026-03-12 | 6 | 27 |

---

## Da Convertire (nessun file dual-mode nella patch)

> La colonna **Pattern** indica il valore `--mode` da usare con `assemble_dualmode.py`:
> A=simple | B=tabs | C=complex | D=complex (multi-window). Verificare con `tri_diff.py` prima di confermare.

### Priorità ALTA

| File | Motivazione | Pattern |
|------|-------------|--------|
| `window_war.gui` | Interfaccia guerra | C |
| `window_title.gui` | Gestione titoli | C |
| `window_government.gui` | Governo/leggi | B |

### Priorità MEDIA

| File | Motivazione | Pattern |
|------|-------------|--------|
| `window_vassal_contracts.gui` | Contratti vassalli | B |
| `window_schemes.gui` | Schema dettaglio | B |
| `window_hook.gui` | Ganci/segreti | A |
| `window_travel.gui` | Viaggio | B |

### Priorità BASSA

| File | Motivazione | Pattern |
|------|-------------|--------|
| `window_struggle.gui` | Conflitti regionali | C |

---

> Il workflow completo passo per passo è in `workflow-nuova-finestra.instructions.md`.

---

> Il workflow completo passo per passo è in `workflow-nuova-finestra.instructions.md`.
