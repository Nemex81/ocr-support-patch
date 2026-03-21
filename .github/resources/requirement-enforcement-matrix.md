# Matrice Requisito → Enforcement — OCR Support Patch

Creata: 2026-03-12 (Fase 1 del Framework Improvement Plan)

Ogni riga mappa un requisito del framework a:
- **Tipo**: lint strutturale / gate automatico / review manuale
- **Owner**: tool Python, skill Copilot, o agente
- **Blocking**: se il mancato rispetto blocca il commit

---

## Legenda colonne

| Colonna | Descrizione |
|---------|-------------|
| Requisito | Regola dichiarata nel framework |
| Fonte | File di istruzione o documento che lo definisce |
| Tipo | `lint` = controllo sintattico locale; `gate` = verificato in audit.py; `manuale` = richiede sign-off umano |
| Owner attuale | Chi lo controlla oggi |
| Blocking | `SI` = blocca il gate; `NO` = avvertenza non bloccante; `MANCANTE` = requisito dichiarato ma nessun enforcement esiste |
| Note | Gap o stati transitori |

---

## Struttura dual-mode

| Requisito | Fonte | Tipo | Owner attuale | Blocking | Note |
|-----------|-------|------|--------------|---------|------|
| Presenza container OCR (`visible = "[Not(GetVariableSystem.Exists('ocr'))]"`) | gui-jomini.instructions.md | gate | gui_validator.py – `_trova_blocchi_modalita` | SI | Pattern `ocr_mode_content`, `ocr_*`, `normal_mode_content` riconosciuti |
| Presenza container vanilla (`visible = "[GetVariableSystem.Exists('ocr')]"`) | gui-jomini.instructions.md | gate | gui_validator.py – `_trova_blocchi_modalita` | SI | Pattern `vanilla_*`, `grafic_version` riconosciuti |
| Visibilità mutuamente esclusiva | gui-jomini.instructions.md | gate | gui_validator.py – controllo inversione | SI | Controlla che i due `visible` siano opposti |
| Pattern vietati (GameRules.GetRule) | copilot-instructions.md | gate | gui_validator.py – check deprecati | SI | |
| Pattern vietati (show_when, ROOT., THIS.) | gui-jomini-scopes.instructions.md | gate | gui_validator.py – check forbidden | SI | |
| Copertura dual-mode in sub-window e file multi-window | gui-jomini.instructions.md | gate | gui_validator.py – `_scansione_copertura_multiwindow` | SI (critico) | Risolto B1: escalation a CRITICO + fix finestra ricerca |

---

## Accessibilità OCR (NVDA)

| Requisito | Fonte | Tipo | Owner attuale | Blocking | Note |
|-----------|-------|------|--------------|---------|------|
| Fontsize ≥ 18 nel blocco OCR | gui-jomini.instructions.md | gate | gui_validator.py – check fontsize | SI (warn) | Produce avvertenza, non critico |
| Header OCR: fontsize 20, colore `{ 255 221 136 255 }` | gui-jomini.instructions.md | gate | gui_validator.py – `_scansione_header_ocr` | SI (critico) | Risolto B3: escalation colore a CRITICO. Fontsize: non ancora |
| Tooltip obbligatorio su ogni pulsante/icona nel blocco OCR | gui-jomini.instructions.md | gate | gui_validator.py – check tooltip | SI (warn) | Produce avvertenza; non blocca ma è segnalato |
| Ordine di lettura NVDA coerente | gui-jomini.instructions.md | manuale | revisore-accessibilita.agent.md | NO | Non verificabile automaticamente |
| Parità funzionale OCR/vanilla (stesse azioni disponibili) | gui-jomini.instructions.md | manuale | revisore-accessibilita.agent.md | NO | Nessun controllo automatico; Fase 2 (completezza OCR) |
| Fallback testo per liste vuote nel blocco OCR | gui-jomini.instructions.md | gate | gui_validator.py – `_scansione_fallback_datamodel_ocr` | SI (critico) | Risolto B2: escalation a CRITICO |

---

## Fedeltà vanilla

| Requisito | Fonte | Tipo | Owner attuale | Blocking | Note |
|-----------|-------|------|--------------|---------|------|
| Container vanilla = copia fedele del CK3 originale | copilot-instructions.md | gate | audit.py → tri_diff.analizza_fedelta | SI (avvertenza) | Risolto B4: DISCREPANZE → CON AVVERTENZE |
| Nessuna modifica al container vanilla | copilot-instructions.md | manuale | revisore-vanilla.agent.md | NO | Solo review manuale oggi |
| Nested window/sub-window vanilla inalterati | gui-jomini.instructions.md | manuale | revisore-vanilla.agent.md | NO | Nessun controllo automatico |

---

## Binding e scope

| Requisito | Fonte | Tipo | Owner attuale | Blocking | Note |
|-----------|-------|------|--------------|---------|------|
| Ogni binding usato deve essere nella whitelist | gui-jomini-scopes.instructions.md | gate | scope_extractor.py + whitelist.md | SI (warn) | ASSENTE produce avvertenza; DA VERIFICARE produce BLOCCANTE |
| Non inventare binding — copiare dal vanilla | copilot-instructions.md | manuale | Implementatore Patch | NO | Solo disciplina autoriale |

---

## Processo e approvazione

| Requisito | Fonte | Tipo | Owner attuale | Blocking | Note |
|-----------|-------|------|--------------|---------|------|
| Step 0: tri_diff pre-analisi | workflow-nuova-finestra.instructions.md | manuale | Analista Tri-Repo | NO | Non automatizzato nel gate; Fase 2 |
| Step 7: audit.py post-commit | workflow-nuova-finestra.instructions.md | gate | audit.py | SI | Eseguito; tri_diff integrato (B4) + pre-flight sorgenti (B5) |
| Sign-off Revisore Accessibilità | auditore-finale.agent.md | manuale | revisore-accessibilita.agent.md | NO | Solo advisory oggi; Fase 3 |
| Sign-off Revisore Vanilla | auditore-finale.agent.md | manuale | revisore-vanilla.agent.md | NO | Solo advisory oggi; Fase 3 |
| Approvazione Auditore Finale | workflow-nuova-finestra.instructions.md | manuale | auditore-finale.agent.md | NO (de facto) | Nessun meccanismo di blocco reale; Fase 3 |

---

## Riepilogo gap per fase

### Tassonomia esiti unificata (C2 — 2026-03-20)

I tool Python e gli agenti Copilot usano nomenclature diverse per i verdetti.
La tabella seguente definisce il mapping ufficiale:

| Verdetto tool (audit.py) | Corrisponde ad agente | Significato | Azione richiesta |
|--------------------------|----------------------|-------------|-----------------|
| `PULITO` | — (non esposto agli agenti, stato internal) | Nessun issue rilevato dal validator | — |
| `OK` | `APPROVED` | Audit superato: 0 critici, 0 avvertenze, fedeltà OK | Commit consentito |
| `CON AVVERTENZE` | `APPROVED con riserve` | 0 critici, avvertenze aperte | Commit consentito; sign-off revisori richiesto per promuovere a "Validata" |
| `BLOCCANTE` | `BLOCKED` | ≥1 critico o binding DA VERIFICARE | Commit bloccato (pre-commit hook); fix obbligatorio |

> **Nota**: `DISCREPANZE_MINORI` da tri_diff è advisory (non impatta il verdetto).
> `DISCREPANZE` (gravi) da tri_diff eleva a `CON AVVERTENZE` se il verdetto sarebbe altrimenti OK.

### Gap risolti (Fasi A-C, 2026-03-20)

| Gap | Fase | Stato |
|-----|------|-------|
| Copertura dual-mode sub-window/multi-window | B1 | ✅ Escalation a CRITICO + fix false positive |
| Controllo fallback datamodel OCR | B2 | ✅ Escalation a CRITICO |
| Controllo header OCR (colore) | B3 | ✅ Escalation a CRITICO |
| Fedeltà vanilla (tri_diff → audit.py) | B4 | ✅ Integrata come gate |
| Pre-flight sorgenti (vanilla + OCR upstream) | B5 | ✅ Check in audit.py |
| Pre-commit hook automatico | C1 | ✅ `.githooks/pre-commit` |
| Tassonomia esiti incoerente | C2 | ✅ Mapping nella matrice |

### Gap Fase 2 originali — stato aggiornato
- ~~Copertura dual-mode sub-window/multi-window~~: **RISOLTO** (B1)
- ~~Controllo header OCR (fontsize 20, colore)~~: **PARZIALMENTE RISOLTO** (B3 — colore, non fontsize)
- Controllo fallback liste vuote OCR: **MANCANTE** (da aggiungere)
- Completezza OCR vs vanilla (parità azioni/dati): **MANCANTE** (da aggiungere)
- ~~Fedeltà vanilla automatizzata (tri_diff → audit.py)~~: **RISOLTO** (B4)

### Gap Fase 3 — stato aggiornato
- Approvazione Auditore Finale: advisory, non bloccante
- Sign-off revisori: nessun meccanismo di tracciabilità
- ~~Tassonomia esiti: incoerente~~: **RISOLTO** (C2)
