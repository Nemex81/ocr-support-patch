---
agent: orchestratore
description: Avvio manuale del ciclo di conversione dual-mode per una singola finestra.
tools: [read, search, terminal]
---

# Avvia conversione dual-mode

Leggi prima:
- ${file:.github/copilot-instructions.md}
- ${file:.github/resources/orchestration_protocol.md}

Input richiesti:
- Nome finestra: ${input:nomeFinestra}
- Pattern conversione: ${input:pattern} (simple | tabs | complex)

Istruzione operativa:
Avvia immediatamente la Fase 0 del protocollo per la finestra indicata, usando il pattern fornito.
Applica il protocollo come riferimento normativo unico, senza riscriverlo in output.
Esegui una sola finestra alla volta.
Rispetta i checkpoint obbligatori CP1 e CP2 con stop esplicito in attesa conferma modder.
