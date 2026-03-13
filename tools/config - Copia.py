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

# Repository 3 — Vanilla CK3 1.17.1 (nota: il path usa spazi, NON trattini)
VANILLA_ROOT = WORKSPACE_ROOT / "CK3 ORIGINAL VERSION"
VANILLA_GUI = VANILLA_ROOT / "ck3origin" / "game" / "gui"

# Risorse framework
WHITELIST_PATH = PATCH_ROOT / ".github" / "resources" / "jomini_scope_whitelist.md"
RESOURCES_PATH = PATCH_ROOT / ".github" / "resources"


if __name__ == "__main__":
    paths = {
        "PATCH_GUI": PATCH_GUI,
        "OCR_GUI": OCR_GUI,
        "VANILLA_GUI": VANILLA_GUI,
        "WHITELIST_PATH": WHITELIST_PATH,
    }
    for nome, path in paths.items():
        stato = "EXISTS" if path.exists() else "MISSING"
        print(f"{nome}: {path} [{stato}]")
