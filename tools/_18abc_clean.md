### Fase 18A — (SE CRASH = OCR UPSTREAM) Documentazione Limitazione Nota

Se il crash esiste in OCR upstream senza la nostra patch:

- [ ] Aggiornare `gui-conversion-progress.instructions.md` con nota "crash nuova partita = OCR upstream bug"
- [ ] Verificare se esiste fix nella community OCR (Agamidae repository issues)
- [ ] La nostra patch NON può risolvere questo crash; la funzionalità "scelta libera governante"
  è limitata finché OCR upstream non aggiorna `sgui_ocr.txt:328`

---

### Fase 18B — (SE CRASH = NOSTRA PATCH) Isolamento File Causa

Se OCR upstream da solo NON crasha, il crash è nella nostra patch.

**Azione**: test hot-swap sistematico. Rimpiazzare temporaneamente nel deploy i file
sospetti con le versioni originali OCR upstream, uno alla volta, testando dopo ciascuno.

**Lista file sospetti (in ordine di priorità)**:

| Priorità | File patch | Dimensione | Sospetto |
|----------|-----------|-----------|----------|
| 1 | `hud.gui` | 7167 righe | Più grande inline; istanziato al boot gioco |
| 2 | `window_character.gui` | 5692 righe | 2° grande inline; possibilmente pre-caricato |
| 3 | `window_army.gui` | ~6100 righe wrapper | Wrapper grandi con vanilla types complessi |
| 4 | `window_intrigue.gui` | ~3700 righe | Inline con schema complesso |
| 5 | Altri inline | < 3000 righe | Meno probabili |

**Procedura per ciascun file sospetto**:
1. Nel deploy path, rinominare `FILE.gui` → `FILE.gui.bak`
2. Copiare `OCR-upstream/FILE.gui` nel deploy path
3. Avviare CK3 → Nuova partita → Scelta libera → testare
4. Se NO CRASH: il file originale era la causa → applicare Fase 19
5. Se CRASH: ripristinare `.bak` → testare il file successivo

- [ ] Test hot-swap `hud.gui` (primo candidato)
- [ ] Test hot-swap `window_character.gui` (secondo candidato)
- [ ] Test hot-swap altri file se necessario
- [ ] File causa identificato: _______________

---

### Fase 18C — (SE CRASH = MIV + NOSTRA PATCH) Conflitto Mod Terze Parti

Se il crash avviene SOLO quando MIV è attivo insieme alla nostra patch (Passo B OK, Passo C CRASH):

- [ ] Disabilitare MIV definitivamente dal load order
- [ ] Documentare in `gui-conversion-progress.instructions.md`: "MIV mod causa conflitto di stack overflow con OCR + nostra patch"
- [ ] La nostra patch è corretta — il problema è MIV; non modificare i nostri file
- [ ] Nota all'utente: MIV non è compatibile con OCR Support in questa configurazione

---

