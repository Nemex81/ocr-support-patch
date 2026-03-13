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
- `../CK3 ORIGINAL VERSION/` — copia parziale vanilla su GitHub (solo .gui), sola lettura
- `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/` — installazione CK3 completa locale, sola lettura
- `.github/agents/` — definizioni agenti, non modificare
- `.github/prompts/` — prompt riutilizzabili, non modificare
- `.github/instructions/` — istruzioni framework, non modificare
- `.vscode/` — configurazione editor, non modificare

## Regola Operativa

Se un task richiede modifiche fuori da `ocr_support_compatibility_pach/gui/` o dalla whitelist scope:
1. **Fermarsi**
2. Segnalare all'utente il file e il motivo
3. Attendere conferma esplicita prima di procedere

## Riferimento machine-readable

Agli script e agli agenti automatizzati suggeriamo di consultare il file
`.github/resources/domain_boundaries.md` prima di decidere il dominio operativo.
Questo file contiene le categorie `framework` e `mod` e regole operative sintetiche
che possono essere usate per decisioni automatiche.
