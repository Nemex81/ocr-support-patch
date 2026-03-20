# Domain boundaries (machine-readable)

framework:
  - path: ".github/"
  - path: "tools/"
  - examples:
    - ".github/instructions/"
    - ".github/agents/"
    - "tools/assemble_dualmode.py"

mod:
  - path: "ocr_support_compatibility_pach/"
  - examples:
    - "ocr_support_compatibility_pach/gui/"
    - "ocr_support_compatibility_pach/descriptor.mod"

workspace_roots:
  - path: "C:/Users/nemex/OneDrive/Documenti/GitHub/ocr-support-patch/"
    access: "read-write"
    note: "Scrittura consentita solo nei sottopercorsi autorizzati da patch-boundaries.instructions.md"
  - path: "C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/"
    access: "read-only"
  - path: "C:/Users/nemex/OneDrive/Documenti/GitHub/CK3-OCR/"
    access: "read-only"
  - path: "C:/Users/nemex/OneDrive/Documenti/Paradox Interactive/Crusader Kings III/logs/"
    access: "read-only"

operational_rules:
  - id: rule_not_touch_mod
    short: "non toccare la mod"
    description: "Se presente, NON modificare file sotto 'ocr_support_compatibility_pach/'. Operare solo nel dominio Framework (.github/, tools/)."
  - id: rule_check_framework
    short: "guarda nel framework"
    description: "Ispezionare o modificare file solo in .github/ e tools/. Non scrivere nella patch senza i checkpoint CP1/CP2 del workflow 'workflow-nuova-finestra.instructions.md'."
  - id: rule_patch_boundaries
    short: "patch-boundaries"
    description: "I percorsi scrivibili e vietati sono definiti in 'patch-boundaries.instructions.md'. Seguire sempre quelle regole."
  - id: rule_workspace_roots_access
    short: "workspace-roots-access"
    description: "Nel workspace multi-root, solo 'C:/Users/nemex/OneDrive/Documenti/GitHub/ocr-support-patch/' e' scrivibile; CK3 vanilla, CK3-OCR e logs sono sola lettura."

# Version
version: 1

# Note
# Questo file è una fonte machine-readable da usare da script/agent per decidere il dominio operativo.
