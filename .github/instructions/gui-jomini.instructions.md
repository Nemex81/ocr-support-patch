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

<!-- Nota progetto: comportamento legacy "variabile ocr" -->
<!-- Per compatibilità con implementazioni storiche, alcuni file usano `GetVariableSystem.Exists('ocr')`. -->
<!-- Avvertenza importante: nel progetto il proprietario ha definito la semantica legacy INVERTITA: -->
<!-- - `GetVariableSystem.Exists('ocr') = true` => modalità NORMALE (vanilla) -->
<!-- - `GetVariableSystem.Exists('ocr') = false` => modalità NON VEDENTE (OCR) -->
<!-- Gli agenti devono: preferire le binding basate su `GameRules.GetRule('ocr_accessibility_mode')`; -->
<!-- se incontrano `GetVariableSystem.Exists('ocr')`, trattarlo come mapping legacy invertito e segnalare il file per normalizzazione. -->

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

### Regole Invariabili del Template

1. I due container sono **mutuamente esclusivi** via `visible`
2. Il container vanilla è **identico** al file CK3 originale — nessuna modifica
3. Font size OCR **minimo 18** ovunque
4. Header sezione OCR: colore `{ 255 221 136 255 }` (giallo), fontsize 20
5. Tutti i bottoni OCR hanno `tooltip` descrittivo
6. Nessun `name` duplicato allo stesso livello gerarchico

---

## Checklist Pre-Commit

Prima di salvare o committare un file `.gui` modificato, verificare:

- [ ] Visibility mutuamente esclusive e corrette
- [ ] Container vanilla identico al file CK3 originale
- [ ] Font size >= 18 in tutto il blocco OCR
- [ ] Ogni bottone OCR ha tooltip
- [ ] Nessun nome widget duplicato a stesso livello
- [ ] Nessun scope non verificato nella whitelist (`gui-jomini-scopes.instructions.md`)

---

## Errori Comuni da Evitare

- ❌ Non usare `show_when` al posto di `visible`
- ❌ Non modificare widget vanilla per "migliorarli"
- ❌ Non usare scope `ROOT` o `THIS` senza verifica
- ❌ Non aggiungere newline extra dentro stringhe `[...]`
- ❌ Non duplicare `name` allo stesso livello gerarchico
- ❌ Non usare `datamodel` senza verificarne il type nel vanilla
- ❌ Non omettere `parentanchor` e `size` dove il vanilla li richiede
