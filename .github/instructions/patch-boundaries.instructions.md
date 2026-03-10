---
applyTo: "**"
---

# Confini Operativi della Patch — CK3 OCR Accessibility

Attive automaticamente per qualunque file nel workspace.

## Percorsi Scrivibili

Copilot può modificare file **esclusivamente** nei seguenti percorsi:

| Percorso | Condizione |
|----------|-----------|
| `ocr_support_compatibility_pach/gui/` | Lavoro principale — conversioni Dual Mode |
| `.github/resources/jomini_scope_whitelist.md` | Solo per aggiunta scope verificati nel vanilla |

## Percorsi Vietati in Scrittura

Qualsiasi edit fuori dai percorsi scrivibili è **proibito senza conferma esplicita dell'utente**. In particolare:

- `../CK3-OCR/` — repository upstream Agamidae, sola lettura
- `../CK3 ORIGINAL VERSION/` — vanilla Paradox, sola lettura
- `coding_ai/` — documentazione storica, non modificare
- `.github/agents/` — definizioni agenti, non modificare
- `.github/prompts/` — prompt riutilizzabili, non modificare
- `.github/instructions/` — istruzioni framework, non modificare
- `.vscode/` — configurazione editor, non modificare

## Regola Operativa

Se un task richiede modifiche fuori da `ocr_support_compatibility_pach/gui/` o dalla whitelist scope:
1. **Fermarsi**
2. Segnalare all'utente il file e il motivo
3. Attendere conferma esplicita prima di procedere
