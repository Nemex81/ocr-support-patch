# OCR Navigation Shortcuts — Standard di Riferimento

Tasti di navigazione rapida per la modalità OCR (keyboard-only).
Derivati dalla convenzione Agamidae CK3-OCR.

## Shortcut Standard

| Tasto | Azione              | Contesto            |
|-------|----------------------|---------------------|
| **Z** | Elemento precedente  | Liste, tab, item    |
| **X** | Elemento successivo  | Liste, tab, item    |
| **G** | Vai a vista correlata| Navigazione tra finestre |
| **E** | Modifica / Azione    | Edit su elemento attivo  |
| **H** | Vista baronie        | County view         |
| **T** | Vista titolo         | Title / holding     |
| **A** | Contee adiacenti     | County view         |

## Pattern di Implementazione

```jomini
hbox = {
    visible = no  # Invisibile ma funzionale — cattura solo shortcut
    size = { 0 0 }

    button_standard = {
        name = "prev_item"
        shortcut = "z"
        onclick = "[SelectPreviousItem]"
    }

    button_standard = {
        name = "next_item"
        shortcut = "x"
        onclick = "[SelectNextItem]"
    }
}
```

## Regole

- Lo shortcut è sempre documentato nel `tooltip` del bottone corrispondente
- Il container shortcut è `visible = no` e `size = { 0 0 }` (invisibile ma funzionale)
- Non tutti gli shortcut si applicano a ogni finestra — usare solo quelli pertinenti
- Z/X sono quasi universali per navigazione lista; G/E dipendono dal contesto
