# Regole e mappatura modelli — OCR Patch

Questo file contiene la lista dei modelli disponibili e le regole consigliate per il loro utilizzo nel framework della patch.

## Modelli (bozza fornita)

1. Claude Haiku 4.5 (Copilot)
   - Contesto: 160K token
   - Funzionalità: visione, toolCalling, agentMode
   - Quota: ogni messaggio conta 0,33x
   - Visibile in model picker: 1/23

2. Claude Opus 4.5 (Copilot)
   - Contesto: 160K token
   - Funzionalità: visione, toolCalling, agentMode
   - Quota: ogni messaggio conta 3x
   - Visibile in model picker: 2/23

3. Claude Opus 4.6 (Copilot)
   - Contesto: 192K token
   - Funzionalità: visione, toolCalling, agentMode
   - Quota: ogni messaggio conta 3x
   - Visibile in model picker: 3/23

4. Claude Sonnet 4 (Copilot)
   - Contesto: 144K token
   - Funzionalità: visione, toolCalling, agentMode
   - Quota: ogni messaggio conta 1x
   - Visibile in model picker: 4/23

5. Claude Sonnet 4.5 (Copilot)
   - Contesto: 160K token
   - Funzionalità: visione, toolCalling, agentMode
   - Quota: ogni messaggio conta 1x
   - Visibile in model picker: 5/23

6. Claude Sonnet 4.6 (Copilot)
   - Contesto: 160K token
   - Funzionalità: visione, toolCalling, agentMode
   - Quota: ogni messaggio conta 1x
   - Visibile in model picker: 6/23

7. Gemini 2.5 Pro (Copilot)
   - Contesto: 173K token
   - Funzionalità: visione, toolCalling, agentMode
   - Quota: ogni messaggio conta 1x
   - Visibile in model picker: 7/23

8. Gemini 3 Flash (Anteprima)
   - Contesto: 173K token
   - Funzionalità: visione, toolCalling, agentMode
   - Quota: ogni messaggio conta 0,33x
   - Visibile in model picker: 8/23

9. Gemini 3 Pro (Anteprima)
   - Contesto: 173K token
   - Funzionalità: visione, toolCalling, agentMode
   - Quota: ogni messaggio conta 1x
   - Visibile in model picker: 9/23

10. Gemini 3.1 Pro (Anteprima)
    - Contesto: 173K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 1x
    - Visibile in model picker: 10/23

11. GPT-4.1 (Copilot)
    - Contesto: 128K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 0x
    - Visibile in model picker: 11/23

12. GPT-4o (Copilot)
    - Contesto: 68K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 0x
    - Visibile in model picker: 12/23

13. GPT-5 mini (Copilot)
    - Contesto: 192K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 0x
    - Visibile in model picker: 13/23

14. GPT-5.1 (Copilot)
    - Contesto: 192K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 1x
    - Visibile in model picker: 14/23

15. Codice GPT-5.1 (Copilot)
    - Contesto: 256K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 1x
    - Visibile in model picker: 15/23

16. GPT-5.1-Codex-Max (Copilot)
    - Contesto: 256K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 1x
    - Visibile in model picker: 16/23

17. GPT-5.1-Codex-Mini (Anteprima)
    - Contesto: 256K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 0,33x
    - Visibile in model picker: 17/23

18. GPT-5.2 (Copilot)
    - Contesto: 192K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 1x
    - Visibile in model picker: 18/23

19. GPT-5.2 codex (Copilot)
    - Contesto: 400K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 1x
    - Visibile in model picker: 19/23

20. GPT-5.3 codex (Copilot)
    - Contesto: 400K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 1x
    - Visibile in model picker: 20/23

21. GPT-5.4 (Copilot)
    - Contesto: 400K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 1x
    - Visibile in model picker: 21/23

22. Grok Code Fast 1 (Copilot)
    - Contesto: 173K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 0,25x
    - Visibile in model picker: 22/23

23. Raptor mini (Anteprima)
    - Contesto: 264K token
    - Funzionalità: visione, toolCalling, agentMode
    - Quota: ogni messaggio conta 0x
    - Visibile in model picker: 23/23

---

## Mappatura consigliata (regole rapide)

- Uso giornaliero / chat operativa: `GPT-5 mini` (default, basso costo, 0x quota)
- Revisione codice, refactor profondi: `GPT-5.2 codex` o `GPT-5.3 codex` (400K)
- Task che richiedono ampio contesto ma non codice: `GPT-5.2` o `GPT-5.1` (192K)
- Pipeline con limiti di quota / alta frequenza: preferire modelli con moltiplicatori bassi o 0x (`GPT-4.1`, `GPT-4o`, `GPT-5 mini`, `Raptor mini`)
- Sperimentale / testing prompt: usare modelli anteprima (`Gemini 3`, `Claude Opus/Haiku`) solo dopo test comparativi

## Integrazione nel sistema (passaggi raccomandati)

1. Posiziona questo file in `ocr_support_compatibility_pach/gui/` (fatto).
2. Aggiungi a `tools/config.py` (o file di configurazione centrale) una funzione che legga questa regola e la trasformi in una struttura dati (YAML/JSON). Esempio (pseudo-python):

```python
import yaml

with open('ocr_support_compatibility_pach/gui/model_rules.md', 'r', encoding='utf-8') as f:
    # estrai la parte YAML o parsifica il contenuto strutturato
    rules = parse_model_rules_md(f.read())
```

3. Implementa uno script `tools/select_model.py` che espone un'API CLI interna: input = `use_case`, `max_quota_multiplier`, `need_context_tokens`; output = modello consigliato + fallback.

4. Aggiorna `workflow-nuova-finestra.instructions.md` aggiungendo un passo che richiede al revisore di verificare la compliance con le `model_rules.md` quando sceglie il modello per l'automazione.

5. (Opzionale) Aggiungi test automatici che confrontino le scelte del selettore con un set di casi d'uso attesi.

## Esempio d'uso rapido (manuale)

Se vuoi che ti consigli ogni volta che chiedi, posso leggere direttamente questo file e rispondere secondo la mappatura. Per automazione completa servirebbe il permesso di modificare `tools/` per aggiungere lo script `select_model.py`.

---

Se vuoi, procedo creando il file e collego il breve script di selezione (richiede permesso per scrivere in `tools/`).
