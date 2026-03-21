---
agent: orchestratore
description: Confronta la patch con upstream OCR e vanilla per rilevare aggiornamenti
tools: [read, search]
---

# Task: Aggiornamento da Upstream

Leggi prima:
- ${file:.github/copilot-instructions.md}
- ${file:.github/resources/orchestration_protocol.md}

Task operativo:
- Esegui il task aggiornamento-upstream gia' definito per Orchestratore.
- Applica il protocollo come riferimento normativo unico, senza duplicarne la logica in output.

Input richiesto:
- Nome file: ${input:nomeFile}

Output atteso:
- Report in italiano con diff rilevanti upstream vs patch
- Verifica fedelta' vanilla del container vanilla nella patch
- Raccomandazioni prioritarie (applicare subito / valutare / ignorare)
- Rischi di regressione per ogni aggiornamento proposto
