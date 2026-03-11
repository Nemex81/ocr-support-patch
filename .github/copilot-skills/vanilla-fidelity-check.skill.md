---
name: vanilla-fidelity-check
description: >
  Confronta il container vanilla nel file della patch con il corrispondente
  file CK3 originale. Emette PASS o FAIL con lista delle differenze
  non autorizzate. Verifica binaria: fedele o non fedele.
parameters:
  - name: file_path
    description: >
      Percorso del file .gui nella patch.
      Esempio: ocr_support_compatibility_pach/gui/window_faith.gui
    required: true
---

# vanilla-fidelity-check

## Logica di Esecuzione

1. Leggi il file `file_path` nella patch.
2. Estrai esclusivamente il blocco con nome che inizia con `vanilla_` e
   visibility `[GetVariableSystem.Exists('ocr')]`.
3. Determina il nome della finestra dal file e costruisci il percorso vanilla:
   `../CK3 ORIGINAL VERSION/ck3origin/game/gui/[nome_file].gui`
4. Leggi il file vanilla originale.
5. Confronta il contenuto del container vanilla estratto con il vanilla originale.
  La verifica e' testuale e comparativa: non promettere automazioni oltre le differenze
  leggibili nel contenuto dei file.

### Differenze AUTORIZZATE (non segnalare come bug)

- Riga wrapper: `container { name = "vanilla_*_container" visible = "..." }`
- Righe di chiusura `}` aggiuntive per il wrapper
- Differenze di indentazione (spazi/tab)
- Righe che iniziano con `#` (commenti aggiunti)

### Differenze NON AUTORIZZATE (= bug da segnalare)

- Widget rimossi rispetto al vanilla
- Widget aggiunti rispetto al vanilla (salvo il wrapper container)
- Proprietà modificate: `size`, `position`, `type`, `name`, binding `[...]`
- Ordine dei widget alterato
- Blocchi `blockoverride` modificati o rimossi
- Proprietà interattive modificate o rimosse: `onclick`, `onrightclick`, `tooltip`, hover feedback, stato `enabled` o `disabled`

---

## Formato Output Obbligatorio

```text
## Verifica Fedeltà Vanilla: [nome_file]

| Widget/Riga | Contenuto Patch | Contenuto Atteso | Tipo Differenza |
|-------------|----------------|------------------|-----------------|
| btn_close | onclick modificato | onclick originale | 🔴 BUG |
| wrapper container | aggiunto | assente in vanilla | ✅ AUTORIZZATA |

**Verdetto**: PASS — container vanilla fedele al CK3 originale.
oppure
**Verdetto**: FAIL — N bug non autorizzati rilevati.
```

---

## Agenti che usano questa skill

- **Revisore Vanilla**: invoca come UNICO passo della sua metodologia.
  Sostituisce interamente i passi 1-5 della metodologia attuale.
- **Auditore Finale**: invoca nella sezione "Fedeltà Vanilla" della checklist.
  Un verdetto FAIL dalla skill è automaticamente un blocco CRITICO nell'audit.
