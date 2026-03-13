# OCR Support Patch — Istruzioni Copilot

## Identità del Progetto

Mod CK3 (v1.17.1) — sistema **Dual Mode** per accessibilità non vedenti.
- **Modalità OCR** (variabile `ocr` **assente**): layout testuale per screen reader
- **Modalità Vanilla** (variabile `ocr` **presente**): layout grafico Paradox originale

Toggle: **Shift+F11** in-game (imposta/rimuove variabile `ocr`).

> ⚠️ `GameRules.GetRule('ocr_accessibility_mode')` è **deprecato** — non usarlo mai.

---

## Percorsi di Riferimento

| Percorso | Ruolo |
|----------|-------|
| `ocr_support_compatibility_pach/gui/` | Patch attiva — **unico percorso scrivibile** |
| `../CK3-OCR/OCR-Support/gui/` | OCR upstream Agamidae — sola lettura |
| `../CK3 ORIGINAL VERSION/ck3origin/game/gui/` | Vanilla CK3 1.17.1 — sola lettura |

> ⚠️ Il path vanilla usa spazi: `CK3 ORIGINAL VERSION` (non trattini)

---

## Struttura Repository

```
.github/
  instructions/          ← istruzioni attivate automaticamente per dominio (applyTo)
  agents/                ← agenti specializzati (Analista, Architetto, Implementatore...)
  prompts/               ← prompt riutilizzabili
  resources/             ← pattern canonical, whitelist scope, priority list
  copilot-skills/        ← skills invocabili dagli agenti con #nome-skill
tools/
  audit.py               ← gate completo: validator + scope + fedelta' vanilla
  tri_diff.py            ← confronto strutturale tra i 3 repo
  gui_validator.py       ← lint strutturale file .gui
  scope_extractor.py     ← estrae binding dal file e aggiorna whitelist
  assemble_dualmode.py   ← assembla qualsiasi finestra in dual-mode (generico)
  assemble_army_dualmode.py  ← assembla window_army.gui (specializzato, mantenuto)
  annotate_datamodels.py ← strumento di manutenzione datamodel
  config.py              ← path centralizzati ai 3 repo
ocr_support_compatibility_pach/gui/  ← file .gui della mod (lavoro attivo)
```

---

## Linguaggio e Compatibilità

- Jomini GUI scripting — CK3 1.17.1 | Encoding: UTF-8 | Estensione: `.gui`
- NON usare scope/widget/proprietà non documentati per CK3 1.17.1
- NON inventare binding — copiare sempre dal file vanilla corrispondente
- Ogni modifica deve essere compatibile con il sistema di override mod di CK3

---

## Principi Irrinunciabili

**Toggle visibilità — meccanismo unico e obbligatorio:**

```jomini
visible = "[Not(GetVariableSystem.Exists('ocr'))]"  # container OCR — non vedente
visible = "[GetVariableSystem.Exists('ocr')]"        # container vanilla — normo-vedente
```

- **Parità funzionale**: OCR e vanilla sono equivalenti — nessuna è una versione ridotta dell'altra.
- **Vanilla immutabile**: il container vanilla è copia fedele del CK3 originale. Nessuna modifica.
- **Checksum/multiplayer parity**: gate non negoziabili per ogni integrazione.
- **Whitelist scope obbligatoria**: ogni binding usato deve essere verificato in `.github/resources/jomini_scope_whitelist.md`. Se non presente dopo verifica nel vanilla → aggiungere immediatamente.

---

## Istruzioni Attive per Dominio

Si attivano automaticamente in base al file aperto:

| File instruction | applyTo | Contenuto |
|-----------------|---------|-----------|
| `patch-boundaries.instructions.md` | `**` | Percorsi scrivibili/vietati |
| `workflow-nuova-finestra.instructions.md` | `**` | Workflow e sequenza agenti per nuova conversione |
| `gui-jomini.instructions.md` | `**/*.gui` | Widget, template canonico, checklist pre-commit |
| `gui-jomini-scopes.instructions.md` | `**/*.gui` | Regole scope e binding Jomini |
| `gui-conversion-progress.instructions.md` | `**` | Stato conversioni: file già convertiti e da convertire |
| `localization-ocr.instructions.md` | `**/localization/**/*.yml` | Convenzioni localizzazione OCR |

---

## Agenti Disponibili

Selezionabili nel picker agenti di VS Code. Ciascuno ha ruolo fisso — non uscire dal ruolo assegnato.

| Agente | File | Ruolo |
|--------|------|-------|
| Analista Tri-Repo | `analista-tri-repo.agent.md` | Confronto 3 repo — solo lettura |
| Architetto Dual-Mode | `architetto-dual-mode.agent.md` | Progettazione OCR/vanilla — no edit |
| Implementatore Patch | `implementatore-patch.agent.md` | Scrive codice nella patch |
| Revisore Accessibilità | `revisore-accessibilita.agent.md` | Qualità OCR/NVDA — no edit |
| Revisore Vanilla | `revisore-vanilla.agent.md` | Fedeltà vanilla — no edit |
| Auditore Finale | `auditore-finale.agent.md` | Review pre-commit, APPROVED o BLOCKED |

---

## Skills Disponibili

In `.github/copilot-skills/` — invocabili dagli agenti con `#nome-skill`.

| Skill | Scopo |
|-------|-------|
| `deprecated-pattern-scanner` | Rileva pattern vietati/deprecati |
| `scope-whitelist-check` | Verifica binding contro whitelist |
| `tri-repo-diff` | Confronto strutturale tra i 3 repo |
| `vanilla-fidelity-check` | Verifica fedeltà container vanilla |
| `accessibility-checklist-runner` | Checklist NVDA automatica |
| `dual-mode-template-generator` | Genera scheletro dual mode — usare solo per finestre senza sorgente OCR esistente |

---

## Principio di Controllo Manuale (non negoziabile)

- Il modder approva **SEMPRE** prima che il file venga scritto nella patch (CHECKPOINT 1)
- Il modder vede **SEMPRE** il verdetto di audit prima dei revisori (CHECKPOINT 2)
- Il sistema **NON** avvia mai la conversione di una finestra successiva automaticamente
- **Una finestra alla volta. Sempre.**

---

## Note Operative

- Il modder è non vedente e usa screen reader. Messaggi di errore: **italiano, chiari, descrittivi**.
- Spiegare sempre il **perché** di ogni scelta tecnica.
- Se un pattern Jomini è ambiguo: chiedere conferma prima di implementare.
- La compatibilità con CK3 1.17.1 è prioritaria rispetto a qualunque feature nuova.
