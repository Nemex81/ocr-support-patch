---
applyTo: "**/localization/**/*.yml"
---

# Istruzioni Localizzazione OCR — CK3 1.17.1

Attive automaticamente per tutti i file `.yml` di localizzazione.

## Convenzioni Chiavi OCR

Prefisso obbligatorio `ocr_`:

```yaml
# Formato: ocr_[finestra]_[sezione]_[elemento]
ocr_character_stats_gold: "Oro: "
ocr_council_task_current: "Compito attuale: "
```

## Requisiti per Screen Reader NVDA

- Nessuna abbreviazione senza spiegazione
- Nessun simbolo grafico come unico contenuto
- Testo sensato se letto ad alta voce
- Numeri con unità: "450 oro" non "450"
- Bonus/malus espliciti: "+15% velocità movimento" non "+15%"

## Encoding

- UTF-8 BOM (obbligatorio per CK3)
- Prima riga: `l_english:`
- Indentazione: 1 spazio prima della chiave
