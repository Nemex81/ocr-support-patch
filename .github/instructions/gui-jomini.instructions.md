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
