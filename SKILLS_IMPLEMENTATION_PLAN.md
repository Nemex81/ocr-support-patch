# Piano di Implementazione Skills — OCR Support Patch
# Framework Multi-Agente CK3 Accessibilità

> **Documento normativo per Copilot.**
> Questo file istruisce Copilot su come creare, strutturare e integrare le 6 skills
> nel framework multi-agente esistente. Le skills sono capacità procedurali
> riutilizzabili che gli agenti invocano automaticamente durante il loro workflow.
> Non è un documento di sola lettura: ogni istruzione qui è vincolante quanto
> quelle in `.github/copilot-instructions.md`.

---

## 1. Contesto e Obiettivo

Il framework attuale dispone di 6 agenti specializzati in `.github/agents/` e di
istruzioni domain-specific in `.github/instructions/`. Il problema attuale è che
la logica procedurale ripetuta (verifica scope, check accessibilità, confronto
vanilla, rilevamento pattern deprecati) è scritta in prosa in più agent file
separati. Quando una regola cambia, va aggiornata in ogni file manualmente.

Le **skills** risolvono questo problema: sono unità di capacità autonome, con
input/output dichiarati, che gli agenti invocano direttamente. Ogni skill
centralizza una logica che oggi è distribuita e ridondante.

### Posizione file skills

```
.github/
└── copilot-skills/
    ├── deprecated-pattern-scanner.skill.md
    ├── scope-whitelist-check.skill.md
    ├── tri-repo-diff.skill.md
    ├── vanilla-fidelity-check.skill.md
    ├── accessibility-checklist-runner.skill.md
    └── dual-mode-template-generator.skill.md
```

VS Code Copilot scopre automaticamente i file `.skill.md` in `.github/copilot-skills/`.
Gli agenti li invocano tramite `#nome-skill` nella chat o tramite riferimento
esplicito nel loro frontmatter YAML nella sezione `tools`.

---

## 2. Regole Generali per Tutte le Skills

Queste regole si applicano a ogni skill senza eccezioni.

1. **Formato file**: frontmatter YAML obbligatorio con `name`, `description`,
   `parameters`. Il corpo in Markdown descrive la logica esatta da eseguire.
2. **Output sempre strutturato**: ogni skill produce output in formato Markdown
   con tabelle o liste, mai prosa libera. Questo rende l'output leggibile
   sia da Copilot che dallo screen reader NVDA dell'utente.
3. **Nessuna scrittura implicita**: le skills di analisi (1-5) non scrivono mai
   file. Solo `dual-mode-template-generator` produce codice, e lo fa come
   output testuale — è l'Implementatore che decide se e dove incollarlo.
4. **Riferimento alle risorse esistenti**: ogni skill che consulta whitelist o
   pattern legge da `.github/resources/` — non ridefinisce le regole, le applica.
5. **Lingua output**: italiano, coerente con il resto del progetto.
6. **Compatibilità CK3 1.17.1**: le skills che analizzano o generano codice
   Jomini operano SOLO su costrutti documentati per CK3 1.17.1.

---

## 3. Sequenza di Implementazione

Rispetta rigorosamente questa sequenza. Le fasi sono dipendenti: non passare
alla successiva finché la corrente non è testata su almeno un file `.gui` reale.

```
Fase 0  →  Struttura cartella + aggiornamento copilot-instructions.md
Fase 1a →  deprecated-pattern-scanner      (solo lettura, lista chiusa)
Fase 1b →  scope-whitelist-check           (solo lettura, dipende da whitelist)
Fase 2a →  tri-repo-diff                   (lettura tri-repo)
Fase 2b →  vanilla-fidelity-check          (confronto binario patch vs vanilla)
Fase 3a →  accessibility-checklist-runner  (checklist NVDA automatica)
Fase 3b →  dual-mode-template-generator    (generazione codice scheletro)
Fase 4  →  Pulizia agent file + test integrazione completa
```

File di test consigliato per ogni fase: `window_faith.gui` — è già convertito,
quindi i risultati attesi sono verificabili senza rischio di regressione.

---

## 4. Fase 0 — Preparazione Struttura

### Azioni richieste

**4.1** Crea la cartella `.github/copilot-skills/` nel repository (basta creare
il primo file skill dentro di essa).

**4.2** Aggiorna `.github/copilot-instructions.md` — sezione "Struttura Repository":
aggiungere la voce mancante nella mappa:
```
│   └── copilot-skills/             ← skills invocabili dagli agenti
```

**4.3** Aggiungi in `.github/copilot-instructions.md` una nuova sezione
"Skills Disponibili" DOPO la sezione "Agenti Disponibili", con questa tabella:

```markdown
## Skills Disponibili in Questo Workspace

Le skills in `.github/copilot-skills/` sono capacità procedurali invocabili
dagli agenti tramite `#nome-skill`. Centralizzano logica ripetuta.

| Skill | File | Scopo |
|-------|------|-------|
| deprecated-pattern-scanner | `deprecated-pattern-scanner.skill.md` | Rileva pattern vietati/deprecati in file .gui |
| scope-whitelist-check | `scope-whitelist-check.skill.md` | Verifica binding Jomini contro whitelist |
| tri-repo-diff | `tri-repo-diff.skill.md` | Confronto strutturale tra i 3 repository |
| vanilla-fidelity-check | `vanilla-fidelity-check.skill.md` | Verifica fedeltà container vanilla |
| accessibility-checklist-runner | `accessibility-checklist-runner.skill.md` | Checklist NVDA automatica |
| dual-mode-template-generator | `dual-mode-template-generator.skill.md` | Genera scheletro dual mode da struttura vanilla |
```

**4.4** NON aggiornare ancora nessun agent file. Gli agent file si aggiornano
solo dopo che la skill corrispondente è scritta e verificata (Fase 4).

---

## 5. Fase 1a — Skill: `deprecated-pattern-scanner`

### File da creare
`.github/copilot-skills/deprecated-pattern-scanner.skill.md`

### Frontmatter YAML
```yaml
---
name: deprecated-pattern-scanner
description: >
  Scansiona un file .gui e segnala tutti i pattern deprecati, vietati o
  pericolosi per CK3 1.17.1 e per il sistema dual mode OCR.
  Output: tabella con riga, pattern trovato, gravità, fix consigliato.
parameters:
  - name: file_path
    description: >
      Percorso del file .gui da analizzare, relativo alla root del workspace.
      Esempio: ocr_support_compatibility_pach/gui/window_faith.gui
    required: true
---
```

### Corpo della skill (logica da eseguire)

Leggi il file indicato in `file_path`. Analizza ogni riga cercando i pattern
nella lista seguente. Per ogni occorrenza trovata, registra: numero di riga,
pattern esatto trovato, categoria, gravità, fix consigliato.

**Pattern da cercare — categoria DEPRECATO:**
- `GameRules.GetRule('ocr_accessibility_mode')` — sostituire con
  `GetVariableSystem.Exists('ocr')` per visibilità vanilla o
  `Not(GetVariableSystem.Exists('ocr'))` per visibilità OCR.

**Pattern da cercare — categoria VIETATO:**
- `show_when` — sostituire con `visible`
- Scope `ROOT` usato in binding GUI senza nota di verifica nel commento
- Scope `THIS` usato in binding GUI senza nota di verifica nel commento
- `datamodel` senza corrispondente verifica del type nella whitelist scope

**Pattern da cercare — categoria STRUTTURALE:**
- `name` duplicati allo stesso livello gerarchico (stesso blocco padre)
- Widget `icon` senza proprietà `tooltip` nella stessa definizione
- Bottone (`button`) senza proprietà `tooltip`
- `text_single` o `text_multi` nel blocco OCR con `fontsize` < 18
- `text_label` usato come header OCR senza `color = { 255 221 136 255 }`

**Pattern da cercare — categoria VISIBILITÀ:**
- Container con nome che inizia con `ocr_` ma con visibility
  `[GetVariableSystem.Exists('ocr')]` (invertita — bug logico)
- Container con nome che inizia con `vanilla_` ma con visibility
  `[Not(GetVariableSystem.Exists('ocr'))]` (invertita — bug logico)

### Formato output obbligatorio

```
## Risultati Scansione: [nome_file]

| Riga | Pattern trovato | Categoria | Gravità | Fix consigliato |
|------|----------------|-----------|---------|-----------------|
| 42   | GameRules.GetRule('ocr_accessibility_mode') | DEPRECATO | 🔴 CRITICO | Sostituire con GetVariableSystem.Exists('ocr') |
| 87   | button senza tooltip | STRUTTURALE | 🔴 CRITICO | Aggiungere tooltip descrittivo |
| 103  | icon senza tooltip | STRUTTURALE | 🟡 ATTENZIONE | Aggiungere tooltip o rimuovere icon standalone |

**Verdetto**: BLOCCANTE / CON AVVERTENZE / PULITO
**Problemi critici**: N
**Avvertenze**: N
```

Se il file è pulito, emettere: `**Verdetto**: PULITO — nessun pattern problematico rilevato.`

### Agenti che usano questa skill
- **Implementatore Patch**: invoca prima di ogni commit, dopo ogni modifica
- **Auditore Finale**: invoca come primo passo della checklist pre-commit

---

## 6. Fase 1b — Skill: `scope-whitelist-check`

### File da creare
`.github/copilot-skills/scope-whitelist-check.skill.md`

### Frontmatter YAML
```yaml
---
name: scope-whitelist-check
description: >
  Data una lista di binding Jomini, verifica la loro presenza in
  .github/resources/jomini_scope_whitelist.md.
  Classifica ogni binding: PRESENTE / ASSENTE / DA VERIFICARE.
  Per i binding ASSENTI, produce la riga pronta da aggiungere alla whitelist.
parameters:
  - name: bindings
    description: >
      Lista di binding da verificare. Uno per riga, formato [Scope.GetXxx]
      o [Scope.HasXxx] o qualunque forma di data binding Jomini.
    required: true
  - name: context
    description: >
      Nome del file o della finestra da cui provengono i binding.
      Usato per compilare la colonna "contesto d'uso" nella whitelist.
    required: false
---
```

### Corpo della skill (logica da eseguire)

Leggi il file `.github/resources/jomini_scope_whitelist.md`. Estrai tutti i
binding già presenti (colonna 1 della tabella, formato `\`NomeScope\``).

Per ogni binding nella lista `bindings` in input:

1. **PRESENTE**: il binding è nella whitelist → segnala con ✅
2. **ASSENTE**: il binding non è nella whitelist → segnala con ❌ e produci
   la riga da aggiungere nel formato:
   `| \`NomeBinding\` | [context se fornito, altrimenti "da specificare"] | verificato in vanilla CK3 1.17.1 |`
3. **DA VERIFICARE**: il binding contiene scope non standard (es. scope di mod
   non vanilla, scope con nome ambiguo) → segnala con ⚠️ e richiedi verifica
   manuale nel file vanilla prima di procedere.

### Formato output obbligatorio

```
## Verifica Whitelist Scope: [context]

| Binding | Stato | Note |
|---------|-------|------|
| `GetPlayer.GetTreasury` | ✅ PRESENTE | — |
| `GetPlayer.GetNewScope` | ❌ ASSENTE | Aggiungere alla whitelist |
| `SomeModScope.GetXxx` | ⚠️ DA VERIFICARE | Scope non standard, verificare in vanilla |

### Righe da aggiungere a jomini_scope_whitelist.md
| `GetPlayer.GetNewScope` | window_faith — sezione header | verificato in vanilla CK3 1.17.1 |

**Riepilogo**: PRESENTI: N | ASSENTI: N | DA VERIFICARE: N
```

Se tutti i binding sono presenti: `**Riepilogo**: Tutti i binding sono in whitelist. ✅`

### Regola critica per l'agente che usa questa skill

Se il risultato contiene binding ASSENTI, l'agente NON può procedere con
l'implementazione finché quei binding non vengono aggiunti alla whitelist.
La skill produce le righe pronte — l'Implementatore le incolla in
`.github/resources/jomini_scope_whitelist.md` prima di continuare.

### Agenti che usano questa skill
- **Architetto Dual-Mode**: invoca durante la progettazione, per ogni binding
  che intende usare nel container OCR
- **Implementatore Patch**: invoca prima di usare qualunque binding non già
  presente nel file che sta modificando
- **Auditore Finale**: invoca come verifica finale su tutti i binding del file

---

## 7. Fase 2a — Skill: `tri-repo-diff`

### File da creare
`.github/copilot-skills/tri-repo-diff.skill.md`

### Frontmatter YAML
```yaml
---
name: tri-repo-diff
description: >
  Legge il file .gui corrispondente nei tre repository (patch attiva,
  OCR upstream Agamidae, vanilla CK3 originale) e produce un report
  strutturato con le differenze per sezioni widget.
  È il punto di ingresso standard per ogni nuova analisi di finestra.
parameters:
  - name: window_name
    description: >
      Nome base del file senza estensione.
      Esempio: window_faith, window_council, window_military
    required: true
---
```

### Corpo della skill (logica da eseguire)

I tre percorsi da usare sono fissi e obbligatori:
- **Patch attiva**: `ocr_support_compatibility_pach/gui/[window_name].gui`
- **OCR upstream**: `../CK3-OCR/OCR-Support/gui/[window_name].gui`
- **Vanilla CK3**: `../CK3 ORIGINAL VERSION/ck3origin/game/gui/[window_name].gui`

> ⚠️ Il path vanilla usa SPAZI, non trattini: `CK3 ORIGINAL VERSION`

Per ognuno dei tre file:
1. Verifica se esiste. Se non esiste, segnalarlo esplicitamente nel report.
2. Leggi la struttura gerarchica: mappa ogni widget con tipo, nome e profondità.
3. Per la patch: identifica separatamente il container OCR e il container vanilla.

Produci il report con queste sezioni:

**Sezione A — Struttura vanilla originale**: albero dei widget principali con
tipo e nome. Questa è la baseline di riferimento.

**Sezione B — Feature OCR upstream (Agamidae) non presenti nella patch**:
widget, sezioni o binding presenti nell'OCR di Agamidae ma assenti nella patch
attiva. Questi sono i gap da colmare.

**Sezione C — Discrepanze container vanilla in patch vs CK3 originale**:
qualunque differenza tra il blocco `vanilla_*_container` nella patch e il
corrispondente file CK3 originale. Differenze accettabili: wrapper container,
proprietà `visible`, indentazione, commenti `#`. Tutto il resto è un bug.

**Sezione D — Stato generale**: la patch è ALLINEATA / PARZIALE / DA CREARE
rispetto all'upstream OCR; il container vanilla è FEDELE / CON BUG / ASSENTE.

### Formato output obbligatorio

```
## Report Tri-Repo: [window_name]

### A — Struttura Vanilla Originale
[albero widget con tipo e nome, profondità indicata da indentazione]

### B — Feature OCR Upstream Mancanti nella Patch
| Feature/Widget | Presente in Agamidae | Presente in Patch | Note |
|----------------|---------------------|-------------------|------|
| sezione_xyz | ✅ | ❌ | Da implementare |

### C — Discrepanze Container Vanilla
| Widget | Valore in Patch | Valore Atteso (vanilla) | Tipo |
|--------|----------------|------------------------|------|
| btn_xyz | modificato | originale | 🔴 BUG |

### D — Stato Generale
- OCR upstream: ALLINEATA / PARZIALE / DA CREARE
- Container vanilla: FEDELE / CON BUG / ASSENTE
```

### Agenti che usano questa skill
- **Analista Tri-Repo**: invoca come UNICO passo della sua metodologia.
  Il report prodotto è l'input diretto per l'Architetto Dual-Mode.
- **Auditore Finale**: invoca per la verifica di completezza pre-commit
  (sezione C del report).

---

## 8. Fase 2b — Skill: `vanilla-fidelity-check`

### File da creare
`.github/copilot-skills/vanilla-fidelity-check.skill.md`

### Frontmatter YAML
```yaml
---
name: vanilla-fidelity-check
description: >
  Confronta il container vanilla nel file della patch con il corrispondente
  file CK3 originale. Emette PASS o FAIL con lista delle differenze
  non autorizzate. Verifica binaria: fedele o non fedele.
parameters:
  - name: file_path
    description: >
      Percorso del file .gui nella patch.
      Esempio: ocr_support_compatibility_pach/gui/window_faith.gui
    required: true
---
```

### Corpo della skill (logica da eseguire)

1. Leggi il file `file_path` nella patch.
2. Estrai esclusivamente il blocco con nome che inizia con `vanilla_` e
   visibility `[GetVariableSystem.Exists('ocr')]`.
3. Determina il nome della finestra dal file e costruisci il percorso vanilla:
   `../CK3 ORIGINAL VERSION/ck3origin/game/gui/[nome_file].gui`
4. Leggi il file vanilla originale.
5. Confronta il contenuto del container vanilla estratto con il vanilla originale.

**Differenze AUTORIZZATE** (non segnalare come bug):
- Riga wrapper: `container { name = "vanilla_*_container" visible = "..." }`
- Righe di chiusura `}` aggiuntive per il wrapper
- Differenze di indentazione (spazi/tab)
- Righe che iniziano con `#` (commenti aggiunti)

**Differenze NON AUTORIZZATE** (= bug da segnalare):
- Widget rimossi rispetto al vanilla
- Widget aggiunti rispetto al vanilla (salvo il wrapper container)
- Proprietà modificate: `size`, `position`, `type`, `name`, binding `[...]`
- Ordine dei widget alterato
- Blocchi `blockoverride` modificati o rimossi

### Formato output obbligatorio

```
## Verifica Fedeltà Vanilla: [nome_file]

| Widget/Riga | Contenuto Patch | Contenuto Atteso | Tipo Differenza |
|-------------|----------------|------------------|-----------------|
| btn_close | onclick modificato | onclick originale | 🔴 BUG |
| wrapper container | aggiunto | assente in vanilla | ✅ AUTORIZZATA |

**Verdetto**: PASS — container vanilla fedele al CK3 originale.
oppure
**Verdetto**: FAIL — N bug non autorizzati rilevati.
```

### Agenti che usano questa skill
- **Revisore Vanilla**: invoca come UNICO passo della sua metodologia.
  Sostituisce interamente i passi 1-5 della metodologia attuale.
- **Auditore Finale**: invoca nella sezione "Fedeltà Vanilla" della checklist.
  Un verdetto FAIL dalla skill è automaticamente un blocco CRITICO nell'audit.

---

## 9. Fase 3a — Skill: `accessibility-checklist-runner`

### File da creare
`.github/copilot-skills/accessibility-checklist-runner.skill.md`

### Frontmatter YAML
```yaml
---
name: accessibility-checklist-runner
description: >
  Esegue la checklist completa di accessibilità NVDA su un file .gui convertito.
  Verifica ogni punto della checklist OCR in modo automatico e produce un
  report pass/fail per ogni punto con riferimento alla riga del file.
parameters:
  - name: file_path
    description: >
      Percorso del file .gui da verificare.
      Esempio: ocr_support_compatibility_pach/gui/window_faith.gui
    required: true
---
```

### Corpo della skill (logica da eseguire)

Leggi il file `file_path`. Estrai SOLO il blocco con nome che inizia con `ocr_`
e visibility `[Not(GetVariableSystem.Exists('ocr'))]`. Analizza quel blocco.

**Check 1 — Font size**: ogni widget `text_single`, `text_multi`, `text_label`,
`button` nel blocco OCR deve avere `fontsize` >= 18. Segnala riga e widget per
ogni violazione.

**Check 2 — Header sezioni**: ogni `text_label` che funge da titolo di sezione
deve avere `color = { 255 221 136 255 }` e `fontsize` >= 20. Un `text_label`
senza colore esplicito è una violazione.

**Check 3 — Tooltip bottoni**: ogni `button` nel blocco OCR deve avere
`tooltip` con testo non vuoto. Un bottone senza tooltip è un blocco CRITICO.

**Check 4 — Icone**: nessun `icon` standalone nel blocco OCR senza `tooltip`.
Un `icon` senza tooltip è invisibile a NVDA.

**Check 5 — Dati numerici con contesto**: i binding che producono valori
numerici (oro, truppe, date, percentuali) devono avere testo contestuale nella
stessa riga di testo (es. `"Oro: [GetGold]"` non solo `"[GetGold]"`). Verifica
che nessun widget OCR contenga un binding numerico isolato.

**Check 6 — Liste vuote**: se il file contiene `datamodel` nel blocco OCR,
verifica che ci sia un widget o testo alternativo per il caso lista vuota.

**Check 7 — Visibilità**: il blocco OCR deve usare ESCLUSIVAMENTE
`visible = "[Not(GetVariableSystem.Exists('ocr'))]"` per la sua visibilità.
Qualunque altra sintassi di visibility nel container OCR è una violazione.

**Check 8 — Struttura gerarchia**: il blocco OCR deve avere almeno un widget
con testo che identifica la finestra (header principale). Un blocco OCR privo
di titolo principale è una violazione.

### Formato output obbligatorio

```
## Checklist Accessibilità NVDA: [nome_file]

| Check | Stato | Dettaglio |
|-------|-------|-----------|
| 1 — Font size >= 18 | ✅ OK | — |
| 2 — Header sezioni gialli | ❌ CRITICO | text_label riga 45: manca colore giallo |
| 3 — Tooltip bottoni | ✅ OK | — |
| 4 — Icone con tooltip | ⚠️ ATTENZIONE | icon riga 78: tooltip presente ma vuoto |
| 5 — Dati numerici contestuali | ✅ OK | — |
| 6 — Fallback liste vuote | ✅ OK | — |
| 7 — Visibilità corretta | ✅ OK | — |
| 8 — Titolo finestra presente | ✅ OK | — |

**Verdetto**: PASS / PASS CON RISERVE / FAIL
**Blocchi critici**: N
**Avvertenze**: N
```

### Agenti che usano questa skill
- **Revisore Accessibilità**: invoca come primo passo. Il suo report finale
  si basa sull'output di questa skill, arricchito da valutazioni qualitative
  (es. ordine lettura, coerenza informativa) che la skill non può valutare
  automaticamente.
- **Auditore Finale**: invoca nella sezione "Qualità OCR" della checklist.
  Un verdetto FAIL è automaticamente un blocco CRITICO nell'audit.

---

## 10. Fase 3b — Skill: `dual-mode-template-generator`

### File da creare
`.github/copilot-skills/dual-mode-template-generator.skill.md`

### Frontmatter YAML
```yaml
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
```

### Corpo della skill (logica da eseguire)

Genera il codice Jomini seguendo ESATTAMENTE il pattern canonical in
`.github/resources/dual_mode_pattern_canonical.md`.

**Regole di generazione obbligatorie:**

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

**Struttura fissa del container OCR generato:**
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

**Struttura fissa del container vanilla generato:**
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

**La skill NON inventa mai il contenuto vanilla.** Il blocco vanilla è sempre
vuoto con il commento di istruzione. Questo è intenzionale e non va cambiato.

**La skill NON aggiunge binding reali.** Usa sempre placeholder espliciti del
tipo `[PlaceholderBinding]` con commento `# Sostituire con binding verificato`.

### Formato output obbligatorio

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

### Agenti che usano questa skill
- **Implementatore Patch**: invoca al passo 4 del workflow ("Costruisci il
  container OCR") passando le sezioni dal progetto dell'Architetto. Usa l'output
  come punto di partenza, sostituisce i placeholder con binding reali.
- **Architetto Dual-Mode**: può invocarla in modalità bozza rapida per
  visualizzare la struttura proposta prima di passarla all'Implementatore.

---

## 11. Fase 4 — Aggiornamento Agent File e Test Integrazione

### Ordine di aggiornamento

Aggiorna gli agent file SOLO dopo che tutte e 6 le skills sono state create e
testate su `window_faith.gui`. Il test è superato quando:
- `deprecated-pattern-scanner` non trova falsi positivi né falsi negativi
- `scope-whitelist-check` classifica correttamente binding noti e sconosciuti
- `tri-repo-diff` produce un report coerente con la struttura reale dei tre file
- `vanilla-fidelity-check` emette PASS su `window_faith.gui` (già convertito)
- `accessibility-checklist-runner` emette PASS su `window_faith.gui`
- `dual-mode-template-generator` genera uno scheletro valido per `window_faith`

### Modifiche per ciascun agent file

**`analista-tri-repo.agent.md`**: sostituire la sezione "Metodologia" (passi 1-6)
con:
```markdown
## Metodologia
1. Invoca `#tri-repo-diff` con il nome della finestra da analizzare.
2. Il report prodotto dalla skill è l'output di questa analisi.
3. Arricchisci il report con osservazioni qualitative se necessario.
4. Suggerisci handoff a Architetto Dual-Mode.
```

**`architetto-dual-mode.agent.md`**: aggiungere in "Riferimenti obbligatori":
```
- Skill scope: #scope-whitelist-check — invocare per ogni binding usato nel progetto
- Skill bozza: #dual-mode-template-generator — usare per validare struttura proposta
```

**`implementatore-patch.agent.md`**: aggiungere come PASSO 0 del workflow:
```
0. Invoca #deprecated-pattern-scanner sul file attuale prima di qualsiasi modifica.
```
Aggiungere come PASSO 4b:
```
4b. Invoca #dual-mode-template-generator con le sezioni del progetto Architetto.
```
Aggiungere come PASSO 7 (dopo verifica nomi duplicati):
```
7. Invoca #scope-whitelist-check su tutti i binding usati nel container OCR.
   Aggiungere i binding ASSENTI alla whitelist prima di procedere.
8. Invoca #deprecated-pattern-scanner sul file modificato.
   Se verdetto != PULITO, correggere prima di passare ai revisori.
```

**`revisore-accessibilita.agent.md`**: aggiungere come PRIMO PASSO:
```
## Passo 1 — Verifica Automatica
Invoca `#accessibility-checklist-runner` sul file da verificare.
Il report della skill copre i check meccanici. La tua analisi qualitativa
(ordine lettura, coerenza informativa, usabilità NVDA) integra ma non
sostituisce il report automatico.
```

**`revisore-vanilla.agent.md`**: sostituire la sezione "Metodologia" (passi 1-5)
con:
```markdown
## Metodologia
1. Invoca `#vanilla-fidelity-check` con il percorso del file patch.
2. Il verdetto della skill è il tuo verdetto di base.
3. Se FAIL: riporta i bug esattamente come identificati dalla skill.
4. Se PASS: aggiungi nota di conferma e suggerisci handoff ad Auditore Finale.
```

**`auditore-finale.agent.md`**: aggiornare la checklist sostituendo le sezioni
con riferimenti alle skill:
```markdown
### Struttura e Pattern
- [ ] #deprecated-pattern-scanner → verdetto PULITO

### Qualità OCR
- [ ] #accessibility-checklist-runner → verdetto PASS o PASS CON RISERVE

### Fedeltà Vanilla
- [ ] #vanilla-fidelity-check → verdetto PASS

### Scope e Binding
- [ ] #scope-whitelist-check → nessun binding ASSENTE o DA VERIFICARE

### Completezza (verifica manuale)
- [ ] TUTTE le informazioni del vanilla rappresentate nell'OCR
- [ ] Nessuna funzionalità vanilla inaccessibile in modalità OCR
- [ ] Tab multipli: tutti con il loro blocco OCR
```

---

## 12. Comportamento Automatico del Framework dopo l'Integrazione

Dopo che le skills sono integrate negli agent file, il framework si comporta
così in risposta alle richieste dell'utente:

| Richiesta utente | Agente attivato | Skills invocate automaticamente |
|-----------------|-----------------|--------------------------------|
| "Analizza window_X" | Analista Tri-Repo | #tri-repo-diff |
| "Converti window_X in dual mode" | Architetto → Implementatore | #scope-whitelist-check, #dual-mode-template-generator, #deprecated-pattern-scanner |
| "Verifica accessibilità di window_X" | Revisore Accessibilità | #accessibility-checklist-runner |
| "Verifica fedeltà vanilla di window_X" | Revisore Vanilla | #vanilla-fidelity-check |
| "Audit pre-commit di window_X" | Auditore Finale | #deprecated-pattern-scanner, #accessibility-checklist-runner, #vanilla-fidelity-check, #scope-whitelist-check |
| "C'è qualcosa di deprecato in window_X?" | (diretto) | #deprecated-pattern-scanner |
| "Questo binding è in whitelist?" | (diretto) | #scope-whitelist-check |

L'utente non deve invocare le skills manualmente: il framework le attiva in
automatico attraverso il workflow degli agenti. Le skills possono anche essere
invocate direttamente dall'utente con `#nome-skill` per operazioni puntuali
senza passare dall'agente.

---

## 13. Regole di Manutenzione delle Skills

1. **Versionamento**: ogni modifica a una skill deve essere riflessa in una
   nota nel corpo della skill con data e motivo della modifica.
2. **Aggiornamento whitelist**: se `scope-whitelist-check` viene aggiornata,
   verificare che la logica di lookup sia ancora compatibile con il formato
   attuale di `jomini_scope_whitelist.md`.
3. **Aggiornamento pattern**: se vengono scoperti nuovi pattern deprecati o
   vietati in CK3 1.17.1, aggiungerli PRIMA in `deprecated-pattern-scanner`
   e poi documentarli in `copilot-instructions.md`.
4. **Nessuna skill inventa regole**: le skills applicano regole esistenti
   definite in `copilot-instructions.md` e `.github/resources/`. Se una regola
   non è documentata in quei file, non va applicata nelle skills.
5. **Test su file convertiti prima di ogni modifica a una skill**: usare
   `window_faith.gui` o `window_council.gui` come file di riferimento per
   verificare che le modifiche non introducano falsi positivi.

---

*Fine del piano di implementazione.*
*Documento creato: 2026-03-11*
*Autore: Analisi framework e piano redatto con Perplexity AI su richiesta di Nemex81*
