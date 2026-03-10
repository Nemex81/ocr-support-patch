# Pattern Canonical Dual Mode — Esempio Completo

Questo file contiene il pattern minimal verificato per implementare il dual mode
in una finestra CK3. Da usare come template di riferimento per Copilot.

## Struttura Minima

```gui
# File: ocr_support_compatibility_pach/gui/window_esempio.gui
# Versione CK3: 1.17.1
# Dual mode: OCR (testo) + Vanilla (grafico)

types WindowEsempio_types {
    # type definitions qui se necessario
}

window = {
    name = "window_esempio"
    size = { 800 600 }
    position = { 0 0 }
    layer = windows_layer

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

            # Header principale
            text_label = {
                name = "ocr_title"
                text = "ESEMPIO — [GetPlayer.GetUINameNoTooltip]"
                fontsize = 20
                autoresize = yes
                color = { 255 221 136 255 }
            }

            # Sezione dati principali
            text_label = {
                name = "ocr_section_info"
                text = "--- INFORMAZIONI ---"
                fontsize = 18
                autoresize = yes
                color = { 255 221 136 255 }
            }

            text_single = {
                name = "ocr_dato_1"
                text = "Valore: [GetPlayer.GetTreasury|0] oro"
                fontsize = 18
                autoresize = yes
            }

            # Bottone OCR con tooltip obbligatorio
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
    # BLOCCO VANILLA — layout grafico originale
    # NON MODIFICARE — copia fedele del vanilla
    # =============================================
    container = {
        name = "vanilla_esempio_container"
        visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('no')]"

        # ... incollare qui il contenuto originale dal file vanilla ...
    }
}
```

## Checklist Pre-Commit

- [ ] I due container hanno visibility mutuamente esclusive
- [ ] Il container vanilla è identico al file CK3 originale
- [ ] Tutti i text_single/text_label hanno autoresize = yes
- [ ] Font size >= 18 in tutto il blocco OCR
- [ ] Ogni bottone OCR ha tooltip descrittivo
- [ ] Nessun nome widget duplicato a stesso livello
- [ ] Nessun scope non verificato usato
