---
applyTo: "**/*.gui"
---

# Regole Scope Jomini — CK3 1.17.1

Copilot **NON deve usare scope non verificati nel vanilla** senza verifica esplicita.

> **Regola obbligatoria**: ogni volta che un nuovo scope viene verificato nel vanilla
> (`C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/gui/`
> — path letto da `tools/config.py` come `VANILLA_GUI`), va aggiunto immediatamente
> a `.github/resources/jomini_scope_whitelist.md` (file master).

**Lista completa scope verificati**: `.github/resources/jomini_scope_whitelist.md`

---

## Binding Dual Mode (obbligatori, non modificare)

```jomini
# Container OCR attivo — modalità non vedente (variabile ocr assente)
visible = "[Not(GetVariableSystem.Exists('ocr'))]"
# Container vanilla attivo — modalità normo-vedente (variabile ocr presente)
visible = "[GetVariableSystem.Exists('ocr')]"
```

> ⚠️ `GameRules.GetRule('ocr_accessibility_mode')` è **deprecato** — non usarlo.

---

## Note operative

- Il modificatore `|0` formatta i numeri — usarlo sempre per valori numerici
- I scope dipendono dal contesto widget parent — verificare sempre la gerarchia
- In caso di dubbio: aprire il file vanilla corrispondente e copiare il binding esatto
- Se un scope non è nel file master: aggiungerlo **solo dopo verifica manuale nel vanilla**
