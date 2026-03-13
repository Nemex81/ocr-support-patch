# .github/resources — Risorse di riferimento del framework

Questa cartella contiene file statici di riferimento usati da script, agenti e istruzioni: pattern canonici, whitelist scope, regole modello, liste priorità, matrice requisiti.

## Descrizione

I file in questa cartella non contengono logica eseguibile: sono documenti consultati da altri componenti del framework. Script Python li leggono per ottenere dati (es. la whitelist scope), agenti li consultano per prendere decisioni (es. quale pattern di conversione usare), e istruzioni li referenziano come fonte autorevole.

Questa cartella è l'unico punto del framework in cui Copilot può scrivere senza checkpoint esplicito, ma solo per aggiornare `jomini_scope_whitelist.md` con nuovi binding verificati nel vanilla. Tutti gli altri file in questa cartella sono in sola lettura tranne autorizzazione esplicita del modder.

La separazione tra "risorse" e "istruzioni" è intenzionale: le risorse sono dati stabili, le istruzioni sono procedura. Le risorse cambiano raramente (quando cambia CK3 o si aggiungono pattern nuovi), le istruzioni cambiano più spesso (quando il workflow evolve).

## File presenti

**conversion-patterns.md** — Descrive in dettaglio i quattro pattern di conversione dual-mode (A: Simple Swap, B: Tabs+SubWindows, C: Complex Layout, D: Bottom-Up Multi-Window). Per ogni pattern: quando usarlo, struttura del container dual-mode, esempi reali dalla patch.

**domain_boundaries.md** — File machine-readable (formato YAML-in-Markdown) con la distinzione operativa tra dominio Framework (`.github/`, `tools/`) e dominio Mod (`ocr_support_compatibility_pach/`). Consultato da script e agenti per decidere il dominio operativo. Contiene anche le regole sintetiche per "non toccare la mod" e "guarda nel framework".

**dual_mode_pattern_canonical.md** — Definisce il pattern Jomini canonico per il sistema dual-mode: struttura esatta del container OCR, struttura esatta del container vanilla, ordine delle proprietà, regole per le `visible` mutuamente esclusive. Fonte di verità per tutti i file generati.

**jomini_scope_whitelist.md** — Lista di tutti i binding Jomini verificati come validi in CK3 1.17.1. Ogni binding è stato verificato nei file vanilla originali. È l'unico file in questa cartella che Copilot può aggiornare autonomamente (aggiunta di nuovi binding verificati). Usato da `scope_extractor.py` e dalla skill `scope-whitelist-check`.

**model_rules.md** — Mappatura dei modelli AI disponibili in GitHub Copilot con capacità, contesto, quota premium e note pratiche. Usato per scegliere il modello corretto per ogni agente in base alla complessità del task.

**ocr-shortcuts-standard.md** — Lista degli shortcut da tastiera standard del sistema OCR Support per CK3. Usato come riferimento per aggiungere indicazioni di navigazione nei container OCR.

**priority_list.md** — Lista prioritizzata delle finestre da convertire, con motivazione e dimensione. Usato per pianificare la sequenza di conversioni nel progetto.

**requirement-enforcement-matrix.md** — Matrice che incrocia requisiti di progetto con i meccanismi di enforcement: quale istruzione, script o agente garantisce ogni requisito. Utile per verificare la copertura dei requisiti dopo modifiche al framework.

## Come si usa

I file in questa cartella si consultano direttamente o vengono referenziati da altri componenti. Non si invocano: sono letti automaticamente dagli script Python o dagli agenti quando necessario.

Per aggiornare `jomini_scope_whitelist.md`: usare `scope_extractor.py` dopo una conversione. Lo script, invocato con il flag `--file percorso_file.gui`, estrae i binding
presenti nel file indicato e li confronta con la whitelist. I binding assenti
vengono aggiunti alla whitelist solo dopo conferma implicita nell'invocazione
dello script — non avviene nulla senza un'esecuzione esplicita da parte del
modder o dell'agente.

Per aggiornare gli altri file: aprire manualmente, modificare, committare. Non modificare `dual_mode_pattern_canonical.md` senza prima verificare la compatibilità con i file già nella patch.

## Dipendenze

- `tools/scope_extractor.py` — aggiorna `jomini_scope_whitelist.md`
- `tools/config.py` — fornisce i path per leggere i file vanilla di riferimento
- I file vanilla in `CK3 ORIGINAL VERSION/` o nell'installazione CK3 locale — richiesti per verificare i binding prima di aggiungerli alla whitelist
