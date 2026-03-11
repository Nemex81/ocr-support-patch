"""
fix_remaining_types.py — Risolve tutti i placeholder TIPO_DA_VERIFICARE rimasti
nei file .gui della patch OCR.

Ogni binding è mappato al tipo Jomini corrispondente, verificato sui file vanilla
e upstream prima dell'annotazione.
"""

import os
import re
import sys

GUI_DIR = os.path.join(
    os.path.dirname(__file__), "..", "ocr_support_compatibility_pach", "gui"
)

# ---------------------------------------------------------------------------
# Mappa completa: stringa binding → tipo item Jomini
# Verificata sui file vanilla/upstream CK3 1.17.1
# ---------------------------------------------------------------------------
BINDING_TO_TYPE = {
    # --- interaction_blackmail.gui ---
    "BlackmailInteractionWindow.GetSecretItems": "BlackmailSecretItem",

    # --- interaction_menu_window.gui ---
    "CharacterInteractionMenuWindow.GetCategoryItems": "InteractionCategoryItem",
    "CharacterInteractionMenuWindow.GetMoreInteractions": "InteractionItem",

    # --- window_activity.gui ---
    "ActivityWindow.GetCharacters": "Character",
    "Character.GetCompletedIntents": "ActivityIntent",
    "Activity.GetPlannedPhases": "PlannedActivityPhase",
    "EventWindowData.GetOptions": "EventOption",

    # --- window_character.gui ---
    "CharacterWindow.GetSkills": "CharacterWindowSkillItem",
    "CharacterWindow.GetTimedModifiers": "ModifierItem",
    "CharacterWindow.GetParents": "Character",
    "CharacterWindow.GetGrandparents": "Character",
    "CharacterWindow.GetSecondarySpouses": "Character",
    "CharacterWindow.GetConcubines": "Character",
    "CharacterWindow.GetChildren": "Character",
    "CharacterWindow.GetSiblings": "Character",
    "CharacterWindow.GetTitles": "Title",
    "CharacterWindow.GetClaims": "Title",
    "CharacterWindow.GetDiplomacyItems": "DiplomacyItem",
    "GetNullCharacterDataModel": "Character",
    "CharacterSelectionList.GetList": "Character",
    "TraitArrays.GetPersonalityTraits": "Trait",
    "TraitArrays.GetTraits": "Trait",
    "TimedModifierPreviewList.GetItems": "TimedModifierPreviewItem",
    "TimedModifierScaledSingleItem.GetEffectItems": "CString",

    # --- window_combat.gui ---
    "CombatWindow.GetLeftCommanderTraits": "Trait",
    "CombatWindow.GetRightCommanderTraits": "Trait",
    "CombatWindow.GetLeftSideMaaTypes": "CombatMaaItem",
    "CombatWindow.GetRightSideMaaTypes": "CombatMaaItem",
    "CombatMaaItem.GetCounteredByMaa": "MenAtArmsType",
    "CombatMaaItem.GetCountersMaa": "MenAtArmsType",

    # --- window_council.gui ---
    "GuiCouncilPosition.GetPotentialCouncilTasks": "CouncilTask",
    "GuiCouncilPosition.GetSkillItems": "SkillItem",

    # --- window_culture.gui ---
    "CultureWindow.GetCultureTraditions": "GuiCultureTradition",
    "CultureWindow.GetCultureEras": "GuiCultureEra",
    "GuiCultureEra.GetCultureEraGroups": "GuiCultureEraGroup",
    "GuiCultureEraGroup.GetInnovations": "Innovation",

    # --- window_decisions.gui ---
    "DecisionsView.GetDecisionGroupItems": "DecisionGroupItem",
    "GetPlayer.GetAcceptedTaskContracts": "TaskContract",
    "DecisionGroupItem.GetDecisions": "Decision",

    # --- window_dynasty_house.gui ---
    "DynastyHouseView.GetHouseModifiers": "ModifierItem",
    "DynastyHouseView.GetHouseUnityModifiers": "ModifierItem",
    "DynastyHouseView.GetDynastyModifiers": "ModifierItem",
    "DynastyHouseView.GetLegacies": "DynastyLegacyItem",
    "DynastyHouseView.GetOrderOptions": "HouseOrderOption",
    "DynastyHouseView.GetDynastyHouses": "DynastyHouse",
    "DynastyHouseView.GetHouseUnityStages": "GUIHouseUnityStage",
    "DynastyHouseView.GetDynastyHouse.GetChangelog": "HouseUnityChangelogEntry",

    # --- window_factions.gui ---
    "FactionsWindow.GetTargetingFactions": "FactionItem",
    "FactionsWindow.GetCantCreateOrJoinFactionVassals": "Character",
    "FactionsWindow.GetJoinedFactions": "FactionItem",
    "FactionsWindow.GetJoinableFactions": "FactionItem",
    "FactionsWindow.GetCreateFactionItems": "CreateFactionItem",
    "FactionItem.GetCharacterMembers": "Character",
    "FactionItem.GetCountyMembers": "Title",

    # --- GetPlayer scope lists (culture/faith shared) ---
    "GetPlayer.MakeScope.GetList('cultures')": "Culture",
    "GetPlayer.MakeScope.GetList('culture_counties')": "Title",
    "Culture.MakeScope.GetList('culture_characters')": "Character",
    "Culture.MakeScope.GetList('adjacent_cultures')": "Culture",
    "Culture.MakeScope.GetList('wrong_counties')": "Title",

    # --- CharacterWindow.GetRelationsOfType (generico, catturato via regex) ---
    # gestito sotto con match parziale
}

# Bindings con pattern parziale (regex match sul valore datamodel)
PARTIAL_PATTERNS = [
    # CharacterWindow.GetRelationsOfType('qualsiasi_cosa')
    (re.compile(r"CharacterWindow\.GetRelationsOfType\("), "Character"),
    # DynastyHouseView.GetDecisions(qualsiasi argomento)
    (re.compile(r"DynastyHouseView\.GetDecisions\("), "Decision"),
    # DataModelSkipLast(DynastyHouseView.GetHouseUnityStages, ...)
    (re.compile(r"DataModelSkipLast\(\s*DynastyHouseView\.GetHouseUnityStages"), "GUIHouseUnityStage"),
    # DataModelFirst(DynastyHouseView.GetDynastyHouse.GetChangelog, ...)
    (re.compile(r"DataModelFirst\(\s*DynastyHouseView\.GetDynastyHouse\.GetChangelog"), "HouseUnityChangelogEntry"),
]

# ----------------------------------------------------------------------------

PLACEHOLDER = "TIPO_DA_VERIFICARE"
ANNOTATION_RE = re.compile(r"(#\s*datamodel\s+verificato\s*:\s*)" + re.escape(PLACEHOLDER), re.IGNORECASE)
DATAMODEL_RE = re.compile(r'datamodel\s*=\s*"\[([^\]]+(?:\([^)]*\))?[^\]]*)\]"')


def resolve_type(binding_value: str) -> str:
    """Restituisce il tipo Jomini per il binding, o None se sconosciuto."""
    # Ricerca esatta prima
    key = binding_value.strip()
    if key in BINDING_TO_TYPE:
        return BINDING_TO_TYPE[key]

    # Ricerca con pattern parziale
    for pattern, tipo in PARTIAL_PATTERNS:
        if pattern.search(key):
            return tipo

    return None


def process_file(filepath: str) -> int:
    """Processa un file .gui e sostituisce TIPO_DA_VERIFICARE dove possibile.
    Restituisce il numero di sostituzioni effettuate."""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    changed = 0
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Controlla se questa riga è un'annotazione con placeholder
        if ANNOTATION_RE.search(line):
            # Cerca il datamodel = nella riga successiva (salta righe vuote/commenti)
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1

            if j < len(lines):
                next_line = lines[j]
                dm_match = DATAMODEL_RE.search(next_line)
                if dm_match:
                    binding = dm_match.group(1).strip()
                    tipo = resolve_type(binding)
                    if tipo:
                        # Sostituisci il placeholder con il tipo corretto
                        line = ANNOTATION_RE.sub(
                            lambda m: m.group(1) + tipo,
                            line
                        )
                        changed += 1

        new_lines.append(line)
        i += 1

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    return changed


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    total = 0

    gui_files = (
        [os.path.join(GUI_DIR, target)] if target
        else [os.path.join(GUI_DIR, f) for f in os.listdir(GUI_DIR) if f.endswith(".gui")]
    )

    for path in sorted(gui_files):
        if not os.path.isfile(path):
            print(f"[SKIP] File non trovato: {path}")
            continue
        n = process_file(path)
        fname = os.path.basename(path)
        if n:
            print(f"[OK]   {fname}: risolti {n} placeholder")
        else:
            print(f"[--]   {fname}: nessun placeholder risolto")
        total += n

    print(f"\nTotale placeholder risolti: {total}")


if __name__ == "__main__":
    main()
