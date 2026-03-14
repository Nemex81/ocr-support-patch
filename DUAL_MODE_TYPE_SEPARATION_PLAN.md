# Dual Mode Type Separation Plan

Data: 2026-03-14
Stato: analisi e piano, nessuna implementazione eseguita
Ambito: OCR Support Patch CK3 1.17.1

## Obiettivo

Documentare in modo completo il piano per introdurre, come possibile standard architetturale,
la separazione del branch vanilla del dual-mode in type definiti in file `.gui` separati,
mantenendo il branch OCR nel file principale della finestra.

Il documento copre:

- convalida tecnica del pattern Jomini
- applicabilita del pattern alle finestre attuali della patch
- piano di implementazione del nuovo standard
- aggiornamenti necessari al framework di sviluppo
- rischi Jomini-specifici e casi limite da gestire prima di un rollout esteso

## Contesto sintetico

OCR Support Patch implementa un sistema dual-mode per CK3 1.17.1:

- modalita OCR: variabile `ocr` assente, layout testuale per screen reader
- modalita vanilla: variabile `ocr` presente, layout grafico Paradox originale

Nella patch attuale, il pattern dominante e:

- file `.gui` singolo per finestra
- container OCR inline nel file principale
- container vanilla inline nello stesso file principale

L'ipotesi da validare e la seguente:

1. definire il layout vanilla come `type` in un file separato
2. istanziare il type con `nome_type = {}` nel file wrapper principale
3. usare la visibilita condizionale per attivare il branch vanilla solo quando `ocr` esiste

## Parte 1 - Convalida tecnica del pattern Jomini

## Verdetto

CONFERMATO, con precisazioni operative importanti.

Il pattern e valido in CK3 1.17.1 e risulta gia usato da Agamidae in almeno una forma pienamente rilevante per il caso d'uso proposto.

## Evidenze raccolte

### 1. Pattern tipo separato + istanziazione vuota

Nel repository CK3-OCR di Agamidae sono presenti due meccanismi distinti:

### 1.a Type vuoti come placeholder

Nel file `OCR-Support/gui/vanilla/00_temp_vanilla.gui` esiste un blocco:

```jomini
types VANILLA {
  type character_old = window {}
  type old_hud = window {}
  ...
}
```

Questi type sono dichiarati ma hanno corpo vuoto. La loro istanziazione, ad esempio `character_old = {}` dentro `window_character.gui`, e sintatticamente valida ma non renderizza contenuto UI. Questo pattern funziona come placeholder strutturale.

### 1.b Type pieni in file separati

Nel file `OCR-Support/gui/vanilla/window_the_great_steppe.gui` Agamidae definisce invece un type pieno:

```jomini
types VANILLA {
    type window_the_great_steppe = window {
        using = vanilla
        ...
    }
}
```

E nel file principale `OCR-Support/gui/window_the_great_steppe.gui` lo istanzia con:

```jomini
window_the_great_steppe = {}
```

Questo dimostra direttamente che il pattern seguente e valido:

- type definito in file `.gui` separato
- type con corpo pieno
- istanziazione con `nome_type = {}` in un altro file

## Risposte puntuali alla teoria iniziale

### a) Il pattern `type X = widget/window { ... }` in file separato + chiamata `X = {}` in un'altra window e sintassi Jomini valida?

Si.

Evidenza forte: `window_the_great_steppe` in Agamidae.

Conclusione operativa: il motore Jomini di CK3 1.17.1 accetta type separati caricati da altri file `.gui` e ne consente l'istanziazione in un wrapper differente.

### b) Esistono vincoli di scope o datacontext che impediscono a un type esterno di accedere ai datacontext della window padre?

Non emergono vincoli bloccanti.

Il type istanziato eredita il contesto del punto in cui viene inserito. In pratica:

- i `datacontext` definiti sulla window padre restano disponibili
- i figli del type possono usarli come qualsiasi altro widget inline

Quindi la separazione del layout vanilla in type esterno non rompe, di per se, l'accesso ai datacontext del wrapper.

### c) Ci sono collisioni di nomi da evitare con tipi gia definiti da Agamidae o dal vanilla?

Si, il rischio esiste se si usano convenzioni generiche.

Agamidae usa numerosi nomi con suffisso `_old` e alcuni con suffisso `_vanilla`.
Per evitare collisioni, la patch non deve riusare:

- `_old`
- `_vanilla` puro senza namespace aggiuntivo

Conclusione: serve una naming convention univoca della patch.

## Dettaglio tecnico importante: `using = vanilla`

Nel file `OCR-Support/gui/preload/00_types_OCR.gui` Agamidae definisce:

```jomini
template vanilla {
    visible = "[GetVariableSystem.Exists('ocr')]"
}
template ocr {
    visible = "[Not(GetVariableSystem.Exists('ocr'))]"
}
```

Questo significa che un type separato puo inglobare gia al suo interno la regola di visibilita del branch vanilla.

Per la patch, tuttavia, e preferibile mantenere la visibilita esplicita e leggibile anche senza dipendere da un template esterno di Agamidae, salvo decisione architetturale esplicita.

## Conclusione tecnica della Parte 1

Il pattern e valido.

Non e una teoria speculativa: esiste un precedente concreto e funzionante nel repository upstream.

La vera questione non e se il pattern funzioni in Jomini, ma come introdurlo nella patch senza:

- perdere fedelta vanilla
- rompere gli strumenti del framework
- complicare audit e manutenzione

## Parte 2 - Applicabilita del pattern alle finestre attuali della patch

## Stato attuale della patch

La patch usa oggi soprattutto questo schema:

```jomini
window = {
    ...

    widget = {
        visible = "[Not(GetVariableSystem.Exists('ocr'))]"
        ... contenuto OCR ...
    }

    widget = {
        visible = "[GetVariableSystem.Exists('ocr')]"
        ... contenuto vanilla inline ...
    }
}
```

Quindi:

- il branch OCR e inline
- il branch vanilla e inline
- l'intero dual-mode vive in un solo file

## Impatto strutturale atteso della separazione vanilla

Stima qualitativa basata sui file attuali e sulle dimensioni vanilla corrispondenti.

| File | Righe patch | Righe vanilla note/stimate | Applicabilita | Note |
|------|-------------|----------------------------|---------------|------|
| window_county_view.gui | 8718 | ~3487 | Si | beneficio alto |
| window_army.gui | 8290 | ~2240 | Si, con cautela | script specializzato da aggiornare |
| window_character.gui | 7385 | ~4975 | Si | massimo beneficio su leggibilita |
| hud.gui | 7167 | ~6810 | Si | beneficio massimo ma rischio alto |
| window_culture.gui | 3832 | ~1748 | Si | pattern complesso ma compatibile |
| window_dynasty_house.gui | 3635 | ~2476 | Si | beneficio alto |
| window_intrigue.gui | 3292 | stima media | Si | nessun blocco noto |
| window_military.gui | 3182 | ~3595 vanilla di riferimento | Si | da verificare rapporto reale post-merge |
| window_combat.gui | 3160 | ~2413 | Si | types gia presenti, ma gestibile |
| window_inventory.gui | 2906 | stima media | Si | nessun blocco noto |
| window_my_realm.gui | 2858 | stima media | Si | file adatto a migrazione precoce |
| window_faith.gui | 2776 | ~1522 | Si | multi-window, richiede disciplina |
| window_character_lifestyle.gui | 2558 | stima media | Si | pattern C compatibile |
| window_council.gui | 2389 | ~1923 | Si | buon candidato di stress test |
| window_activity.gui | 1676 | stima media | Si | con attenzione ai tab child |
| window_factions.gui | 1467 | stima media | Si | pattern B compatibile |
| window_court.gui | 1266 | stima media | Si | fattibile |
| window_activity_list.gui | 1197 | stima media | Si | fattibile |
| window_decisions.gui | 1041 | stima media | Si | ottimo candidato PoC reale |
| interaction_blackmail.gui | 456 | stima bassa | Si, beneficio modesto | non prioritaria |
| interaction_menu_window.gui | 383 | stima bassa | Si, beneficio modesto | non prioritaria |
| interaction_interfere_in_war_notification.gui | 186 | stima bassa | Si, beneficio minimo | ideale solo come PoC tecnico |

## Valutazione per categoria di finestra

### Pattern A - Simple Swap

Finestre semplici come `window_decisions.gui`, `window_my_realm.gui`, `window_intrigue.gui` sono facilmente migrabili.

Motivo:

- un solo wrapper principale
- pochi livelli di sub-window
- separazione vanilla poco rischiosa

### Pattern B - Tabs + SubWindows

Finestre come `window_council.gui`, `window_activity.gui`, `window_factions.gui` restano tecnicamente compatibili, ma ogni sub-window dual-mode potrebbe richiedere:

- un proprio type vanilla dedicato
- oppure un file type che contenga piu type correlati

Il pattern e applicabile ma richiede una convenzione rigorosa.

### Pattern C - Complex Layout

Finestre come `window_character_lifestyle.gui`, `window_decisions.gui`, `window_court.gui` sono buone candidate.

La separazione del branch vanilla alleggerisce molto il file wrapper e rende piu leggibile il blocco OCR, che e il vero oggetto di manutenzione frequente.

### Pattern D - Bottom-Up Multi-Window

Finestre come `window_county_view.gui`, `window_faith.gui`, `window_culture.gui` restano applicabili ma sono ad alto rischio operativo.

Qui il pattern type-separato non va introdotto come primo test esteso. Serve prima validazione del meccanismo su file piu controllabili.

## Vincoli strutturali rilevati

### 1. States e proprieta window-level

Gli `state`, `layer`, `movable`, `allow_outside`, `widgetid`, `attachto` e proprieta analoghe devono restare nel file wrapper principale se appartengono semanticamente alla window.

La separazione riguarda soprattutto il contenuto del branch vanilla, non la definizione completa della window host.

### 2. Tipi condivisi fra OCR e vanilla

Se una finestra usa types comuni ai due rami, quei types non vanno necessariamente separati.

Regola: separare solo cio che diverge davvero.

### 3. Dimensione del beneficio

Il beneficio e maggiore nelle finestre dove il branch vanilla occupa gran parte del file. In queste finestre la separazione migliora:

- leggibilita
- manutenzione OCR
- review diff
- audit visivo del wrapper

## Conclusione della Parte 2

Il pattern e tecnicamente applicabile alla quasi totalita delle finestre gia convertite nella patch.

Non tutte le finestre hanno pero la stessa convenienza di migrazione. Serve un rollout graduale.

## Parte 3 - Piano di implementazione proposto

## Obiettivo del rollout

Introdurre un nuovo standard architetturale facoltativo o preferenziale per le finestre dual-mode, in cui:

- il file principale contiene wrapper, states, datacontext e branch OCR
- il branch vanilla vive in uno o piu type definiti in file separati

## 3.a Struttura di cartelle proposta

Proposta principale:

```text
ocr_support_compatibility_pach/
  gui/
    window_character.gui
    window_council.gui
    ...
    vanilla_types/
      character_patch_vanilla.gui
      council_patch_vanilla.gui
      decisions_patch_vanilla.gui
      ...
```

### Motivazioni

- separa chiaramente wrapper e branch vanilla
- evita di mescolare file runtime principali con file type di supporto
- consente naming stabile e prevedibile
- rende immediata la ricerca dei file vanilla separati

### Nota critica

Prima del rollout, va verificato in-game che CK3 carichi senza problemi i `.gui` della sottocartella `gui/vanilla_types/` nella patch.

Se questa ipotesi fallisse, fallback semplice:

- mantenere i file type nella cartella `ocr_support_compatibility_pach/gui/` principale

## 3.b Naming convention proposta

## Principi

- nessuna collisione con Agamidae
- nessuna collisione con eventuali type vanilla o di altre mod
- naming grep-friendly e immediato

## Convenzione consigliata

### Nome type

`{finestra_senza_window}_patch_vanilla`

Esempi:

- `character_patch_vanilla`
- `council_patch_vanilla`
- `decisions_patch_vanilla`
- `county_view_patch_vanilla`

### Nome file

`{finestra_senza_window}_patch_vanilla.gui`

Esempi:

- `character_patch_vanilla.gui`
- `council_patch_vanilla.gui`

### Nome blocco types

`types OCR_PATCH_VANILLA { ... }`

Questo namespace e leggibile, descrittivo e distinto da `types VANILLA` usato da Agamidae.

## 3.c Template standard del wrapper dual-mode

## Variante consigliata: type `widget`

File principale:

```jomini
window = {
    name = "character_window"
    widgetid = "character_window"
    datacontext = "[GetVariableSystem]"
    datacontext = "[CharacterWindow.GetCharacter]"
    movable = no
    allow_outside = yes

    state = {
        name = _show
        ...
    }

    state = {
        name = _hide
        ...
    }

    widget = {
        name = "ocr_character_container"
        visible = "[Not(GetVariableSystem.Exists('ocr'))]"
        ... contenuto OCR ...
    }

    character_patch_vanilla = {}
}
```

File separato:

```jomini
types OCR_PATCH_VANILLA {
    type character_patch_vanilla = widget {
        name = "vanilla_character_container"
        visible = "[GetVariableSystem.Exists('ocr')]"

        using = Window_Size_Sidebar
        using = Window_Background_Sidebar

        vbox = {
            using = Window_Margins_Sidebar
            ... contenuto vanilla fedele ...
        }
    }
}
```

## Perche `widget` come default

- evita il rischio di `window` annidata dentro `window`
- mantiene nel wrapper gli stati e il comportamento window-level
- limita il type separato al solo layout vanilla effettivo

## Eccezione possibile

Se una finestra dipende da proprieta tipiche di `window` dentro il branch vanilla separato, si puo valutare `type ... = window { ... }`, ma solo dopo verifica tecnica del caso specifico.

## 3.d Ordine di migrazione suggerito

## Fase PoC stretta

### 1. PoC tecnico minimo

`interaction_interfere_in_war_notification.gui`

Perche:

- file piccolo
- gia validato
- rischio contenuto
- perfetto per verificare caricamento file separato e comportamento base

### 2. PoC realistico semplice

`window_decisions.gui`

Perche:

- dimensione gestibile
- wrapper semplice
- buon compromesso tra realismo e rischio

### 3. Test di pattern B

`window_council.gui`

Perche:

- tabs e sub-windows
- testa la sostenibilita del pattern oltre il caso semplice

### 4. Test ad alto impatto

`window_character.gui`

Perche:

- enorme beneficio in leggibilita
- ottimo benchmark architetturale

### 5. Rollout graduale sulle altre finestre

Ordine consigliato:

- `window_my_realm.gui`
- `window_intrigue.gui`
- `window_court.gui`
- `window_character_lifestyle.gui`
- `window_combat.gui`
- `window_inventory.gui`
- `window_factions.gui`
- `window_activity.gui`
- `window_activity_list.gui`
- `window_faith.gui`
- `window_culture.gui`
- `window_county_view.gui`
- `hud.gui`
- `window_army.gui`

`hud.gui` e `window_army.gui` vanno lasciati tardi perche sono i casi operativamente piu delicati.

## 3.e Rischi e casi limite da documentare

## Rischi critici

### 1. Caricamento dei file `.gui` in sottocartella

Va verificato in-game che la cartella `gui/vanilla_types/` sia caricata correttamente dalla mod.

Questo e il primo gate reale. Se fallisce, il piano va adattato senza insistere su quella cartella.

### 2. Tooling non allineato

Gli script attuali presumono di lavorare principalmente su file `.gui` principali nella patch.

Se si introduce il pattern senza aggiornare il framework, si rischia di:

- perdere audit di fedelta vanilla
- non validare i type separati
- generare falsi positivi o falsi negativi nei report

## Rischi medi

### 3. Window-level properties nel type separato

Se si sposta troppo contenuto dal wrapper al type, si rischia di rompere:

- `state`
- `widgetid`
- `layer`
- `attachto`
- flusso show/hide

Regola: il type separato non deve assorbire responsabilita del wrapper senza una ragione precisa.

### 4. Multi-window complesse

Nelle finestre pattern B/D la gestione dei type separati va standardizzata bene o il costo di manutenzione puo peggiorare invece di migliorare.

### 5. Nomi widget interni duplicati

Anche se i rami sono mutuamente esclusivi via `visible`, vanno controllate eventuali collisioni di nomi significativi a runtime.

## Rischi bassi ma reali

### 6. Maggior numero di file

Il carico cognitivo passa da file enormi a piu file piu piccoli. E un vantaggio se le convenzioni sono forti, uno svantaggio se il naming e confuso.

### 7. Diff piu frammentati

Le modifiche si distribuiranno su due file invece di uno. E accettabile, ma va esplicitato nel workflow di review.

## Conclusione della Parte 3

L'introduzione del pattern e realistica, ma va fatta in modo incrementale e solo dopo allineamento del framework.

## Parte 4 - Aggiornamenti framework necessari

Questa parte documenta cosa va aggiornato nel framework se il pattern viene approvato come standard o standard alternativo supportato.

## 4.a `.github/copilot-instructions.md`

## Sezioni da aggiornare

- `Struttura Repository`
- `Principi Irrinunciabili`
- eventuale nuova sezione `Architettura Dual Mode`

## Cosa aggiungere/modificare

- descrizione del pattern type-separato come architettura supportata
- chiarimento su quando preferire inline vs file separato
- aggiunta della cartella `ocr_support_compatibility_pach/gui/vanilla_types/` se adottata
- naming convention ufficiale dei type vanilla della patch

## Dipendenze

- `dual_mode_pattern_canonical.md`
- `conversion-patterns.md`

## 4.b `.github/resources/dual_mode_pattern_canonical.md`

## Cosa aggiungere/modificare

- un template canonico completo del pattern wrapper + type separato
- regola chiara su cosa resta nel wrapper e cosa puo andare nel type
- esempi di naming ufficiali
- checklist dedicata al type separato

## Dipendenze

- `copilot-instructions.md`
- `gui-jomini.instructions.md`

## 4.c `.github/resources/conversion-patterns.md`

## Cosa aggiungere/modificare

- per i pattern A/B/C/D, descrivere la variante con vanilla separato
- indicare quando il pattern e consigliato e quando no
- documentare casi ad alto rischio come HUD e multi-window profonde

## Dipendenze

- `dual_mode_pattern_canonical.md`

## 4.d `.github/instructions/workflow-nuova-finestra.instructions.md`

## Cosa aggiungere/modificare

- un passo esplicito per la generazione del file type separato nel dry-run
- istruzioni CP1/CP2 aggiornate per includere sia wrapper sia file vanilla type
- aggiornamento comandi previsti per `assemble_dualmode.py`

## Dipendenze

- `assemble_dualmode.py`
- `audit.py`

## 4.e `.github/instructions/gui-jomini.instructions.md`

## Cosa aggiungere/modificare

- regole specifiche per file contenenti blocchi `types`
- convenzioni di naming per type separati
- checklist pre-commit estesa a wrapper + type separato

## Dipendenze

- `dual_mode_pattern_canonical.md`

## 4.f `.github/instructions/gui-conversion-progress.instructions.md`

## Cosa aggiungere/modificare

- eventuale nota o colonna che indichi se una finestra usa ancora vanilla inline o type separato
- stato di migrazione progressiva al nuovo standard

## Dipendenze

- nessuna forte, ma utile allineamento con workflow e audit

## 4.g `.github/agents/implementatore-patch.agent.md`

## Cosa aggiungere/modificare

- istruzioni per gestire due artefatti per finestra: wrapper e file vanilla type
- chiarimento sui casi in cui non si deve separare il vanilla
- verifica del punto di scrittura consentito per i file type

## Dipendenze

- workflow aggiornato
- script di assemblaggio

## 4.h `.github/agents/revisore-vanilla.agent.md`

## Cosa aggiungere/modificare

- revisione della fedelta vanilla spostata dal container inline al file type separato
- regole per confrontare correttamente contenuto wrapper e contenuto type

## Dipendenze

- `audit.py`
- eventuale skill `vanilla-fidelity-check`

## 4.i `.github/agents/auditore-finale.agent.md`

## Cosa aggiungere/modificare

- audit finale esteso ai type separati
- checklist aggiornata per file multipli associati alla stessa finestra

## Dipendenze

- `audit.py`

## 4.j `.github/copilot-skills/vanilla-fidelity-check.skill.md`

## Cosa aggiungere/modificare

- supporto alla lettura del vanilla type separato come sorgente di confronto
- chiarimento su come ricostruire logicamente il branch vanilla di una finestra quando non e piu inline

## Dipendenze

- `audit.py`

## 4.k `.github/copilot-skills/dual-mode-template-generator.skill.md`

## Cosa aggiungere/modificare

- generazione di due file invece di uno quando il pattern separato e richiesto
- naming convention coerente con lo standard approvato

## Dipendenze

- `dual_mode_pattern_canonical.md`

## 4.l `tools/assemble_dualmode.py`

## Cosa aggiungere/modificare

- nuovo flag, ad esempio `--separated-vanilla` o equivalente
- generazione del wrapper principale senza container vanilla inline
- generazione del file `vanilla_types/..._patch_vanilla.gui`
- logica per estrarre dal vanilla solo la porzione corretta da incapsulare nel type

## Dipendenze

- `config.py`
- eventuali helper nuovi per path e naming

## 4.m `tools/audit.py`

## Cosa aggiungere/modificare

- rilevamento automatico del file type associato al wrapper
- audit di fedelta vanilla sul type separato
- reporting che unisca i risultati di wrapper e type

## Dipendenze

- `config.py`
- `gui_validator.py`

## 4.n `tools/gui_validator.py`

## Cosa aggiungere/modificare

- validazione dei file in `vanilla_types/`
- supporto esplicito a blocchi `types ... {}`
- controlli coerenti su `visible`, struttura e integrita dei type

## Dipendenze

- nessuna forte, ma allineamento con canonical pattern

## 4.o `tools/config.py`

## Cosa aggiungere/modificare

- costante dedicata al path dei file vanilla type separati, se la cartella viene adottata

## Dipendenze

- `assemble_dualmode.py`
- `audit.py`

## 4.p `README.md` root

## Cosa aggiungere/modificare

- sezione aggiornata sulla struttura del repository
- spiegazione del ruolo dei file type separati
- chiarimento che il framework puo ora generare wrapper + type dedicati

## Dipendenze

- `copilot-instructions.md`

## 4.q `patch-boundaries.instructions.md`

## Cosa aggiungere/modificare

- se il pattern viene adottato, il percorso scrivibile va esteso esplicitamente per includere anche `ocr_support_compatibility_pach/gui/vanilla_types/`

## Dipendenze

- workflow operativo

## Parte 5 - Raccomandazione finale

## Verdetto complessivo

Il pattern e tecnicamente valido e puo portare un miglioramento concreto nella manutenibilita della patch, soprattutto per le finestre piu grandi.

## Raccomandazione pratica

Non introdurlo subito come obbligo globale.

Ordine consigliato:

1. validare il caricamento di file type separati con un PoC piccolo
2. aggiornare il framework minimo necessario
3. migrare una finestra reale semplice
4. solo dopo, decidere se renderlo standard preferenziale oppure opzione supportata

## Decisione strategica consigliata

Adottare il pattern come:

- standard consigliato per file grandi o ad alta complessita
- opzione non obbligatoria per file piccoli dove il beneficio e minimo

## Gate da non saltare

Prima di dichiarare il pattern pronto per produzione, devono essere confermati tutti i punti seguenti:

- CK3 carica correttamente i `.gui` type-separati nel path scelto
- `assemble_dualmode.py` sa generare correttamente wrapper + type
- `audit.py` sa verificare fedelta e struttura del nuovo modello
- `gui_validator.py` non produce falsi esiti sui file type
- il workflow CP1/CP2 resta leggibile per il modder

## Sintesi finale in una riga

La teoria e confermata; il vero lavoro non e dimostrare che Jomini lo supporta, ma aggiornare in modo disciplinato il framework perche questo pattern diventi sicuro, auditabile e mantenibile nella patch.