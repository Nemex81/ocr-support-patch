"""Mostra solo i CRITICI dal validator. Uso: python3.14 tools/_show_critici.py <file.gui>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.gui_validator import analizza_file

percorso = Path(sys.argv[1])
risultato = analizza_file(percorso)
critici = [i for i in risultato["issues"] if i["severity"] == "CRITICO"]
print(f"Critici totali: {len(critici)}")
for i in critici:
    print(f"  Riga {i['line']}: [{i['category']}] {i['pattern']}")
