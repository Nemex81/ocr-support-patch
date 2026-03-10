# OCR Support Patch — Istruzioni Copilot

## Identità del Progetto

Questo repository contiene una **mod per Crusader Kings 3 (versione 1.17.1)** che implementa il sistema **Dual Mode** per l'accessibilità dei giocatori non vedenti.
Ogni finestra GUI viene convertita per supportare due modalità:
- **Modalità OCR** (`ocr_accessibility_mode = yes`): layout testuale puro, leggibile da screen reader
- **Modalità Vanilla** (`ocr_accessibility_mode = no`): layout grafico originale Paradox, invariato

Il toggle è controllato dalla game_rule `ocr_accessibility_mode`, attivabile con **Shift+F11** in-game.

---

## Struttura Repository

```
ocr-support-patch/
├── .github/
│   ├── copilot-instructions.md     ← questo file
│   └── prompts/                    ← prompt riutilizzabili per Copilot
ocr_support_compatibility_pach/
│   └── gui/                        ← file .gui della mod (lavoro attivo)
coding_ai/
│   └── gui/                        ← note e riferimenti per Copilot
```

I file GUI vanilla di riferimento si trovano in:
`../CK3-ORIGINAL-VERSION/ck3origin/game/gui/`

I file GUI OCR upstream (Agamidae) si trovano in:
`../CK3-OCR/OCR-Support/gui/`

---

## Linguaggio e Sintassi

- Linguaggio: **Jomini GUI scripting** (proprietario Paradox, CK3 1.17.1)
- Estensione file: `.gui`
- Encoding: `UTF-8`
- **NON usare** widget type, scope, datatype o proprietà Jomini non documentati per CK3 1.17.1
- **NON inventare** nomi di funzioni o binding non presenti nei file vanilla di riferimento
- Ogni modifica DEVE essere compatibile con il sistema di override mod di CK3

---

## Pattern Obbligatorio — Dual Mode

Ogni finestra convertita DEVE seguire questo schema:

```
types NomeFinestra_types {
    # ... type definitions ...
}

window = {
    name = "nome_finestra"

    # === BLOCCO OCR ===
    container = {
        name = "ocr_nome_container"
        visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('yes')]"
        # Solo: text_single, text_multi, flowcontainer, text_label, button con tooltip testuale
        # Font size minimo: 18 | Colore testo: #FFFFFF o #FFDD88
        # Struttura gerarchica con header testuali espliciti per ogni sezione
        # NESSUN widget grafico: niente icon, portrait, progressbar visivi
    }

    # === BLOCCO VANILLA ===
    container = {
        name = "vanilla_nome_container"
        visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('no')]"
        # Layout grafico originale Paradox — identico al file vanilla CK3
        # NON modificare questa sezione salvo bugfix espliciti
    }
}
```

**Regola critica**: I due container sono mutualmente esclusivi via `visible`. Il container vanilla deve essere una copia fedele del file CK3 originale. Il container OCR è la nuova implementazione accessibile.

---

## Regole Widget OCR

- `text_single` / `text_multi`: testo informativo — sempre con `autoresize = yes`
- `flowcontainer`: raggruppamento di elementi testuali — direzione `down` preferita
- Bottoni: sempre con `tooltip` testuale descrittivo, NON solo icona
- Sezioni con dati variabili: usare `item` dentro `fixedgridwidget` o `vbox`
- Header di sezione: `text_label` con font_size = 20, colore = `{ 255 221 136 255 }` (giallo)
- Dati numerici: sempre con unità e contesto (es. "Oro: [GetGold]" non solo "[GetGold]")
- Nessun `icon` standalone senza `tooltip` leggibile

---

## Regole Blockoverride

Se il file usa `blockoverride`, le modifiche OCR vanno inserite **dentro** il block esistente, NON creando nuovi block paralleli:

```
blockoverride "nome_block" {
    # contenuto vanilla originale...
    # in fondo al block aggiungere:
    container = {
        name = "ocr_nome_inline"
        visible = "[GameRules.GetRule('ocr_accessibility_mode').GetSetting().IsSet('yes')]"
        # ...
    }
}
```

---

## File Già Convertiti (Pattern di Riferimento)

I seguenti file sono stati convertiti e rappresentano il pattern canonical:
- `window_character.gui` — finestra personaggio complessa, multi-tab
- `window_council.gui` — consiglio con tab e interazioni
- `window_culture.gui` — finestra cultura con alberi e progressi
- `window_faith.gui` — fede con tab e dottrine
- `window_combat.gui` — combattimento con dati militari
- `window_intrigue.gui` — intrigo con schemi e agenti
- `window_inventory.gui` — inventario con artefatti
- `window_military.gui` — militare con tab eserciti
- `window_council.gui` — consiglio
- `hud.gui` — HUD principale

Prima di implementare una nuova finestra, **consulta sempre** un file già convertito come esempio.

---

## Workflow Standard per Nuova Finestra

1. Apri il file vanilla da `../CK3-ORIGINAL-VERSION/ck3origin/game/gui/nome_file.gui`
2. Apri il file OCR upstream da `../CK3-OCR/OCR-Support/gui/nome_file.gui`
3. Identifica la struttura dei widget vanilla (tipo, nome, gerarchia)
4. Costruisci il container OCR rispettando la stessa gerarchia informativa
5. Incapsula il vanilla originale nel container vanilla senza modifiche
6. Verifica che le due visibility siano mutuamente esclusive
7. Testa la logica visible con entrambi i valori di `ocr_accessibility_mode`

---

## Errori Comuni da Evitare

- ❌ Non usare `show_when` al posto di `visible`
- ❌ Non modificare widget vanilla per "migliorarli"
- ❌ Non usare scope `ROOT` o `THIS` in contesti GUI senza verifica
- ❌ Non aggiungere newline extra dentro stringhe di binding `[...]`
- ❌ Non duplicare `name` identici dentro lo stesso livello di gerarchia
- ❌ Non usare `datamodel` senza verificarne il type nel data_binding vanilla
- ❌ Non omettere `parentanchor` e `size` dove il layout vanilla li richiede

---

## Note Operative

- Il modder è non vedente: usa screen reader. I messaggi di errore devono essere chiari e in italiano.
- Preferire risposte che spiegano il **perché** di ogni scelta tecnica
- Se un pattern Jomini è ambiguo, chiedere conferma prima di implementare
- La compatibilità con CK3 1.17.1 è prioritaria rispetto a qualunque feature nuova
