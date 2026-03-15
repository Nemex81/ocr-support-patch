# TODO — Aggiornamento Framework (Pattern Type-Separated v1.1)

> **Regola inderogabile:** aggiornare questo file spuntando le checkbox al termine di ogni fase
> completata, prima di passare alla fase successiva. Mantenerlo sempre sincronizzato con lo
> stato reale dell'implementazione.
>
> Branch di lavoro: `experiment/dual-mode-type-separation`
> Piano completo di riferimento: `DUAL_MODE_TYPE_SEPARATION_PLAN.md`
> Ultimo aggiornamento: 2026-03-14

---

## Legenda

- `[ ]` — da fare
- `[x]` — completato
- `⚠️` — richiede verifica manuale o conferma del modder
- `GATE` — checkpoint bloccante: la fase successiva non inizia se il gate non è superato

---

## FASE 0 — Prerequisiti: path e confini (dipendenza zero — iniziare qui)

Aggiornare le fondamenta: dove vivono i file, quali percorsi sono scrivibili.
Nessuna altra fase può referenziare `gui/vanilla/` prima che questa sia completa.

- [x] **0.1** `tools/config.py` — aggiungere costante `VANILLA_TYPES_GUI`
  - Aggiungere dopo la riga `PATCH_GUI = ...`:
    `VANILLA_TYPES_GUI = PATCH_ROOT / "ocr_support_compatibility_pach" / "gui" / "vanilla"`
  - Aggiungere la costante al blocco `__main__` per il report path
  - Nessuna dipendenza da altri file

- [x] **0.2** `.github/instructions/patch-boundaries.instructions.md` — estendere percorsi scrivibili
  - Aggiungere riga alla tabella "Percorsi Scrivibili":
    `ocr_support_compatibility_pach/gui/vanilla/` | File type vanilla separati — pattern v1.1
  - Condizione: solo per finestre che adottano il pattern type-separated
  - ⚠️ Richiede conferma esplicita del modder (file è in `.github/instructions/` — percorso
    normalmente vietato in scrittura senza conferma)

- [x] **0.3** `.github/resources/domain_boundaries.md` — registrare il nuovo path
  - Aggiungere `ocr_support_compatibility_pach/gui/vanilla/` nella sezione `mod`
  - Indicare context condizionale: "solo pattern type-separated"
  - Verificare che il file esista; se assente, valutare se crearlo o saltare

> **GATE 0:** I passi 0.1–0.3 devono essere completati prima di avviare la Fase 1.
> Verificare che `config.py` importi correttamente il nuovo path con `python tools/config.py`.

---

## FASE 1 — Pattern canonical e documenti core

Definire il template ufficiale e le regole di classificazione. Questi file sono la fonte
di verità che tutti gli altri file (istruzioni, agenti, skills) devono referenziare.

- [x] **1.1** `.github/resources/dual_mode_pattern_canonical.md` — append template v1.1
  - Aggiungere sezione separata `## Pattern v1.1 — Type-Separated Vanilla` dopo il contenuto attuale
  - Includere: template completo wrapper + type separato con naming ufficiale
  - Includere: regola "cosa resta nel wrapper / cosa va nel type"
  - Includere: checklist dedicata al pattern type-separated
  - Naming ufficiale da usare:
    - Folder: `ocr_support_compatibility_pach/gui/vanilla/`
    - Type name: `{finestra_senza_window}_patch_vanilla`
    - File name: `{finestra_senza_window}_patch_vanilla.gui`
    - Blocco types: `types OCR_PATCH_VANILLA { }`
  - Guard visibilità nel type: `visible = "[GetVariableSystem.Exists('ocr')]"` (esplicita, non `using = vanilla`)

- [x] **1.2** `.github/resources/conversion-patterns.md` — append variante type-separated
  - Aggiungere sezione `## Variante V — Type-Separated Vanilla (Pattern v1.1)` dopo i pattern A/B/C/D
  - Criteri di scelta: quando usare inline vs separato
    - Separato consigliato: file > 2000 righe, branch vanilla > 40% del totale
    - Separato sconsigliato: file < 500 righe, beneficio minimo
  - Indicare per ogni pattern A/B/C/D se la variante separata è compatibile e il livello di rischio
  - Casi ad alto rischio da documentare: hud.gui, window_army.gui, finestre pattern D

> **GATE 1:** I passi 1.1–1.2 devono essere approvati (lettura) dal modder prima di Fase 2.
> Template canonical = fonte di verità: se è errato, tutto il resto eredita l'errore.

---

## FASE 2 — Istruzioni operative

Aggiornare le istruzioni che guidano il lavoro quotidiano. Dipendono dal pattern canonical (Fase 1).

  - [x] **2.1** `.github/copilot-instructions.md` — aggiungere sezione architettura type-separated
  - Aggiungere nuova sezione `## Architettura Dual Mode — Pattern Type-Separated (v1.1+)` dopo "Principi Irrinunciabili"
  - Contenuto: descrizione del pattern, quando usarlo, naming convention ufficiale, folder `gui/vanilla/`
  - Aggiornare tabella `Struttura Repository` aggiungendo riga per `gui/vanilla/`
  - Non modificare la sezione "Principi Irrinunciabili" esistente
  - ⚠️ File in `.github/` — richiede conferma dal modder

  - [x] **2.2** `.github/instructions/workflow-nuova-finestra.instructions.md` — estendere per pattern separato
  - Aggiungere passo opzionale `3b` nel ramo "Pattern v1.1":
    `python tools/assemble_dualmode.py --window nome --mode X --separate-vanilla --dry-run`
  - Aggiornare CP1: se pattern separato, il modder approva DUE file (wrapper + type)
  - Aggiornare CP2: audit coppia wrapper+type
  - Aggiungere nota: "se il file vanilla type è assente, audit.py segnala ATTENZIONE non CRITICO"
  - ⚠️ File in `.github/instructions/` — richiede conferma dal modder

  - [x] **2.3** `.github/instructions/gui-jomini.instructions.md` — naming convention type-separated
  - Aggiungere sezione "Naming convention type-separated (Pattern v1.1)" alla checklist pre-commit
  - Regole da aggiungere: nome type `_patch_vanilla`, blocco `types OCR_PATCH_VANILLA {}`, guard visibilità esplicita
  - Aggiungere regola: il type separato NON deve contenere `state`, `widgetid`, `layer`, `attachto`
  - ⚠️ File in `.github/instructions/` — richiede conferma dal modder

  - [x] **2.4** `.github/resources/requirement-enforcement-matrix.md` *(se esiste)*
  - Aggiungere requisiti: coerenza naming type-separated, guard visibilità obbligatoria nel type,
    assenza di proprietà window-level nel type separato
  - Se il file non esiste, documentare il requisito in `dual_mode_pattern_canonical.md` invece

> **GATE 2:** Completion Fase 2 deve precedere qualsiasi modifica ai tool Python (Fase 3).
> Le istruzioni framework devono riflettere il comportamento atteso dai tool.

---

## FASE 3 — Tool Python

Aggiornare gli strumenti automatizzati. Dipendono dalla Fase 0 (path) e Fase 1 (pattern).
**Ogni tool va testato singolarmente con un dry-run prima di passare al successivo.**

- [ ] **3.1** `tools/assemble_dualmode.py` — aggiungere flag `--separate-vanilla`
  - [x] **3.1** `tools/assemble_dualmode.py` — aggiungere flag `--separate-vanilla`
  - Aggiungere argomento `--separate-vanilla` al parser argparse
  - Se attivo: output su DUE file invece di uno
    - File 1: `ocr_support_compatibility_pach/gui/{nome}.gui` (wrapper — OCR + istanziazione type)
    - File 2: `ocr_support_compatibility_pach/gui/vanilla/{nome_senza_window}_patch_vanilla.gui` (type)
  - Messaggio errore se `--separate-vanilla` usato senza `--dry-run` e la cartella `gui/vanilla/` non esiste:
    `ERRORE: cartella gui/vanilla/ non trovata. Crearla prima di procedere.`
  - Creare la cartella `gui/vanilla/` se `--dry-run` non attivo e cartella assente
  - Aggiornare help CLI con descrizione italiana
  - Accettazione: `--dry-run --separate-vanilla` stampa entrambi i file senza scriverli

- [ ] **3.2** `tools/gui_validator.py` — riconoscere pattern type-separated
  - [x] **3.2** `tools/gui_validator.py` — riconoscere pattern type-separated
  - Aggiungere rilevamento blocchi `types OCR_PATCH_VANILLA { }` come struttura valida
  - Non segnalare come errore i file contenenti solo `types ... { type ... = widget { ... } }`
  - Aggiungere errore `VISIBILITA_TYPE_SEPARATED_INCOHERENTE` se:
    - file in `gui/vanilla/` contiene type con `visible` assente o `visible = "[Not(...)]"` (OCR invece di vanilla)
  - Aggiungere warning `TYPE_SEPARATO_NO_NOME` se type manca di `name = "..."`
  - Accettazione: `--file gui/vanilla/decisions_patch_vanilla.gui` non produce falsi positivi

- [ ] **3.3** `tools/audit.py` — orchestrare audit coppia wrapper+type
  - [x] **3.3** `tools/audit.py` — orchestrare audit coppia wrapper+type
  - Aggiungere rilevamento automatico file type associato: cerca `gui/vanilla/{nome}_patch_vanilla.gui`
    quando analizza un wrapper che usa `{nome}_patch_vanilla = {}`
  - Se file type trovato: eseguire audit fidelità vanilla SUL FILE TYPE (non sul wrapper)
  - Produrre verdetto cumulativo: `wrapper OK + type OK = APPROVATO`
  - Se file type atteso ma assente: emettere `ATTENZIONE` (non critico) con messaggio:
    `ATTENZIONE: file vanilla type atteso non trovato: gui/vanilla/{nome}_patch_vanilla.gui`
  - Accettazione: `python tools/audit.py --window decisions` con coppia presente produce report unificato

> **GATE 3 (critico):** Prima di procedere alla migrazione di qualsiasi finestra (todo_dual_mode.md),
> eseguire dry-run completo con `interaction_interfere_in_war_notification.gui` come PoC.
> I trei tool devono produrre output corretto senza errori imprevisti.

---

## FASE 4 — Agenti e skills

Aggiornare gli agenti specializzati e le skills per gestire il pattern v1.1.
Dipendono da Fase 2 (istruzioni) e Fase 3 (tool).

- [ ] **4.1** `.github/agents/implementatore-patch.agent.md` — gestione due artefatti
  - [x] **4.1** `.github/agents/implementatore-patch.agent.md` — gestione due artefatti
  - Aggiungere regola: in modalità `--separate-vanilla`, scrivere entrambi i file
  - Specificare punto di scrittura consentito per file type: `ocr_support_compatibility_pach/gui/vanilla/`
  - Aggiungere chiarimento: non separare vanilla se file < 500 righe o se beneficio è minimo
  - ⚠️ File in `.github/agents/` — richiede conferma dal modder

- [ ] **4.2** `.github/agents/revisore-vanilla.agent.md` — fidelità vanilla su file type separato
  - [x] **4.2** `.github/agents/revisore-vanilla.agent.md` — fidelità vanilla su file type separato
  - Aggiornare le istruzioni di confronto: cercare il branch vanilla nel type file se wrapper non lo contiene inline
  - Aggiungere regola: il type file in `gui/vanilla/` è la sorgente del confronto vanilla, non il wrapper
  - ⚠️ File in `.github/agents/` — richiede conferma dal modder

- [ ] **4.3** `.github/agents/auditore-finale.agent.md` — audit file multipli per stessa finestra
  - [x] **4.3** `.github/agents/auditore-finale.agent.md` — audit file multipli per stessa finestra
  - Aggiornare checklist: includere verifica esistenza file type se finestra usa pattern separato
  - Aggiungere criterio BLOCKED: file type mancante quando wrapper lo referenzia
  - ⚠️ File in `.github/agents/` — richiede conferma dal modder

- [ ] **4.4** `.github/copilot-skills/vanilla-fidelity-check.skill.md` — supporto type separato
  - [x] **4.4** `.github/copilot-skills/vanilla-fidelity-check.skill.md` — supporto type separato
  - Aggiornare istruzioni per leggere il branch vanilla dal file type invece che dal container inline
  - Aggiungere logica: se `gui/vanilla/{nome}_patch_vanilla.gui` esiste, usare quello come sorgente vanilla
  - ⚠️ File in `.github/copilot-skills/` — richiede conferma dal modder

- [ ] **4.5** `.github/copilot-skills/dual-mode-template-generator.skill.md` — output due file
  - [x] **4.5** `.github/copilot-skills/dual-mode-template-generator.skill.md` — output due file
  - Aggiornare per generare due template: wrapper + type separato
  - Includere naming convention aggiornata: `types OCR_PATCH_VANILLA`, `_patch_vanilla`
  - ⚠️ File in `.github/copilot-skills/` — richiede conferma dal modder

> **GATE 4:** Tutti gli agenti e le skills aggiornati devono essere verificati su un caso reale
> (PoC già completato in Fase 3) prima di usarli per nuove conversioni.

---

## FASE 5 — Documentazione finale

Aggiornare i documenti visibili all'utente e il registro conversioni.

- [ ] **5.1** `.github/instructions/gui-conversion-progress.instructions.md` — colonna pattern
  - [x] **5.1** `.github/instructions/gui-conversion-progress.instructions.md` — colonna pattern
  - Aggiungere colonna `Arch.` alle tabelle delle finestre convertite
  - Valori: `inline` (pattern attuale) o `sep` (type-separated v1.1)
  - Tutte le voci esistenti: `inline` (default retrocompatibile)
  - ⚠️ File in `.github/instructions/` — richiede conferma dal modder

- [ ] **5.2** `README.md` (root repo) — struttura repository aggiornata
  - [x] **5.2** `README.md` (root repo) — struttura repository aggiornata
  - Aggiornare sezione struttura directory con `gui/vanilla/`
  - Aggiungere brevissima spiegazione del ruolo dei file type separati
  - Non rimuovere contenuto esistente — solo aggiungere

---

## Stato Complessivo

| Fase | Descrizione | Completata |
|------|-------------|-----------|
| Fase 0 | Prerequisiti: path e confini | [x] |
| Fase 1 | Pattern canonical e documenti core | [x] |
| Fase 2 | Istruzioni operative | [x] |
| Fase 3 | Tool Python | [ ] |
| Fase 3 | Tool Python | [x] |
| Fase 4 | Agenti e skills | [ ] |
| Fase 4 | Agenti e skills | [x] |
| Fase 5 | Documentazione finale | [ ] |
| Fase 5 | Documentazione finale | [x] |
| Fase 2 | Istruzioni operative | [x] |
| Fase 3 | Tool Python | [x] |
| Fase 4 | Agenti e skills | [x] |
| Fase 5 | Documentazione finale | [x] |

---

> **Nota operativa:** Le fasi con file in `.github/instructions/`, `.github/agents/` e
> `.github/copilot-skills/` richiedono conferma esplicita del modder prima della scrittura,
> secondo le regole di `patch-boundaries.instructions.md`. Nella sessione corrente, il modder
> ha dato conferma globale per l'intera sessione di framework update. Registrare qui se la
> conferma è valida: ⚠️ **CONFERMA GLOBALE DA RICEVERE O CONFERMARE PRIMA DI FASE 2+**
