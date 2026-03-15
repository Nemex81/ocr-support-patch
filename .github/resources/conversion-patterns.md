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

---

## Variante V — Type-Separated Vanilla (Pattern v1.1)

Applicabile a qualsiasi pattern A/B/C/D. Sposta il branch vanilla in un type `.gui`
separato nella cartella `gui/vanilla/`, mantenendo il branch OCR inline nel wrapper.

### Criteri di scelta: inline vs separato

| Condizione | Scelta |
|------------|--------|
| File wrapper > 2000 righe E vanilla > 40% del totale | **Separato consigliato** |
| File < 500 righe | **Inline preferibile** — beneficio minimo |
| File di interazione semplici (`interaction_*.gui`) | **Inline** |
| File HUD o multi-window pattern D | **Separato con cautela** — alto rischio |

### Compatibilità per pattern

| Pattern | Compatibile con v1.1 | Livello di rischio | Note |
|---------|---------------------|-------------------|------|
| A — Simple Swap | ✅ Sì | Basso | Ideale per PoC |
| B — Tabs + SubWindows | ✅ Sì | Medio | Ogni sub-window può richiedere type dedicato |
| C — Complex Layout | ✅ Sì | Medio | Verificare types condivisi prima di separare |
| D — Bottom-Up Multi-Window | ✅ Sì | Alto | Introdurre solo dopo validazione su A/B/C |

### Casi ad alto rischio (non introdurre per primi)

- `hud.gui` — dipendenze da layer e stati del motore di gioco; separare solo dopo consolidamento completo del pattern
- `window_army.gui` — script specializzato `assemble_army_dualmode.py` da aggiornare prima
- Qualsiasi finestra pattern D con 3+ window interconnesse

### Riferimento tecnico

Template completo, naming convention e checklist pre-commit in
`.github/resources/dual_mode_pattern_canonical.md` — sezione "Pattern v1.1 — Type-Separated Vanilla".
