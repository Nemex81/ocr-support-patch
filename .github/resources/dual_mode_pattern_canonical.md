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

## Separazione dei Types

- Regola: se il rendering diverge tra OCR e vanilla, separa i `types`
- Naming: usa suffissi `_ocr` e `_vanilla` per i type divergenti; mantieni type condivisi solo quando struttura e comportamento restano identici
- La fedeltà vanilla include anche le proprietà interattive rilevanti: `onclick`, `onrightclick`, `tooltip`, stato `enabled` o `disabled`

Mini-pattern per componente interattivo divergente:

```jomini
types example_action_button_ocr = button {
    fontsize = 18
    tooltip = "Descrizione azione"
}

types example_action_button_vanilla = button {
    onclick = "[DoThing]"
    onrightclick = "[OpenContextMenu]"
    tooltip = "Vanilla hover text"
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

---

## Limitazioni Note

### Pattern B — Tab Sync Non Sincronizzato

**Stato**: limitazione architetturale nota, non un bug.

Nelle finestre Pattern B (tab navigation), i container OCR e vanilla usano
sistemi di tab **completamente indipendenti**:

- **OCR**: `GetVariableSystem.HasValue('nome_tabs', 'valore')` — variabili GUI gestite
  dal mod, settate tramite bottoni OCR con `onclick = "[GetVariableSystem.Set(...)]"`.
- **Vanilla**: API C++ native del controller CK3 (es. `CourtWindow.IsShowPositions`,
  `CouncilWindow.IsPlayerCouncilShown`) — non accessibili da Jomini per lettura/scrittura.

**Conseguenza**: quando il giocatore cambia modalità con Shift+F11, il tab attivo
potrebbe non corrispondere tra OCR e vanilla. CK3 1.17.1 non espone API per
sincronizzare lo stato tab C++ con le variabili GUI.

**Mitigazione applicata**: nessun workaround automatico possibile. Il comportamento
è accettabile perché il cambio OCR↔vanilla è raro durante il gameplay normale.

**File coinvolti**: `window_court.gui`, `window_council.gui`, e tutte le finestre
Pattern B con tab navigation.

**Rilevato**: 2026-03-13 (diagnosi rapporto tecnico)
