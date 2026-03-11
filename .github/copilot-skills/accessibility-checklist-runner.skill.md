---
name: accessibility-checklist-runner
description: >
  Esegue la checklist completa di accessibilità NVDA su un file .gui convertito.
  Verifica ogni punto della checklist OCR in modo automatico e produce un
  report pass/fail per ogni punto con riferimento alla riga del file.
parameters:
  - name: file_path
    description: >
      Percorso del file .gui da verificare.
      Esempio: ocr_support_compatibility_pach/gui/window_faith.gui
    required: true
---

## Logica di Esecuzione

Leggi il file `file_path`. Estrai SOLO il blocco con nome che inizia con `ocr_`
e visibility `[Not(GetVariableSystem.Exists('ocr'))]`. Analizza quel blocco.

### Check 1 — Font size

Ogni widget `text_single`, `text_multi`, `text_label`, `button` nel blocco OCR
deve avere `fontsize` >= 18. Segnala riga e widget per ogni violazione.

### Check 2 — Header sezioni

Ogni `text_label` che funge da titolo di sezione deve avere
`color = { 255 221 136 255 }` e `fontsize` >= 20.
Un `text_label` senza colore esplicito è una violazione.

### Check 3 — Tooltip bottoni

Ogni `button` nel blocco OCR deve avere `tooltip` con testo non vuoto.
Un bottone senza tooltip è un blocco CRITICO.

### Check 4 — Icone

Nessun `icon` standalone nel blocco OCR senza `tooltip`.
Un `icon` senza tooltip è invisibile a NVDA.

### Check 5 — Dati numerici con contesto

I binding che producono valori numerici (oro, truppe, date, percentuali) devono
avere testo contestuale nella stessa riga di testo
(es. `"Oro: [GetGold]"` non solo `"[GetGold]"`).
Verifica che nessun widget OCR contenga un binding numerico isolato.

### Check 6 — Liste vuote

Se il file contiene `datamodel` nel blocco OCR, verifica che ci sia un widget
o testo alternativo per il caso lista vuota.

### Check 7 — Visibilità

Il blocco OCR deve usare ESCLUSIVAMENTE
`visible = "[Not(GetVariableSystem.Exists('ocr'))]"` per la sua visibilità.
Qualunque altra sintassi di visibility nel container OCR è una violazione.

### Check 8 — Struttura gerarchia

Il blocco OCR deve avere almeno un widget con testo che identifica la finestra
(header principale). Un blocco OCR privo di titolo principale è una violazione.

---

## Formato Output Obbligatorio

```
## Checklist Accessibilità NVDA: [nome_file]

| Check | Stato | Dettaglio |
|-------|-------|-----------|
| 1 — Font size >= 18 | ✅ OK | — |
| 2 — Header sezioni gialli | ❌ CRITICO | text_label riga 45: manca colore giallo |
| 3 — Tooltip bottoni | ✅ OK | — |
| 4 — Icone con tooltip | ⚠️ ATTENZIONE | icon riga 78: tooltip presente ma vuoto |
| 5 — Dati numerici contestuali | ✅ OK | — |
| 6 — Fallback liste vuote | ✅ OK | — |
| 7 — Visibilità corretta | ✅ OK | — |
| 8 — Titolo finestra presente | ✅ OK | — |

**Verdetto**: PASS / PASS CON RISERVE / FAIL
**Blocchi critici**: N
**Avvertenze**: N
```

---

## Agenti che usano questa skill

- **Revisore Accessibilità**: invoca come primo passo. Il suo report finale
  si basa sull'output di questa skill, arricchito da valutazioni qualitative
  (es. ordine lettura, coerenza informativa) che la skill non può valutare
  automaticamente.
- **Auditore Finale**: invoca nella sezione "Qualità OCR" della checklist.
  Un verdetto FAIL è automaticamente un blocco CRITICO nell'audit.
