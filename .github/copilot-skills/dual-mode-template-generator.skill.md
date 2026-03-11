---
name: dual-mode-template-generator
description: >
  Genera lo scheletro Jomini dual mode completo per una finestra CK3.
  Produce il container OCR strutturato e il wrapper container vanilla.
  Il container vanilla è sempre un blocco vuoto con commento: il contenuto
  vanilla originale va incollato dall'Implementatore, mai inventato dalla skill.
parameters:
  - name: window_name
    description: >
      Nome della finestra senza estensione.
      Esempio: window_faith, window_council
    required: true
  - name: sections
    description: >
      Lista delle sezioni da creare nel container OCR, con tipo di dati.
      Formato: nome_sezione:tipo_contenuto separati da virgola.
      Esempio: "intestazione:titolo,oro:dato_numerico,vassalli:lista,chiudi:bottone"
      Tipi validi: titolo, dato_numerico, dato_testuale, lista, bottone, tab_header
    required: true
  - name: window_size
    description: >
      Dimensioni della finestra in pixel, formato LARGHEZZAxALTEZZA.
      Esempio: 800x600. Se non fornito, usa 800x600 come default.
    required: false
---

## Logica di Esecuzione

Genera il codice Jomini seguendo ESATTAMENTE il pattern canonical in
`.github/resources/dual_mode_pattern_canonical.md`.

### Regole di generazione obbligatorie

Per ogni sezione in `sections`, genera il widget corrispondente nel container OCR:

- `titolo` → `text_label` con `fontsize = 20`, `color = { 255 221 136 255 }`,
  `autoresize = yes`. Testo: nome sezione in MAIUSCOLO con placeholder binding.
- `dato_numerico` → `text_single` con `fontsize = 18`, `autoresize = yes`.
  Testo: `"NomeSezione: [PlaceholderBinding]"` — il modder sostituirà il binding.
- `dato_testuale` → `text_multi` con `fontsize = 18`, `autoresize = yes`,
  `max_width = 600`.
- `lista` → `vbox` con `spacing = 4` contenente un `fixedgridwidget` vuoto
  con commento `# Sostituire con datamodel corretto`.
- `bottone` → `button` con `fontsize = 18`, `tooltip = "DESCRIVERE AZIONE"`,
  `text = "[ NomeSezione ]"`. Il tooltip è sempre un placeholder esplicito.
- `tab_header` → `hbox` con `spacing = 8` contenente placeholder `button` per
  ogni tab, fontsize 18.

### Struttura fissa del container OCR generato

```jomini
container = {
    name = "ocr_[window_name]_container"
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"
    size = { 100% 100% }

    vbox = {
        layoutpolicy_horizontal = expanding
        layoutpolicy_vertical = expanding
        spacing = 4

        # [sezioni generate qui]
    }
}
```

### Struttura fissa del container vanilla generato

```jomini
container = {
    name = "vanilla_[window_name]_container"
    visible = "[GetVariableSystem.Exists('ocr')]"

    # =============================================
    # VANILLA ORIGINALE — NON MODIFICARE MAI
    # Incollare qui il contenuto del file:
    # ../CK3 ORIGINAL VERSION/ck3origin/game/gui/[window_name].gui
    # Identico al vanilla senza nessuna modifica.
    # =============================================
}
```

### Vincoli assoluti

- La skill NON inventa mai il contenuto vanilla. Il blocco vanilla è sempre
  vuoto con il commento di istruzione. Questo è intenzionale e non va cambiato.
- La skill NON aggiunge binding reali. Usa sempre placeholder espliciti del
  tipo `[PlaceholderBinding]` con commento `# Sostituire con binding verificato`.

---

## Formato Output Obbligatorio

La skill produce direttamente il codice Jomini in un blocco di codice markdown,
preceduto da questo header:

```
## Template Dual Mode Generato: [window_name]

> ⚠️ Questo è uno scheletro. Prima di usarlo:
> 1. Sostituire tutti i `[PlaceholderBinding]` con binding verificati in whitelist
> 2. Incollare il vanilla originale nel container vanilla
> 3. Invocare #scope-whitelist-check sui binding scelti
> 4. Invocare #deprecated-pattern-scanner sul file completato

[codice Jomini]
```

---

## Agenti che usano questa skill

- **Implementatore Patch**: invoca al passo 4 del workflow ("Costruisci il
  container OCR") passando le sezioni dal progetto dell'Architetto. Usa l'output
  come punto di partenza, sostituisce i placeholder con binding reali.
- **Architetto Dual-Mode**: può invocarla in modalità bozza rapida per
  visualizzare la struttura proposta prima di passarla all'Implementatore.
