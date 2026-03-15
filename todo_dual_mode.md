# TODO — Migrazione Finestre al Pattern Type-Separated (v1.1)

> **Regola inderogabile:** aggiornare questo file spuntando le checkbox al termine di ogni finestra
> completata, prima di passare alla successiva. Registrare anche eventuali blocchi o avvertenze.
>
> **Prerequisito assoluto:** `todo_framework.md` interamente completato (tutte le fasi 0–5
> spuntate) prima di iniziare qualsiasi migrazione in questo file.
>
> Branch di lavoro: `experiment/dual-mode-type-separation`
> Ultimo aggiornamento: 2026-03-14

---

## Legenda

- `[ ]` — da fare
- `[x]` — completato (wrapper + type + audit OK)
- `[~]` — in corso
- `⚠️` — avvertenze aperte o verifica manuale richiesta
- `GATE` — checkpoint bloccante: non procedere senza superarlo

---

## Convenzione naming applicata a tutte le migrazioni

| Elemento | Convenzione |
|----------|-------------|
| Folder type file | `ocr_support_compatibility_pach/gui/vanilla/` |
| Nome type | `{finestra_senza_window}_patch_vanilla` |
| Nome file type | `{finestra_senza_window}_patch_vanilla.gui` |
| Blocco types | `types OCR_PATCH_VANILLA { }` |
| Guard nel type | `visible = "[GetVariableSystem.Exists('ocr')]"` |
| Istanziazione wrapper | `{finestra_senza_window}_patch_vanilla = {}` |

---

## FASE 0 — PoC tecnico (gate d'ingresso del sistema)

Verifica che il meccanismo funzioni in CK3 prima di qualsiasi migrazione reale.
**Non procedere alla Fase 1 se questo PoC fallisce in-game.**
- [~] **F0.1** `interaction_interfere_in_war_notification.gui` — PoC tecnico minimo
  - Pattern: A (simple)
  - Motivazione: file più piccolo (186 righe), già validato, rischio contenuto
  - Scopo: verificare che CK3 carichi correttamente un file type in `gui/vanilla/`
  - Output atteso: `interaction_interfere_in_war_notification.gui` (wrapper ridotto) +
    `gui/vanilla/interfere_in_war_notification_patch_vanilla.gui` (type)
  - ⚠️ Verifica in-game obbligatoria: aprire la notifica e confermare rendering corretto in entrambe le modalità
  - ⚠️ audit.py deve produrre report coppia senza critici

> **GATE 0:** PoC confermato in-game (OCR + vanilla entrambi visibili e corretti).
> Se fallisce: NON procedere — investigare e correggere tool o pattern prima di continuare.

---

## FASE 1 — PoC realistici semplici (Pattern A)

Finestre semplici, singolo wrapper, struttura lineare.

- [~] **F1.1** `window_decisions.gui` — Pattern A, ottimo candidato PoC reale
  - Dimensione attuale: 26KB, ~1041 righe patch
  - Beneficio atteso: medio (semplice ma buon benchmark)
  - Output: `window_decisions.gui` (wrapper) + `gui/vanilla/decisions_patch_vanilla.gui`
  - Upstream vanilla Agamidae: ❌ non presente in `gui/vanilla/`

- [~] **F1.2** `window_my_realm.gui` — Pattern B, upstream vanilla disponibile
  - Dimensione attuale: 85KB, ~2858 righe patch
  - Beneficio atteso: alto
  - Output: `window_my_realm.gui` (wrapper) + `gui/vanilla/my_realm_patch_vanilla.gui`
  - Upstream vanilla Agamidae: ✅ `gui/vanilla/window_my_realm.gui` già presente

> **GATE 1:** Entrambi i file migrati, audit OK su coppia, nessun critico aperto.

---

## FASE 2 — Stress test pattern B (Tab + SubWindows)

Verifica che il pattern regga con tab navigation e sub-windows modali.

- [~] **F2.1** `window_council.gui` — Pattern B, stress test tabs
  - Dimensione attuale: 117KB, ~2389 righe patch
  - Beneficio atteso: alto
  - Output: `window_council.gui` + `gui/vanilla/council_patch_vanilla.gui`
  - ⚠️ Ogni tab potrebbe richiedere type vanilla dedicato — valutare struttura prima del dry-run
  - Upstream vanilla Agamidae: ❌ non presente in `gui/vanilla/`

- [~] **F2.2** `window_military.gui` — Pattern B, upstream vanilla disponibile
  - Dimensione attuale: 91KB, ~3182 righe patch
  - Upstream vanilla Agamidae: ✅ `gui/vanilla/window_military.gui` già presente
  - Output: `window_military.gui` + `gui/vanilla/military_patch_vanilla.gui`

> **GATE 2:** Pattern B validato. Verificare che sub-windows con tabs funzionino correttamente
> in entrambe le modalità prima di procedere ai file grandi.

---

## FASE 3 — File medi — beneficio immediato

Finestre medie con beneficio concreto immediato in leggibilità e manutenibilità.

- [~] **F3.1** `window_intrigue.gui` — Pattern C
  - Dimensione attuale: 90KB, ~3292 righe patch
  - Beneficio atteso: alto (molto testo vanilla inline attualmente)

- [~] **F3.2** `window_court.gui` — Pattern C
  - Dimensione attuale: 38KB, ~1266 righe patch
  - Beneficio atteso: medio

- [~] **F3.3** `window_character_lifestyle.gui` — Pattern C
  - Dimensione attuale: 73KB, ~2558 righe patch
  - Beneficio atteso: alto

- [~] **F3.4** `window_inventory.gui` — Pattern C
  - Dimensione attuale: 82KB, ~2906 righe patch
  - Beneficio atteso: alto

- [~] **F3.5** `window_factions.gui` — Pattern B
  - Dimensione attuale: 39KB, ~1467 righe patch
  - Beneficio atteso: medio

- [~] **F3.6** `window_combat.gui` — Pattern C
  - Dimensione attuale: 123KB, ~3160 righe patch
  - Beneficio atteso: alto (molti tipi condivisi da verificare)
  - ⚠️ Types condivisi esistenti: verificare che non interferiscano con la separazione

> **GATE 3:** Almeno 4 delle 6 finestre della fase completate con audit OK prima di procedere.

---

## FASE 4 — File grandi — alto impatto

Finestre grandi che beneficiano maggiormente dalla separazione.

- [~] **F4.1** `window_activity_list.gui` — Pattern B
  - Dimensione attuale: 30KB, ~1197 righe patch
  - Note: 3 window radice senza dual-mode (avvertenza aperta) — verificare prima della migrazione

- [~] **F4.2** `window_activity.gui` — Pattern B+
  - Dimensione attuale: 44KB, ~1676 righe patch
  - ⚠️ Tab child: attenzione ai tab child nella separazione

- [~] **F4.3** `window_dynasty_house.gui` — Pattern C
  - Dimensione attuale: 90KB, ~3635 righe patch
  - Beneficio atteso: alto

- [~] **F4.4** `window_character.gui` — Pattern C (al massimo beneficio)
  - Dimensione attuale: 187KB, ~7385 righe patch
  - Beneficio atteso: massimo (4975 righe vanilla stimate)
  - ⚠️ File enorme — massima attenzione a multi-tab e datacontext
  - ⚠️ Valutare un type per tab, non un solo type monolitico

> **GATE 4:** Completare F4.4 (`window_character.gui`) dimostra la maturità del pattern
> su file di grandi dimensioni. Obbligatorio prima di procedere alle finestre ad alto rischio.

---

## FASE 5 — Complessità alta (Pattern D)

Finestre multi-window interconnesse. Alto beneficio ma alto rischio operativo.

- [~] **F5.1** `window_faith.gui` — Pattern D
  - Dimensione attuale: 137KB, ~2776 righe patch
  - ⚠️ Multi-window con tab dottrine e siti sacri — richede disciplina nella separazione

- [~] **F5.2** `window_culture.gui` — Pattern D
  - Dimensione attuale: 99KB, ~3832 righe patch
  - ⚠️ Alberi cultura: struttura complessa con nodi navigabili

- [~] **F5.3** `window_county_view.gui` — Pattern D (massima complessità)
  - Dimensione attuale: 269KB, ~8718 righe patch
  - Beneficio atteso: massimo (alleggerimento enorme del wrapper)
  - ⚠️ File più grande della patch — migrazione da pianificare in più sessioni
  - ⚠️ 45 avvertenze aperte (tutte datamodel) — verificare prima della migrazione

> **GATE 5:** Pattern D validato su almeno F5.1 prima di procedere ai casi critici.

---

## FASE 6 — Casi critici (ultimi — nessuna fretta)

File con complessità operativa massima. Migrare solo dopo che il pattern è pienamente stabile.

- [~] **F6.1** `window_army.gui` — script specializzato
  - Dimensione attuale: ~130KB, ~8290 righe patch
  - ⚠️ Script specializzato `assemble_army_dualmode.py` — aggiornarlo per supportare `--separate-vanilla`
  - ⚠️ Fix critico 2026-03-13 recente — verificare stabilità prima della migrazione
  - Note: 55 avvertenze aperte (tutte datamodel)

- [ ] **F6.2** `hud.gui` — rischio massimo
  - Dimensione attuale: 177KB, ~7167 righe patch
  - Beneficio atteso: massimo (6810 righe vanilla stimate)
  - ⚠️ HUD principale di gioco — dipendenze da stati e layer di primaria importanza
  - ⚠️ Migrazione da pianificare in sessione dedicata con verifica in-game estesa
  - Note: 16 avvertenze aperte

> **GATE 6 (finale):** Entrambi i file migrati, audit OK coppia, verificati in-game.
> Questo gate segna il completamento della migrazione completa al pattern v1.1.

---

## Interazioni (già convertite — NON migrare per ora)

File piccoli dove il beneficio della separazione è minimo.
Decidere in una sessione futura se vale la pena migrare.

- `interaction_blackmail.gui` — 13KB, beneficio modesto
- `interaction_menu_window.gui` — 9KB, beneficio modesto
- `interaction_interfere_in_war_notification.gui` — 2KB, usato solo come PoC (F0.1)

---

## Finestre Da Convertire (conversione + migrazione simultanea)

Le seguenti finestre non sono ancora convertite al dual-mode. Quando saranno convertite,
applicare direttamente il pattern type-separated v1.1 se la dimensione lo giustifica.

| File | Pattern | Priorità | Note migrazione v1.1 |
|------|---------|----------|---------------------|
| `window_title.gui` | C | ALTA | Candidato diretto a separazione, file grande |
| `window_government_administration.gui` | B | ALTA | Valutare separazione se > 1500 righe |
| `interaction_modify_vassal_window.gui` | B | MEDIA | Probabilmente inline (file piccolo) |
| `window_travel_planner.gui` | B | MEDIA | Valutare dimensione post-conversione |
| `window_travel_option_selection.gui` | A | MEDIA | Probabilmente inline |
| `window_travel_route_edit.gui` | A | MEDIA | Probabilmente inline |
| `window_struggle.gui` | C | BASSA | Valutare |

---

## Riepilogo avanzamento

| Fase | Descrizione | Finestre | Completate |
|------|-------------|----------|-----------|
| Fase 0 | PoC tecnico | 1 | 0/1 |
| Fase 1 | PoC realistici Pattern A | 2 | 0/2 |
| Fase 2 | Stress test Pattern B | 2 | 0/2 |
| Fase 3 | File medi | 6 | 0/6 |
| Fase 4 | File grandi | 4 | 0/4 |
| Fase 5 | Complessità alta Pattern D | 3 | 0/3 |
| Fase 6 | Casi critici | 2 | 0/2 |
| **Totale** | | **20** | **0/20** |

---

## Avanzamento Tecnico Sessione 2026-03-14 (esecuzione autonoma)

Stato corrente dopo esecuzione batch `assemble_dualmode --separate-vanilla` + `audit.py`:

- ✅ PoC scritto: `interaction_interfere_in_war_notification.gui` + type file creato
- ⚠️ PoC audit: `CON AVVERTENZE` (0 critici, 1 avvertenza)
- ❌ Assemble fallito (nessuna window trovata):
  - `hud.gui`
- ⚠️ Audit BLOCCANTE dopo migrazione: `window_county_view`, `window_army`
- ⚠️ Audit CON AVVERTENZE: `window_decisions`, `window_my_realm`, `window_council`, `window_military`, `window_intrigue`, `window_court`, `window_character_lifestyle`, `window_inventory`, `window_factions`, `window_combat`, `window_activity_list`, `window_activity`, `window_dynasty_house`, `window_character`, `window_faith`, `window_culture`

### Blocco operativo attuale

Il piano non puo' essere marcato completato (`[x]`) per le finestre in stato `[~]` finché:

1. I casi `ASSEMBLE_FAIL` non vengono risolti in `tools/assemble_dualmode.py`
2. I casi `BLOCCANTE` non raggiungono almeno `CON AVVERTENZE` senza critici
3. Ogni finestra non ottiene audit OK secondo la definizione del TODO (`wrapper + type + audit OK`)
