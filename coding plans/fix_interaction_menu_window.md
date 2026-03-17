# Piano Correttivo — interaction_menu_window.gui

Data: 2026-03-16 (v2 — aggiornamento post-test in-game)
File: `ocr_support_compatibility_pach/gui/interaction_menu_window.gui`
Stato attuale: Convertita — Revisione Necessaria (fix parziale applicato)

---

## Storico Fix Precedenti (v1 — 2026-03-16)

Le azioni v1 sono state implementate con successo:
- ✅ Rimosso blocco `window_ocr` duplicato (eliminata doppia registrazione widgetid)
- ✅ Sostituito container OCR semplificato in italiano con contenuto completo upstream
- ✅ Container vanilla confermato fedele
- ✅ Verifiche strutturali superate (1 solo widgetid, 0 errori editor)

---

## 1. Diagnosi v2 — Problema di Rendering OCR Post-Fix

### Sintomo segnalato dall'utente

Test in-game post-fix v1:
- **Modalità normo-vedente (ocr presente)**: OK — menu si apre, voci selezionabili
- **Modalità non vedente (ocr assente)**: PROBLEMA — il menu appare con la grafica
  CK3 originale invece del layout testuale OCR Support. Lo switch sembra eseguirsi
  ma il contenuto non viene visualizzato nel formato OCR atteso.

### Analisi strutturale comparativa

Il problema è nella **struttura wrapper** del container OCR, non nel contenuto.
Il contenuto OCR (verificato identico all'upstream) funziona ma viene reso dentro
un involucro che non replica la struttura del type `window_ocr` usato dall'upstream.

#### Come l'upstream OCR renderizza la finestra

L'upstream usa il type `window_ocr` (definito in `shared/00_windows.gui` riga 128),
che è un `type window_ocr = widget { ... }` — cioè un **widget**, NON una **window**.

Il type `window_ocr` fornisce automaticamente:

| Elemento strutturale | Valore | Fonte |
|---------------------|--------|-------|
| Tipo root | `widget` (nessun `gfxtype = windowgfx`) | Definizione type |
| Background | `gfx/solid_dark_grey.dds` — sfondo grigio scuro solido | Template `Background_Area_Border_Solid` dentro `ocr_window_bg` |
| Dimensione | `745 x 100%` | Template `Window_Size_CharacterList` dentro `ocr_window_bg` |
| alwaystransparent | `no` (tipo) → sovrascritto a `yes` (istanza) | `ocr_window_bg` + override istanza |
| Scrollbox | contenuto OCR inside `scrollbox { blockoverride "scrollbox_content" }` | Layout `vbox` del type |
| TooltipFocus | Background nero full-screen `gfx/interface/colors/black.dds` con `margin = { 1920 1080 }` | `using = TooltipFocus` nell'istanza |

Struttura espansa dell'upstream (semplificata):
```
widget = {                              ← tipo base: widget, SENZA gfxtype=windowgfx
    size = { 745 100% }                 ← da ocr_window_bg → Window_Size_CharacterList
    background = { solid_dark_grey }    ← da ocr_window_bg → Background_Area_Border_Solid
    background = { black full-screen }  ← da using = TooltipFocus
    vbox = {
        scrollbox = {                   ← dal type window_ocr
            flowcontainer = {           ← da blockoverride "ocr_content"
                ... contenuto OCR ...
            }
        }
    }
}
```

#### Come la nostra patch renderizza la finestra in OCR mode

```
window = {                              ← tipo base: WINDOW con gfxtype=windowgfx
    gfxtype = windowgfx                 ← ❌ CHROME GRAFICA FINESTRA
    position = { 420 70 }               ← posizione vanilla (per popup)
    alwaystransparent = yes

    container = {                       ← ❌ NESSUN background
        visible = [Not(Exists('ocr'))]  ← ❌ NESSUNA dimensione fissa
                                        ← ❌ NESSUN scrollbox
        flowcontainer = {               ← contenuto diretto (corretto)
            ... contenuto OCR ...
        }
    }
}
```

### PROBLEMA IDENTIFICATO — Mismatch strutturale wrapper OCR

Il container OCR nella patch è un **involucro vuoto** (`container` senza background,
senza dimensione, senza scrollbox) che contiene il contenuto upstream corretto.
Il risultato è che:

1. **Nessun background solido**: il testo OCR fluttua sopra l'interfaccia di gioco,
   rendendo visibili gli elementi grafici di CK3 sotto/dietro il testo.
   Questo è ciò che l'utente descrive come "la grafica di CK3 originale".

2. **Nessuna dimensione fissa**: il container OCR non ha una dimensione propria
   (`745 x 100%`), quindi si adatta ai figli. Questo può causare layout irregolare.

3. **Nessun scrollbox**: il contenuto OCR non è scrollabile. Con liste lunghe
   di interazioni, il contenuto esce dallo schermo senza possibilità di scorrimento.

4. **Assenza TooltipFocus**: nell'upstream, un background nero full-screen dietro
   la finestra ("focus overlay") maschera tutta l'interfaccia di gioco.
   Senza di esso, l'interfaccia CK3 resta visibile attorno al menu OCR.

Il contenuto OCR è corretto (verificato in v1). Il wrapper è il problema.

---

## 2. Piano Correttivo v2

### Azione 1 — Ristrutturare il container OCR (CRITICO)

**Cosa**: Trasformare il container OCR da `container` a `widget` con struttura
che replica lo strato wrapper del type `window_ocr`.

**Da** (attuale):
```jomini
container = {
    name = "ocr_interaction_menu_container"
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"

    flowcontainer = {
        ... contenuto OCR ...
    }
}
```

**A** (corretto):
```jomini
widget = {
    name = "ocr_interaction_menu_container"
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"
    size = { 745 100% }
    allow_outside = yes

    background = {
        texture = "gfx/solid_dark_grey.dds"
        spriteType = Corneredtiled
        spriteborder = { 16 16 }
        texture_density = 2
    }

    vbox = {
        layoutpolicy_horizontal = expanding
        layoutpolicy_vertical = expanding

        scrollbox = {
            layoutpolicy_horizontal = expanding
            layoutpolicy_vertical = expanding

            blockoverride "scrollbox_content" {
                flowcontainer = {
                    ... contenuto OCR invariato ...
                }
            }
        }

        expand = {}
    }
}
```

**Perché ogni elemento è necessario**:

| Aggiunta | Motivo |
|----------|--------|
| `widget` invece di `container` | Supporto completo per `size`, `background`, layout box |
| `size = { 745 100% }` | Dimensione fissa dell'OCR upstream (da `Window_Size_CharacterList`) |
| `allow_outside = yes` | Permette al contenuto di estendersi oltre i limiti del widget (come l'upstream) |
| `background solid_dark_grey` | Sfondo solido: copre l'interfaccia CK3 sotto il testo OCR. Senza di esso, il testo fluttua su grafica vanilla |
| `vbox + scrollbox` | Struttura wrapper identica al type `window_ocr`: contenuto scrollabile, layout espandibile |
| `expand = {}` | Riempie spazio verticale residuo (standard del type `window_ocr`) |

### Azione 2 — NON toccare: container vanilla, stati window, gfxtype (NESSUNA MODIFICA)

**Container vanilla**: confermato fedele. Funziona correttamente (testato dall'utente).

**Stati `_show`/`_hide`**: logica condizionale corretta per entrambe le modalità (confermato in v1).

**`gfxtype = windowgfx`**: il window ha `alwaystransparent = yes` e nessun background
proprio. Il `gfxtype = windowgfx` è necessario per la gestione finestra CK3.
Lo sfondo del widget OCR (solid_dark_grey) coprirà eventuali artefatti grafici.

---

## 3. Ordine di Esecuzione v2

1. Ristrutturare il container OCR (Azione 1) — un'unica modifica strutturale
2. Verifica sintassi e bilanciamento parentesi
3. Verifica in-game: modalità OCR mostra sfondo scuro + testo leggibile
4. Verifica in-game: modalità vanilla invariata (già funzionante)

---

## 4. Risultato Atteso v2

- **Modalità non vedente** (ocr assente): il menu interazioni si apre con sfondo
  grigio scuro solido (identico all'OCR Support originale), contenuto testuale
  scrollabile, nessun elemento grafico CK3 visibile sotto/dietro il testo.
- **Modalità normo-vedente** (ocr presente): invariata — funziona già correttamente.
- Struttura interna del file preservata — una sola modifica chirurgica al wrapper OCR.

---

## 5. Rischi e Note v2

- **Risk basso**: la modifica è confinata al wrapper del container OCR.
  Il contenuto interno resta invariato (già verificato identico all'upstream).
- **Texture `gfx/solid_dark_grey.dds`**: fornita dalla mod OCR upstream.
  Disponibile quando la mod OCR è attiva (condizione sempre vera per la patch).
- **Scrollbox**: usa il type `scrollbox` standard di CK3, disponibile senza dipendenze.
- **TooltipFocus non incluso**: il background nero full-screen del TooltipFocus
  NON è incluso in questa correzione. Il solid_dark_grey di `745 x 100%` dovrebbe
  essere sufficiente come sfondo. Se l'utente segnala che l'interfaccia CK3
  è ancora visibile ai lati del menu, si potrà aggiungere in un fix successivo.
