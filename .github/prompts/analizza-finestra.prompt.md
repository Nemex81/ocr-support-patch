---
mode: agent
description: Analizza una finestra GUI e produce un report strutturale
tools: [codebase, read_file]
---

# Task: Analisi Strutturale Finestra GUI

Leggi: `${file:.github/copilot-instructions.md}`

File da analizzare: `${input:percorsoFile}`

## Cosa produrre

1. **Struttura gerarchica** dei widget principali (tipo, nome, profondità)
2. **Tab presenti** con nome e contenuto sintetico di ciascuna
3. **Blockoverride** usati (lista con nome e scopo)
4. **Binding datamodel** presenti (tipo, scope)
5. **Sezioni già convertite** in OCR vs sezioni ancora solo vanilla
6. **Problemi rilevati** (naming duplicati, widget non accessibili, binding ambigui)
7. **Stima complessità** conversione: bassa / media / alta + motivazione

Formato output: markdown strutturato, sezioni numerate, in italiano.
