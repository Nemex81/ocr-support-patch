---
mode: agent
description: Analizza un errore Jomini dai log CK3 e propone fix
tools: [read, search]
model: ['GPT-5.2 Codex', 'GPT-5.4']
---

# Task: Debug Errore Jomini

Leggi: `${file:.github/copilot-instructions.md}`

## Errore da analizzare
```
${input:testoErrore}
```

## File coinvolto (se noto)
`${input:fileGui}`

## Procedura

1. Identifica il tipo di errore (syntax, missing widget, invalid scope, missing datatype...)
2. Individua la riga/widget specifico nel file
3. Confronta con il file vanilla in `../CK3 ORIGINAL VERSION/ck3origin/game/gui/` per capire lo stato atteso
4. Proponi il fix minimo necessario senza toccare altro
5. Spiega in italiano perché si è verificato l'errore e come evitarlo in futuro

## Vincolo
Non proporre mai fix che rompono la compatibilità con CK3 1.17.1.
Se l'errore richiede una feature non disponibile in 1.17.1, dillo esplicitamente.
