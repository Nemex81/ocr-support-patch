---
name: deprecated-pattern-scanner
description: >
  Scansiona un file .gui e segnala tutti i pattern deprecati, vietati o
  pericolosi per CK3 1.17.1 e per il sistema dual mode OCR.
  Output: tabella con riga, pattern trovato, gravità, fix consigliato.
parameters:
  - name: file_path
    description: >
      Percorso del file .gui da analizzare, relativo alla root del workspace.
      Esempio: ocr_support_compatibility_pach/gui/window_faith.gui
    required: true
---

# deprecated-pattern-scanner

## Pre-Run Automatico

Prima di qualsiasi analisi manuale, eseguire:
```
python tools/gui_validator.py --file <file_path>
```
L'output dello script è la fonte autoritativa per tutti i problemi CRITICO.
Procedere con l'analisi manuale SOLO per completare i flag ATTENZIONE
o per fornire contesto interpretativo ai problemi già rilevati dallo script.
Se lo script riporta verdetto PULITO, la skill può concludere immediatamente
senza analisi manuale ulteriore.

## Logica di Esecuzione

Leggi il file indicato in `file_path`. Analizza ogni riga cercando i pattern
nella lista seguente. Per ogni occorrenza trovata, registra: numero di riga,
pattern esatto trovato, categoria, gravità, fix consigliato.

### Pattern da cercare — categoria DEPRECATO

- Qualunque variante realistica di `GameRules.GetRule('ocr_accessibility_mode')`, incluse:
  - apici singoli o doppi
  - spazi variabili tra `GetRule`, parentesi e stringa
  - uso dentro binding più lunghi sulla stessa riga
  Sostituire con `GetVariableSystem.Exists('ocr')` per visibilità vanilla o
  `Not(GetVariableSystem.Exists('ocr'))` per visibilità OCR.

### Pattern da cercare — categoria VIETATO

- `show_when` — sostituire con `visible`
- Scope `ROOT` usato in binding GUI senza nota di verifica nel commento
- Scope `THIS` usato in binding GUI senza nota di verifica nel commento
- `datamodel` senza corrispondente verifica del type nella whitelist scope

### Pattern da cercare — categoria STRUTTURALE

- `name` duplicati allo stesso livello gerarchico (stesso blocco padre)
- Widget `icon` senza proprietà `tooltip` nella stessa definizione
- Bottone (`button`) senza proprietà `tooltip`
- `text_single` o `text_multi` nel blocco OCR con `fontsize` < 18
- `text_label` usato come header OCR senza `color = { 255 221 136 255 }`

### Pattern da cercare — categoria VISIBILITÀ

- Container con nome che inizia con `ocr_` ma con visibility
  `[GetVariableSystem.Exists('ocr')]` (invertita — bug logico)
- Container con nome che inizia con `vanilla_` ma con visibility
  `[Not(GetVariableSystem.Exists('ocr'))]` (invertita — bug logico)

---

## Formato Output Obbligatorio

```text
## Risultati Scansione: [nome_file]

| Riga | Pattern trovato | Categoria | Gravità | Fix consigliato |
|------|----------------|-----------|---------|-----------------|
| 42   | GameRules.GetRule('ocr_accessibility_mode') | DEPRECATO | 🔴 CRITICO | Sostituire con GetVariableSystem.Exists('ocr') |
| 87   | button senza tooltip | STRUTTURALE | 🔴 CRITICO | Aggiungere tooltip descrittivo |
| 103  | icon senza tooltip | STRUTTURALE | 🟡 ATTENZIONE | Aggiungere tooltip o rimuovere icon standalone |

**Verdetto**: BLOCCANTE / CON AVVERTENZE / PULITO
**Problemi critici**: N
**Avvertenze**: N
```

Se il file è pulito, emettere: `**Verdetto**: PULITO — nessun pattern problematico rilevato.`

---

## Agenti che usano questa skill

- **Implementatore Patch**: invoca prima di ogni commit, dopo ogni modifica
- **Auditore Finale**: invoca come primo passo della checklist pre-commit
