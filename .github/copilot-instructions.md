# OCR Support Patch — Istruzioni Copilot

## Identità del Progetto

Questo repository contiene una **mod per Crusader Kings 3 (versione 1.17.1)** che implementa il sistema **Dual Mode** per l'accessibilità dei giocatori non vedenti.
Ogni finestra GUI viene convertita per supportare due modalità:
- **Modalità OCR** (`ocr_accessibility_mode = yes`): layout testuale puro, leggibile da screen reader
- **Modalità Vanilla** (`ocr_accessibility_mode = no`): layout grafico originale Paradox, invariato

Il toggle è controllato dalla game_rule `ocr_accessibility_mode`, attivabile con **Shift+F11** in-game.

---

## Struttura Repository

```
ocr-support-patch/
├── .github/
│   ├── copilot-instructions.md     ← questo file
│   ├── agents/                     ← definizioni agenti specializzati
│   ├── instructions/               ← istruzioni attive per dominio
│   ├── prompts/                    ← prompt riutilizzabili per Copilot
│   ├── resources/                  ← whitelist scope, pattern canonical, priority list
│   └── copilot-skills/             ← skills invocabili dagli agenti
ocr_support_compatibility_pach/
│   └── gui/                        ← file .gui della mod (lavoro attivo)
coding_ai/                          ← documentazione storica (sola lettura)
```

I file GUI vanilla di riferimento si trovano in:
`../CK3 ORIGINAL VERSION/ck3origin/game/gui/`

I file GUI OCR upstream (Agamidae) si trovano in:
`../CK3-OCR/OCR-Support/gui/`

---

## Linguaggio e Sintassi

- Linguaggio: **Jomini GUI scripting** (proprietario Paradox, CK3 1.17.1)
- Estensione file: `.gui`
- Encoding: `UTF-8`
- **NON usare** widget type, scope, datatype o proprietà Jomini non documentati per CK3 1.17.1
- **NON inventare** nomi di funzioni o binding non presenti nei file vanilla di riferimento
- Ogni modifica DEVE essere compatibile con il sistema di override mod di CK3

---

## Pattern Obbligatorio — Dual Mode

Ogni finestra convertita DEVE seguire questo schema:

```
types NomeFinestra_types {
    # ... type definitions ...
}

window = {
    name = "nome_finestra"

    # === BLOCCO OCR — modalità NON VEDENTE (variabile ocr assente) ===
    container = {
        name = "ocr_nome_container"
        visible = "[Not(GetVariableSystem.Exists('ocr'))]"
        # Solo: text_single, text_multi, flowcontainer, text_label, button con tooltip testuale
        # Font size minimo: 18 | Colore testo: #FFFFFF o #FFDD88
        # Struttura gerarchica con header testuali espliciti per ogni sezione
        # NESSUN widget grafico: niente icon, portrait, progressbar visivi
    }

    # === BLOCCO VANILLA — modalità normo-vedente (variabile ocr presente) ===
    container = {
        name = "vanilla_nome_container"
        visible = "[GetVariableSystem.Exists('ocr')]"
        # Layout grafico originale Paradox — identico al file vanilla CK3
        # NON modificare questa sezione salvo bugfix espliciti
    }
}
```

**Regola critica**: I due container sono mutualmente esclusivi via `visible`. Il container vanilla deve essere una copia fedele del file CK3 originale. Il container OCR è la nuova implementazione accessibile.

---

## Regole Widget OCR

- `text_single` / `text_multi`: testo informativo — sempre con `autoresize = yes`
- `flowcontainer`: raggruppamento di elementi testuali — direzione `down` preferita
- Bottoni: sempre con `tooltip` testuale descrittivo, NON solo icona
- Sezioni con dati variabili: usare `item` dentro `fixedgridwidget` o `vbox`
- Header di sezione: `text_label` con font_size = 20, colore = `{ 255 221 136 255 }` (giallo)
- Dati numerici: sempre con unità e contesto (es. "Oro: [GetGold]" non solo "[GetGold]")
- Nessun `icon` standalone senza `tooltip` leggibile

---

## Regole Blockoverride

Se il file usa `blockoverride`, le modifiche OCR vanno inserite **dentro** il block esistente, NON creando nuovi block paralleli:

```
blockoverride "nome_block" {
    # contenuto vanilla originale...
    # in fondo al block aggiungere:
    container = {
        name = "ocr_nome_inline"
        visible = "[Not(GetVariableSystem.Exists('ocr'))]"
        # ...
    }
}
```

---

## File Già Convertiti (Pattern di Riferimento)

I seguenti file sono stati convertiti e rappresentano il pattern canonical:
- `window_character.gui` — finestra personaggio complessa, multi-tab
- `window_council.gui` — consiglio con tab e interazioni
- `window_culture.gui` — finestra cultura con alberi e progressi
- `window_faith.gui` — fede con tab e dottrine
- `window_combat.gui` — combattimento con dati militari
- `window_intrigue.gui` — intrigo con schemi e agenti
- `window_inventory.gui` — inventario con artefatti
- `window_military.gui` — militare con tab eserciti
- `window_my_realm.gui` — tab regno
- `window_dynasty_house.gui` — dinastia/casata
- `window_county_view.gui` — vista contea
- `window_court.gui` — corte
- `window_decisions.gui` — decisioni
- `window_activity.gui` — attività
- `window_activity_list.gui` — lista attività
- `window_character_lifestyle.gui` — stile di vita
- `window_factions.gui` — fazioni
- `hud.gui` — HUD principale
- `interaction_blackmail.gui` — interazione ricatto
- `interaction_menu_window.gui` — menu interazioni
- `interaction_interfere_in_war_notification.gui` — notifica guerra

Lista aggiornata con priorità in `.github/resources/priority_list.md`.

Prima di implementare una nuova finestra, **consulta sempre** un file già convertito come esempio.

---

## Workflow Standard per Nuova Finestra

1. Apri il file vanilla da `../CK3 ORIGINAL VERSION/ck3origin/game/gui/nome_file.gui`
2. Apri il file OCR upstream da `../CK3-OCR/OCR-Support/gui/nome_file.gui`
3. Identifica la struttura dei widget vanilla (tipo, nome, gerarchia)
4. Costruisci il container OCR rispettando la stessa gerarchia informativa
5. Incapsula il vanilla originale nel container vanilla senza modifiche
6. Verifica che le due visibility siano mutuamente esclusive
7. Testa la logica visible con entrambi i valori di `ocr_accessibility_mode`

---

## Regola Whitelist Scope — Aggiornamento Obbligatorio

Ogni volta che un binding o uno scope viene verificato direttamente in un file vanilla
(`../CK3 ORIGINAL VERSION/ck3origin/game/gui/`), **deve essere aggiunto immediatamente**
a `.github/resources/jomini_scope_whitelist.md` se non è già presente.

Questo vale per qualunque agente o sessione di lavoro. Non è opzionale.

Formato da aggiungere:
```
| `NomeScope` | contesto d'uso | note operative |
```

---

## Regola Toggle Visibilità — Meccanismo Primario

Il toggle di visibilità usa `GetVariableSystem.Exists('ocr')` come meccanismo **principale e unico**:

- `GetVariableSystem.Exists('ocr') = true` (variabile presente) → modalità **NORMO-VEDENTE** (vanilla)
- `GetVariableSystem.Exists('ocr') = false` (variabile assente) → modalità **NON VEDENTE** (OCR)

```jomini
# Container OCR attivo — modalità non vedente (variabile ocr assente)
visible = "[Not(GetVariableSystem.Exists('ocr'))]"
# Container vanilla attivo — modalità normo-vedente (variabile ocr presente)
visible = "[GetVariableSystem.Exists('ocr')]"
```

> ⚠️ `GameRules.GetRule('ocr_accessibility_mode')` è **deprecato** — non usarlo nelle nuove conversioni.


## Errori Comuni da Evitare

- ❌ Non usare `show_when` al posto di `visible`
- ❌ Non modificare widget vanilla per "migliorarli"
- ❌ Non usare scope `ROOT` o `THIS` in contesti GUI senza verifica
- ❌ Non aggiungere newline extra dentro stringhe di binding `[...]`
- ❌ Non duplicare `name` identici dentro lo stesso livello di gerarchia
- ❌ Non usare `datamodel` senza verificarne il type nel data_binding vanilla
- ❌ Non omettere `parentanchor` e `size` dove il layout vanilla li richiede

---

## Note Operative

- Il modder è non vedente: usa screen reader. I messaggi di errore devono essere chiari e in italiano.
- Preferire risposte che spiegano il **perché** di ogni scelta tecnica
- Se un pattern Jomini è ambiguo, chiedere conferma prima di implementare
- La compatibilità con CK3 1.17.1 è prioritaria rispetto a qualunque feature nuova

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

## Skills Disponibili in Questo Workspace

Le skills in `.github/copilot-skills/` sono capacità procedurali invocabili
dagli agenti tramite `#nome-skill`. Centralizzano logica ripetuta.

| Skill | File | Scopo |
|-------|------|-------|
| deprecated-pattern-scanner | `deprecated-pattern-scanner.skill.md` | Rileva pattern vietati/deprecati in file .gui |
| scope-whitelist-check | `scope-whitelist-check.skill.md` | Verifica binding Jomini contro whitelist |
| tri-repo-diff | `tri-repo-diff.skill.md` | Confronto strutturale tra i 3 repository |
| vanilla-fidelity-check | `vanilla-fidelity-check.skill.md` | Verifica fedeltà container vanilla |
| accessibility-checklist-runner | `accessibility-checklist-runner.skill.md` | Checklist NVDA automatica |
| dual-mode-template-generator | `dual-mode-template-generator.skill.md` | Genera scheletro dual mode da struttura vanilla |

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
- `.github/instructions/patch-boundaries.instructions.md` → attiva per tutti i file — confini operativi scrivibili
- `.github/instructions/gui-jomini.instructions.md` → attiva per `*.gui` — widget, template, checklist
- `.github/instructions/gui-jomini-scopes.instructions.md` → attiva per `*.gui` — regole scope (lista completa in `.github/resources/jomini_scope_whitelist.md`)
- `.github/instructions/gui-conversion-progress.instructions.md` → attiva per `.github/**` — stato conversioni
- `.github/instructions/localization-ocr.instructions.md` → attiva per `*.yml`

## Percorsi Repository di Riferimento

- Patch attiva: `ocr_support_compatibility_pach/gui/`
- OCR upstream (Agamidae): `../CK3-OCR/OCR-Support/gui/`
- Vanilla CK3 1.17.1: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/`

> ⚠️ Il path vanilla usa spazi, NON trattini: `CK3 ORIGINAL VERSION`
