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

## Visibility Dual Mode (pattern canonico e varianti supportate)

```jomini
# Container OCR attivo — modalità non vedente (variabile ocr assente)
visible = "[Not(GetVariableSystem.Exists('ocr'))]"
# Container vanilla attivo — modalità normo-vedente (variabile ocr presente)
visible = "[GetVariableSystem.Exists('ocr')]"
```

> ⚠️ `GameRules.GetRule('ocr_accessibility_mode')` è **deprecato** — non usarlo.

Pattern legacy supportati nel repository quando gia' presenti nei file modello Agamidae:

```jomini
# OCR attivo
visible = "[Isnt('ocr')]"
# Vanilla attivo
visible = "[Is('ocr')]"
```

Per nuove conversioni, preferire sempre `GetVariableSystem.Exists('ocr')`.

---

## Template Canonico Dual Mode

Struttura minima verificata per ogni nuova finestra (CK3 1.17.1):

```jomini
# File: ocr_support_compatibility_pach/gui/window_esempio.gui
# Versione CK3: 1.17.1

window = {
    name = "window_esempio"
    size = { 800 600 }

    # =============================================
    # BLOCCO OCR — solo testo, screen reader ready
    # variabile ocr ASSENTE = modalità non vedente
    # =============================================
    container = {
        name = "ocr_esempio_container"
        visible = "[Not(GetVariableSystem.Exists('ocr'))]"
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
    # variabile ocr PRESENTE = modalità normo-vedente
    # NON MODIFICARE MAI — identico al vanilla
    # =============================================
    container = {
        name = "vanilla_esempio_container"
        visible = "[GetVariableSystem.Exists('ocr')]"

        # Incollare qui il contenuto originale dal file vanilla
        # senza nessuna modifica
    }
}
```

### Regole Invariabili del Template

1. I due blocchi OCR/vanilla sono **mutuamente esclusivi** via `visible`
2. Il blocco vanilla è **fedele** al contenuto CK3 originale corrispondente
3. Font size OCR **minimo 18** ovunque
4. Header sezione OCR: colore `{ 255 221 136 255 }` (giallo), fontsize 20
5. Tutti i bottoni OCR hanno `tooltip` descrittivo
6. Nessun `name` duplicato allo stesso livello gerarchico

## Naming dei blocchi Dual Mode

Naming preferito per nuove conversioni:

- `ocr_*_container`
- `vanilla_*_container`

Naming legacy gia' valido nel repository se la visibility e' chiara e mutuamente esclusiva:

- `ocr_mode_content`
- `normal_mode_content`
- `window_ocr`
- `grafic_version`
- wrapper anonimi con `visible` esplicito

La validazione dei tool deve basarsi prima sulla `visible`, non solo sul naming.

## Mouse Input Parity

Checklist operativa da applicare a ogni `.gui` quando il widget vanilla è interattivo:

- preservare `onclick` quando il widget vanilla lo definisce
- preservare `onrightclick` se presente nel vanilla
- preservare feedback `enabled` o `disabled` se influenza l'uso reale del controllo
- preservare `tooltip` e feedback hover quando fanno parte dell'esperienza vanilla
- non ridurre testo o icona cliccabili a puro display nel container vanilla
- non trasformare item di grid o lista interattivi in elementi passivi nel container vanilla

---

## Checklist Pre-Commit

Prima di salvare o committare un file `.gui` modificato, verificare:

- [ ] Visibility mutuamente esclusive e corrette
- [ ] Blocco vanilla fedele al contenuto CK3 originale corrispondente
- [ ] Font size >= 18 in tutto il blocco OCR
- [ ] Ogni bottone OCR ha tooltip
- [ ] Nessun nome widget duplicato a stesso livello
- [ ] Nessun scope non verificato nella whitelist (`gui-jomini-scopes.instructions.md`)

### Checklist aggiuntiva per pattern v1.1 (type-separated)

Applicare **in aggiunta** alle voci sopra quando si usa il pattern con vanilla separato:

- [ ] File type presente in `gui/vanilla/{nome}_patch_vanilla.gui`
- [ ] Blocco `types OCR_PATCH_VANILLA { }` nel file type
- [ ] Guard `visible = "[GetVariableSystem.Exists('ocr')]"` presente dentro il type
- [ ] Il type **non contiene** proprietà window-level: `state`, `widgetid`, `layer`, `attachto`, `movable`
- [ ] Istanziazione nel wrapper: `{nome}_patch_vanilla = {}` senza `visible` esplicita
- [ ] Contenuto vanilla nel type identico al file CK3 originale
- [ ] `audit.py` produce report unificato coppia wrapper+type senza critici

---

## Naming Convention Type-Separated (Pattern v1.1)

> Attiva solo per file che adottano il pattern vanilla separato.

| Elemento | Regola |
|----------|--------|
| Nome type | `{finestra_senza_window}_patch_vanilla` (es. `character_patch_vanilla`) |
| Nome file | `{finestra_senza_window}_patch_vanilla.gui` |
| Blocco types | `types OCR_PATCH_VANILLA { }` — mai `types VANILLA` |
| Widget base | `widget` come default; `window` solo se documentato e verificato |
| Guard visibilità | `visible = "[GetVariableSystem.Exists('ocr')]"` — mai `using = vanilla` |

**Proprietà VIETATE nel type separato** (devono restare nel wrapper):
`state`, `widgetid`, `layer`, `attachto`, `movable`, `allow_outside`, `parentanchor`

---

## Functional Parity — Checklist Verificabile

**OCR e vanilla devono essere funzionalmente equivalenti**: nessuna delle due modalità è una versione ridotta dell'altra.

### Checklist OCR

- [ ] Tutte le informazioni leggibili nel vanilla sono presenti come testo nel blocco OCR
- [ ] Ogni azione disponibile nel vanilla ha un bottone OCR equivalente con tooltip
- [ ] L'ordine di lettura OCR riflette la gerarchia logica del vanilla
- [ ] Le liste vuote hanno un messaggio di fallback testuale

### Checklist Vanilla

- [ ] Il blocco vanilla rappresenta fedelmente la sezione CK3 originale corrispondente
- [ ] Nessun widget rimosso, spostato o rinominato
- [ ] `onclick`, `onrightclick`, `tooltip` preservati senza modifiche

### Checklist Multiplayer / Checksum

- [ ] Nessun `scripted_gui`, `effect` o `trigger` aggiunto che alteri il checksum
- [ ] I due container usano solo `visible` per il toggle — nessuna logica script-side
- [ ] Il file non introduce nuovi `game_rule` o `on_action`

---

## Performance Guidelines

- **File size**: l'overhead atteso per la duplicazione dual-mode è ~15–20% per finestra (es. 40 KB → 48 KB)
- **Parse time**: +2–5 ms per window load — trascurabile
- **Runtime overhead**: ZERO — solo i widget visibili vengono processati dal motore
- **Ottimizzazione**: riuso di types condivisi riduce l'impatto a ~10%

Il trade-off è accettabile: la compatibilità multiplayer vale il piccolo overhead di file size.

---

## Errori Comuni da Evitare

- ❌ Non usare `show_when` al posto di `visible`
- ❌ Non modificare widget vanilla per "migliorarli"
- ❌ Non usare scope `ROOT` o `THIS` senza verifica
- ❌ Non aggiungere newline extra dentro stringhe `[...]`
- ❌ Non duplicare `name` allo stesso livello gerarchico
- ❌ Non usare `datamodel` senza verificarne il type nel vanilla
- ❌ Non omettere `parentanchor` e `size` dove il vanilla li richiede
- ❌ Non usare `GameRules.GetRule('ocr_accessibility_mode')` — **deprecato**, segnalare e sostituire con `GetVariableSystem.Exists('ocr')`
