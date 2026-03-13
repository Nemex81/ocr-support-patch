---
agent: agent
description: Verifica la correttezza del dual mode in un file GUI già convertito
tools: [read, search]
---

# Task: Verifica Dual Mode

Leggi: `${file:.github/copilot-instructions.md}`

File da verificare: `ocr_support_compatibility_pach/gui/${input:nomeFile}.gui`

Usa questo prompt come entrypoint rapido e user-friendly.
Per la verifica sostanziale, delega alle skill e ai revisori del framework invece di
replicare una checklist completa concorrente.

## Flusso di verifica raccomandato

- Invoca `#deprecated-pattern-scanner` per escludere pattern deprecati o vietati
- Invoca `#accessibility-checklist-runner` per i controlli OCR automatici
- Invoca `#vanilla-fidelity-check` per la fedelta' del container vanilla
- Se emergono dubbi qualitativi OCR, passa a `revisore-accessibilita`
- Se emergono dubbi di fedelta' vanilla o interazioni mouse-only, passa a `revisore-vanilla`
- Se tutto e' coerente, suggerisci `auditore-finale`

## Output

- Riassunto breve dei risultati delle skill invocate
- Bug o rischi residui ancora da far valutare ai revisori
- Prossimo handoff consigliato: `revisore-accessibilita`, `revisore-vanilla` oppure `auditore-finale`
