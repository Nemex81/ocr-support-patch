# Piano di Ristrutturazione Framework Dual-Mode
## OCR Support Patch — CK3 1.17.1

**Data**: 13 Marzo 2026  
**Autore**: Luca (Nemex81)  
**Scopo**: Rendere il framework sinergico, coeso e completamente operativo per la conversione dual-mode di ogni finestra di gioco CK3, una finestra alla volta, con controllo manuale obbligatorio del modder su ogni fase critica.

---

## Obiettivo Finale

Il framework deve permettere questa operazione, per qualsiasi finestra:

1. Il modder digita: `#converti-finestra window_nome` nel chat di Copilot
2. Il framework legge il file OCR upstream (Agamidae) → estrae il contenuto accessibile già scritto
3. Il framework legge il file vanilla CK3 originale → estrae il contenuto grafico completo
4. Assembla il file dual-mode nella patch con i due container corretti
5. Valida automaticamente il file prodotto
6. Chiede approvazione manuale al modder
7. Se approvato: revisori e audit finale
8. Commit solo dopo APPROVED

**Principio fondamentale**: il sistema non inventa nulla. Il container OCR viene dall'OCR upstream di Agamidae, già scritto e verificato. Il container vanilla viene dal CK3 originale, copiato identico. Il framework assembla, non genera.

**Vincolo non negoziabile**: una finestra alla volta. Nessuna elaborazione automatica consecutiva su più finestre senza approvazione esplicita del modder tra una e l'altra.

---

## Stato Attuale — Diagnosi

### Problema Centrale
Il framework ha tre livelli che non si parlano:
- **Livello 1** — Script Python (`tools/`): eseguiti a mano da terminale
- **Livello 2** — Agenti + Skills (`.github/agents/` + `.github/copilot-skills/`): operano dentro VS Code Copilot con `read/edit/search`, non chiamano mai gli script
- **Livello 3** — Prompt + Instructions: istruzioni di contesto passive, non coordinano nessuno

Il collegamento tra i livelli è umano: il modder fa da bridge manuale. Questo rende il processo lento, error-prone e non ripetibile.

### Problemi Specifici Identificati
1. `assemble_army_dualmode.py` è hardcoded per `window_army.gui` — non funziona per nessun'altra finestra
2. Gli agenti non hanno `terminal` nei tools — non possono eseguire script Python
3. La skill `dual-mode-template-generator` genera placeholder invece di estrarre contenuto reale
4. Il prompt `converti-finestra-dual-mode.prompt.md` non specifica "estrai da sorgenti reali"
5. `tri_diff.py` può dare falsi negativi in Sezione C se il container vanilla non ha naming `vanilla_*`
6. Path hardcoded in `assemble_army_dualmode.py` bypassano `config.py`
7. Script obsoleti nel repository che generano confusione

---

## Interventi — Lista Completa Ordinata per Priorità

---

### FASE 1 — Pulizia Repository (prerequisito)

**Obiettivo**: eliminare codice obsoleto e consolidare prima di costruire.

#### 1.1 — Eliminare script obsoleti da `tools/`

| File | Motivo eliminazione |
|------|---------------------|
| `tools/fix_faith_types.py` | Fix one-shot già applicato, non serve più |
| `tools/fix_remaining_types.py` | Fix one-shot già applicato, non serve più |
| `tools/classify_critico.py` | Funzione minimale già presente in `audit.py` |
| `tools/test_enc.py` | Test usa-e-getta, 407 byte, nessun valore operativo |
| `tools/debug_ocr_windows.py` | Debug puntuale senza integrazione nel workflow |
| `tools/debug_vanilla_blocks.py` | Debug puntuale senza integrazione nel workflow |

**Come procedere**: eliminare ogni file con git, verificare che nessun altro script li importi.

#### 1.2 — Fix path hardcoded in `assemble_army_dualmode.py`

Prima del refactor, fix immediato: sostituire i path calcolati autonomamente con import da `config.py`.

File: `tools/assemble_army_dualmode.py`  
Problema: usa `ROOT.parent / "CK3-OCR/..."` invece di importare `config.OCR_PATH` e `config.VANILLA_PATH`.  
Fix: aggiungere `from config import OCR_PATH, VANILLA_PATH, PATCH_PATH` e usare queste variabili.

---

### FASE 2 — Script Python Core: Refactor `assemble_dualmode.py`

**Obiettivo**: creare lo strumento di assemblaggio generico che è il pezzo mancante più importante.

#### 2.1 — Refactor di `assemble_army_dualmode.py` → `assemble_dualmode.py`

Il file non viene eliminato e riscritto da zero. Viene convertito: le funzioni utility generiche restano, le parti army-specifiche vengono rimosse o parametrizzate.

**Funzioni da mantenere invariate** (già generiche):
- `find_top_level_windows(content)` — trova tutti i blocchi `window = {}` in qualsiasi file
- `find_block_end(lines, start)` — bilanciamento graffe, funziona su qualsiasi blocco
- `find_window_end(lines, start)` — alias specializzato, mantenere
- `find_type_block(content, type_name)` — trova `type X = ...` per nome
- `find_template_block(content, template_name)` — trova `template X {}` per nome
- `indent_lines(lines, spaces)` — utility di indentazione generica
- `build_sub_window_dual(ocr_block, vanilla_block, window_name)` — già generico, solo aggiustamenti naming

**Funzioni da rimuovere** (army-specifiche):
- `extract_inner_vbox_from_ocr_army_window()` — cerca `size = {400 100%}` e `size = {800 100%}`, valori hardcoded army
- `build_army_window()` — costruttore army-specifico
- Le costanti `VANILLA_CONTAINER_HEADER`, `VANILLA_REORG_HEADER`, `VANILLA_ATTACH_HEADER` con dimensioni army

**Funzioni da aggiungere** (nuove, parametriche):

```python
def extract_window_content(content: str) -> list[dict]:
    """
    Estrae tutti i blocchi top-level da un file .gui.
    Restituisce lista di dict con keys: type, name, raw_content.
    type può essere: 'window', 'type', 'template', 'types_block'
    """

def build_ocr_container(window_name: str, ocr_inner_content: str) -> str:
    """
    Avvolge il contenuto OCR estratto nel container standard con
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"
    Segue il pattern canonical in .github/resources/dual_mode_pattern_canonical.md
    """

def build_vanilla_container(window_name: str, vanilla_inner_content: str) -> str:
    """
    Avvolge il contenuto vanilla nel container standard con
    visible = "[GetVariableSystem.Exists('ocr')]"
    Nessuna modifica al contenuto vanilla — copia fedele.
    """

def assemble_simple(window_name: str, ocr_content: str, vanilla_content: str) -> str:
    """Pattern A: una sola window, struttura semplice."""

def assemble_tabs(window_name: str, ocr_content: str, vanilla_content: str) -> str:
    """Pattern B: window principale + sub-windows."""

def assemble_complex(window_name: str, ocr_content: str, vanilla_content: str) -> str:
    """Pattern C/D: window + types + templates separati."""
```

**Entry point**:
```
python tools/assemble_dualmode.py --window window_nome --mode simple|tabs|complex [--dry-run]
```

- `--dry-run`: stampa il file assemblato su stdout senza scrivere nulla. Permette al modder di verificare prima di procedere.
- Senza `--dry-run`: scrive in `ocr_support_compatibility_pach/gui/window_nome.gui`
- `--mode`: determina quale strategia di assemblaggio usare (corrisponde ai Pattern A/B/C/D)

**Test di regressione obbligatorio**: dopo il refactor, eseguire il nuovo script con `--window window_army --mode complex --dry-run` e confrontare l'output con il file attuale in patch. Se identico (o differenze solo nel wrapper container), il refactor è corretto. Solo dopo eliminare `assemble_army_dualmode.py`.

#### 2.2 — Fix `tri_diff.py`: Sezione C più robusta

Problema: la Sezione C trova il container vanilla solo se si chiama `vanilla_*` o ha `Exists('ocr')` esplicito. Se il naming è diverso, dice "blocco non trovato" — falso negativo silenzioso.

Fix: aggiungere fallback nella ricerca del container vanilla:
1. Prima cerca `name = "vanilla_*"` (comportamento attuale)
2. Se non trovato, cerca `visible = "[GetVariableSystem.Exists('ocr')]"` (qualsiasi naming)
3. Se ancora non trovato: segnalare esplicitamente "CONTAINER VANILLA NON TROVATO — verifica naming"

---

### FASE 3 — Agenti: Aggiungere `terminal` ai Tools

**Obiettivo**: far sì che gli agenti possano eseguire script Python direttamente invece di chiedere al modder di farlo.

#### 3.1 — Agente Analista Tri-Repo

File: `.github/agents/analista-tri-repo.agent.md`

Modifica: aggiungere `terminal` ai tools.

```yaml
tools: [read, search, terminal]
```

Aggiungere alla metodologia:
```
1. Esegui direttamente: python tools/tri_diff.py --window <nome_finestra>
   Usa l'output come base per l'analisi. Non chiedere al modder di eseguirlo.
```

#### 3.2 — Agente Implementatore Patch

File: `.github/agents/implementatore-patch.agent.md`

Modifica: aggiungere `terminal` ai tools.

```yaml
tools: [edit, read, search, terminal]
```

Riscrivere i passi 0, 3-4, 7-8 per usare i nuovi script:

```
PASSO 0: python tools/tri_diff.py --window <nome>
         → analisi pre-intervento (eseguito direttamente)

PASSO 3: python tools/assemble_dualmode.py --window <nome> --mode <pattern> --dry-run
         → mostra bozza assemblaggio al modder
         → STOP: attendere approvazione esplicita del modder prima di continuare

PASSO 4: [SOLO DOPO APPROVAZIONE MODDER]
         python tools/assemble_dualmode.py --window <nome> --mode <pattern>
         → scrive il file nella patch

PASSO 7: python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/<nome>.gui
         → eseguito direttamente

PASSO 8: python tools/audit.py --window <nome>
         → eseguito direttamente
         → se BLOCCANTE: correggere prima di passare ai revisori
```

**Regola anti-automazione a catena**: dopo il completamento di una finestra, l'agente NON deve proporre di iniziare la finestra successiva. Deve suggerire handoff a Revisore Accessibilità e attendere istruzioni del modder.

#### 3.3 — Agente Auditore Finale

File: `.github/agents/auditore-finale.agent.md`

Modifica: aggiungere `terminal` ai tools.

```yaml
tools: [read, search, terminal]
```

Aggiornare Sezione 0:
```
SEZIONE 0 — PRE-AUDIT AUTOMATICO (obbligatorio)
Esegui direttamente: python tools/audit.py --window <nome_finestra>
Non chiedere al modder di eseguirlo. Il gate è obbligatorio prima di qualsiasi valutazione manuale.
```

---

### FASE 4 — Prompt: Riscrivere il Punto di Ingresso

**Obiettivo**: il prompt `converti-finestra-dual-mode.prompt.md` diventa l'unico comando che il modder usa per avviare la conversione di una finestra.

#### 4.1 — Riscrivere `converti-finestra-dual-mode.prompt.md`

File: `.github/prompts/converti-finestra-dual-mode.prompt.md`

Contenuto attuale: incompleto, non specifica "estrai da sorgenti reali", non ha checkpoint manuali.

Nuovo contenuto:

```markdown
---
agent: agent
description: Converte una singola finestra GUI CK3 al sistema dual-mode OCR/Vanilla. UNA FINESTRA ALLA VOLTA.
tools: [read, search, terminal]
---

# Conversione Dual-Mode — Una Finestra

Leggi prima le istruzioni globali: `${file:.github/copilot-instructions.md}`
Leggi il pattern canonical: `${file:.github/resources/dual_mode_pattern_canonical.md}`
Leggi i pattern di conversione: `${file:.github/resources/conversion-patterns.md}`

## Input

- Nome finestra: ${input:nomeFinestra}
- Pattern di conversione: ${input:pattern} (simple | tabs | complex)

## File sorgente (sola lettura obbligatoria)

- OCR upstream: `../CK3-OCR/OCR-Support/gui/${input:nomeFinestra}.gui`
- Vanilla CK3: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/${input:nomeFinestra}.gui`
- Patch attuale: `ocr_support_compatibility_pach/gui/${input:nomeFinestra}.gui`

## Sequenza operativa — SEGUIRE NELL'ORDINE, NON SALTARE PASSI

### PASSO 1 — Analisi tri-repo
```
python tools/tri_diff.py --window ${input:nomeFinestra}
```
Mostrare il report completo al modder. Aspettare conferma prima di continuare.

### PASSO 2 — Verifica sorgenti
Verificare che entrambi i file sorgente esistano:
- Se OCR upstream mancante: comunicarlo al modder, STOP.
- Se vanilla mancante: comunicarlo al modder, STOP.
- Se entrambi presenti: procedere.

### PASSO 3 — Bozza assemblaggio (DRY-RUN)
```
python tools/assemble_dualmode.py --window ${input:nomeFinestra} --mode ${input:pattern} --dry-run
```
Mostrare l'output completo al modder.

### CHECKPOINT 1 — APPROVAZIONE MODDER OBBLIGATORIA
**STOP. Chiedere al modder: "La bozza è corretta? Posso scrivere il file nella patch?"**
Non procedere senza risposta affermativa esplicita.

### PASSO 4 — Scrittura file nella patch
```
python tools/assemble_dualmode.py --window ${input:nomeFinestra} --mode ${input:pattern}
```

### PASSO 5 — Estrazione scope e aggiornamento whitelist
```
python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/${input:nomeFinestra}.gui
```
Aggiungere alla whitelist tutti i binding ASSENTI.

### PASSO 6 — Audit automatico
```
python tools/audit.py --window ${input:nomeFinestra}
```
- Se BLOCCANTE: elencare i CRITICO, correggerli, ri-eseguire audit. Non procedere fino a OK.
- Se CON AVVERTENZE: documentarle per il modder, procedere con nota.
- Se OK: procedere.

### CHECKPOINT 2 — VERDETTO AUDIT AL MODDER
Mostrare il verdetto completo di audit.py al modder prima di passare ai revisori.

### PASSO 7 — Revisori
Invocare in sequenza:
1. Agente Revisore Accessibilità
2. Agente Revisore Vanilla
3. Agente Auditore Finale → emette APPROVED o BLOCKED

### PASSO 8 — Chiusura
- Se APPROVED: aggiornare `gui-conversion-progress.instructions.md`
- Se BLOCKED: elencare fix richiesti, aspettare istruzioni modder

## Vincolo assoluto
Dopo il completamento, NON proporre di iniziare un'altra finestra.
Attendere istruzioni esplicite del modder per qualsiasi operazione successiva.
```

---

### FASE 5 — Skills: Riallineamento al Nuovo Approccio

**Obiettivo**: le skills devono riflettere il paradigma "estrai da sorgenti reali, non generare".

#### 5.1 — Riscrivere `dual-mode-template-generator.skill.md`

File: `.github/copilot-skills/dual-mode-template-generator.skill.md`

Problema attuale: genera scheletri con `[PlaceholderBinding]` che poi l'implementatore riempie a mano. Con il nuovo approccio il contenuto viene estratto dai file sorgente, non generato.

Nuovo paradigma della skill:
- Il parametro `sections` diventa opzionale
- Viene aggiunto parametro `ocr_source_path` (path del file OCR upstream)
- Viene aggiunto parametro `vanilla_source_path` (path del file vanilla)
- Se i path sono forniti: la skill legge i file e produce il template con contenuto reale
- Se i path non sono forniti (retrocompatibilità): comportamento attuale con placeholder, deprecato

Aggiungere nota esplicita:
```
> DEPRECATO: generazione da placeholder. Usare assemble_dualmode.py --dry-run per
> visualizzare la bozza di assemblaggio prima di usare questa skill.
> Questa skill rimane utile solo per finestre nuove senza sorgente OCR esistente.
```

#### 5.2 — Verificare `tri-repo-diff.skill.md`

La skill attualmente dice di eseguire `python tools/tri_diff.py` come "pre-run automatico" ma poi fa lo stesso lavoro con logica LLM interna.

Modifica: rendere esplicito che con `terminal` disponibile lo script viene eseguito direttamente e l'output dello script è la fonte primaria. La skill usa la logica LLM solo per interpretare le discrepanze della Sezione C, non per ricalcolare l'intero diff.

---

### FASE 6 — Instructions: Aggiornamenti di Coerenza

#### 6.1 — Aggiornare `workflow-nuova-finestra.instructions.md`

File: `.github/instructions/workflow-nuova-finestra.instructions.md`

Modifiche:
- Passo 0: specificare che `tri_diff.py` viene eseguito dall'agente direttamente, non dal modder
- Passo 3-4: sostituire con riferimento a `assemble_dualmode.py` (non più `assemble_army_dualmode.py`)
- Aggiungere i due CHECKPOINT di approvazione manuale nella tabella
- Aggiungere riga nella tabella per il `--dry-run` come passo obbligatorio pre-scrittura

Nuova tabella sequenza:

| Passo | Chi | Azione |
|-------|-----|--------|
| 1 | Agente | `python tools/tri_diff.py --window nome` |
| 2 | Agente | Verifica esistenza file sorgente |
| 3 | Agente | `python tools/assemble_dualmode.py --window nome --mode X --dry-run` |
| **CP1** | **MODDER** | **Approva bozza o chiede modifiche** |
| 4 | Agente | `python tools/assemble_dualmode.py --window nome --mode X` |
| 5 | Agente | `python tools/scope_extractor.py --file ...` |
| 6 | Agente | `python tools/audit.py --window nome` |
| **CP2** | **MODDER** | **Prende nota del verdetto audit** |
| 7 | Agente | Revisore Accessibilità → Revisore Vanilla → Auditore Finale |
| 8 | Agente | Aggiorna `gui-conversion-progress.instructions.md` |

#### 6.2 — Aggiornare `gui-conversion-progress.instructions.md`

Verificare che la lista delle finestre da convertire sia aggiornata. Aggiungere colonna "Pattern" per ogni finestra (A/B/C/D) per guidare la scelta del `--mode` corretto nello script.

---

### FASE 7 — copilot-instructions.md: Aggiornamenti Finali

File: `.github/copilot-instructions.md`

Modifiche:
1. Aggiornare la tabella strumenti sotto "Struttura Repository": sostituire `assemble_army_dualmode.py` con `assemble_dualmode.py`
2. Aggiungere sezione "Principio di Controllo Manuale":
   ```
   ## Principio di Controllo Manuale (non negoziabile)
   - Il modder approva SEMPRE prima che il file venga scritto nella patch (CHECKPOINT 1)
   - Il modder vede SEMPRE il verdetto di audit prima dei revisori (CHECKPOINT 2)
   - Il sistema NON avvia mai la conversione di una finestra successiva automaticamente
   - Una finestra alla volta. Sempre.
   ```
3. Aggiornare la lista degli script sotto `tools/`: rimuovere gli script eliminati in FASE 1

---

## Ordine di Esecuzione per Copilot

Copilot deve eseguire le fasi nell'ordine indicato. Non passare alla fase successiva senza completare quella corrente.

```
FASE 1 → Pulizia repository
   1.1 Elimina 6 script obsoleti
   1.2 Fix path in assemble_army_dualmode.py

FASE 2 → Refactor script core
   2.1 Refactor assemble_army_dualmode.py → assemble_dualmode.py
       → test di regressione su window_army
       → solo se regressione OK: elimina assemble_army_dualmode.py
   2.2 Fix tri_diff.py Sezione C

FASE 3 → Aggiornamento agenti
   3.1 Analista: aggiungi terminal
   3.2 Implementatore: aggiungi terminal, riscrivi passi 0/3-4/7-8
   3.3 Auditore: aggiungi terminal, aggiorna Sezione 0

FASE 4 → Riscrivi prompt principale
   4.1 converti-finestra-dual-mode.prompt.md

FASE 5 → Aggiornamento skills
   5.1 dual-mode-template-generator: nuovo paradigma
   5.2 tri-repo-diff: chiarimento ruolo con terminal

FASE 6 → Aggiornamento instructions
   6.1 workflow-nuova-finestra
   6.2 gui-conversion-progress (aggiunta colonna Pattern)

FASE 7 → Aggiornamento copilot-instructions.md
```

---

## Criteri di Successo

Il framework è ristrutturato correttamente quando:

1. `python tools/assemble_dualmode.py --window window_faith --mode complex --dry-run` produce un file dual-mode valido senza errori
2. `python tools/audit.py --window window_faith` su quel file restituisce OK o CON AVVERTENZE (non BLOCCANTE)
3. Il prompt `#converti-finestra` eseguito in Copilot agent mode completa la sequenza senza richiedere al modder di aprire un terminale separato
4. Dopo il completamento il sistema non propone automaticamente la finestra successiva
5. `assemble_army_dualmode.py` non esiste più nel repository
6. Gli 6 script obsoleti non esistono più nel repository

---

## Note per Copilot

- Leggere questo piano dall'inizio alla fine prima di iniziare qualsiasi modifica
- Eseguire FASE 1 prima di qualsiasi altra cosa — non modificare script da eliminare
- Il test di regressione in FASE 2.1 è obbligatorio — non saltarlo
- Ogni fase completata: comunicare al modder prima di passare alla successiva
- Se un passo è ambiguo: chiedere chiarimenti al modder, non procedere per ipotesi
- Non modificare mai file in `../CK3-OCR/` o `../CK3 ORIGINAL VERSION/` — sola lettura assoluta
- Non modificare file in `ocr_support_compatibility_pach/gui/` tranne quando esplicitamente richiesto dal piano (FASE 2.1, test di regressione)
