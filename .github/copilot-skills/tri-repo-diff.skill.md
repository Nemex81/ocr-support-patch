---
name: tri-repo-diff
description: >
  Legge il file .gui corrispondente nei tre repository (patch attiva,
  OCR upstream Agamidae, vanilla CK3 originale) e produce un report
  strutturato con le differenze per sezioni widget.
  È il punto di ingresso standard per ogni nuova analisi di finestra.
parameters:
  - name: window_name
    description: >
      Nome base del file senza estensione.
      Esempio: window_faith, window_council, window_military
    required: true
---

## Logica di Esecuzione

I tre percorsi da usare sono fissi e obbligatori:
- **Patch attiva**: `ocr_support_compatibility_pach/gui/[window_name].gui`
- **OCR upstream**: `../CK3-OCR/OCR-Support/gui/[window_name].gui`
- **Vanilla CK3**: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/[window_name].gui`

> ⚠️ Il path vanilla usa SPAZI, non trattini: `CK3 ORIGINAL VERSION`

Per ognuno dei tre file:
1. Verifica se esiste. Se non esiste, segnalarlo esplicitamente nel report.
2. Leggi la struttura gerarchica: mappa ogni widget con tipo, nome e profondità.
3. Per la patch: identifica separatamente il container OCR e il container vanilla.

Produci il report con queste sezioni:

**Sezione A — Struttura vanilla originale**: albero dei widget principali con
tipo e nome. Questa è la baseline di riferimento.

**Sezione B — Feature OCR upstream (Agamidae) non presenti nella patch**:
widget, sezioni o binding presenti nell'OCR di Agamidae ma assenti nella patch
attiva. Questi sono i gap da colmare.

**Sezione C — Discrepanze container vanilla in patch vs CK3 originale**:
qualunque differenza tra il blocco `vanilla_*_container` nella patch e il
corrispondente file CK3 originale. Differenze accettabili: wrapper container,
proprietà `visible`, indentazione, commenti `#`. Tutto il resto è un bug.

**Sezione D — Stato generale**: la patch è ALLINEATA / PARZIALE / DA CREARE
rispetto all'upstream OCR; il container vanilla è FEDELE / CON BUG / ASSENTE.

---

## Formato Output Obbligatorio

```
## Report Tri-Repo: [window_name]

### A — Struttura Vanilla Originale
[albero widget con tipo e nome, profondità indicata da indentazione]

### B — Feature OCR Upstream Mancanti nella Patch
| Feature/Widget | Presente in Agamidae | Presente in Patch | Note |
|----------------|---------------------|-------------------|------|
| sezione_xyz | ✅ | ❌ | Da implementare |

### C — Discrepanze Container Vanilla
| Widget | Valore in Patch | Valore Atteso (vanilla) | Tipo |
|--------|----------------|------------------------|------|
| btn_xyz | modificato | originale | 🔴 BUG |

### D — Stato Generale
- OCR upstream: ALLINEATA / PARZIALE / DA CREARE
- Container vanilla: FEDELE / CON BUG / ASSENTE
```

---

## Agenti che usano questa skill

- **Analista Tri-Repo**: invoca come UNICO passo della sua metodologia.
  Il report prodotto è l'input diretto per l'Architetto Dual-Mode.
- **Auditore Finale**: invoca per la verifica di completezza pre-commit
  (sezione C del report).
