# Pattern di Conversione Dual Mode — Classificazione

Classificazione delle finestre per complessità di conversione.
Ogni pattern ha un approccio strutturale specifico.

---

## Pattern A — Simple Swap (Finestre Semplici)

**Caratteristiche**: una sola window principale, nessun sub-widget complesso, conversione 1:1.

**Uso tipico**: Character, My Realm, Military, Intrigue.

**Struttura**:
```
window = {
    container = { visible OCR  → contenuto accessibile }
    container = { visible vanilla → copia CK3 originale }
}
```

---

## Pattern B — Tabs + SubWindows (Finestre Medie)

**Caratteristiche**: window principale con tab navigation, sub-windows modali, datamodel dinamici.

**Uso tipico**: Council, Activity, Activity List, Factions.

**Struttura**:
```
window = {                         # Main window dual-mode
    container = { visible OCR }
    container = { visible vanilla }
}
window = {                         # Ogni sub-window è anch'essa dual-mode
    container = { visible OCR }
    container = { visible vanilla }
}
```

---

## Pattern C — Complex Layout (Finestre Complesse)

**Caratteristiche**: layout multi-colonna, grid dinamici, nested scrollbox, custom types estesi.

**Uso tipico**: Court, Decisions, Character Lifestyle.

**Struttura**:
```
types = {
    type custom_type_ocr = { ... }
    type custom_type_vanilla = { ... }
}
window = {
    container OCR → linearizzato in vbox singolo con scrollbox
    container vanilla → grid multi-colonna preservato
}
```

---

## Pattern D — Bottom-Up Multi-Window (Sistema Complesso)

**Caratteristiche**: sistema multi-finestra interconnesso, types condivisi, sub-windows già dual-mode.

**Uso tipico**: County View, Faith View, Culture View.

**Approccio incrementale**:
1. **Types first** — definire tutti i custom types
2. **Secondary windows** — convertire finestre secondarie
3. **Main window** — Skeleton → OCR → Vanilla Header → Vanilla Content

---

## Come Scegliere il Pattern

| Criterio                        | A    | B    | C    | D    |
|--------------------------------|------|------|------|------|
| Finestre nella conversione     | 1    | 2+   | 1    | 3+   |
| Sub-windows modali             | No   | Sì   | No   | Sì   |
| Layout multi-colonna           | No   | No   | Sì   | Sì   |
| Custom types richiesti         | 0–1  | 1–2  | 3+   | 5+   |
