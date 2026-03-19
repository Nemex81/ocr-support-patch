import os, re

VANILLA_LOC = r"C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/localization"
PATCH_LOC = r"C:/Users/nemex/OneDrive/Documenti/GitHub/ocr-support-patch/ocr_support_compatibility_pach/localization"
OCR_LOC = r"C:/Users/nemex/OneDrive/Documenti/GitHub/CK3-OCR/OCR-Support/localization"

KEYS = [
    "vengeance_obsessed_modifier",
    "watchman_guidance_modifier",
    "inspection_bandits_in_x_populace_modifier",
    "inspection_selfless_ruler_modifier",
    "legend_chain_army_modifier",
    "oath_greatest_hunter",
    "depose_desc_general",
    "game_concept_agents_desc",
    "ra_court_pos_open_view_desc",
    "game_concept_coronation_anointment_desc",
]

def search_in(base, lang_filter="spanish"):
    results = {}
    if not os.path.exists(base):
        return results
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.endswith(".yml") and lang_filter in f:
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, encoding="utf-8-sig", errors="replace") as fh:
                        for i, line in enumerate(fh, 1):
                            for k in KEYS:
                                if re.match(r"\s*" + re.escape(k) + r"\s*:", line):
                                    results.setdefault(k, []).append((fpath.replace("\\", "/"), i, line.strip()))
                except Exception:
                    pass
    return results

print("=" * 60)
print("RICERCA CHIAVI LOC NELLE FONTI DISPONIBILI")
print("=" * 60)

for repo_name, base in [("PATCH (spanish)", PATCH_LOC), ("OCR UPSTREAM (spanish)", OCR_LOC), ("VANILLA (spanish)", VANILLA_LOC)]:
    results = search_in(base)
    print(f"\n--- {repo_name} ---")
    for k in KEYS:
        if k in results:
            for path, ln, content in results[k]:
                rel = path.split("/localization/")[-1]
                print(f"  FOUND   | {k}")
                print(f"           File: {rel}  L{ln}")
                print(f"           Testo: {content[:150]}")
        else:
            print(f"  MISSING | {k}")

# Cerca anche la chiave watchman_guidance_modifier per capire il contesto IsFemale
print("\n\n=== CONTESTO COMPLETO watchman_guidance_modifier (vanilla all langs) ===")
for root, dirs, files in os.walk(VANILLA_LOC):
    for f in files:
        if f.endswith(".yml"):
            fpath = os.path.join(root, f)
            try:
                with open(fpath, encoding="utf-8-sig", errors="replace") as fh:
                    lines = fh.readlines()
                for i, line in enumerate(lines):
                    if re.match(r"\s*watchman_guidance_modifier\s*:", line):
                        start = max(0, i - 1)
                        end = min(len(lines), i + 3)
                        print(f"File: {fpath.replace(chr(92), '/')} L{i+1}")
                        for l in lines[start:end]:
                            print("  " + l.rstrip())
            except Exception:
                pass
