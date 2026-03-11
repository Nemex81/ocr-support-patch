#!/usr/bin/env python3
"""
fix_faith_types.py — Risolve i placeholder TIPO_DA_VERIFICARE in window_faith.gui
"""
import re
from pathlib import Path

p = Path(__file__).parent.parent / "ocr_support_compatibility_pach" / "gui" / "window_faith.gui"

faith_map = {
    "FaithWindow.GetGroupingHelper": "GuiFaithDoctrineItem",
    "FaithWindow.GetHolySites": "GuiHolySiteItem",
    "FaithWindow.GetSins": "GuiVirtueOrSinItem",
    "FaithWindow.GetVirtues": "GuiVirtueOrSinItem",
    "GetGlobalList('faith_followers_sort')": "Scope",
    "FaithWindow.GetFaith.MakeScope.GetList('followers')": "Character",
    "Faith.MakeScope.GetList('faith_counties')": "Title",
    "Faith.MakeScope.GetList('wrong_counties')": "Title",
    "FaithWindow.GetFaith.MakeScope.GetList('adjacent_faiths')": "Faith",
    "ReligionWindow.GetOrderByOptions": "OrderFaithOption",
    "ReligionWindow.GetFaiths": "Faith",
}

lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
new_lines = []
fixed = 0
i = 0
RE_PLACEHOLDER = re.compile(r'^(\s*)# datamodel verificato: TIPO_DA_VERIFICARE\n?$')

while i < len(lines):
    line = lines[i]
    m = RE_PLACEHOLDER.match(line)
    if m and i + 1 < len(lines):
        next_line = lines[i + 1]
        indent = m.group(1)
        found_type = None
        for binding, tipo in faith_map.items():
            if binding in next_line:
                found_type = tipo
                break
        if found_type:
            new_lines.append(f"{indent}# datamodel verificato: {found_type}\n")
            fixed += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)
    i += 1

p.write_text("".join(new_lines), encoding="utf-8")
print(f"Fixed {fixed} placeholders in window_faith.gui")
