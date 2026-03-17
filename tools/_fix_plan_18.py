#!/usr/bin/env python3
"""
Fix unico: rimuove le righe 966-990 (1-based) dalla sezione 18A-18C corrotta
e le rimpiazza con le sezioni 18A e 18C corrette.
Le righe 991+ (18B header + contenuto) vengono mantenute intatte.
"""
import sys

PLAN = r"c:\Users\nemex\OneDrive\Documenti\GitHub\ocr-support-patch\PIANO_CORRETTIVO_CRASH_AVVIO_2026-03-17.md"

with open(PLAN, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Righe totali: {len(lines)}")

# Mostra righe 965-991 (0-indexed 964-990) per verifica
for i in range(964, min(991, len(lines))):
    print(f"[{i+1}] {lines[i].rstrip()}")

# Determina intervallo da sostituire: righe 965-990 (0-indexed 964-989)
# (queste contengono le sezioni 18A truncata, 18C truncata, 18B header orfano, 18A duplicata)
START = 964  # 0-indexed
END = 990    # 0-indexed (esclusivo)

# Contenuto corretto delle sezioni 18A e 18C (poi arriva 18B dal file)
clean = [
    "### Fase 18A \u2014 (SE CRASH = OCR UPSTREAM) Documentazione Limitazione Nota\n",
    "\n",
    "Se il crash esiste in OCR upstream senza la nostra patch:\n",
    "\n",
    "- [ ] Aggiornare `gui-conversion-progress.instructions.md` con nota \"crash nuova partita = OCR upstream bug\"\n",
    "- [ ] Verificare se esiste fix nella community OCR (Agamidae repository issues)\n",
    "- [ ] La nostra patch NON pu\u00f2 risolvere questo crash; la funzionalit\u00e0 \"scelta libera governante\"\n",
    "  \u00e8 limitata finch\u00e9 OCR upstream non aggiorna `sgui_ocr.txt:328`\n",
    "\n",
    "---\n",
    "\n",
    "### Fase 18B \u2014 (SE CRASH = NOSTRA PATCH) Isolamento File Causa\n",
    "\n",
    "Se OCR upstream da solo NON crasha, il crash \u00e8 nella nostra patch.\n",
    "\n",
    "**Azione**: test hot-swap sistematico. Rimpiazzare temporaneamente nel deploy i file\n",
    "sospetti con le versioni originali OCR upstream, uno alla volta, testando dopo ciascuno.\n",
    "\n",
    "**Lista file sospetti (in ordine di priorit\u00e0)**:\n",
    "\n",
    "| Priorit\u00e0 | File patch | Dimensione | Sospetto |\n",
    "|----------|-----------|-----------|----------|\n",
    "| 1 | `hud.gui` | 7167 righe | Pi\u00f9 grande inline; istanziato al boot gioco |\n",
    "| 2 | `window_character.gui` | 5692 righe | 2\u00b0 grande inline; possibilmente pre-caricato |\n",
    "| 3 | `window_army.gui` | ~6100 righe wrapper | Wrapper grandi con vanilla types complessi |\n",
    "| 4 | `window_intrigue.gui` | ~3700 righe | Inline con schema complesso |\n",
    "| 5 | Altri inline | < 3000 righe | Meno probabili |\n",
    "\n",
    "**Procedura per ciascun file sospetto**:\n",
    "1. Nel deploy path, rinominare `FILE.gui` \u2192 `FILE.gui.bak`\n",
    "2. Copiare `OCR-upstream/FILE.gui` nel deploy path\n",
    "3. Avviare CK3 \u2192 Nuova partita \u2192 Scelta libera \u2192 testare\n",
    "4. Se NO CRASH: il file originale era la causa \u2192 applicare Fase 19\n",
    "5. Se CRASH: ripristinare `.bak` \u2192 testare il file successivo\n",
    "\n",
    "- [ ] Test hot-swap `hud.gui` (primo candidato)\n",
    "- [ ] Test hot-swap `window_character.gui` (secondo candidato)\n",
    "- [ ] Test hot-swap altri file se necessario\n",
    "- [ ] File causa identificato: _______________\n",
    "\n",
    "---\n",
    "\n",
    "### Fase 18C \u2014 (SE CRASH = MIV + NOSTRA PATCH) Conflitto Mod Terze Parti\n",
    "\n",
    "Se il crash avviene SOLO quando MIV \u00e8 attivo insieme alla nostra patch (Passo B OK, Passo C CRASH):\n",
    "\n",
    "- [ ] Disabilitare MIV definitivamente dal load order\n",
    "- [ ] Documentare in `gui-conversion-progress.instructions.md`: \"MIV mod causa conflitto di stack overflow con OCR + nostra patch\"\n",
    "- [ ] La nostra patch \u00e8 corretta \u2014 il problema \u00e8 MIV; non modificare i nostri file\n",
    "- [ ] Nota all'utente: MIV non \u00e8 compatibile con OCR Support in questa configurazione\n",
    "\n",
    "---\n",
    "\n",
]

# Trova dove 18B content inizia dopo la corruzione (riga "Se OCR upstream da solo NON crasha...")
# Cerca la prima occorrenza dalla riga END in poi
skip_until = None
for i in range(END, len(lines)):
    if lines[i].strip().startswith("Se OCR upstream da solo NON crasha"):
        skip_until = i
        print(f"18B body trovato alla riga {i+1}: {lines[i].rstrip()}")
        break

if skip_until is None:
    # Fallback: cerca "### Fase 19"
    for i in range(END, len(lines)):
        if lines[i].strip().startswith("### Fase 19"):
            skip_until = i
            break

# Costruisci il file: righe prima di START + clean + righe da skip_until in poi
# (salta il corpo di 18B dal file poiche' lo inseriamo nel clean)
# Prima trova dove inizia 18B e dove finisce 18B
# 18B body = da skip_until fino a fine 18B (prima di "### Fase 19")
fase19_line = None
for i in range(END, len(lines)):
    if "### Fase 19" in lines[i]:
        fase19_line = i
        print(f"Fase 19 trovata alla riga {i+1}")
        break

if fase19_line is None:
    print("ERRORE: Fase 19 non trovata")
    sys.exit(1)

# Il "clean" include già tutto il contenuto di 18B e 18C riscritto da zero.
# Quindi skippiamo le righe dal file che vanno da START fino a fase19_line-1,
# e manteniamo righe 0..START-1 + clean + righe fase19_line..end
new_lines = lines[0:START] + clean + lines[fase19_line:]

print(f"Righe dopo fix: {len(new_lines)}")

with open(PLAN, "w", encoding="utf-8", newline="\r\n") as f:
    f.writelines(new_lines)

print("Salvato con CRLF e UTF-8 senza BOM.")
print("Verifica sezioni 18A-18C:")
for i, ln in enumerate(new_lines):
    if "### Fase 18" in ln or "### Fase 17" in ln or "### Fase 19" in ln:
        print(f"  [{i+1}] {ln.rstrip()}")
