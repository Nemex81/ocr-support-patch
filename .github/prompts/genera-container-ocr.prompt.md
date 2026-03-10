---
agent: agent
description: Genera il container OCR per una sezione specifica di una finestra
tools: [read, search]
model: ['GPT-5.2 Codex', 'GPT-5.1 Codex Max', 'GPT-5.4']
---

# Task: Genera Container OCR

Leggi: `${file:.github/copilot-instructions.md}`

## Input
- **Finestra**: `${input:nomeFinestra}`
- **Sezione da convertire**: `${input:nomeSezione}` (es: "tab_stats", "section_vassals", "panel_army")
- **File vanilla**: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/${input:nomeFile}.gui`

## Regole di generazione

1. Leggi la sezione vanilla indicata
2. Estrai TUTTE le informazioni mostrate (testo, numeri, stati, binding)
3. Genera il container OCR con:
   - `name = "ocr_${input:nomeSezione}_container"`
   - `visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('yes')]"`
   - Header giallo per la sezione
   - Ogni dato vanilla rappresentato come testo leggibile
   - Bottoni con tooltip descrittivi
4. NON omettere nessuna informazione presente nel vanilla
5. Output: solo il blocco codice Jomini, pronto per copia-incolla
