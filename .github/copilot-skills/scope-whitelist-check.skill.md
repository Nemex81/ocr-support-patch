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

## Pre-Run Automatico

Prima di qualsiasi verifica manuale, eseguire:
```
python tools/scope_extractor.py --file <percorso_file_gui>
```
Lo script produce automaticamente la lista dei binding ASSENTI con le righe
già formattate per la whitelist. Usare il suo output come input per questa skill.
La verifica manuale rimane necessaria solo per i binding DA VERIFICARE (⚠️).

## Logica di Esecuzione

Leggi il file `.github/resources/jomini_scope_whitelist.md`. Estrai tutti i
binding già presenti (colonna 1 della tabella, formato `` `NomeScope` ``).

Per ogni binding nella lista `bindings` in input:

1. **PRESENTE**: il binding è nella whitelist → segnala con ✅
2. **ASSENTE**: il binding non è nella whitelist → segnala con ❌ e produci
   la riga da aggiungere nel formato:
   `` | `NomeBinding` | [context se fornito, altrimenti "da specificare"] | verificato in vanilla CK3 1.17.1 | ``
3. **DA VERIFICARE**: il binding contiene scope non standard (es. scope di mod
   non vanilla, scope con nome ambiguo) → segnala con ⚠️ e richiedi verifica
   manuale nel file vanilla prima di procedere.

---

## Formato Output Obbligatorio

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

---

## Regola Critica per l'Agente che usa questa Skill

Se il risultato contiene binding ASSENTI, l'agente NON può procedere con
l'implementazione finché quei binding non vengono aggiunti alla whitelist.
La skill produce le righe pronte — l'Implementatore le incolla in
`.github/resources/jomini_scope_whitelist.md` prima di continuare.

---

## Agenti che usano questa skill

- **Architetto Dual-Mode**: invoca durante la progettazione, per ogni binding
  che intende usare nel container OCR
- **Implementatore Patch**: invoca prima di usare qualunque binding non già
  presente nel file che sta modificando
- **Auditore Finale**: invoca come verifica finale su tutti i binding del file
