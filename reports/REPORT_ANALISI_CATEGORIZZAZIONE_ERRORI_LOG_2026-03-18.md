# Report analisi incrociata log CK3

Data analisi: 2026-03-18
Obiettivo: categorizzare gli errori per importanza e per mod/fonte collegata, raggruppando i problemi correlati.

## 1) Fonti analizzate

- Patch attiva: ocr_support_compatibility_pach/gui/
- Vanilla CK3: C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/
- OCR upstream: ../CK3-OCR/OCR-Support/gui/
- Log runtime: C:/Users/nemex/Documents/Paradox Interactive/Crusader Kings III/logs/

File log letti:
- error.log
- gui_warnings.log
- debug.log
- game.log
- setup.log
- system.log
- text.log
- message.log
- multiplayer.log
- profile.log
- database_conflicts.log
- custom_automated_stats.log
- dedicated_server.log
- memory.log
- code_revisions.log

## 2) Sintesi esecutiva

Il volume errori e' concentrato quasi interamente in cluster GUI ripetitivi e fortemente correlati tra loro.
La priorita' va data a pochi gruppi ad alto impatto che causano cascata parser/datasystem.

Quadro quantitativo rapido:
- error.log: 1012 errori (linee totali 2189)
- gui_warnings.log: 514 errori + 160 warning (linee totali 1615)
- game.log: 30 errori
- debug.log: 31 errori (ma soprattutto debug/duplicazioni chiavi)

Conclusione operativa:
- il nucleo bloccante e' GUI (parser + data binding)
- il resto (texture mancanti, alcuni errori game.log) e' secondario o conseguenza

## 3) Categorizzazione per mod/fonte collegata

Classificazione su tutte le righe GUI E/W con path gui/...:

- shared-all-patch-ocr-vanilla: 1015
  - file presenti in patch, OCR upstream e vanilla (la patch li puo' sovrascrivere)
- vanilla-only: 119
  - file presenti solo vanilla (spesso effetto cascata da errori a monte)
- ocr+vanilla-no-patch: 42
  - file non presenti nella patch ma presenti in OCR upstream e vanilla
- ocr-only: 29
  - file presenti solo OCR upstream

Lettura pratica:
- La maggior parte dei problemi e' su file che la patch copre direttamente.
- Esiste una quota non trascurabile legata a file non patchati (OCR upstream/vanilla), da trattare in un secondo passaggio mirato.

## 4) Gruppi di errori correlati (con priorita')

### P0 - Gruppo A: parse desync massivo su window_activity.gui
Impatto: critico (rumore enorme, possibile effetto domino su widget/type/property)

Evidenze:
- Duplicate property in error.log:
  - gui/window_activity.gui:412 duplicate text
  - gui/window_activity.gui:498 duplicate text
  - gui/window_activity.gui:681 duplicate visible
- In gui_warnings.log compaiono molte righe correlate:
  - token interpretati come proprieta' invalide
  - not a valid widget/type/property
  - could not find template ''

Volume:
- 653 eventi E/W su questo file (il cluster piu' grande)

Nota tecnica:
- pattern tipico da struttura sbilanciata o blocchi dual-mode non chiusi correttamente.

---

### P0 - Gruppo B: espressioni visibilita' non compatibili in window_faith.gui
Impatto: critico (data statements non parseabili, errore ripetitivo ad alta frequenza)

Evidenze:
- Failed parsing data statement su Or(IsNot(...)) / IsNot(...)
- pattern nel file: Isnt/Has combinati in condizioni tab/doctrine

Volume:
- 120 eventi E/W su window_faith.gui

Nota tecnica:
- il motore segnala funzioni non risolte (IsNot/HasNot) come conversione interna di espressioni non compatibili nel contesto corrente.

---

### P1 - Gruppo C: data context/type non risolti su window_county_view.gui
Impatto: alto (UI parzialmente rotta, errori ripetuti ma piu' confinati)

Evidenze:
- failed converting property datacontext
- binding tipo Building.HasVariants / GUIBuildingItem.GetBuilding non risolti
- errori localizzazione collegati (Title.GetAverageFertilityDesc)

Volume:
- 125 eventi E/W su window_county_view.gui

---

### P1 - Gruppo D: datacontext/localize non risolti su window_character_lifestyle.gui
Impatto: alto (interfaccia lifestyle degradata)

Evidenze:
- failed converting datacontext
- failed parsing localized text ([Perk.GetDescription], [FocusType.GetDescription], ecc.)
- funzioni/type non risolti collegati (PerkGuiItem/PerkTreeItem/FocusItem)

Volume:
- 36 eventi E/W

---

### P1 - Gruppo E: vettori/minimumsize su window_decisions.gui
Impatto: medio-alto (errori ripetitivi ma localizzati)

Evidenze:
- parse fail su Select_CVector2f / CVector2f
- nella patch presenti pattern stringati '(CVector2f)527,65' che risultano fragili in parsing

Volume:
- 8 eventi E/W (ma sintomo strutturale da correggere presto)

---

### P2 - Gruppo F: file non patchati (OCR upstream/vanilla) con widget/type mancanti
Impatto: medio (puo' dipendere da load order e da dipendenze non allineate)

File ricorrenti:
- gui/window_activity_locale.gui (non in patch)
- gui/window_hybridize_culture.gui (non in patch)
- gui/window_manage_tax_slots.gui (non in patch)
- gui/preload/00_types_OCR.gui (OCR-only)
- gui/_OCR_WIDGET.gui (OCR-only)

Evidenze:
- not a valid widget/type/property
- missing widget in plugin widget
- unknown game view ''

Interpretazione:
- cluster probabilmente legato a overlay OCR upstream + altri override, non direttamente a un file patchato singolo.

---

### P2 - Gruppo G: asset/texture mancanti
Impatto: medio (degrado visuale; meno probabile causa primaria)

Texture mancanti ricorrenti:
- gfx/interface/icons/icon_fertility.dds
- gfx/interface/icons/symbols/icon_variants.dds
- gfx/interface/window_legend/chronicle_marginalia_divider.dds
- gfx/interface/window_duel_event_window/decoration_frame_bottom_thin_duel.dds

---

### P3 - Gruppo H: errori game.log non GUI
Impatto: basso-medio (non primo target finche' i P0/P1 non sono risolti)

Evidenze:
- culture_history_entry: innovazioni bloccate (set iniziale/culture mod)
- succession_order invalid su personaggio specifico

## 5) Ordine di priorita' consigliato (focus per gruppi)

Ordine proposto per massimizzare riduzione errori rapida:

1. Gruppo A (window_activity)
2. Gruppo B (window_faith)
3. Gruppo C (window_county_view)
4. Gruppo D (window_character_lifestyle)
5. Gruppo E (window_decisions)
6. Gruppo F (non patchati OCR/vanilla, con verifica load order)
7. Gruppo G (texture mancanti)
8. Gruppo H (gameplay non GUI)

Razionale:
- A+B spiegano la parte maggiore del rumore e generano cascata.
- C+D sono il secondo blocco ad alta densita'.
- E e' un fix puntuale ma utile per pulizia parser.
- F/G/H vanno affrontati dopo stabilizzazione GUI core.

## 6) Cluster di lavoro pratici (per sessioni successive)

Sessione 1 (alta resa):
- solo window_activity + window_faith
- target: abbattere almeno il 60-70% degli errori GUI totali

Sessione 2:
- window_county_view + window_character_lifestyle

Sessione 3:
- window_decisions + gruppo file non patchati (OCR upstream/vanilla no patch)

Sessione 4:
- texture e residui game.log

## 7) Evidenze puntuali (estratti)

Esempi da error.log:
- duplicate property: linee 3, 6, 9
- invalid widget/type/property: linee 56, 58, 60, 84, 152
- faith parsing Or(IsNot...): linee 54, 73, 136, 336, 370
- county datacontext fail: linee 77, 626, 637, 652, 668
- lifestyle datacontext fail: linee 43, 116, 157, 162
- texture missing: linee 83, 88, 170, 177, 184
- unlocalized text: linee 62, 63, 286, 287, 288
- lexer backslash: linee 1, 12, 14

## 8) Nota metodologica

L'analisi e' stata fatta in lettura sui log effettivi e confronto incrociato con i tre domini sorgente (patch, OCR upstream, vanilla) per attribuzione per-fonte. Il report e' di triage/prioritizzazione: non include ancora fix, solo ordinamento operativo e cluster correlati.
