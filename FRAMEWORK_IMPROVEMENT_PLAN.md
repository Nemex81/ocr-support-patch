## Plan: Hardening Framework Review Gate

Documento operativo di tracciabilita' per la revisione concreta del framework. Durante l'implementazione ogni fase completata dovra' essere spuntata, e lo stesso vale per ogni punto interno alla fase, cosi' il documento restera' aggiornato in tempo reale e utilizzabile come fonte unica dello stato lavori.

## Indice Operativo

- [x] Fase 1 — Baseline e riallineamento stato
Breve descrizione: definire i criteri di successo, mappare requisiti e enforcement reali, e correggere il significato dello stato delle finestre.
Sezione: Fase 1

- [x] Fase 2 — Rafforzamento del gate automatico
Breve descrizione: trasformare audit.py nel gate centrale reale e aggiungere i controlli mancanti piu' importanti su fedelta' vanilla, copertura dual-mode e completezza OCR.
Sezione: Fase 2

- [x] Fase 3 — Governance ed enforcement operativo
Breve descrizione: rendere coerenti workflow, agenti, skill, nomenclatura degli esiti e meccanismi pratici di blocco o override.
Sezione: Fase 3

- [x] Fase 4 — Taratura empirica e chiusura
Breve descrizione: provare il framework rafforzato sulle finestre gia' convertite, classificare i finding e riallineare il registro stato con gli esiti reali.
Sezione: Fase 4

---

## Obiettivo

Portare il framework OCR-Patch da insieme di regole e skill advisory a sistema di review realmente affidabile. Il principio guida e' che ogni requisito dichiarato dal framework debba corrispondere a un controllo automatico vincolante oppure a una sign-off manuale esplicita e tracciabile.

---

## Fase 1 — Baseline e riallineamento stato

- [x] Definire i criteri di successo del framework
- [x] Distinguere formalmente tra lint strutturale, gate automatico e review manuale obbligatoria
- [x] Costruire la matrice requisito -> enforcement -> owner
- [x] Mappare i requisiti dichiarati in .github contro i controlli reali presenti in tools
- [x] Verificare il registro in .github/instructions/gui-conversion-progress.instructions.md contro i file reali in ocr_support_compatibility_pach/gui
- [x] Separare lo stato delle finestre in tre classi: convertita, convertita ma non validata, non convertita
- [x] Registrare i mismatch tra stato dichiarato ed evidenza reale emersa dagli audit

---

## Fase 2 — Rafforzamento del gate automatico

- [x] Trasformare tools/audit.py nel gate centrale reale
- [x] Integrare in audit.py un controllo automatico di fedelta' vanilla basato su tools/tri_diff.py o logica equivalente condivisa
- [x] Strutturare l'output di audit.py per categoria: structural, accessibility, whitelist, vanilla fidelity, coverage
- [x] Estendere tools/gui_validator.py con controllo di copertura dual-mode per file multi-window e sub-window
- [x] Aggiungere in gui_validator.py controlli minimi coerenti per header OCR
- [x] Aggiungere in gui_validator.py controlli su fallback di liste vuote quando il blocco OCR usa datamodel
- [x] Introdurre un controllo esplicito di completezza OCR
- [x] Verificare presenza di dati leggibili nel ramo OCR rispetto al ramo vanilla
- [x] Verificare presenza di azioni OCR equivalenti alle azioni vanilla
- [x] Verificare copertura di sezioni, tab e sottofinestre rilevanti
- [x] Tenere fuori dalla prima iterazione la semantica runtime profonda di Jomini, ma segnalarla come limite noto
- [ ] Introdurre un controllo esplicito di completezza OCR
- [ ] Verificare presenza di dati leggibili nel ramo OCR rispetto al ramo vanilla
- [ ] Verificare presenza di azioni OCR equivalenti alle azioni vanilla
- [ ] Verificare copertura di sezioni, tab e sottofinestre rilevanti
- [ ] Tenere fuori dalla prima iterazione la semantica runtime profonda di Jomini, ma segnalarla come limite noto

---

## Fase 3 — Governance ed enforcement operativo

- [x] Allineare workflow, agenti e skill al gate reale
- [x] Aggiornare il workflow dichiarato in .github/instructions/workflow-nuova-finestra.instructions.md
- [x] Aggiornare Auditore Finale per riflettere i controlli realmente vincolanti
- [x] Aggiornare Revisore Accessibilita' con i confini reali tra automazione e sign-off manuale
- [x] Aggiornare Revisore Vanilla con i confini reali tra diff automatico e parity interattiva manuale
- [x] Unificare la tassonomia degli esiti tra tool e agenti
- [x] Definire un lessico coerente per PULITO, CON AVVERTENZE, BLOCCANTE, PASS, FAIL, FEDELE, DA RIFARE
- [x] Scegliere il meccanismo minimo di enforcement operativo
- [x] Valutare comando unico locale di gate
- [ ] Valutare hook pre-commit
- [ ] Valutare status check di PR come step successivo
- [x] Definire la politica di override per gli esiti CON AVVERTENZE

---

## Fase 4 — Taratura empirica e chiusura

- [x] Rieseguire il gate rafforzato su tutte le finestre gia' convertite
- [x] Selezionare almeno un campione per i pattern A, B, C e D
- [x] Classificare ogni finding come vero positivo, falso positivo, falso negativo storico o requisito non coperto
- [x] Confrontare il delta rispetto al baseline attuale
- [x] Aggiornare il registro conversioni distinguendo conversione da validazione
- [ ] Valutare se aggiungere data ultimo audit e risultato sintetico per finestra
- [x] Verificare il criterio di chiusura del progetto framework
- [x] Confermare che ogni requisito critico abbia enforcement automatico o sign-off manuale tracciata
- [x] Confermare che il gate produca pochi falsi positivi sul corpus campione
- [x] Confermare che il registro stato sia coerente con l'audit reale

---

## File Rilevanti

- `.github/instructions/gui-jomini.instructions.md` — requisiti canonici del dual mode, checklist OCR/vanilla e parita' funzionale
- `.github/instructions/gui-jomini-scopes.instructions.md` — regole di whitelist e binding
- `.github/instructions/workflow-nuova-finestra.instructions.md` — workflow dichiarato e obblighi di aggiornamento stato
- `.github/instructions/gui-conversion-progress.instructions.md` — registro conversioni da riallineare con la realta'
- `.github/agents/auditore-finale.agent.md` — audit finale dichiarato e aspettative di gate
- `.github/agents/revisore-accessibilita.agent.md` — confine della review NVDA e punti oggi non automatizzati
- `.github/agents/revisore-vanilla.agent.md` — confine della review di fedelta' vanilla
- `.github/copilot-skills/accessibility-checklist-runner.skill.md` — checklist OCR automatizzabile e sue lacune
- `.github/copilot-skills/vanilla-fidelity-check.skill.md` — specifica di fedelta' vanilla da portare nel gate reale
- `tools/audit.py` — orchestratore da trasformare in gate centrale
- `tools/gui_validator.py` — controlli strutturali da estendere per multi-window e OCR coverage
- `tools/scope_extractor.py` — controllo whitelist da mantenere come gate ma senza sovraccaricarlo con semantica runtime
- `tools/tri_diff.py` — base migliore per automatizzare la vanilla fidelity
- `ocr_support_compatibility_pach/gui/` — corpus reale per taratura del framework sui pattern A/B/C/D

---

## Verifica

- [ ] Costruire una matrice requisito -> tool/skill/agent -> tipo enforcement -> blocking/non-blocking
- [ ] Eseguire il gate corrente su tutte le finestre segnate come gia' convertite e registrare il baseline per severita', categoria e file
- [ ] Dopo ogni iterazione del framework, rieseguire l'audit completo sul corpus convertito e confrontare il delta di veri positivi, falsi positivi e finestre BLOCCANTE
- [ ] Validare almeno un file per pattern A, B, C e D con review manuale comparata vanilla/OCR
- [ ] Verificare che il registro conversioni distingua esplicitamente conversione da validazione
- [ ] Se si adotta enforcement operativo, verificare che il gate fallisca davvero in presenza di CRITICO o BLOCCANTE senza dipendere dalla disciplina manuale

---

## Decisioni

- Incluso: correzione del framework, dei tool di audit, delle skill di review e della governance del processo
- Incluso: riallineamento del registro stato con la realta' delle finestre e con gli esiti audit
- Escluso dalla prima ondata: verifica runtime in-game completa e resolver semantico profondo dei binding Jomini; restano review manuali assistite
- Vincolo: le modifiche coprono percorsi fuori dalla patch boundary standard (.github e tools); l'utente ha autorizzato esplicitamente l'implementazione

---

## Raccomandazioni

- Partire da una v1 del gate con tre blocchi obbligatori soltanto: audit.py centralizzato, vanilla fidelity integrata, sub-window dual-mode coverage
- Introdurre due stati distinti per ogni finestra, Conversione e Validazione, invece di una sola colonna implicita di completamento
- Trattare l'accessibilita' NVDA reale come sign-off manuale obbligatorio, non come obiettivo di automazione completa nella prima iterazione
