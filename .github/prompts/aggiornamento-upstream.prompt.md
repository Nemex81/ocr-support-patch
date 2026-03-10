---
mode: agent
description: Confronta la patch con upstream OCR e vanilla per rilevare aggiornamenti
tools: [read, search]
model: ['Claude Opus 4.6', 'GPT-5.4']
---

# Task: Aggiornamento da Upstream

Leggi: `${file:.github/copilot-instructions.md}`

## File da confrontare
- Patch attuale: `ocr_support_compatibility_pach/gui/${input:nomeFile}.gui`
- OCR upstream: `../CK3-OCR/OCR-Support/gui/${input:nomeFile}.gui`
- Vanilla baseline: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/${input:nomeFile}.gui`

## Cosa rilevare

1. **Differenze upstream → patch**: cosa ha aggiornato Agamidae non ancora nella patch?
2. **Differenze vanilla → container vanilla patch**: il container vanilla è ancora fedele?
3. **Regressioni**: la patch introduce comportamenti assenti nell'originale OCR?
4. **Conflitti**: ci sono modifiche incompatibili tra upstream e vanilla baseline?

## Output

Report in italiano con:
- Lista diff rilevanti (non cosmetici) upstream vs patch
- Lista diff vanilla baseline vs container vanilla nella patch
- Raccomandazioni prioritizzate: applicare subito / valutare / ignorare
- Rischi di regressione per ogni aggiornamento proposto

## Passo successivo suggerito

Se ci sono aggiornamenti da applicare: invoca **Implementatore Patch** dalla chat.
