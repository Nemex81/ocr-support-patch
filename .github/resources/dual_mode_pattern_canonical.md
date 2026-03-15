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

## Pattern v1.1 — Type-Separated Vanilla

Architettura alternativa supportata. Il branch vanilla viene spostato in un type `.gui` separato
nella sottocartella `gui/vanilla/`, alleggerendo il wrapper principale.

**Quando usare il pattern separato:**
- File wrapper > 2000 righe E branch vanilla occupa > 40% del totale → **separato consigliato**
- File < 500 righe o beneficio minimo → **inline preferibile**

**Naming convention ufficiale** (non derogare, rischio collisione con Agamidae):

| Elemento | Convenzione | Esempio |
|----------|-------------|---------|
| Folder type file | `ocr_support_compatibility_pach/gui/vanilla/` | — |
| Nome type | `{finestra_senza_window}_patch_vanilla` | `character_patch_vanilla` |
| Nome file type | `{finestra_senza_window}_patch_vanilla.gui` | `character_patch_vanilla.gui` |
| Blocco types | `types OCR_PATCH_VANILLA { }` | — |
| Guard visibilità | `visible = "[GetVariableSystem.Exists('ocr')]"` esplicita | — |

> ⚠️ Non usare mai: suffisso `_old`, namespace `VANILLA` puro, suffisso `_vanilla` senza `_patch_`.
> Questi nomi collidono con pattern Agamidae (`types VANILLA {}`, type `character_old = window {}`).

### Template wrapper (file principale)

```jomini
# File: ocr_support_compatibility_pach/gui/window_esempio.gui
# Pattern v1.1 — il branch vanilla è in gui/vanilla/esempio_patch_vanilla.gui

window = {
    name = "window_esempio"
    # window-level: states, layer, movable, widgetid, datacontext — restano qui
    state = { name = _show ... }
    state = { name = _hide ... }

    # =============================================
    # BLOCCO OCR — inline nel wrapper come sempre
    # =============================================
    widget = {
        name = "ocr_esempio_container"
        visible = "[Not(GetVariableSystem.Exists('ocr'))]"
        size = { 100% 100% }

        vbox = {
            # ... contenuto OCR ...
        }
    }

    # =============================================
    # BLOCCO VANILLA — istanziazione del type separato
    # visible è gestita DENTRO il type, non qui
    # =============================================
    esempio_patch_vanilla = {}
}
```

### Template file type separato

```jomini
# File: ocr_support_compatibility_pach/gui/vanilla/esempio_patch_vanilla.gui
# Solo il branch vanilla — nessun contenuto OCR in questo file

types OCR_PATCH_VANILLA {
    type esempio_patch_vanilla = widget {
        name = "vanilla_esempio_container"
        visible = "[GetVariableSystem.Exists('ocr')]"

        # Incollare qui il contenuto vanilla originale dal file CK3
        # senza nessuna modifica — identico al vanilla
    }
}
```

### Regole strutturali del type separato

- Il type separato contiene **solo** il layout vanilla — nessun contenuto OCR
- La guard `visible = "[GetVariableSystem.Exists('ocr')]"` è **obbligatoria** dentro il type
- Il type **non deve** contenere: `state`, `widgetid`, `layer`, `attachto`, `movable`
  (queste proprietà appartengono al wrapper)
- Il wrapper non aggiunge una `visible` sull'istanziazione `esempio_patch_vanilla = {}` —
  la visibilità è gestita esclusivamente dentro il type
- Usare `widget` come tipo base di default; usare `window` solo se documentazione tecnica
  specifica lo richiede e dopo verifica esplicita

### Checklist pre-commit aggiuntiva (pattern v1.1)

- [ ] File type presente in `gui/vanilla/{nome}_patch_vanilla.gui`
- [ ] Blocco `types OCR_PATCH_VANILLA { }` nel file type
- [ ] Guard `visible = "[GetVariableSystem.Exists('ocr')]"` presente nel type
- [ ] Nessuna proprietà window-level (`state`, `layer`, `widgetid`) nel type separato
- [ ] Istanziazione nel wrapper: `{nome}_patch_vanilla = {}` senza `visible` esplicita
- [ ] Contenuto vanilla nel type identico al file CK3 originale — nessuna modifica
- [ ] `audit.py` riconosce la coppia wrapper + type e produce report unificato
