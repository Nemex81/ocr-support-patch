# Regole e mappatura modelli — OCR Patch

Aggiornato al **13 marzo 2026**.

## Premesse importanti

- **Disponibilità reale nel picker**: dipende dal piano Copilot, dalle policy dell'organizzazione e dal rollout. GitHub documenta i modelli supportati, ma precisa anche che la disponibilità può cambiare nel tempo.
- **Contesto del provider != contesto effettivo in Copilot/VS Code**: dove possibile riporto la finestra di contesto ufficiale del provider. In alcuni casi GitHub ha storicamente imposto o documentato finestre pratiche diverse dentro Copilot.
- **Ordine nel model picker**: non è una regola stabile e non conviene codificarlo. Ho quindi rimosso i campi tipo `1/23`, `2/23`, ecc.
- **Capacità**: in questo file separo ciò che è certo da ciò che è solo ragionevole. Per questo evito di dare per scontato che “visione”, “tool calling” o “agent mode” siano identici tra API del provider e comportamento del picker di Copilot.

---

## Modelli confermati o rilevanti per VS Code + Copilot

### 1. Claude Haiku 4.5 (Copilot)
- **Provider**: Anthropic
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **200K** token
- **Input ufficiali**: testo, immagine
- **Quota premium**: **0,33x** sui piani paid, **1x** su Copilot Free
- **Note pratiche**: modello rapido e leggero. Ha senso per task semplici, piccoli fix, domande veloci, spiegazioni brevi.

### 2. Claude Opus 4.5 (Copilot)
- **Provider**: Anthropic
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **200K** token
- **Input ufficiali**: testo, immagine
- **Quota premium**: **3x**
- **Note pratiche**: molto forte su ragionamento e debug complesso, ma costoso in premium requests.

### 3. Claude Opus 4.6 (Copilot)
- **Provider**: Anthropic
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **200K** token standard, **1M** token in beta su API/contesto lungo
- **Input ufficiali**: testo, immagine
- **Quota premium**: **3x**
- **Note pratiche**: variante Opus più aggiornata e più potente di Opus 4.5. Ottima per casi difficili, ma da usare con criterio perché divora quota come un falò burocratico.

### 4. Claude Sonnet 4 (Copilot)
- **Provider**: Anthropic
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **200K** token standard, **1M** token in beta su API/contesto lungo
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: ancora valido, ma ormai è una scelta di retrocompatibilità più che di preferenza.

### 5. Claude Sonnet 4.5 (Copilot)
- **Provider**: Anthropic
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **200K** token standard, **1M** token in beta su API/contesto lungo
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: buon equilibrio fra qualità e costo. Resta molto utile, ma Sonnet 4.6 lo supera.

### 6. Claude Sonnet 4.6 (Copilot)
- **Provider**: Anthropic
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **200K** token standard, **1M** token in beta su API/contesto lungo
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: una delle scelte migliori per coding generale, agenti, review e debug con buon rapporto qualità/costo.

### 7. Gemini 2.5 Pro (Copilot)
- **Provider**: Google
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **1.048.576 input / 65.536 output**
- **Input ufficiali**: testo, immagine, video, audio, PDF
- **Capacità ufficiali principali**: function calling, code execution, file search, search grounding
- **Quota premium**: **1x**
- **Note pratiche**: molto valido per reasoning, ricerca tecnica e casi multimodali seri.

### 8. Gemini 3 Flash (Copilot)
- **Provider**: Google
- **Stato in Copilot**: Public preview
- **Contesto ufficiale**: **1.048.576 input / 65.536 output**
- **Input ufficiali**: testo, immagine, video, audio, PDF
- **Capacità ufficiali principali**: function calling, code execution, file search, computer use
- **Quota premium**: **0,33x**
- **Note pratiche**: buon modello veloce per task semplici o iterazioni rapide.

### 9. Gemini 3 Pro (Copilot)
- **Provider**: Google
- **Stato in Copilot**: Public preview, ma **in dismissione**
- **Contesto ufficiale**: **1.048.576 input / 65.536 output**
- **Input ufficiali**: testo, immagine, video, audio, PDF
- **Capacità ufficiali principali**: function calling, code execution, file search
- **Quota premium**: **1x**
- **Note pratiche**: **non conviene più usarlo come regola stabile**. Google lo ha già spento lato provider il **9 marzo 2026** e GitHub ne ha annunciato la deprecazione in Copilot per il **26 marzo 2026**.

### 10. Gemini 3.1 Pro (Copilot)
- **Provider**: Google
- **Stato in Copilot**: Public preview
- **Contesto ufficiale**: **1.048.576 input / 65.536 output**
- **Input ufficiali**: testo, immagine, video, audio, PDF
- **Capacità ufficiali principali**: function calling, code execution, file search (AI Studio), search grounding, URL context, structured outputs
- **Quota premium**: **1x**
- **Note pratiche**: è il sostituto naturale di Gemini 3 Pro.

### 11. GPT-4.1 (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **1.047.576** token
- **Input ufficiali**: testo, immagine
- **Quota premium**: **0x** sui piani paid, **1x** su Copilot Free
- **Note pratiche**: ottimo default gratuito sui piani paid. Non-reasoning, ma molto solido per task comuni.

### 12. GPT-4o (legacy / compatibilità)
- **Provider**: OpenAI
- **Stato in Copilot**: caso ambiguo
- **Contesto documentato da GitHub in passato**: **64K** in Copilot Chat generale, **128K** in VS Code Insiders
- **Quota premium**: **0x** sui piani paid, **1x** su Copilot Free
- **Note pratiche**: non compare più nell'elenco principale dei modelli supportati di Copilot, ma compare ancora nella tabella dei moltiplicatori. Trattalo come **legacy/compatibilità**, non come base per nuove regole. Se lo vedi ancora nel picker, usalo solo per continuità o confronto storico.

### 13. GPT-5 mini (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **400.000 input+output complessivi**, con **128.000 max output**
- **Input ufficiali**: testo, immagine
- **Quota premium**: **0x** sui piani paid, **1x** su Copilot Free
- **Note pratiche**: uno dei migliori default pratici. Rapido, economico, buono per chat operativa, codice quotidiano e visual reasoning.

### 14. GPT-5.1 (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: GA, ma **in deprecazione**
- **Contesto ufficiale**: **400.000** con **128.000 max output**
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: non conviene costruirci regole nuove. GitHub ne ha annunciato la deprecazione per il **1 aprile 2026**.

### 15. GPT-5.1-Codex (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: GA, ma **in deprecazione**
- **Contesto ufficiale**: **400.000** con **128.000 max output**
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: modello agentic/coding valido, ma in uscita. Alternative: **GPT-5.3-Codex** o **GPT-5.2-Codex**.

### 16. GPT-5.1-Codex-Max (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: GA, ma **in deprecazione**
- **Contesto ufficiale**: **400.000** con **128.000 max output**
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: pensato per task agentic lunghi, ma anche questo va verso la pensione tecnica il **1 aprile 2026**.

### 17. GPT-5.1-Codex-Mini (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: Public preview, ma **in deprecazione**
- **Contesto ufficiale**: **400.000** con **128.000 max output**
- **Input ufficiali**: testo, immagine
- **Quota premium**: **0,33x**
- **Note pratiche**: economico per compiti agentic/coding più leggeri, ma ormai non è più una base solida per regole future.

### 18. GPT-5.2 (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **400.000** con **128.000 max output**
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: forte su analisi tecnica e ragionamento complesso, ma oggi GPT-5.4 è il riferimento più moderno.

### 19. GPT-5.2-Codex (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **400.000** con **128.000 max output**
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: ottimo per agenti di coding, review, refactor complessi e task lunghi.

### 20. GPT-5.3-Codex (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **400.000** con **128.000 max output**
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: tra i migliori modelli da scegliere per coding serio e lavori agentic end-to-end. È anche l'alternativa indicata da GitHub per la dismissione dei 5.1-Codex.

### 21. GPT-5.4 (Copilot)
- **Provider**: OpenAI
- **Stato in Copilot**: GA dal **5 marzo 2026**
- **Contesto ufficiale**: **1.050.000** token circa, con **128.000 max output**
- **Input ufficiali**: testo, immagine
- **Quota premium**: **1x**
- **Note pratiche**: top tier per reasoning, architettura, analisi tecnica e task complessi. Da usare quando serve qualità vera, non quando stai chiedendo una regex o un commento di tre righe.

### 22. Grok Code Fast 1 (Copilot)
- **Provider**: xAI
- **Stato in Copilot**: GA
- **Contesto ufficiale**: **256K** token
- **Input ufficiali pubblicamente documentati**: principalmente testo; xAI lo presenta come modello reasoning per coding agentic con supporto nativo al tool calling
- **Quota premium**: **0,25x** sui piani paid, **1x** su Copilot Free
- **Note pratiche**: molto interessante per coding rapido e debugging multi-linguaggio, con costo premium basso.

### 23. Raptor mini (Copilot)
- **Provider**: fine-tuned GPT-5 mini (Microsoft)
- **Stato in Copilot**: Public preview
- **Contesto ufficiale pubblico**: **non documentato chiaramente da GitHub**
- **Quota premium**: **0x** sui piani paid, **1x** su Copilot Free
- **Note pratiche**: GitHub lo descrive come adatto a completamenti rapidi, spiegazioni e uso generale leggero. Non fissare assunzioni rigide sul contesto token finché GitHub non lo documenta.

### 24. Goldeneye (Copilot)
- **Provider**: fine-tuned GPT-5.1-Codex (Microsoft)
- **Stato in Copilot**: Public preview
- **Contesto ufficiale pubblico**: **non documentato chiaramente da GitHub**
- **Quota premium**: **non applicabile** sui piani paid, **1x** su Copilot Free
- **Note pratiche**: **mancava nella bozza originale**, ma compare nell'elenco attuale dei modelli supportati da Copilot. GitHub lo posiziona nei casi di deep reasoning/debugging.

---

## Correzioni chiave rispetto alla bozza originale

### Errori corretti
- Ho **rimosso l'ordine fisso del picker** (`1/23`, `2/23`, ecc.), perché non è una proprietà stabile documentata.
- Ho **corretto GPT-4o**: il valore `68K` non è allineato alle fonti ufficiali disponibili. GitHub aveva documentato **64K** in generale e **128K in VS Code Insiders**.
- Ho **corretto tutta la famiglia GPT-5 / Codex**: molti valori non erano 192K o 256K, ma **400K** per GPT-5 mini, 5.1, 5.2 e per le varianti Codex 5.1/5.2/5.3.
- Ho **corretto GPT-5.4**: non è 400K, ma circa **1,05M** di contesto ufficiale.
- Ho **corretto Gemini 2.5 Pro / 3 Flash / 3 Pro / 3.1 Pro**: non sono 173K, ma circa **1.048.576 input / 65.536 output**.
- Ho **corretto Claude Sonnet 4 / 4.5 / 4.6**: il valore base è **200K**, con **1M beta** dove previsto, non 144K o 160K come nella bozza.
- Ho **corretto Claude Opus 4.5 e 4.6**: il valore base documentato è **200K**, non 160K o 192K.
- Ho **corretto Grok Code Fast 1**: il contesto ufficiale pubblico è **256K**, non 173K.
- Ho **corretto lo stato di Gemini 3 Pro**: è già **spento lato provider** e in uscita anche da Copilot.
- Ho **segnalato la deprecazione di GPT-5.1 e delle sue varianti Codex**, che nella bozza apparivano come opzioni stabili.
- Ho **aggiunto Goldeneye**, che non era presente nella bozza ma risulta tra i modelli supportati da Copilot.

### Campi che conviene NON usare più nelle regole
- `Visibile in model picker: x/23`
- `toolCalling = sì` come affermazione assoluta identica tra provider API e Copilot
- `agentMode = sì` come scorciatoia non qualificata
- qualunque assunzione sul fatto che il contesto dichiarato dal provider sia sempre uguale a quello effettivo esposto da Copilot

---

## Mappatura consigliata aggiornata

### Default pratico
- **Uso giornaliero / chat operativa**: `GPT-5 mini`
- **Coding generale con buon equilibrio**: `Claude Sonnet 4.6`
- **Debug e reasoning pesante**: `GPT-5.4` oppure `Claude Opus 4.6`
- **Refactor e task agentic lunghi**: `GPT-5.3-Codex` oppure `GPT-5.2-Codex`
- **Task rapidi con quota bassa**: `Claude Haiku 4.5`, `Gemini 3 Flash`, `Grok Code Fast 1`
- **Visual reasoning su screenshot/diagrammi**: `GPT-5 mini`, `Claude Sonnet 4.6`

### Modelli da evitare come base di policy futura
- `Gemini 3 Pro`
- `GPT-5.1`
- `GPT-5.1-Codex`
- `GPT-5.1-Codex-Mini`
- `GPT-5.1-Codex-Max`
- `GPT-4o` come default moderno

---

## Regole rapide pronte per il framework

- Se il task è **semplice, frequente o iterativo**, prova prima `GPT-5 mini`.
- Se il task è **di coding generale ma vuoi più affidabilità**, usa `Claude Sonnet 4.6`.
- Se il task è **architetturale, multi-file, lungo o ad alto rischio di allucinazioni operative**, usa `GPT-5.4` o `Claude Opus 4.6`.
- Se il task è **agentic puro** con refactor, test, review e pipeline lunghe, usa `GPT-5.3-Codex` o `GPT-5.2-Codex`.
- Se vuoi **contenere il consumo premium**, preferisci modelli a **0x / 0,25x / 0,33x**.
- Se una regola punta a un modello **preview o in deprecazione**, definisci sempre un **fallback stabile**.

### Fallback consigliati
- `Gemini 3 Pro` -> `Gemini 3.1 Pro`
- `GPT-5.1*` -> `GPT-5.3-Codex`
- `GPT-4o` -> `GPT-4.1` oppure `GPT-5 mini`
- `Claude Sonnet 4` -> `Claude Sonnet 4.6`
- `Claude Opus 4.5` -> `Claude Opus 4.6`

---

## Indicazione per l'integrazione nel sistema

Quando trasformi questo file in configurazione leggibile da codice, ti conviene modellare almeno questi campi:

- `name`
- `provider`
- `copilot_status`
- `official_context_window`
- `official_output_limit`
- `premium_multiplier_paid`
- `premium_multiplier_free`
- `recommended_for`
- `avoid_for`
- `is_preview`
- `is_deprecating`
- `fallback_model`

Non memorizzare come dato strutturale:

- posizione del modello nel picker
- assunzioni assolute sul fatto che ogni modello supporti esattamente le stesse feature di Copilot in ogni client

---
