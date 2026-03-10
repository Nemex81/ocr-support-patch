# Piano di Implementazione — Framework Copilot CK3 OCR Accessibility
> **Versione**: 2.0 — Validato da Opus 4.6, corretto il 2026-03-10
> **Correzioni applicate**: 7 (5 critiche + 2 significative) — vedi sezione CHANGELOG

> **DOCUMENTO PER COPILOT — AGENT MODE**
>
> Questo documento è scritto per essere letto ed eseguito da GitHub Copilot in Agent Mode
> su VSCode Insiders (versione marzo 2026, v1.111+).
>
> **Obiettivo**: costruire un framework completo di sviluppo per il modding di CK3
> accessibile ai giocatori non vedenti, sfruttando tutte le funzionalità avanzate
> di Copilot disponibili nella versione corrente.
>
> **Come usare questo documento**:
> Apri Copilot Chat in Agent Mode, seleziona questo file come contesto,
> e chiedi: *"Implementa il piano in questo documento, fase per fase"*.
> Copilot eseguirà ogni fase in sequenza, creando e modificando i file indicati.

---

## CHANGELOG — Correzioni v2.0

| # | Errore | Correzione applicata |
|---|--------|---------------------|
| C1 | Tool alias sbagliati in tutti gli agenti | Sostituiti: `codebase`→`search`, `read_file`→`read`, `fetch`→`web`, `editFiles`→`edit` |
| C2 | Hook format sbagliato (non può invocare agenti) | **Fase 6 eliminata**. Hook da introdurre in fase successiva come script shell |
| C3 | Path vanilla con trattini, sbagliato | Corretto in `../CK3 ORIGINAL VERSION/ck3origin/` (con spazi) ovunque |
| C4 | File `coding_ai/gui/` citati ma inesistenti | Aggiunta **Fase 0** che li crea prima di tutto il resto |
| C5 | `handoffs` nei prompt non supportato | Rimosso dai file `.prompt.md`. Handoffs solo negli agenti `.agent.md` |
| C6 | Settings keys dubbie o inutili | Ridotte alle sole chiavi verificate in VSCode Insiders |
| C7 | Schema `handoffs` agenti non verificabile | Nota aggiunta: testare manualmente dopo Fase 3, rimuovere se non funzionano |

---

## Stato Attuale del Repository

Prima di implementare, Copilot deve sapere cosa esiste già.

### File già presenti (NON ricreare):

```
.github/
├── copilot-instructions.md          ← ESISTE, va MODIFICATO (vedi Fase 1)
└── prompts/                         ← ESISTE, va ESTESO (vedi Fase 2)
    ├── converti-finestra-dual-mode.prompt.md
    ├── analizza-finestra.prompt.md
    ├── verifica-dual-mode.prompt.md
    ├── debug-errore-jomini.prompt.md
    └── genera-container-ocr.prompt.md

coding_ai/
└── PIANO_IMPLEMENTAZIONE_FRAMEWORK.md   ← questo file, non toccare

.vscode/
└── settings.json                    ← ESISTE, va MODIFICATO (vedi Fase 5)

ck3_modding.code-workspace           ← ESISTE, mantenere
```

> ⚠️ ATTENZIONE: i file `coding_ai/gui/jomini_scope_whitelist.md`,
> `coding_ai/gui/dual_mode_pattern_canonical.md` e `coding_ai/gui/priority_list.md`
> NON esistono ancora. Vengono creati nella Fase 0.

### File da creare (obiettivo di questo piano):

```
coding_ai/gui/                       ← CREARE (Fase 0)
├── jomini_scope_whitelist.md
├── dual_mode_pattern_canonical.md
└── priority_list.md

.github/
├── agents/                          ← CREARE (Fase 3)
│   ├── analista-tri-repo.agent.md
│   ├── architetto-dual-mode.agent.md
│   ├── implementatore-patch.agent.md
│   ├── revisore-accessibilita.agent.md
│   ├── revisore-vanilla.agent.md
│   └── auditore-finale.agent.md
└── instructions/                    ← CREARE (Fase 4)
    ├── gui-jomini.instructions.md
    └── localization-ocr.instructions.md
```

> ℹ️ La Fase 6 (hooks pre-commit) è stata **eliminata** da questa versione del piano.
> Gli hook richiedono script shell esterni e non possono invocare agenti direttamente.
> Verranno introdotti in una fase successiva separata.

---

## FASE 0 — Crea i File di Riferimento in `coding_ai/gui/`

**Priorità**: PRIMA DI TUTTO. Gli agenti della Fase 3 li referenziano come obbligatori.
**Azione**: CREARE la cartella `coding_ai/gui/` e i 3 file seguenti.

### 0a. `coding_ai/gui/jomini_scope_whitelist.md`

```markdown
# Jomini Scope Whitelist — CK3 1.17.1

Scope e binding verificati nei file vanilla di CK3 1.17.1.
Copilot NON deve usare scope non presenti qui senza verifica esplicita nel vanilla.

## Scope GUI principali verificati

| Scope | Contesto | Note |
|-------|---------|------|
| `GetPlayer` | globale | personaggio del giocatore |
| `GetCharacter` | contesto personaggio | richiede scope parent corretto |
| `GetTitle` | contesto titolo | richiede scope parent corretto |
| `GetFaith` | contesto fede | richiede scope parent corretto |
| `GetCulture` | contesto cultura | richiede scope parent corretto |
| `GetDynasty` | contesto dinastia | richiede scope parent corretto |
| `GetHouse` | contesto casata | richiede scope parent corretto |
| `GetArmy` | contesto esercito | richiede scope parent corretto |
| `GetWar` | contesto guerra | richiede scope parent corretto |
| `GetFaction` | contesto fazione | richiede scope parent corretto |
| `GameRules` | globale | accesso alle game rules |

## Binding Dual Mode (obbligatori, non modificare)

```jomini
# Visibilità OCR attiva
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('yes')]"
# Visibilità vanilla attiva
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('no')]"
```

## Pattern binding dati comuni verificati

```jomini
# Oro del giocatore
text = "[GetPlayer.GetTreasury|0]"
# Pietà
text = "[GetPlayer.GetPiety|0]"
# Prestigio
text = "[GetPlayer.GetPrestige|0]"
# Nome UI senza tooltip
text = "[GetPlayer.GetUINameNoTooltip]"
# Data corrente
text = "[GetDate]"
```

## Note operative

- Il modificatore `|0` formatta i numeri — usarlo sempre per valori numerici
- I scope dipendono dal contesto widget parent — verificare sempre la gerarchia
- In caso di dubbio: aprire il file vanilla corrispondente e copiare il binding esatto
- Se un scope non è in questa lista: aggiungerlo solo dopo verifica manuale nel vanilla

**Aggiornare questo file ogni volta che si verifica un nuovo scope nel vanilla.**
Ultimo aggiornamento: 2026-03-10
```

### 0b. `coding_ai/gui/dual_mode_pattern_canonical.md`

```markdown
# Pattern Canonical Dual Mode — CK3 1.17.1

Template di riferimento verificato per il dual mode OCR/vanilla.
Da usare come base per ogni nuova finestra.

## Struttura Minima Verificata

```jomini
# File: ocr_support_compatibility_pach/gui/window_esempio.gui
# Versione CK3: 1.17.1

window = {
    name = "window_esempio"
    size = { 800 600 }

    # =============================================
    # BLOCCO OCR — solo testo, screen reader ready
    # =============================================
    container = {
        name = "ocr_esempio_container"
        visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('yes')]"
        size = { 100% 100% }

        vbox = {
            layoutpolicy_horizontal = expanding
            layoutpolicy_vertical = expanding
            spacing = 4

            # Header sezione — testo giallo obbligatorio
            text_label = {
                name = "ocr_title"
                text = "ESEMPIO — [GetPlayer.GetUINameNoTooltip]"
                fontsize = 20
                autoresize = yes
                color = { 255 221 136 255 }
            }

            # Dato informativo
            text_single = {
                name = "ocr_dato_oro"
                text = "Oro: [GetPlayer.GetTreasury|0]"
                fontsize = 18
                autoresize = yes
            }

            # Bottone con tooltip obbligatorio
            button = {
                name = "ocr_close_button"
                text = "[ Chiudi finestra ]"
                fontsize = 18
                tooltip = "Chiude la finestra Esempio"
                onclick = "[ExecuteConsoleCommand('close_window window_esempio')]"
            }
        }
    }

    # =============================================
    # BLOCCO VANILLA — copia fedele del CK3 originale
    # NON MODIFICARE MAI — identico al vanilla
    # =============================================
    container = {
        name = "vanilla_esempio_container"
        visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('no')]"

        # Incollare qui il contenuto originale dal file vanilla
        # senza nessuna modifica
    }
}
```

## Regole Invariabili

1. I due container sono **mutuamente esclusivi** via `visible`
2. Il container vanilla è **identico** al file CK3 originale — nessuna modifica
3. Font size OCR **minimo 18** ovunque
4. Header sezione OCR: colore `{ 255 221 136 255 }` (giallo), fontsize 20
5. Tutti i bottoni OCR hanno `tooltip` descrittivo
6. Nessun `name` duplicato allo stesso livello gerarchico

## Checklist Pre-Commit

- [ ] Visibility mutuamente esclusive e corrette
- [ ] Container vanilla identico al file CK3 originale
- [ ] Font size >= 18 in tutto il blocco OCR
- [ ] Ogni bottone OCR ha tooltip
- [ ] Nessun nome widget duplicato a stesso livello
- [ ] Nessun scope non verificato nella whitelist
```

### 0c. `coding_ai/gui/priority_list.md`

```markdown
# Priority List — Finestre da Convertire

Stato aggiornato al: 2026-03-10

## ✅ Già Convertite

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

## 🔄 Da Convertire

| File | Priorità | Motivazione |
|------|----------|-------------|
| `window_army.gui` | ALTA | Gestione eserciti, uso frequente |
| `window_war.gui` | ALTA | Interfaccia guerra |
| `window_title.gui` | ALTA | Gestione titoli |
| `window_government.gui` | ALTA | Governo/leggi |
| `window_vassal_contracts.gui` | MEDIA | Contratti vassalli |
| `window_schemes.gui` | MEDIA | Schema dettaglio |
| `window_hook.gui` | MEDIA | Ganci/segreti |
| `window_travel.gui` | MEDIA | Viaggio |
| `window_struggle.gui` | BASSA | Conflitti regionali |
```

---

## FASE 1 — Aggiorna `.github/copilot-instructions.md`

**Azione**: MODIFICARE il file esistente — appendere in fondo. NON riscrivere da zero.

**Sezione da aggiungere in fondo al file**:

```markdown
---

## Agenti Disponibili in Questo Workspace

Il progetto dispone di agenti specializzati in `.github/agents/`.
VS Code li scopre automaticamente — selezionali nel picker agenti di Copilot Chat.
Ciascun agente ha un ruolo fisso: non uscire dal ruolo assegnato.

| Agente | File | Ruolo |
|--------|------|-------|
| Analista Tri-Repo | `analista-tri-repo.agent.md` | Solo lettura e confronto tra i 3 repo |
| Architetto Dual-Mode | `architetto-dual-mode.agent.md` | Progetta struttura OCR/vanilla, no edit |
| Implementatore Patch | `implementatore-patch.agent.md` | Scrive codice solo in `ocr_support_compatibility_pach/` |
| Revisore Accessibilità | `revisore-accessibilita.agent.md` | Verifica qualità OCR/NVDA, no edit |
| Revisore Vanilla | `revisore-vanilla.agent.md` | Verifica fedeltà al vanilla originale, no edit |
| Auditore Finale | `auditore-finale.agent.md` | Review completa pre-commit, no edit |

## Workflow Raccomandato per Nuova Finestra

Sequenza standard con handoff tra agenti:
1. **Analista Tri-Repo** — analizza i 3 file, produce report strutturale
2. **Architetto Dual-Mode** — progetta la struttura OCR basandosi sul report
3. **Implementatore Patch** — scrive il codice seguendo il progetto
4. **Revisore Accessibilità** — verifica leggibilità NVDA, tooltip, ordine lettura
5. **Revisore Vanilla** — verifica fedeltà container vanilla al CK3 originale
6. **Auditore Finale** — checklist completa, APPROVED o BLOCKED

## Istruzioni Specifiche per Dominio

Attivate automaticamente per tipo di file:
- `.github/instructions/gui-jomini.instructions.md` → attiva per `*.gui`
- `.github/instructions/localization-ocr.instructions.md` → attiva per `*.yml`

## Percorsi Repository di Riferimento

- Patch attiva: `ocr_support_compatibility_pach/gui/`
- OCR upstream (Agamidae): `../CK3-OCR/OCR-Support/gui/`
- Vanilla CK3 1.17.1: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/`

> ⚠️ Il path vanilla usa spazi, NON trattini: `CK3 ORIGINAL VERSION`
```

---

## FASE 2 — Aggiorna i Prompt Esistenti

**Azione**: i prompt NON supportano `handoffs` nel frontmatter.
I handoffs sono implementati negli agenti (Fase 3).
Qui si aggiunge solo il prompt mancante e si corregge il tool alias nei prompt esistenti.

### 2a. Correggi tool alias nei 3 prompt esistenti

In `converti-finestra-dual-mode.prompt.md`, `analizza-finestra.prompt.md`,
`verifica-dual-mode.prompt.md`:

Sostituire nel frontmatter:
```yaml
# DA (sbagliato)
tools: [codebase, read_file]

# A (corretto)
tools: [read, search]
```

### 2b. CREA NUOVO — `aggiornamento-upstream.prompt.md`

```markdown
---
mode: agent
description: Confronta la patch con upstream OCR e vanilla per rilevare aggiornamenti
tools: [read, search]
---

# Task: Aggiornamento da Upstream

Leggi: `${file:.github/copilot-instructions.md}`

## File da confrontare
- Patch attuale: `ocr_support_compatibility_pach/gui/${input:nomeFile}.gui`
- OCR upstream: `../CK3-OCR/OCR-Support/gui/${input:nomeFile}.gui`
- Vanilla baseline: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/${input:nomeFile}.gui`

## Cosa rilevare

1. **Differenze upstream → patch**: cosa ha aggiornato Agamidae non ancora nella patch?
2. **Differenze vanilla → container vanilla patch**: il container vanilla è ancora fedele?
3. **Regressioni**: la patch introduce comportamenti assenti nell'originale OCR?
4. **Conflitti**: ci sono modifiche incompatibili tra upstream e vanilla baseline?

## Output

Report in italiano con:
- Lista diff rilevanti (non cosmetici) upstream vs patch
- Lista diff vanilla baseline vs container vanilla nella patch
- Raccomandazioni prioritizzate: applicare subito / valutare / ignorare
- Rischi di regressione per ogni aggiornamento proposto

## Passo successivo suggerito

Se ci sono aggiornamenti da applicare: invoca **Implementatore Patch** dalla chat.
```

---

## FASE 3 — Crea gli Agenti Custom in `.github/agents/`

> ⚠️ NOTA SU `handoffs`: il campo `handoffs` negli agenti è documentato ma lo schema
> interno (label/agent/prompt/send) non è verificabile dalla documentazione pubblica.
> **Procedere con la struttura proposta e testare manualmente il primo agente creato.**
> Se i handoff non appaiono nell'UI di VS Code dopo la creazione, rimuoverli da tutti
> gli agenti e sostituirli con istruzioni testuali nel corpo che suggeriscono il prossimo
> agente da invocare manualmente.

> ℹ️ VS Code scopre automaticamente gli agenti da `.github/agents/` — nessuna
> configurazione aggiuntiva in settings.json necessaria.

### 3a. `analista-tri-repo.agent.md`

```markdown
---
name: Analista Tri-Repo
description: Analizza e confronta i tre repository CK3 (patch, OCR upstream, vanilla). Solo lettura, nessuna modifica.
tools: [read, search]
handoffs:
  - label: "→ Progetta struttura"
    agent: architetto-dual-mode
    prompt: "Basandoti sull'analisi appena prodotta, progetta la struttura dual mode."
    send: false
---

# Analista Tri-Repo — CK3 OCR Accessibility

Sei l'agente di analisi del progetto. Il tuo ruolo è SOLO leggere e confrontare.
Non modifichi mai nessun file, non proponi fix, non scrivi codice.

## I Tre Repository

- **Patch attiva**: `ocr_support_compatibility_pach/gui/`
- **OCR upstream** (Agamidae): `../CK3-OCR/OCR-Support/gui/`
- **Vanilla CK3 1.17.1**: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/`

> ⚠️ Il path vanilla usa spazi: `CK3 ORIGINAL VERSION` (non trattini)

## Metodologia

Per ogni analisi:
1. Leggi i tre file corrispondenti
2. Mappa la struttura gerarchica (tipo widget, nome, profondità)
3. Identifica cosa è presente solo in uno, in due, in tutti e tre
4. Segnala discrepanze tra container vanilla della patch e file vanilla originale
5. Segnala feature OCR dell'upstream assenti nella patch
6. Produci il report in italiano, formato markdown strutturato

## Passo successivo

Dopo l'analisi, suggerisci di invocare **Architetto Dual-Mode** per la progettazione.
```

### 3b. `architetto-dual-mode.agent.md`

```markdown
---
name: Architetto Dual-Mode
description: Progetta la struttura OCR/vanilla per una finestra CK3. Solo progettazione, nessuna modifica.
tools: [read, search]
handoffs:
  - label: "→ Implementa"
    agent: implementatore-patch
    prompt: "Implementa il progetto architetturale appena definito."
    send: false
---

# Architetto Dual-Mode — CK3 OCR Accessibility

Ricevi l'analisi dall'Analista Tri-Repo e produci un documento di progetto.
Non modifichi mai file .gui direttamente.

## Input atteso

Report dell'Analista Tri-Repo con la struttura della finestra da convertire.

## Output da produrre

Documento di progetto in italiano con:
1. **Struttura container OCR**: lista widget da creare, con tipo e nome
2. **Binding da usare**: scope e datatype per ogni dato
3. **Sezioni e header**: titolo di ogni sezione OCR
4. **Bottoni OCR**: testo e tooltip per ogni azione
5. **Container vanilla**: conferma uso vanilla originale invariato
6. **Rischi**: pattern Jomini ambigui, scope da verificare, edge case
7. **Sequenza implementazione**: ordine consigliato

## Riferimenti obbligatori

- Pattern: `coding_ai/gui/dual_mode_pattern_canonical.md`
- Scope verificati: `coding_ai/gui/jomini_scope_whitelist.md`

## Regole architetturali

- Usa SOLO scope presenti nella whitelist. Se manca: segnalare come "DA VERIFICARE"
- Container vanilla: identico al file `../CK3 ORIGINAL VERSION/ck3origin/game/gui/[file].gui`
- Font size OCR minimo 18 | Header: colore `{ 255 221 136 255 }` (giallo)

## Passo successivo

Dopo il progetto, suggerisci di invocare **Implementatore Patch**.
```

### 3c. `implementatore-patch.agent.md`

```markdown
---
name: Implementatore Patch
description: Scrive e modifica i file .gui della patch. Opera SOLO su ocr_support_compatibility_pach/.
tools: [edit, read, search]
handoffs:
  - label: "→ Verifica Accessibilità"
    agent: revisore-accessibilita
    prompt: "Verifica qualità OCR e accessibilità NVDA del file appena modificato."
    send: false
  - label: "→ Verifica Vanilla"
    agent: revisore-vanilla
    prompt: "Verifica che il container vanilla sia fedele al CK3 originale."
    send: false
---

# Implementatore Patch — CK3 OCR Accessibility

Sei l'UNICO agente autorizzato a modificare file.
Operi ESCLUSIVAMENTE in `ocr_support_compatibility_pach/gui/`.
Non tocchi mai `../CK3-OCR/` o `../CK3 ORIGINAL VERSION/`.

## Regole operative

1. Prima di modificare: leggi il file attuale nella patch
2. Leggi il corrispondente vanilla da `../CK3 ORIGINAL VERSION/ck3origin/game/gui/`
3. Container vanilla = copia fedele del vanilla — copialo direttamente senza modifiche
4. Container OCR = segue il progetto dell'Architetto o il pattern canonical
5. Ogni modifica è minima — non toccare ciò che non è nel task
6. Dopo ogni edit: verifica assenza di `name` duplicati allo stesso livello

## Riferimenti obbligatori (leggere prima di ogni implementazione)

- Istruzioni globali: `.github/copilot-instructions.md`
- Pattern: `coding_ai/gui/dual_mode_pattern_canonical.md`
- Scope: `coding_ai/gui/jomini_scope_whitelist.md`

## Cosa NON fare

- Non modificare file fuori da `ocr_support_compatibility_pach/gui/`
- Non toccare `coding_ai/`, `.github/`, `.vscode/`, `ck3_modding.code-workspace`
- Non inventare scope o binding non nella whitelist
- Non "migliorare" il container vanilla

## Passo successivo

Dopo l'implementazione, suggerisci di invocare **Revisore Accessibilità** e **Revisore Vanilla**.
```

### 3d. `revisore-accessibilita.agent.md`

```markdown
---
name: Revisore Accessibilità
description: Verifica qualità OCR e accessibilità NVDA dei file convertiti. Solo lettura e report.
tools: [read, search]
handoffs:
  - label: "→ Fix implementatore"
    agent: implementatore-patch
    prompt: "Applica i fix di accessibilità identificati nel report di revisione."
    send: false
  - label: "→ Audit Finale"
    agent: auditore-finale
    prompt: "Esegui l'audit finale su questo file."
    send: false
---

# Revisore Accessibilità — CK3 OCR Accessibility

Il tuo utente finale è un giocatore non vedente che usa NVDA.
Non modifichi mai file. Produci solo report.

## Checklist NVDA

### Leggibilità
- [ ] Font size >= 18 in tutti i widget OCR
- [ ] Testo normale: bianco | Header: giallo `{ 255 221 136 255 }`
- [ ] Nessun testo abbreviato senza tooltip
- [ ] Numeri con unità e contesto ("Oro: 450" non "450")

### Navigazione
- [ ] Ogni sezione ha header testuale esplicito
- [ ] Ordine lettura top→down riflette gerarchia informativa
- [ ] Sezioni secondarie indentate o separate
- [ ] Tab con header descrittivi del contenuto

### Bottoni
- [ ] Ogni bottone ha `tooltip` con descrizione azione
- [ ] Testo bottone è descrittivo (non solo simbolo)
- [ ] Azioni irreversibili hanno warning nel tooltip

### Binding
- [ ] Nessun binding che produce stringa vuota in condizioni normali
- [ ] Valori condizionali hanno fallback testuale
- [ ] Liste vuote hanno messaggio esplicito

## Output

Una riga per voce: ✅ OK / ⚠️ Attenzione / ❌ Critico
Per ogni problema: widget, riga stimata, fix raccomandato.
Verdetto finale: **PASS** / **PASS CON RISERVE** / **FAIL**
```

### 3e. `revisore-vanilla.agent.md`

```markdown
---
name: Revisore Vanilla
description: Verifica fedeltà del container vanilla alla baseline CK3 originale. Solo lettura.
tools: [read, search]
handoffs:
  - label: "→ Fix vanilla"
    agent: implementatore-patch
    prompt: "Ripristina la fedeltà del container vanilla rispetto al CK3 originale."
    send: false
---

# Revisore Vanilla — CK3 OCR Accessibility

Confronti il container vanilla nella patch con il file CK3 originale.
Qualsiasi differenza non autorizzata è un bug. Non modifichi mai file.

## Metodologia

1. Leggi file patch: `ocr_support_compatibility_pach/gui/[file].gui`
2. Leggi vanilla: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/[file].gui`
3. Estrai solo il blocco `vanilla_*_container` dalla patch
4. Confronta con il vanilla originale
5. Documenta ogni differenza

## Differenze Accettabili

- Wrapper container aggiunto: `container { name = "vanilla_*_container" visible = "..." }`
- Indentazione diversa per formattazione
- Commenti aggiunti (righe `#`)

## Differenze NON Accettabili (= bug)

- Widget rimossi o aggiunti rispetto al vanilla
- Proprietà modificate (size, position, type, name, binding)
- Ordine widget alterato

## Output

Lista differenze con tipo (accettabile / bug).
Per ogni bug: widget coinvolto, patch vs atteso.
Verdetto: **FEDELE** / **MODIFICATO CON BUG** / **DA RIFARE**
```

### 3f. `auditore-finale.agent.md`

```markdown
---
name: Auditore Finale
description: Audit completo pre-commit. Emette verdetto APPROVED o BLOCKED. Solo lettura.
tools: [read, search]
handoffs:
  - label: "→ Fix implementatore"
    agent: implementatore-patch
    prompt: "Risolvi i problemi critici identificati nell'audit prima del commit."
    send: false
---

# Auditore Finale — CK3 OCR Accessibility

Sei l'ultimo controllo prima del commit. Non modifichi mai file.
Il tuo verdetto è vincolante: **APPROVED** o **BLOCKED**.

## Checklist Completa

### Struttura
- [ ] UN container OCR e UN container vanilla per ogni window
- [ ] Visibility mutuamente esclusive con game_rule corretta
- [ ] Nessun `name` duplicato allo stesso livello gerarchico
- [ ] Blockoverride gestiti correttamente

### Qualità OCR
- [ ] Font size >= 18 ovunque nel blocco OCR
- [ ] Tutti i bottoni OCR hanno tooltip
- [ ] Tutte le sezioni hanno header giallo
- [ ] Ordine lettura NVDA corretto

### Fedeltà Vanilla
- [ ] Container vanilla identico al file CK3 originale (diff pulito)

### Compatibilità CK3 1.17.1
- [ ] Nessun scope non verificato nella whitelist
- [ ] Nessun widget type non documentato per 1.17.1
- [ ] Nessun binding che referenzia feature di versioni successive

### Completezza
- [ ] TUTTE le informazioni del vanilla rappresentate nell'OCR
- [ ] Nessuna funzionalità vanilla inaccessibile in modalità OCR
- [ ] Tab multipli: tutti con il loro blocco OCR

## Output

**APPROVED** — pronto per commit, nessun blocco critico

oppure

**BLOCKED** — problemi da risolvere prima del commit:
- `[CRITICO]` widget + problema + fix richiesto
- `[ATTENZIONE]` raccomandazione non bloccante

Non emettere APPROVED con problemi CRITICI aperti.
```

---

## FASE 4 — Crea le Istruzioni di Dominio in `.github/instructions/`

Le instruction files si attivano automaticamente per glob pattern.

### 4a. `gui-jomini.instructions.md`

```markdown
---
applyTo: "**/*.gui"
---

# Istruzioni Jomini GUI — CK3 1.17.1

Attive automaticamente per tutti i file `.gui`.

## Widget Consentiti nel Blocco OCR

`container`, `vbox`, `hbox`, `flowcontainer`, `text_single`, `text_multi`,
`text_label`, `button`, `fixedgridwidget`, `scrollarea`

## Widget VIETATI nel Blocco OCR

`icon` senza tooltip, `portrait_button`, `coa_shield_slot`, `map_zoom_widget`,
qualunque widget con solo contenuto grafico e nessun testo.

## Proprietà Obbligatorie

```jomini
text_single = {
    name = "nome_univoco"
    text = "[Binding o stringa]"
    fontsize = 18
    autoresize = yes
}

button = {
    name = "ocr_nome_button"
    text = "[ Descrizione azione ]"
    fontsize = 18
    tooltip = "Descrizione estesa per screen reader"
    onclick = "[...]"
}
```

## Visibility Dual Mode (unica sintassi valida)

```jomini
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('yes')]"
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('no')]"
```
```

### 4b. `localization-ocr.instructions.md`

```markdown
---
applyTo: "**/localization/**/*.yml"
---

# Istruzioni Localizzazione OCR — CK3 1.17.1

Attive automaticamente per tutti i file `.yml` di localizzazione.

## Convenzioni Chiavi OCR

Prefisso obbligatorio `ocr_`:

```yaml
# Formato: ocr_[finestra]_[sezione]_[elemento]
ocr_character_stats_gold: "Oro: "
ocr_council_task_current: "Compito attuale: "
```

## Requisiti per Screen Reader NVDA

- Nessuna abbreviazione senza spiegazione
- Nessun simbolo grafico come unico contenuto
- Testo sensato se letto ad alta voce
- Numeri con unità: "450 oro" non "450"
- Bonus/malus espliciti: "+15% velocità movimento" non "+15%"

## Encoding

- UTF-8 BOM (obbligatorio per CK3)
- Prima riga: `l_english:`
- Indentazione: 1 spazio prima della chiave
```

---

## FASE 5 — Aggiorna `.vscode/settings.json`

**Azione**: MODIFICARE aggiungendo SOLO queste chiavi verificate in VSCode Insiders.
Non aggiungere chiavi non presenti in questa lista.

```json
"github.copilot.nextEditSuggestions.enabled": true,
"github.copilot.chat.edits.suggestRelatedFilesFromGitHistory": true,
"github.copilot.chat.reviewSelection.enabled": true
```

> ℹ️ **Chiavi rimosse dalla versione precedente del piano** (non verificate o non necessarie):
> - `chat.useCustomAgentHooks` — legata agli hook eliminati
> - `chat.agentFilesLocations` — VS Code scopre agenti automaticamente da `.github/agents/`
> - `github.copilot.chat.agent.enabled` — non verificata come chiave valida
> - `github.copilot.chat.agent.runTasks` — non verificata come chiave valida
> - `github.copilot.chat.subAgents.enabled` — non verificata come chiave valida
> - `github.copilot.chat.organizationCustomAgents.enabled` — non pertinente

---

## Ordine di Esecuzione

```
0. FASE 0  — Crea coding_ai/gui/ con 3 file di riferimento  ← PRIMA DI TUTTO
1. FASE 1  — Modifica .github/copilot-instructions.md (append)
2. FASE 2  — Correggi tool alias nei 3 prompt + crea aggiornamento-upstream.prompt.md
3. FASE 3  — Crea .github/agents/ con 6 file .agent.md
4. FASE 4  — Crea .github/instructions/ con 2 file .instructions.md
5. FASE 5  — Modifica .vscode/settings.json (aggiungi 3 chiavi verificate)
```

Dopo ogni fase: confermare i file creati/modificati prima di procedere alla fase successiva.

---

## Verifica Finale

Struttura completa attesa dopo l'implementazione:

```
coding_ai/gui/
├── jomini_scope_whitelist.md          ← NUOVO (Fase 0)
├── dual_mode_pattern_canonical.md     ← NUOVO (Fase 0)
└── priority_list.md                   ← NUOVO (Fase 0)

.github/
├── copilot-instructions.md            ← modificato con sezione agenti (Fase 1)
├── agents/
│   ├── analista-tri-repo.agent.md     ← NUOVO (Fase 3)
│   ├── architetto-dual-mode.agent.md  ← NUOVO (Fase 3)
│   ├── implementatore-patch.agent.md  ← NUOVO (Fase 3)
│   ├── revisore-accessibilita.agent.md← NUOVO (Fase 3)
│   ├── revisore-vanilla.agent.md      ← NUOVO (Fase 3)
│   └── auditore-finale.agent.md       ← NUOVO (Fase 3)
├── prompts/
│   ├── converti-finestra-dual-mode.prompt.md  ← tool alias corretto (Fase 2)
│   ├── analizza-finestra.prompt.md            ← tool alias corretto (Fase 2)
│   ├── verifica-dual-mode.prompt.md           ← tool alias corretto (Fase 2)
│   ├── debug-errore-jomini.prompt.md          ← invariato
│   ├── genera-container-ocr.prompt.md         ← invariato
│   └── aggiornamento-upstream.prompt.md       ← NUOVO (Fase 2)
└── instructions/
    ├── gui-jomini.instructions.md     ← NUOVO (Fase 4)
    └── localization-ocr.instructions.md← NUOVO (Fase 4)

.vscode/
└── settings.json                      ← 3 chiavi aggiunte (Fase 5)
```

Se un file manca: crearlo. Se una sezione manca in un file esistente: aggiungerla.
