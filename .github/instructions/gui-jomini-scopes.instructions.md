---
applyTo: "**/*.gui"
---

# Regole Scope Jomini — CK3 1.17.1

Copilot **NON deve usare scope non verificati nel vanilla** senza verifica esplicita.

> **Regola obbligatoria**: ogni volta che un nuovo scope viene verificato nel vanilla
> (`../CK3 ORIGINAL VERSION/ck3origin/game/gui/`), va aggiunto immediatamente
> a `.github/resources/jomini_scope_whitelist.md` (file master).

**Lista completa scope verificati**: `.github/resources/jomini_scope_whitelist.md`

---

## Binding Dual Mode (obbligatori, non modificare)

```jomini
# Visibilità OCR attiva
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('yes')]"
# Visibilità vanilla attiva
visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('no')]"
```

---

## Note operative

- Il modificatore `|0` formatta i numeri — usarlo sempre per valori numerici
- I scope dipendono dal contesto widget parent — verificare sempre la gerarchia
- In caso di dubbio: aprire il file vanilla corrispondente e copiare il binding esatto
- Se un scope non è nel file master: aggiungerlo **solo dopo verifica manuale nel vanilla**
