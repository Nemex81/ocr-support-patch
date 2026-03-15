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
| Copertura dual-mode in sub-window e file multi-window | gui-jomini.instructions.md | gate | **MANCANTE** | MANCANTE | gui_validator.py non verifica sub-window; Fase 2 |

---

## Accessibilità OCR (NVDA)

| Requisito | Fonte | Tipo | Owner attuale | Blocking | Note |
|-----------|-------|------|--------------|---------|------|
| Fontsize ≥ 18 nel blocco OCR | gui-jomini.instructions.md | gate | gui_validator.py – check fontsize | SI (warn) | Produce avvertenza, non critico |
| Header OCR: fontsize 20, colore `{ 255 221 136 255 }` | gui-jomini.instructions.md | manuale | revisore-accessibilita.agent.md | NO | Nessun controllo automatico; Fase 2 (da aggiungere come lint) |
| Tooltip obbligatorio su ogni pulsante/icona nel blocco OCR | gui-jomini.instructions.md | gate | gui_validator.py – check tooltip | SI (warn) | Produce avvertenza; non blocca ma è segnalato |
| Ordine di lettura NVDA coerente | gui-jomini.instructions.md | manuale | revisore-accessibilita.agent.md | NO | Non verificabile automaticamente |
| Parità funzionale OCR/vanilla (stesse azioni disponibili) | gui-jomini.instructions.md | manuale | revisore-accessibilita.agent.md | NO | Nessun controllo automatico; Fase 2 (completezza OCR) |
| Fallback testo per liste vuote nel blocco OCR | gui-jomini.instructions.md | gate | **MANCANTE** | MANCANTE | Fase 2 |

---

## Fedeltà vanilla

| Requisito | Fonte | Tipo | Owner attuale | Blocking | Note |
|-----------|-------|------|--------------|---------|------|
| Container vanilla = copia fedele del CK3 originale | copilot-instructions.md | manuale | revisore-vanilla.agent.md | NO | tri_diff.py esiste ma non è integrato in audit.py; Fase 2 |
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
| Step 7: audit.py post-commit | workflow-nuova-finestra.instructions.md | gate | audit.py | SI | Eseguito, ma tri_diff non è incluso |
| Sign-off Revisore Accessibilità | auditore-finale.agent.md | manuale | revisore-accessibilita.agent.md | NO | Solo advisory oggi; Fase 3 |
| Sign-off Revisore Vanilla | auditore-finale.agent.md | manuale | revisore-vanilla.agent.md | NO | Solo advisory oggi; Fase 3 |
| Approvazione Auditore Finale | workflow-nuova-finestra.instructions.md | manuale | auditore-finale.agent.md | NO (de facto) | Nessun meccanismo di blocco reale; Fase 3 |

---

## Riepilogo gap per fase

### Gap Fase 2 (gate automatico da rafforzare)
---

## Pattern v1.1 — Type-Separated Vanilla

| Requisito | Fonte | Tipo | Owner attuale | Blocking | Note |
|-----------|-------|------|--------------|---------|------|
| Naming type: `{nome}_patch_vanilla` (non `_old`, non `_vanilla` puro) | copilot-instructions.md | lint | gui_validator.py (da implementare Fase 3) | SI | Previene collisioni con Agamidae |
| Blocco `types OCR_PATCH_VANILLA { }` nel file type | dual_mode_pattern_canonical.md | lint | gui_validator.py (da implementare Fase 3) | SI | Namespace univoco della patch |
| Guard `visible = "[GetVariableSystem.Exists('ocr')]"` presente nel type | dual_mode_pattern_canonical.md | gate | gui_validator.py (da implementare Fase 3) | SI | Errore VISIBILITA_TYPE_SEPARATED_INCOHERENTE |
| Assenza proprietà window-level nel type (`state`, `widgetid`, `layer`, `attachto`, `movable`) | dual_mode_pattern_canonical.md | lint | gui_validator.py (da implementare Fase 3) | SI | Warning TYPE_SEPARATO_NO_NOME se name assente |
| Istanziazione wrapper senza `visible` esplicita | dual_mode_pattern_canonical.md | lint | gui_validator.py (da implementare Fase 3) | WARN | La visibilità è responsabilità del type |
| File type in `gui/vanilla/` presente quando wrapper lo referenzia | workflow-nuova-finestra.instructions.md | gate | audit.py (da implementare Fase 3) | WARN | ATTENZIONE: non blocca ma da risolvere pre-commit |
| Contenuto vanilla nel type identico al file CK3 originale | dual_mode_pattern_canonical.md | manuale | revisore-vanilla.agent.md | NO | Nessun controllo automatico |
| Audit cumulativo coppia wrapper+type | workflow-nuova-finestra.instructions.md | gate | audit.py (da implementare Fase 3) | SI | Verdetto unificato obbligatorio |

---

- Copertura dual-mode sub-window/multi-window: MANCANTE
- Controllo header OCR (fontsize 20, colore): MANCANTE
- Controllo fallback liste vuote OCR: MANCANTE
- Completezza OCR vs vanilla (parità azioni/dati): MANCANTE
- Fedeltà vanilla automatizzata (tri_diff → audit.py): MANCANTE

### Gap Fase 3 (governance da rafforzare)
- Approvazione Auditore Finale: advisory, non bloccante
- Sign-off revisori: nessun meccanismo di tracciabilità
- Tassonomia esiti: incoerente tra tool (PULITO/CON AVVERTENZE/BLOCCANTE) e agenti (APPROVED/BLOCKED)
