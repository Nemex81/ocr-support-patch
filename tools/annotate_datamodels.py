#!/usr/bin/env python3
"""
annotate_datamodels.py — Aggiunge annotazioni '# datamodel verificato: NomeTipo'
a tutte le righe `datamodel = "..."` nei file .gui della patch.

Esecuzione:
    python tools/annotate_datamodels.py
"""
import re
from pathlib import Path

GUI_DIR = Path(__file__).parent.parent / "ocr_support_compatibility_pach" / "gui"

# ---------------------------------------------------------------------------
# Mappatura binding → tipo verificato (da file vanilla + context items)
# ---------------------------------------------------------------------------
BINDING_TO_TYPE: dict[str, str] = {
    # hud.gui
    "DataModelLast(InGameTopbar.GetDiplomaticItems":     "DiplomaticItem",
    "DataModelLast(InGameTopbar.GetAlertItems":          "GUIAlertItem",
    "GetPlayer.GetAcceptedTaskContracts":                "TaskContract",
    "GetPlayer.GetSponsoredInspirations":                "Inspiration",
    "GetPlayer.GetFaith.GetDefensiveGreatHolyWars":      "GreatHolyWar",
    "GetPlayer.GetHostileRaiders":                       "Character",
    "GetPlayer.GetRaidTargets":                          "Character",
    "InGameBottomBar.GetWarItems":                       "WarItem",
    "InGameBottomBar.GetSchemes":                        "BottomBarSchemeItem",
    "GetPlayer.GetInvolvedSituations":                   "Situation",
    "GetPlayer.GetInvolvedStruggles":                    "Struggle",
    "GetPlayer.GetInterloperStruggles":                  "Struggle",
    "InGameBottomBar.GetEpidemicsInRealm":               "Epidemic",
    "InGameBottomBar.GetEpidemicsBorderingRealm":        "Epidemic",
    "InGameBottomBar.GetGlobalNotificationEpidemics":    "Epidemic",
    "LegitimacyType.GetLevels":                         "LegitimacyLevel",

    # window_county_view.gui
    "Province.MakeScope.GetList('sea_crossings')":              "Province",
    "Province.MakeScope.GetList('river_large_crossings')":      "Province",
    "Province.MakeScope.GetList('river_crossings')":            "Province",
    "HoldingView.GetCountyTitle.MakeScope.GetList('adjacent_seas')":    "Title",
    "HoldingView.GetCountyTitle.MakeScope.GetList('adjacent_rivers')":  "Title",
    "HoldingView.GetHoldingStatuses":                           "HoldingStatus",
    "HoldingView.GetBuildings":                                 "Building",
    "HoldingView.GetCountyTitle.MakeScope.GetList('county_holdings')":  "Title",
    "Scope.Province.MakeScope.GetList('buildings_ledger')":     "Building",
    "Scope.Province.MakeScope.GetList('duchy_building_ledger')":"Building",
    "HoldingView.GetCountyModifiers":                           "Modifier",
    "Title.MakeScope.GetList('adjacent_seas')":                 "Title",
    "Title.MakeScope.GetList('adjacent_rivers')":               "Title",
    "HoldingView.GetCountyTitle.MakeScope.GetList('adjacent_counties')":               "Title",
    "HoldingView.GetCountyTitle.MakeScope.GetList('adjacent_counties_2')":             "Title",
    "HoldingView.GetCountyTitle.MakeScope.GetList('adjacent_counties_3')":             "Title",
    "HoldingView.GetCountyTitle.MakeScope.GetList('adjacent_counties_across_water')":  "Title",
    "HoldingView.GetDeJureLieges":                              "Title",
    "HoldingView.GetCountyHoldings":                            "Title",
    "GetPlayer.MakeScope.GetList('province_regions')":          "Region",
    "HoldingView.GetPotentialBuildings":                        "Building",
    "GUITrackItem.GetPreLevelItems":                            "GUITrackLevelItem",
    "GUITrackItem.GetPostLevelItems":                           "GUITrackLevelItem",
    "HoldingView.GetHoldingTypeItems":                          "HoldingTypeItem",
    "DataModelFirst(Province.MakeScope.GetList('adjacent_seas')":    "Province",
    "DataModelFirst(Province.MakeScope.GetList('adjacent_rivers')":  "Province",
    "DataModelFirst(HoldingView.GetCountyTitle.MakeScope.GetList('adjacent_seas')":    "Title",
    "DataModelFirst(HoldingView.GetCountyTitle.MakeScope.GetList('adjacent_rivers')":  "Title",

    # window_my_realm.gui
    "GetAllVassalStances":                                      "VassalStance",
    "MyRealmWindow.GetRealmLaws":                               "GuiLawGroup",
    "GuiLawGroup.GetLaws":                                      "Law",
    "MyRealmWindow.GetDomainItems":                             "DomainItem",
    "DuchyGroup.GetCounties":                                   "CountyGroup",
    "CountyGroup.GetHoldings":                                  "Title",
    "CountyGroup.GetEmptyHoldings":                             "Title",
    "MyRealmWindow.GetGovernmentTypeFilters":                   "GovernmentTypeFilter",
    "MyRealmWindow.GetVassalStanceFilters":                     "VassalStanceFilter",
    "DataModelSubSpan( MyRealmWindow.GetVassals":               "Character",
    "CharacterSelectionList.GetList":                           "Character",
    "PageModelFive(CharacterSelectionList.GetList)":            "Character",
    "MyRealmWindow.GetMyPartitionShare":                        "PartitionShare",
    "MyRealmWindow.GetTitleSuccession":                         "TitleSuccessionItem",
    "TitleSuccessionItem.GetPartitionTitles":                   "Title",
    "TitleSuccessionItem.GetExceptionTitles":                   "Title",
    "MyRealmWindow.GetSuccessionExceptions":                    "SuccessionException",
    "MyRealmWindow.GetLineOfSuccession":                        "Character",
    "MyRealmWindow.GetTitlesCanVote":                           "Title",
    "GuiLawGroup.GetLaws":                                      "Law",
    "GetPlayer.MakeScope.GetList('special_buildings')":         "Building",
    "GetPlayer.MakeScope.GetList('build_farms')":               "Title",
    "GetPlayer.MakeScope.GetList('integrate_titles')":          "Title",
    "GetPlayer.MakeScope.GetList('low_control_counties')":      "Title",

    # window_military.gui
    "MilitaryView.GetRallyPoints":                              "RallyPointItem",
    "MilitaryItem.GetOwnedMaa":                                 "Regiment",
    "MilitaryView.GetEventTroops":                              "MilitaryViewEventTroop",
    "MilitaryView.GetHiredMercenaries":                         "HiredTroopItem",
    "HiredTroopItem.GetRegiments":                              "Regiment",
    "MilitaryView.GetHiredHolyOrders":                          "HiredTroopItem",
    "MilitaryView.GetAllMercenaries":                           "HiredTroopItem",
    "PageModelGlobal(MilitaryView.GetAllMercenaries)":          "HiredTroopItem",
    "MilitaryView.GetAllHolyOrders":                            "HiredTroopItem",
    "MilitaryView.GetAllHireableRulers":                        "HiredTroopItem",
    "GetPlayer.MakeScope.GetList('ongoing_wars')":              "War",
    "War.MakeScope.GetList('allies')":                          "Character",
    "MilitaryViewEventTroop.GetRegiments":                      "Regiment",
    "GetTraits":                                                "Trait",
    "MilitaryView.GetHeldTitleItems":                           "MilitaryItem",
    "MilitaryView.GetAllAdministrativeArmies":                  "HiredTroopItem",

    # window_intrigue.gui
    "SkillSchemeGroup.GetSchemes":                              "SchemeItem",
    "IntrigueWindow.GetKnownSchemes":                           "SchemeItem",
    "IntrigueWindow.GetMyHooks":                                "Hook",
    "IntrigueWindow.GetSecretsKnownToMe":                       "Secret",
    "IntrigueWindow.GetHooksOnMe":                              "Hook",
    "IntrigueWindow.GetMySecrets":                              "Secret",
    "IntrigueWindowSecretItem.GetKnownBy":                      "Character",
    "IntrigueWindowSecretGroup.GetSecrets":                     "Secret",
    "SchemeItem.GetAgentSlots":                                 "AgentSlot",
    "Scheme.GetModifiers":                                      "SchemeModifier",
    "IntrigueWindow.GetCountermeasures":                        "SchemeCountermeasureType",

    # window_inventory.gui
    "InventoryView.GetUniqueInventorySlotTypes":                "InventorySlotType",
    "InventoryView.GetArtifactSortOptions":                     "SortOption",
    "ArtifactClaimsList.GetSortOptions":                        "SortOption",
    "InventoryView.GetSortedArtifacts":                         "Artifact",
    "ArtifactClaimsList.GetClaims":                             "ArtifactClaim",
    "GetPlayer.MakeScope.GetList('all_artifacts')":             "Artifact",
    "PageModelGlobal(GetPlayer.MakeScope.GetList('all_artifacts'))": "Artifact",

    # window_court.gui
    "PageModel('court_window_page'":                            "Character",

    # window_activity_list.gui
    "ActivityListWindow.GetActivityGroupItems":                 "ActivityGroupItem",
    "ActivityGroupItem.GetActivities":                          "Activity",

    # window_character_lifestyle.gui
    "PerkGuiTree.GetItems":                                     "PerkGuiTreeItem",
    "CharacterLifestyleWindow.GetFocuses":                      "LifestyleFocus",
    "CharacterLifestyleWindow.GetLifestyles":                   "Lifestyle",
    "CharacterLifestyleWindow.GetPerkTrees":                    "PerkGuiTree",
    "PerkGuiTree.GetConnections":                               "PerkGuiConnection",

    # window_county_view.gui — PageModel variants (dynamic list names)
    "PageModel('province_region_page'":                         "Province",
    "GetPlayer.MakeScope.GetList(Concatenate(":                  "Province",
}


RE_DATAMODEL = re.compile(r'^(\s*)(datamodel\s*=\s*"[^"]*")\s*$')
RE_ALREADY_ANNOTATED = re.compile(r"#\s*datamodel\s+verificato\s*:", re.IGNORECASE)


def _find_type(value_str: str) -> str | None:
    """
    Cerca il tipo corrispondente al binding nel BINDING_TO_TYPE.
    Usa il matching per prefix per gestire binding lunghi/composti.
    """
    for prefix, tipo in BINDING_TO_TYPE.items():
        if prefix in value_str:
            return tipo
    return None


def annotate_file(path: Path) -> int:
    """
    Aggiunge annotazioni '# datamodel verificato: NomeTipo' alle righe datamodel.
    Restituisce il numero di righe annotate.
    """
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    annotate_count = 0
    new_lines = []

    for i, line in enumerate(lines):
        # Riga commentata → salta
        if line.lstrip().startswith("#"):
            new_lines.append(line)
            continue

        m = RE_DATAMODEL.match(line)
        if not m:
            new_lines.append(line)
            continue

        # Già annotata (inline o riga precedente)?
        preceding = lines[i - 1] if i > 0 else ""
        if RE_ALREADY_ANNOTATED.search(line) or RE_ALREADY_ANNOTATED.search(preceding):
            new_lines.append(line)
            continue

        tipo = _find_type(m.group(2))
        if tipo is None:
            # Tipo sconosciuto: aggiungi placeholder per segnalarlo
            tipo = "TIPO_DA_VERIFICARE"

        indent = m.group(1)
        annotation_line = f"{indent}# datamodel verificato: {tipo}\n"
        new_lines.append(annotation_line)
        new_lines.append(line)
        annotate_count += 1

    path.write_text("".join(new_lines), encoding="utf-8")
    return annotate_count


def main() -> None:
    gui_files = sorted(GUI_DIR.glob("*.gui"))
    total = 0
    for gui_file in gui_files:
        count = annotate_file(gui_file)
        if count:
            print(f"  {gui_file.name}: {count} righe annotate")
        else:
            print(f"  {gui_file.name}: nessuna nuova annotazione")
        total += count
    print(f"\nTotale annotazioni aggiunte: {total}")


if __name__ == "__main__":
    main()
