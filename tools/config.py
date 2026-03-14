"""
config.py — Path centralizzati per i tre repository OCR Support Patch.
Tutti gli script in tools/ importano da qui. Non hardcodare path altrove.
"""

from pathlib import Path

# Root del workspace (directory padre che contiene tutti e tre i repo)
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent

# Repository 1 — Patch attiva (questo repo)
PATCH_ROOT = Path(__file__).resolve().parent.parent
PATCH_GUI = PATCH_ROOT / "ocr_support_compatibility_pach" / "gui"

# Repository 2 — OCR upstream (Agamidae)
OCR_ROOT = WORKSPACE_ROOT / "CK3-OCR"
OCR_GUI = OCR_ROOT / "OCR-Support" / "gui"

# Repository 3 — Installazione CK3 completa locale (fonte autorevole, sola lettura)
VANILLA_ROOT = Path("C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III")
VANILLA_GUI = VANILLA_ROOT / "game" / "gui"

# Alias mantenuto per compatibilità con script che lo referenziano direttamente
CK3_INSTALL_ROOT = VANILLA_ROOT
CK3_INSTALL_GUI = VANILLA_GUI

# Risorse framework
WHITELIST_PATH = PATCH_ROOT / ".github" / "resources" / "jomini_scope_whitelist.md"
RESOURCES_PATH = PATCH_ROOT / ".github" / "resources"


if __name__ == "__main__":
    paths = {
        "PATCH_GUI": PATCH_GUI,
        "OCR_GUI": OCR_GUI,
        "VANILLA_GUI": VANILLA_GUI,
        "CK3_INSTALL_GUI": CK3_INSTALL_GUI,
        "WHITELIST_PATH": WHITELIST_PATH,
    }
    for nome, path in paths.items():
        stato = "EXISTS" if path.exists() else "MISSING"
        print(f"{nome}: {path} [{stato}]")
