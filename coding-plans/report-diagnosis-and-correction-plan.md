# Piano di Consolidamento Framework — OCR Support Patch

Data creazione: 2026-03-13 | Aggiornamento: 2026-03-20
Fonti incrociate: patch (`ocr_support_compatibility_pach/gui/`), vanilla CK3 1.17.1, OCR upstream Agamidae

---

# PARTE I — Diagnosi Rapporto Tecnico Esterno

## 1. Verdetto Globale sul Rapporto

Il rapporto tecnico analizzato proviene da un **contesto di fork diverso** (riferimenti a
`ck3-ocr-support-by-nemex` e a un manuale `istruzioni sviluppo sistema accessible dual-mode.md v4.0`
che **non esiste** in questo workspace). Le convenzioni di naming e alcune regole invarianti
dichiarate **non corrispondono** al framework effettivo.

**Affidabilità complessiva: MEDIA-BASSA** — 4 claim su 6 confermati, 2 falsi;
2 regole invarianti criticamente errate su 8.

---

## 2. Verifica Claim per Claim

### CLAIM 1 — Dual-State Divergente nel Pattern B (Tab Sync)
- **Verdetto: ✅ CONFERMATO — CRITICO**
- `window_court.gui`: OCR usa `GetVariableSystem.HasValue('court_tabs', ...)` (righe 712, 721, 927),
  vanilla usa `CourtWindow.IsShowPositions`/`IsShowCourt`/`IsShowPrison` (righe 99, 114, 120).
  Nessuna sincronizzazione tra i due sistemi.
- `window_council.gui`: OCR usa `GetVariableSystem.HasValue('council_tabs', ...)` (righe 64, 401),
  vanilla usa `CouncilWindow.IsPlayerCouncilShown` (righe 453, 482).
  Stesso problema: tab state completamente indipendente.
- **Impatto**: Cambio OCR↔vanilla con Shift+F11 perde la posizione del tab attivo.

### CLAIM 2 — Type Pollution in window_council.gui
- **Verdetto: ✅ CONFERMATO — MEDIO**
- Il type `council_task_info` (riga 629) contiene sia `using = ocr` (righe 644, 668)
  che `using = vanilla` (riga 672) nella stessa definizione.
- Non esistono type separati `council_task_info_ocr` e `council_task_info_vanilla`.
- **Impatto**: Il type viene renderizzato per entrambe le modalità — i contenuti OCR
  appaiono nel vanilla e viceversa (ridondanza visiva, potenziale confusione screen reader).

### CLAIM 3 — window_character.gui Non Integrata
- **Verdetto: ❌ FALSO**
- Il file è già presente nella patch (187 KB), con dual-mode alle righe 37 (OCR) e 80 (vanilla).
- Stato nel tracker: "Convertite — Revisione Necessaria" (0 critici, 65 avvertenze).

### CLAIM 4 — Mancanza Catalogo Dipendenze
- **Verdetto: ✅ CONFERMATO — BASSO**
- Nessun file DEPENDENCY_MAP o catalogo dipendenze finestre trovato in tutto il workspace.
- **Impatto**: Rischio di regressione quando si modifica un file condiviso (types, templates).
  Attualmente gestito implicitamente — non bloccante.

### CLAIM 5 — Invisible Button Workaround (size 0 0)
- **Verdetto: ✅ CONFERMATO — INFORMATIVO**
- 20+ occorrenze in 10 file GUI (hud.gui, window_army.gui, window_combat.gui, ecc.).
- Pattern tipico: `button = { size = { 0 0 } shortcut = "..." onclick = "..." }`.
- Nessun template `shortcutbar_ocr` centralizzato esiste.
- **Impatto**: Non è un bug — è il pattern standard CK3/OCR upstream per shortcut da tastiera.
  Funziona correttamente. Un template centralizzato sarebbe utile ma non prioritario.

### CLAIM 6 — window_dynasty_house.gui Senza Copertura OCR
- **Verdetto: ❌ FALSO**
- Il file ha dual-mode: riga 39 (OCR con `using = ocr_window`) e riga 1133 (vanilla).
- Stato nel tracker: "Convertite — Revisione Necessaria" (0 critici, 26 avvertenze).

---

## 3. Verifica Regole Invarianti

### Container Naming
- **Rapporto dice**: `ocrmodecontent` / `normalmodecontent`
- **Realtà**: `ocr_[nome]_container` / `vanilla_[nome]_container`
  (con varianti legacy: `ocr_mode_content` / `normal_mode_content` in alcuni file convertiti prima)
- **Verdetto: ❌ NAMING ERRATO NEL RAPPORTO**

### "Mai hbox in OCR Layout"
- **Rapporto dice**: layout OCR esclusivamente `vbox` lineare, mai `hbox`
- **Realtà**: almeno 8+ `hbox` trovati in sezioni OCR (window_decisions, window_intrigue)
  usati per tab button e testo inline.
- **Verdetto: ❌ REGOLA ERRATA NEL RAPPORTO**
- **Nota**: l'uso di `hbox` in OCR è legittimo per tab navigation e testo compatto —
  non viola l'accessibilità screen reader se il contenuto è testuale.

### datacontext GetVariableSystem
- **Rapporto dice**: sempre al top-level della window
- **Realtà**: usato sia a livello window che annidato in sub-widget (20 match totali)
- **Verdetto: ✅ Parzialmente corretto** (top-level sì, ma anche nested)

### Altre regole invarianti (type suffix, OCR buttons, vanilla immutabile, checksum)
- **Verdetto: ✅ Tutte confermate**

---

## 4. Problemi Reali Confermati — Priorità e Correzione

### P1 — CRITICO: Tab State Divergente (Claim 1)

**File coinvolti**: `window_court.gui`, `window_council.gui`
(potenzialmente tutti i file Pattern B con tab navigation)

**Problema**: OCR usa `GetVariableSystem.HasValue` per tab, vanilla usa API C++ nativa
(es. `CourtWindow.IsShowPositions`). I due sistemi sono indipendenti — toggle Shift+F11
perde la posizione del tab.

**Strategia di correzione**: Questo è un limite architetturale noto del dual-mode Pattern B.
La sincronizzazione richiederebbe hook `on_visible` che settino i `VariableSystem` in base
allo stato C++ e viceversa — ma CK3 1.17.1 non espone API per leggere lo stato tab C++
da Jomini. **Raccomandazione**: documentare come limitazione nota, non come bug.
Se si vuole mitigare: impostare un tab default noto (es. primo tab) su `on_visible`
di ciascun container, così dopo il toggle si parte sempre da una posizione prevedibile.

**Azione framework**: aggiungere sezione "Limitazioni Note" in
`.github/resources/dual_mode_pattern_canonical.md` — Pattern B, tab sync.

---

### P2 — MEDIO: Type Pollution in council_task_info (Claim 2)

**File coinvolto**: `window_council.gui`

**Problema**: Un singolo type contiene template OCR e vanilla mescolati.

**Strategia di correzione**: Separare in `council_task_info_ocr` e `council_task_info_vanilla`
con `visible` mutuamente esclusivi. Richiede rigenriazione del file tramite
`assemble_dualmode.py` o edit manuale.

**Azione mod**: correggere `window_council.gui` nella prossima sessione di manutenzione.
Audit preventivo: `python tools/audit.py --window window_council`.

---

### P3 — BASSO: Catalogo Dipendenze Mancante (Claim 4)

**Problema**: Nessun catalogo formale delle dipendenze tra finestre (types condivisi,
template cross-file, datamodel impliciti).

**Strategia**: Creare `.github/resources/dependency_map.md` con:
- Elenco types condivisi e file che li definiscono
- Elenco template OCR (`ocr_window`, `ocr_margins`, `base_ocr_window`, ecc.) e file sorgente
- Matrice dipendenze finestra → type/template
- Generabile automaticamente da `scope_extractor.py` con flag `--deps`

**Azione framework**: task di bassa priorità, utile per manutenzione a lungo termine.

---

### P4 — INFORMATIVO: Template Shortcut Centralizzato (Claim 5)

**Problema**: I bottoni invisibili `size = { 0 0 }` per shortcut sono sparsi senza template.

**Strategia**: Opzionale — creare un template `shortcutbar_ocr` per standardizzare.
Non prioritario perché il pattern attuale funziona.

**Azione**: nessuna azione immediata richiesta.

---

## 5. Incoerenze del Rapporto — Riepilogo

| Elemento | Rapporto dice | Realtà | Severità |
|----------|---------------|--------|----------|
| Container naming | `ocrmodecontent`/`normalmodecontent` | `ocr_[nome]_container`/`vanilla_[nome]_container` | ALTA — nomenclatura completamente errata |
| hbox in OCR | "Mai usare hbox" | 8+ hbox nelle sezioni OCR | MEDIA — regola inventata |
| window_character.gui | "Non integrata" | Presente con dual-mode (187 KB) | ALTA — informazione falsa |
| window_dynasty_house.gui | "Senza copertura OCR" | Presente con dual-mode | ALTA — informazione falsa |
| Manuale di riferimento | `istruzioni sviluppo sistema accessible dual-mode.md v4.0` | Non esiste nel workspace | MEDIA — fonte non verificabile |
| Nome repository | `ck3-ocr-support-by-nemex` | `ocr-support-patch` | BASSA — contesto fork diverso |

---

## 6. Raccomandazioni Operative

1. **NON usare il rapporto come fonte autorevole** per lo stato delle conversioni.
   Il tracker ufficiale è `gui-conversion-progress.instructions.md`.

2. **Correggere P1 (tab sync)**: documentare come limitazione nota nel canonical pattern.

3. **Correggere P2 (type pollution)**: richiede intervento su `window_council.gui`.
   Schedulare nella prossima sessione di manutenzione file Pattern B.

4. **Valutare P3 (dependency map)**: utile ma non urgente. Può essere generato
   incrementalmente durante le prossime conversioni.

5. **Ignorare P4 (shortcut template)**: pattern attuale funzionante, ottimizzazione opzionale.

---

## 7. Prossimi Passi dalla Diagnosi Rapporto (rinviati a dopo consolidamento)

- [ ] Aggiornare `dual_mode_pattern_canonical.md` con sezione "Limitazioni Note Pattern B"
- [ ] Aprire sessione manutenzione per `window_council.gui` (type pollution)
- [ ] Eventuale creazione `dependency_map.md` (bassa priorità)

---
---

# PARTE II — Strategia di Consolidamento Framework

> **Obiettivo**: assicurarsi che, quando si passerà a revisionare le finestre .gui,
> il framework sia in grado di **analizzare** in modo efficiente, **progettare e pianificare**
> in modo preciso e completo, **implementare** in modo meticoloso, e **convalidare**
> verificando ed eventualmente revisionando ogni modifica.

---

## Stato Attuale del Framework (sintesi audit 2026-03-20)

### Cosa funziona bene
- **Workflow a checkpoint** (workflow-nuova-finestra.instructions.md): sequenza 0→8 con CP1 e CP2 chiara.
- **Toolchain Python**: audit.py, gui_validator.py, scope_extractor.py, tri_diff.py, assemble_dualmode.py — tutti funzionanti e testati.
- **Sistema agenti**: 6 agenti con ruoli distinti e non sovrapponibili, handoff definiti.
- **Skills**: 6 skill specializzate collegabili agli agenti.
- **Istruzioni per dominio**: attivazione automatica per pattern file (*.gui, localization, ecc.).
- **Risorse canoniche**: pattern dual-mode, conversion patterns, shortcut OCR documentati.

### Cosa non funziona o manca

| Area | Gap | Rif. |
|------|-----|------|
| **Gate automatico** | gui_validator.py non verifica copertura dual-mode in file multi-window | F4 |
| **Gate automatico** | Nessun fallback testuale per datamodel vuoto verificato automaticamente | F6 |
| **Gate automatico** | Header OCR (fontsize 20, colore) solo ATTENZIONE, non CRITICO | F5 |
| **Gate automatico** | tri_diff.py (fedeltà vanilla) non integrato in audit.py — solo advisory | F7 |
| **Whitelist scope** | Incompleta: copre solo finestre già convertite, non le prossime | F2 |
| **Whitelist scope** | Nessuna tracciabilità (chi ha aggiunto cosa/quando) | F11 |
| **Whitelist scope** | Aggiornamento manuale — nessun agente autorizzato a editare | F3/F8 |
| **Fonti di verità** | `priority_list.md` e `gui-conversion-progress.instructions.md` duplicati e divergenti | F1 |
| **Governance** | Verdetto Auditore Finale non bloccante — nessun pre-commit hook | F12 |
| **Documentazione** | assemble_army_dualmode.py non documentato nel workflow | F10 |
| **Pre-flight** | assemble_dualmode.py non verifica esistenza file sorgente prima di procedere | F9 |

---

## Fasi di Consolidamento

Il consolidamento è organizzato in **3 fasi sequenziali**. Ogni fase ha obiettivo,
deliverable verificabili e criterio di completamento.

### FASE A — Pulizia e Coerenza (priorità immediata)

**Obiettivo**: eliminare contraddizioni, duplicazioni e ambiguità nel framework.
Nessun tool Python da modificare — solo documentazione e risorse.

| # | Azione | File | Criterio di completamento |
|---|--------|------|--------------------------|
| A1 | **Deprecare `priority_list.md`** — aggiungere nota iniziale che rimanda a `gui-conversion-progress.instructions.md` come unica fonte di verità. Rimuovere dati duplicati. | `.github/resources/priority_list.md` | File contiene solo redirect + nota deprecazione |
| A2 | **Allineare `gui-conversion-progress.instructions.md`** — verificare che tutti i 23 file .gui nella patch siano elencati nella sezione corretta e che "Da Convertire" non includa file già presenti | `.github/instructions/gui-conversion-progress.instructions.md` | `ls ocr_support_compatibility_pach/gui/` = file elencati nel tracker 1:1 |
| A3 | **Documentare assemble_army_dualmode.py** — aggiungere nota in gui-conversion-progress che window_army.gui usa script specializzato | `.github/instructions/gui-conversion-progress.instructions.md` | Nota presente |
| A4 | **Aggiungere tracciabilità alla whitelist** — nuova colonna "Verificato da" (file vanilla sorgente) per ogni binding | `.github/resources/jomini_scope_whitelist.md` | Colonna presente su ogni riga |
| A5 | **Autorizzare Implementatore su whitelist** — aggiungere permesso esplicito per scope_extractor output | `.github/agents/implementatore-patch.agent.md` | Agent ha permesso documentato |
| A6 | **Documentare limitazione Pattern B** (tab sync) in pattern canonico | `.github/resources/dual_mode_pattern_canonical.md` | Sezione "Limitazioni Note" presente |

**Stima**: 6 azioni, tutte editoriali su file .md. Nessun rischio di regressione.

---

### FASE B — Rafforzamento Gate Automatico (priorità alta)

**Obiettivo**: ampliare gui_validator.py e audit.py per catturare automaticamente
i gap che oggi richiedono solo review manuale.

| # | Azione | File | Criterio di completamento |
|---|--------|------|--------------------------|
| B1 | **Copertura multi-window** — gui_validator.py deve verificare che OGNI blocco `window = { }` radice in un file abbia almeno un container OCR e uno vanilla con `visible` mutuamente esclusivi | `tools/gui_validator.py` | Test su `window_county_view.gui` (6+ window radice) passa |
| B2 | **Fallback datamodel vuoto** — gui_validator.py deve segnalare come CRITICO ogni `datamodel` o `item` dentro OCR che non ha un fallback testuale (es. `text_single` con messaggio "nessun elemento") | `tools/gui_validator.py` | Test su file con datamodel vuoto noto |
| B3 | **Header OCR enforcement** — escalare la verifica header (fontsize 20, colore) da ATTENZIONE a CRITICO in gui_validator.py | `tools/gui_validator.py` | Header mancante → CRITICO nel report |
| B4 | **Integrazione tri_diff in audit.py** — il report fedeltà vanilla div enta gate bloccante se container vanilla diverge dal file vanilla originale in modo non-triviale (onclick rimosso, tooltip alterato, widget mancante) | `tools/audit.py` + `tools/tri_diff.py` | `audit.py --window X` include sezione fedeltà con verdetto PASS/FAIL |
| B5 | **Pre-flight sorgente** — audit.py verifica esistenza file OCR upstream e vanilla prima di procedere con scope_extractor | `tools/audit.py` | Errore chiaro se file sorgente mancante |
| B6 | **Pre-popolare whitelist** — eseguire scope_extractor.py su tutti i file vanilla delle finestre prossime (window_title, window_government_administration, interaction_modify_vassal_window) e aggiungere binding alla whitelist | `.github/resources/jomini_scope_whitelist.md` | Binding delle 3 finestre priority alta presenti |

**Stima**: 6 azioni, 4 modifiche Python + 1 risorsa + 1 integrazione cross-tool.
Ogni modifica Python è testabile con `audit.py --window` su file esistenti.

---

### FASE C — Governance e Automazione (priorità media)

**Obiettivo**: rendere il workflow robusto contro errori umani e tracciabile.

| # | Azione | File | Criterio di completamento |
|---|--------|------|--------------------------|
| C1 | **Pre-commit hook git** — script che legge l'ultimo verdetto di audit.py e blocca il commit se BLOCCANTE | `.githooks/pre-commit` o `.github/` | `git commit` fallisce se ultimo audit = BLOCCANTE |
| C2 | **Tassonomia esiti unificata** — allineare la nomenclatura tra tool (PULITO / CON AVVERTENZE / BLOCCANTE) e agenti (APPROVED / BLOCKED) con mapping esplicito | `requirement-enforcement-matrix.md` | Tabella mapping aggiunta |
| C3 | **scope_extractor auto-update** — opzione `--update-whitelist` che aggiunge automaticamente i binding ASSENTI (verificati nel vanilla) senza edit manuale | `tools/scope_extractor.py` | `--update-whitelist` funziona su test reale |
| C4 | **Dependency map incrementale** — generare `dependency_map.md` dai type/template usati cross-file nella patch | Nuovo: `.github/resources/dependency_map.md` + script | File generato e veritiero |

**Stima**: 4 azioni, mix di scripting e documentazione. Non bloccante per le conversioni.

---

## Ordine di Esecuzione Raccomandato

```
FASE A (pulizia)
├── A1 → A2 → A3   (fonte di verità — prima di tutto)
├── A4 → A5         (whitelist — parallelo con sopra)
└── A6              (docs pattern — indipendente)

FASE B (gate)
├── B1 → B2 → B3   (gui_validator.py — incrementale)
├── B4 → B5         (audit.py — incrementale)
└── B6              (whitelist scope — indipendente, ma dopo A4)

FASE C (governance)
├── C1              (pre-commit — dopo B4)
├── C2              (tassonomia — indipendente)
├── C3              (scope auto-update — dopo A5)
└── C4              (dependency map — solo se tempo)
```

---

## Criteri di Successo (Definition of Done)

Il framework è "consolidato" quando:

1. **Analisi**: `tri_diff.py` + `scope_extractor.py` producono report completo per qualsiasi finestra
   senza binding ASSENTI irrisolti (whitelist pre-popolata per finestre prossime). ✅ = Fase A+B6
2. **Progettazione**: `assemble_dualmode.py --dry-run` genera bozza corretta per i 4 pattern (A/B/C/D)
   e il modder/architetto hanno documentazione chiara su limitazioni (tab sync). ✅ = Fase A6
3. **Implementazione**: il flusso assemble → scope_extractor → whitelist update è fluido
   (nessun copy-paste manuale necessario). ✅ = Fase B6 + C3
4. **Convalida**: `audit.py` cattura TUTTI i problemi critici automaticamente (multi-window,
   fallback vuoto, header OCR, fedeltà vanilla) e il verdetto è bloccante. ✅ = Fase B1-B5 + C1

---

## Rischi e Mitigazioni

| Rischio | Mitigazione |
|---------|-------------|
| Modifica gui_validator.py introduce falsi positivi | Testare ogni regola nuova su 3+ file già validati prima di attivare |
| Pre-popolare whitelist con binding errati | Usare scope_extractor in modalità `--verify` (confronta con vanilla) |
| Pre-commit hook troppo restrittivo | Opzione `--force` documentata per casi eccezionali (con log) |
| Fase B richiede più tempo del previsto | Le fasi sono indipendenti — Fase A dà già valore immediato |
