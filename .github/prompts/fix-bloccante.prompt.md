---
mode: agent
description: Risolve i CRITICO aperti in una finestra nella sezione Bloccanti. Esegui con l'Implementatore Patch. Una finestra alla volta.
tools: [edit, read, search, terminal]
---

# Fix Bloccante — Risoluzione Critici

Finestra target: **${nomeFinestra}**
(es: `window_activity_list`, senza estensione `.gui`)

---

## PASSO 1 — Audit iniziale

Esegui e mostrami l'output completo senza modificare nulla:

```
python tools/audit.py --window ${nomeFinestra}
```

Per ogni CRITICO trovato riporta:
- Numero di riga esatto
- Tipo di problema (strutturale / binding assente / pattern deprecato / tooltip mancante)
- Messaggio completo

---

## PASSO 2 — Contesto righe critiche

Per ciascun CRITICO identificato nel passo precedente:
- Mostrami le righe da `[riga - 8]` a `[riga + 8]` del file
  `ocr_support_compatibility_pach/gui/${nomeFinestra}.gui`
- Descrivi in italiano cosa fa il widget in quel punto

Non proporre fix. Non aprire altri file. Aspetta il CHECKPOINT.

---

## ⛔ CHECKPOINT — Approvazione modder

Presentami il riepilogo:
- Numero di CRITICO trovati
- Per ciascuno: riga, tipo, contesto breve
- La tua proposta di fix per ciascuno (una riga di spiegazione)

**Attendi conferma esplicita prima di procedere al Passo 3.**

---

## PASSO 3 — Applicazione fix

Solo dopo approvazione esplicita del modder:

- Applica i fix approvati sul file `ocr_support_compatibility_pach/gui/${nomeFinestra}.gui`
- Ogni modifica deve essere minima — tocca solo le righe del CRITICO
- Non correggere avvertenze, non riorganizzare codice, non migliorare nulla fuori scope

---

## PASSO 4 — Verifica post-fix

Esegui di nuovo:

```
python tools/audit.py --window ${nomeFinestra}
```

Riporta il nuovo verdetto completo.

- Se 0 CRITICO → procedi al Passo 5
- Se ancora CRITICO aperti → torna al Passo 2 con i critici residui

---

## PASSO 5 — Aggiornamento registro

Aggiorna `.github/instructions/gui-conversion-progress.instructions.md`:

- Se nuovo verdetto = `OK` (0 critici, 0 avvertenze):
  sposta la voce in **Convertite — Validate**

- Se nuovo verdetto = `CON AVVERTENZE` (0 critici, avvertenze aperte):
  sposta la voce in **Convertite — Revisione Necessaria**

- Aggiorna i valori nelle colonne: `Ultimo audit`, `Critici`, `Avv.`
- Aggiorna la data "Ultimo aggiornamento" in cima al file con la descrizione del fix applicato

---

## Note operative

- Le avvertenze (`ATTENZIONE`) **non sono oggetto di questo prompt** — ignorale
- Se il CRITICO è un binding assente dalla whitelist scope:
  esegui `python tools/scope_extractor.py --file ocr_support_compatibility_pach/gui/${nomeFinestra}.gui`
  e aggiungi i binding mancanti a `.github/resources/jomini_scope_whitelist.md`
- Se il CRITICO è strutturale (visible non mutuamente esclusivi):
  coinvolgi l'Architetto Dual-Mode prima di modificare
