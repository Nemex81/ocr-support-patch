---
agent: agent
description: Converte una finestra GUI CK3 al sistema dual mode OCR/Vanilla
tools: [read, search]
---

# Task: Conversione Dual Mode

Leggi prima le istruzioni globali del progetto:
`${file:.github/copilot-instructions.md}`

## Input richiesti
- **File target** (nella patch): `ocr_support_compatibility_pach/gui/${input:nomeFile}.gui`
- **File vanilla di riferimento**: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/${input:nomeFile}.gui`
- **File OCR upstream**: `../CK3-OCR/OCR-Support/gui/${input:nomeFile}.gui`

## Procedura

1. Leggi il file vanilla — identifica: struttura widget, nomi container, tab, blockoverride
2. Leggi il file OCR upstream di Agamidae — identifica cosa ha già implementato
3. Confronta i due per trovare discrepanze e sezioni mancanti nella patch attuale
4. Implementa il dual mode seguendo ESATTAMENTE il pattern in `.github/copilot-instructions.md`
5. Il container vanilla = copia fedele del vanilla originale, NESSUNA modifica
6. Il container OCR = implementazione testuale accessibile di TUTTE le informazioni presenti nel vanilla

## Vincoli
- CK3 versione 1.17.1 — nessuna feature di versioni successive
- Nessun widget grafico nel blocco OCR
- Font size OCR minimo: 18
- Ogni sezione OCR deve avere un header testuale in giallo (#FFDD88)
- Tutti i bottoni OCR devono avere tooltip descrittivo
