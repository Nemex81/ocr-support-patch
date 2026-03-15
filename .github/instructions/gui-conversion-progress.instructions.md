---
applyTo: "**"
---

# Stato Conversioni GUI — CK3 1.17.1

Registro delle finestre del progetto. Consultare prima di iniziare qualsiasi nuova conversione.

Ultimo aggiornamento: 2026-03-15 (rigenerazione massiva stabilizzazione crash — tutti i file rigenerati da OCR upstream + vanilla, file vanilla type-separati creati, wrapper troncati convertiti a inline)

## Convenzione stati

Ogni finestra ha due stati distinti e indipendenti:

- **Convertita**: il file in `ocr_support_compatibility_pach/gui/` contiene entrambi i container OCR e vanilla con visible mutuamente esclusivi.
- **Validata**: l'ultima esecuzione di `python tools/audit.py` ha prodotto esito OK (0 critici, 0 binding assenti, 0 avvertenze non accettate).

Un file può essere convertito ma non validato (avvertenze o critici aperti).
Un file non ancora nella cartella patch si trova nella sezione "Da Convertire".

La colonna **Arch.** indica l'architettura dual-mode usata:
- `inline` — Pattern v1.0: entrambi i branch OCR e vanilla nello stesso file wrapper (default retrocompatibile)
- `sep` — Pattern v1.1: branch vanilla estratto in `gui/vanilla/<nome>_patch_vanilla.gui` (type-separated)

---

## Convertite — Validate (audit OK)

| File | Arch. | Dim. | Note | Ultimo audit | Critici | Avv. |
|------|-------|------|------|-------------|---------|------|
| `interaction_interfere_in_war_notification.gui` | inline | 2KB | Notifica guerra | 2026-03-12 | 0 | 0 |

---

## Convertite — Revisione Necessaria (CON AVVERTENZE)

Dual-mode presente, nessun critico, ma avvertenze aperte. Verificare prima di dichiarare validata.

| File | Arch. | Dim. | Note | Ultimo audit | Critici | Avv. | Binding assenti |
|------|-------|------|------|-------------|---------|------|-----------------|
| `hud.gui` | inline | 177KB | HUD principale | 2026-03-13 | 0 | 16 | 0 |
| `window_activity_list.gui` | inline | 51KB | Lista attività — rigenerato inline 2026-03-15 (era v1.1 troncato) | 2026-03-13 | 0 | — | — |
| `interaction_blackmail.gui` | inline | 13KB | Interazione | 2026-03-12 | 0 | 2 | 0 |
| `interaction_menu_window.gui` | inline | 9KB | Menu interazioni | 2026-03-12 | 0 | 4 | 0 |
| `window_activity.gui` | inline | 99KB | Attività — rigenerato inline 2026-03-15 | 2026-03-15 | — | — | — |
| `window_character.gui` | inline | 185KB | Multi-tab, complessa — rigenerato inline 2026-03-15 (era v1.1 troncato) | 2026-03-13 | 0 | — | — |
| `window_combat.gui` | sep | 22KB+52KB | Dati militari — rigenerato v1.1 2026-03-15 | 2026-03-13 | 0 | 16 | 2 |
| `window_character_lifestyle.gui` | sep | 32KB+41KB | Stile di vita — rigenerato v1.1 2026-03-15 | 2026-03-13 | 0 | — | — |
| `window_council.gui` | inline | 83KB | Tab task/skills — rigenerato inline 2026-03-15 (era v1.1 troncato) | 2026-03-13 | 0 | — | — |
| `window_culture.gui` | sep | 50KB+37KB | Alberi cultura — rigenerato v1.1 2026-03-15 | 2026-03-12 | 0 | 16 | 2 |
| `window_decisions.gui` | inline | 27KB | Decisioni — rigenerato inline 2026-03-15 (era v1.1 troncato) | 2026-03-12 | 0 | — | — |
| `window_dynasty_house.gui` | sep | 31KB+45KB | Dinastia/casata — rigenerato v1.1 2026-03-15 | 2026-03-13 | 0 | 26 | 0 |
| `window_court.gui` | sep | 24KB+21KB | Corte — rigenerato v1.1 2026-03-15 | 2026-03-13 | 0 | — | — |
| `window_factions.gui` | inline | 32KB | Fazioni — rigenerato inline 2026-03-15 (era v1.1 troncato) | 2026-03-12 | 0 | — | — |
| `window_faith.gui` | sep | 43KB+29KB | Tab dottrine/siti — rigenerato v1.1 2026-03-15 | 2026-03-15 | — | — | — |
| `window_inventory.gui` | inline | 78KB | Artefatti — rigenerato inline 2026-03-15 | 2026-03-15 | — | — | — |
| `window_intrigue.gui` | inline | 93KB | Schemi/agenti — rigenerato inline 2026-03-15 (era v1.1 troncato) | 2026-03-13 | 0 | — | — |
| `window_county_view.gui` | sep | 137KB+57KB | Vista contea — rigenerato v1.1 2026-03-15 | 2026-03-15 | — | — | — |
| `window_military.gui` | sep | 55KB+35KB | Tab eserciti — rigenerato v1.1 2026-03-15 | 2026-03-13 | 0 | 34 | 0 |
| `window_my_realm.gui` | sep | 88KB+11KB | Tab regno — rigenerato v1.1 2026-03-15 | 2026-03-13 | 0 | 27 | 0 |
| `window_army.gui` | sep | 152KB+37KB | Gestione eserciti — rigenerato v1.1 2026-03-15 | 2026-03-13 | 0 | 55 | 0 |

> Nota: `window_army.gui` era erroneamente classificata come "Da Convertire". Il file è presente nella patch con dual-mode funzionante. Spostata in "Revisione Necessaria" il 2026-03-12. Spostata in "Bloccanti" il 2026-03-13: rilevati 4 critici (icon senza tooltip, righe 1044–1082). Fix applicato il 2026-03-13: 0 critici, 55 avvertenze.

> **Nota 2026-03-15 — RIGENERAZIONE MASSIVA PER STABILIZZAZIONE CRASH**: tutti i file con Pattern v1.1 avevano la cartella `gui/vanilla/` completamente vuota — i tipi vanilla referenziati non esistevano, causando errori di tipo al bootstrap GUI (EXCEPTION_ACCESS_VIOLATION). Fix: rigenerazione completa di tutti i wrapper da sorgente OCR upstream + vanilla. File con wrapper troncato (window_character, window_council, window_activity_list, window_decisions, window_factions, window_intrigue) convertiti a inline. Stato qualità audit da reverificare in sessione successiva. Dati "-" nella tabella indicano che l'audit precedente non è più valido dopo la rigenerazione.

> Nota (audit 2026-03-13): `window_court.gui` — 0 critici confermati, 1 critico nel tracker era stima non verificata. Dati: 0 critici, 5 avvertenze, 0 binding assenti, fedeltà OK.

> Stato: `window_court.gui` spostata in **Convertite — Revisione Necessaria** (Ultimo audit 2026-03-13 — 0 critici, 5 avvertenze — tutte datamodel).

> Nota (audit 2026-03-13): `window_activity_list.gui` — 0 critici confermati, 1 critico nel tracker era stima non verificata. Dati: 0 critici, 7 avvertenze (4× datamodel, 3× window radice senza dual-mode), 0 binding assenti, fedeltà MINOR. Le 3 window radice senza dual-mode richiedono verifica manuale in sessione futura.

> Stato: `window_activity_list.gui` spostata in **Convertite — Revisione Necessaria** (Ultimo audit 2026-03-13 — 0 critici, 7 avvertenze — tutte datamodel / root-window checks richieste).

> Nota (audit 2026-03-13): `window_intrigue.gui` — 0 critici confermati, 1 critico nel tracker era stima non verificata. Dati: 0 critici, 34 avvertenze (tutte datamodel senza nota verifica type), 0 binding assenti, fedeltà MINOR.

> Stato: `window_intrigue.gui` spostata in **Convertite — Revisione Necessaria** (Ultimo audit 2026-03-13 — 0 critici, 34 avvertenze — tutte datamodel senza nota verifica type).

> Nota (audit 2026-03-13): `window_inventory.gui` — 0 critici confermati, 1 critico nel tracker era stima non verificata. Dati: 0 critici, 15 avvertenze (tutte datamodel), 0 binding assenti, fedeltà MINOR.

> Nota (audit 2026-03-13): `window_military.gui` — rilevato 1 CRITICO (button senza tooltip, riga 1524). Fix applicato 2026-03-13: aggiunto `tooltip = "[War.GetName]"`. Dati post-fix: 0 critici, 34 avvertenze (tutte datamodel), 0 binding assenti, fedeltà MINOR.

> Nota (audit 2026-03-13): `window_character_lifestyle.gui` — rilevato 1 CRITICO (button SelectFocus senza tooltip, riga 544). Fix applicato 2026-03-13: aggiunto `tooltip = "[FocusType.GetDescription]"`. Dati post-fix: 0 critici, 22 avvertenze (tutte datamodel), 0 binding assenti, fedeltà MINOR.

> Nota (audit 2026-03-13): `window_county_view.gui` — rilevati 4 CRITICI (button senza tooltip, righe 592, 852, 1070, 3147). Fix applicati 2026-03-13: `PROVINCE_CONTROLLER_TOOLTIP` (hostile controller), `[Title.GetNameNoTierNoTooltip]` (capital), `GRANT_TITLE_TOOLTIP` (grant holding), `"Across water adjacent counties, Shift E."` (across_water toggle). Dati post-fix: 0 critici, 45 avvertenze (tutte datamodel), 0 binding assenti, fedeltà MINOR.

---

## Convertite — Bloccanti (critici aperti, fix richiesti)

Dual-mode presente ma con almeno un CRITICO rilevato da `audit.py`. Non dichiarare validata prima della correzione.

| File | Dim. | Note | Ultimo audit | Critici | Avv. |
|------|------|------|-------------|---------|------|

---

## Gestione Alternativa OCR (NON convertire al dual-mode)

Queste finestre NON devono essere convertite al sistema dual-mode.
Il sistema OCR le copre tramite shortcut da tastiera e override completo
in OCR upstream Agamidae. Convertirle causerebbe duplicazione e potenziale
conflitto con i meccanismi esistenti.

| File | Meccanismo OCR alternativo | Shortcut |
|------|---------------------------|----------|
| `window_war_overview.gui` | Override OCR completo (2496 righe) in upstream Agamidae + shortcut apertura | Shift+W |

---

## Da Convertire (nessun file dual-mode nella patch)

> La colonna **Pattern** indica il valore `--mode` da usare con `assemble_dualmode.py`:
> A=simple | B=tabs | C=complex | D=complex (multi-window). Verificare con `tri_diff.py` prima di confermare.

### Priorità ALTA

| File | Motivazione | Pattern |
|------|-------------|--------|
| `window_title.gui` | GAP PARZIALE: info base (nome, contea, liege) già in griglia mappa OCR. Mancano: crea/usurpa/distruggi titolo, linea successione, claimant, storia titolo, vassalli de jure navigabili. | C |
| `window_government_administration.gui` | Governo/leggi | B |

### Priorità MEDIA

| File | Motivazione | Pattern |
|------|-------------|--------|
| `interaction_modify_vassal_window.gui` | Contratti vassalli | B |
| `window_travel_planner.gui` | Pianificazione viaggio | B |
| `window_travel_option_selection.gui` | Selezione opzioni viaggio | A |
| `window_travel_route_edit.gui` | Modifica rotta viaggio | A |

### Priorità BASSA

| File | Motivazione | Pattern |
|------|-------------|--------|
| `window_struggle.gui` | Conflitti regionali | C |

---

> Il workflow completo passo per passo è in `workflow-nuova-finestra.instructions.md`.

> Note sui file rimossi: `window_schemes.gui` e `window_hook.gui` non esistono come finestre separate in vanilla né in OCR upstream — `window_hook.gui` non ha controparte, la logica degli schemi è già inclusa in `window_intrigue.gui` (presente nella patch).
