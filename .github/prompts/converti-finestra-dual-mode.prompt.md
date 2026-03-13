---
agent: agent
description: Converte una singola finestra GUI CK3 al sistema dual-mode OCR/Vanilla. UNA FINESTRA ALLA VOLTA.
tools: [read, search, terminal]
---

# Conversione Dual-Mode — Una Finestra

Leggi prima le istruzioni globali: `${file:.github/copilot-instructions.md}`
Leggi il pattern canonical: `${file:.github/resources/dual_mode_pattern_canonical.md}`
Leggi i pattern di conversione: `${file:.github/resources/conversion-patterns.md}`

## Input

- Nome finestra: ${input:nomeFinestra}
- Pattern di conversione: ${input:pattern} (simple | tabs | complex)

## File sorgente (sola lettura obbligatoria)

- OCR upstream: `../CK3-OCR/OCR-Support/gui/${input:nomeFinestra}.gui`
- Vanilla CK3: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/${input:nomeFinestra}.gui`
- Patch attuale: `ocr_support_compatibility_pach/gui/${input:nomeFinestra}.gui`

## Sequenza operativa — SEGUIRE NELL'ORDINE, NON SALTARE PASSI

### PASSO 1 — Analisi tri-repo
```
python tools/tri_diff.py --window ${input:nomeFinestra}
```
Mostrare il report completo al modder. Aspettare conferma prima di continuare.

### PASSO 2 — Verifica sorgenti
Verificare che entrambi i file sorgente esistano:
- Se OCR upstream mancante: comunicarlo al modder, STOP.
- Se vanilla mancante: comunicarlo al modder, STOP.
- Se entrambi presenti: procedere.

### PASSO 3 — Bozza assemblaggio (DRY-RUN)
```
python tools/assemble_dualmode.py --window ${input:nomeFinestra} --mode ${input:pattern} --dry-run
```
Mostrare l'output completo al modder.

### CHECKPOINT 1 — APPROVAZIONE MODDER OBBLIGATORIA
**STOP. Chiedere al modder: "La bozza è corretta? Posso scrivere il file nella patch?"**
Non procedere senza risposta affermativa esplicita.

### PASSO 4 — Scrittura file nella patch
```
python tools/assemble_dualmode.py --window ${input:nomeFinestra} --mode ${input:pattern}
```

### PASSO 5 — Estrazione scope e aggiornamento whitelist
```
python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/${input:nomeFinestra}.gui
```
Aggiungere alla whitelist `.github/resources/jomini_scope_whitelist.md` tutti i binding ASSENTI.

### PASSO 6 — Audit automatico
```
python tools/audit.py --window ${input:nomeFinestra}
```
- Se BLOCCANTE: elencare i CRITICO, correggerli, ri-eseguire audit. Non procedere fino a OK.
- Se CON AVVERTENZE: documentarle per il modder, procedere con nota.
- Se OK: procedere.

### CHECKPOINT 2 — VERDETTO AUDIT AL MODDER
Mostrare il verdetto completo di audit.py al modder prima di passare ai revisori.

### PASSO 7 — Revisori
Invocare in sequenza:
1. Agente **Revisore Accessibilità**
2. Agente **Revisore Vanilla**
3. Agente **Auditore Finale** → emette APPROVED o BLOCKED

### PASSO 8 — Chiusura
- Se APPROVED: aggiornare `gui-conversion-progress.instructions.md`
- Se BLOCKED: elencare fix richiesti, aspettare istruzioni modder

## Vincolo assoluto
Dopo il completamento, NON proporre di iniziare un'altra finestra.
Attendere istruzioni esplicite del modder per qualsiasi operazione successiva.
