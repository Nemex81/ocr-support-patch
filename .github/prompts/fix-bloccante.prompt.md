---
agent: orchestratore
description: Risolve i CRITICO aperti in una finestra nella sezione Bloccanti. Esegui con l'Implementatore Patch. Una finestra alla volta.
tools: [edit, read, search, terminal]
---

# Fix Bloccante — Risoluzione Critici

Finestra target: ${input:nomeFinestra}

Leggi prima:
- ${file:.github/copilot-instructions.md}
- ${file:.github/resources/orchestration_protocol.md}

Task operativo:
- Esegui il task fix-bloccante gia' definito per Orchestratore.
- Applica il protocollo come riferimento normativo unico, senza duplicarne la logica nel prompt.
- Opera su una sola finestra alla volta e rispetta i checkpoint obbligatori previsti dal protocollo.

Output atteso:
- Verdetto audit iniziale con elenco CRITICO
- Piano di fix minimo per ciascun critico
- Verdetto audit post-fix
- Stato finale finestra (Validate / Revisione Necessaria / Bloccanti)
