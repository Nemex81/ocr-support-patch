---
agent: agent
description: Verifica la correttezza del dual mode in un file GUI già convertito
tools: [read, search]
---

# Task: Verifica Dual Mode

Leggi: `${file:.github/copilot-instructions.md}`

File da verificare: `ocr_support_compatibility_pach/gui/${input:nomeFile}.gui`

## Checklist da verificare

- [ ] Ogni window/widget ha il container OCR e il container vanilla
- [ ] Le visibility sono mutuamente esclusive e usano la game_rule corretta
- [ ] Il container vanilla è identico al file in `../CK3 ORIGINAL VERSION/ck3origin/game/gui/${input:nomeFile}.gui`
- [ ] Il container OCR non contiene widget grafici (icon standalone, portrait, progressbar visive)
- [ ] Tutti i bottoni OCR hanno tooltip testuale
- [ ] Font size OCR >= 18 ovunque
- [ ] Nessun `name` duplicato allo stesso livello gerarchico
- [ ] Nessun scope o datatype non verificato nel vanilla
- [ ] Gli header di sezione OCR sono presenti e in giallo

## Output

Per ogni voce della checklist: ✅ OK / ❌ Problema + riga/widget specifico.
In fondo: lista prioritizzata dei fix necessari.
