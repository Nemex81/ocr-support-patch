# TODO operativo corrente

Stato: in attesa conferma del modder prima di iniziare l'implementazione
Fase attiva prevista: Fase 1 - Quick wins e pulizia immediata
Riferimento piano generale: `coding plans/PIANO_GENERALE_CORREZIONE_LOG_2026-03-18.md`

## Regola d'uso

- [ ] Aggiornare questo file in tempo reale durante la codifica.
- [ ] Spuntare ogni voce solo dopo verifica effettiva sul file modificato.
- [ ] A fine Fase 1, aggiornare anche la checkbox della Fase 1 nel piano generale.
- [ ] Non passare alla Fase 2 senza aver riscritto questo file per la nuova fase attiva.

## Fase 1 - Lista dettagliata delle modifiche da eseguire

### Blocco A - Verifica lessicale rapida

- [ ] Verificare se `frontend_main.gui` nella patch contiene ancora stringhe con backslash non parser-safe.
- [ ] Correggere eventuali apostrofi/backslash non parser-safe in `frontend_main.gui` con formulazione testuale compatibile CK3.
- [ ] Verificare se `window_dynasty_legacy.gui` nella patch contiene ancora stringhe con backslash non parser-safe.
- [ ] Correggere eventuali apostrofi/backslash non parser-safe in `window_dynasty_legacy.gui`.
- [ ] Verificare `window_inventory.gui` sul punto segnalato dal log e correggere la stringa parser-safe se ancora necessaria.

### Blocco B - Localizzazione/testo rapido

- [ ] Verificare `interaction_modify_vassal_window.gui` sui punti segnalati dal log per `NON_FEUDAL_SUBJECT_CONTRACT_OBLIGATIONS_TITLE`.
- [ ] Decidere per ogni punto se usare `text` con chiave valida oppure `raw_text`, senza inventare chiavi nuove.
- [ ] Verificare `window_faith.gui` sui punti segnalati come testo non localizzato (`CLOSE_WINDOW`, `BACK`, `,`).
- [ ] Correggere solo i casi realmente presenti nel ramo patchato attivo.

### Blocco C - Fix rapido minimumsize

- [ ] Ispezionare `window_decisions.gui` sui due `minimumsize` segnalati dal log.
- [ ] Sostituire il pattern vettoriale fragile con una forma compatibile con il parser CK3 1.17.1, mantenendo il comportamento originale.
- [ ] Verificare che i due casi restino coerenti tra loro.

### Blocco D - Chiusura fase

- [ ] Rileggere i file toccati per confermare che i fix siano minimali e coerenti con il dual-mode.
- [ ] Eseguire una nuova raccolta log dopo i fix della Fase 1.
- [ ] Confrontare `error.log` e `gui_warnings.log` con la baseline attuale.
- [ ] Aggiornare questo file trasformandolo nel TODO dettagliato della Fase 2.
- [ ] Spuntare la checkbox della Fase 1 nel piano generale solo dopo il confronto log post-fix.