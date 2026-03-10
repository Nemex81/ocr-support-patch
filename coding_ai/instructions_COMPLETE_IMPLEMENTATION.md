# GITHUB COPILOT AGENT: COMPLETE IMPLEMENTATION SPECIFICATION
## Dual-Mode Combat Window - CK3 1.17.1 Phase 3

**Date**: 2026-01-07  
**Status**: ✅ PRODUCTION READY  
**For**: GitHub Copilot Coding Agent  
**Duration**: ~6 hours  
**Deliverable**: window_combat.gui + 8 commits + full traceability  

---

# TABLE OF CONTENTS

1. [EXECUTIVE SUMMARY](#executive-summary)
2. [YOUR MISSION](#your-mission)
3. [ARCHITECTURE OVERVIEW](#architecture-overview)
4. [8-COMMIT ROADMAP](#8-commit-roadmap)
5. [10 MANDATORY DESIGN PATTERNS](#10-mandatory-design-patterns)
6. [NON-NEGOTIABLE CONSTRAINTS](#non-negotiable-constraints)
7. [INCREMENTAL COMMIT STRATEGY](#incremental-commit-strategy)
8. [COMMIT MESSAGE TEMPLATE](#commit-message-template)
9. [VALIDATION CHECKLIST](#validation-checklist)
10. [COMMON PITFALLS](#common-pitfalls)
11. [REFERENCE: VANILLA vs OCR](#reference-vanilla-vs-ocr)
12. [ARCHITECTURAL DECISIONS](#architectural-decisions-q1-q11)
13. [PATTERN DETAILS & EXAMPLES](#pattern-details--examples)
14. [PROGRESS TRACKING](#progress-tracking)
15. [TROUBLESHOOTING](#troubleshooting)
16. [SUCCESS CRITERIA](#success-criteria)

---

# EXECUTIVE SUMMARY

## What You're Building
A single `window_combat.gui` file with **dual rendering paths**:
- **VANILLA MODE** (default): Identical to CK3 baseline (portraits, animations, glow)
- **ACCESSIBILITY MODE** (Shift+F11 toggle): Text-only, screen-reader friendly (WCAG 2.1 AA)

## Success Criteria
✅ Vanilla parity: 100% pixel-perfect vs baseline  
✅ Accessibility completeness: 100% (all elements have text)  
✅ FPS delta: < 5% (both modes)  
✅ Memory delta: < +5% (accessibility vs vanilla)  
✅ Zero console errors  
✅ Hotkey toggle: Smooth (< 200ms lag)  
✅ 8 incremental commits with full traceability  
✅ All 10 design patterns followed  

## Timeline
**Estimated**: 6 hours total  
**Target Date**: 2026-01-08 (end of day)  
**Breakdown**: ~30 min per small section, ~1 hour per complex section, ~1 hour for integration  

---

# YOUR MISSION

## 120-Second Overview

You must implement a **single window_combat.gui** that seamlessly renders two visual modes:

**MODE 1 - VANILLA** (Default, active by default)
- Portraits with images (2x portrait_body)
- Animated progress bars with glow effects
- Full command UI with animations
- **Requirement**: 100% identical to CK3 baseline (zero changes)
- **Validation**: Pixel-perfect visual comparison

**MODE 2 - ACCESSIBILITY** (Toggle with Shift+F11)
- Text labels instead of images
- No animations (cognitive load reduction)
- Screen-reader friendly (WCAG 2.1 AA)
- Retreat UI (accessibility-only feature)
- **Requirement**: 100% complete (all elements have text)
- **Validation**: NVDA screen reader test pass

**ARCHITECTURE**: Single file, blockoverride branching, shared state machine

**DELIVERY**: 8 incremental commits (1-3 sections per commit) with full traceability

---

# ARCHITECTURE OVERVIEW

## Core Pattern: Blockoverride Branching

```guiscript
# VANILLA baseline (default, skeleton):
window = {
    name = "combat_window"
    state = { name = "_show" }  # SHARED state machine
    
    widget = {
        vbox = {
            # SECTION 1: PORTRAIT
            block "portrait_section_vanilla" {
                # Default: vanilla rendering (2x portrait_body)
            }
            
            block "portrait_section_accessibility" {
                # Default: empty (hidden)
            }
            
            # SECTION 2: PROGRESS BAR
            block "combat_progress_vanilla" {
                # Default: animated progressbar
            }
            
            block "combat_progress_accessibility" {
                # Default: empty (hidden)
            }
            
            # ... repeat for all sections
        }
    }
}

# ACCESSIBILITY TEMPLATE OVERRIDE:
types CombatWindow {
    type combat_window_accessibility = window_combat {
        # Hide vanilla sections
        blockoverride "portrait_section_vanilla" {}
        
        # Show accessibility sections
        blockoverride "portrait_section_accessibility" {
            hbox = {
                text_single = { raw_text = "Commander: [Name]" }
            }
        }
        
        # Repeat for all sections...
    }
}
```

**How it works**:
1. **Vanilla mode** (default): All `_vanilla` blocks active, `_accessibility` blocks hidden
2. **Accessibility mode** (Shift+F11): All `_vanilla` blocks hidden/empty, `_accessibility` blocks active
3. **State machine**: Shared by both modes (same events, same triggers)
4. **Toggle**: `GetVariableSystem.Exists('accessibility_mode')` via Shift+F11

---

# 8-COMMIT ROADMAP

## Implementation Sequence (Critical Path)

### COMMIT 1: Scaffolding + State Machine (30 min)
**Sections**: Framework setup

**Changes**:
- Create window_combat.gui skeleton
- All block names pre-defined (portrait, progress, advantage, MAA, commanders, retreat)
- Implement shared state machine (_show, _hide, phase_change, new_battle_event)
- Add global accessibility_mode toggle handler
- Create template type CombatWindow (accessibility variant)

**Validation**:
```
[ ] File syntax valid (no parse errors)
[ ] State machine intact (all events fire)
[ ] Accessibility_mode toggle works (Shift+F11)
[ ] Console clean (no errors)
```

**Patterns Used**: Pattern 2, 6, 10

---

### COMMIT 2: Portrait Section (45 min)
**Sections**: Portrait rendering

**Changes**:
- block "portrait_section_vanilla" → 2x portrait_body (vanilla default)
- block "portrait_section_accessibility" → text labels (empty for now, filled in template)
- Datacontext preserved (no re-binding)
- Tooltips outside blockoverride

**Validation**:
```
[ ] Vanilla portrait identical to baseline (100%)
[ ] Accessibility portrait doesn't crash on toggle
[ ] Hotkey toggle smooth (< 200ms)
[ ] Console clean
[ ] FPS impact: < 1%
```

**Patterns Used**: Pattern 1, 2, 3, 5, 10

---

### COMMIT 3: Combat Progress Bar (30 min)
**Sections**: Progress bar rendering

**Changes**:
- block "combat_progress_vanilla" → progressbar with animation
- block "combat_progress_accessibility" → text percentage (static)
- Animation handler shared via state machine (Pattern 6)
- Enum mapping consistent

**Validation**:
```
[ ] Vanilla progress bar animates smoothly
[ ] Accessibility shows static percentage
[ ] Hotkey toggle smooth
[ ] Console clean
[ ] FPS impact: < 2%
```

**Patterns Used**: Pattern 1, 2, 4, 6, 10

---

### COMMIT 4: Advantage Section (45 min)
**Sections**: Advantage rendering (complex, conditional)

**Changes**:
- block "advantage_section_vanilla" → icon + text (conditional layout)
- block "advantage_section_accessibility" → text only (flattened)
- Enum mapping consistency (shared function, Pattern 8)
- Conditional logic without if/else (Pattern 4)

**Validation**:
```
[ ] Vanilla advantages display with icons correctly
[ ] Accessibility shows text alternatives
[ ] Enum mapping identical in both branches
[ ] Console clean
[ ] FPS impact: < 2%
```

**Patterns Used**: Pattern 1, 2, 4, 8, 10

---

### COMMIT 5: MAA Section (1 hour)
**Sections**: Multiple Attribute Advantage (complex, nested)

**Changes**:
- block "maa_section_vanilla" → 2x progress bars with animations
- block "maa_section_accessibility" → text list (flattened, -40% nesting depth)
- Nesting flattening per Pattern 9
- Item template handling

**Validation**:
```
[ ] Vanilla MAA bars animated smoothly
[ ] Accessibility text list flat (no nested vbox/hbox/vbox)
[ ] Nesting verification: -40% depth reduction
[ ] Console clean
[ ] FPS impact: < 3%
```

**Patterns Used**: Pattern 1, 2, 4, 9, 10

---

### COMMIT 6: Commanders Section (1 hour)
**Sections**: Commander list rendering

**Changes**:
- block "commanders_section_vanilla" → item template with portraits
- block "commanders_section_accessibility" → item template with text names
- Item template inheritance (Pattern 3, 7)
- Data binding consistency

**Validation**:
```
[ ] Vanilla commanders show portraits + stats
[ ] Accessibility shows text names only
[ ] Item iteration works in both branches
[ ] Console clean
[ ] FPS impact: < 3%
```

**Patterns Used**: Pattern 1, 2, 3, 4, 7, 10

---

### COMMIT 7: Retreat Window (30 min)
**Sections**: Retreat UI (accessibility-only feature)

**Changes**:
- block "retreat_window" → accessibility-only feature
- Vanilla: retreat button only (simple)
- Accessibility: full retreat UI
- Feature parity with OCR mod

**Validation**:
```
[ ] Vanilla: retreat button visible (simple)
[ ] Accessibility: full retreat window visible
[ ] Feature hidden/shown correctly on toggle
[ ] Console clean
[ ] FPS impact: < 1%
```

**Patterns Used**: Pattern 1, 2, 4, 5, 10

---

### COMMIT 8: Final Integration + Hotkey Toggle (1 hour)
**Sections**: Integration & final validation

**Changes**:
- Link all sections to accessibility_mode toggle
- Add comprehensive comments (Pattern 10: split responsibility)
- Final validation (vanilla parity 100%, accessibility complete)
- Performance benchmark (FPS delta, memory delta)

**Validation**:
```
[ ] Vanilla parity: 100% pixel-perfect vs baseline
[ ] Accessibility completeness: 100%
[ ] Hotkey toggle (Shift+F11): Smooth < 200ms
[ ] Console clean: No errors/warnings
[ ] FPS delta: < 5%
[ ] Memory delta: < +5%
[ ] Screen reader compatible (NVDA test)
```

**Patterns Used**: All 10 patterns (final verification)

---

# 10 MANDATORY DESIGN PATTERNS

**CRITICAL**: Every line of code MUST follow one of these patterns. Pattern violations = automatic rejection.

## Pattern 1: Global Blockoverride Structure
**When**: Creating any dual-rendering section  
**Rule**: Always define `block "NAME_vanilla"` + `block "NAME_accessibility"` as pairs

```guiscript
# ✅ CORRECT
vbox = {
    block "portrait_section_vanilla" {
        # Vanilla rendering
    }
    block "portrait_section_accessibility" {
        # Accessibility rendering
    }
}

# ❌ WRONG - No paired blocks
vbox = {
    block "portrait_section" {
        # Only one block
    }
}
```

---

## Pattern 2: Visibility-Guarded Blockoverride
**When**: Toggling sections on/off based on accessibility_mode  
**Rule**: Use `visible = no` in blockoverride, NEVER use if/else

```guiscript
# ✅ CORRECT - Vanilla section empty when accessibility on
blockoverride "portrait_section_vanilla" {
    visible = no  # Controlled by template override
    hbox = {
        portrait_body = { ... }
    }
}

# ❌ WRONG - Using if/else logic in blockoverride
blockoverride "portrait_section_vanilla" {
    if = { trigger = { NOT = { scope:window.GetVariableSystem.Exists('accessibility_mode') } }
        # Can't do this in blockoverride
    }
}
```

---

## Pattern 3: Datacontext Preservation
**When**: Passing data down widget hierarchy  
**Rule**: Bind once at top, inherit down (no re-binding)

```guiscript
# ✅ CORRECT - Bind once, inherit
vbox = {
    datacontext = "[Character.GetPortrait(...)]"  # Bind ONCE
    
    block "portrait_vanilla" {
        # Use inherited datacontext
        image = { texture = "[GetRoot.GetPortraitPath(...)]" }
    }
    
    block "portrait_accessibility" {
        # Use same inherited datacontext
        text_single = { raw_text = "[Name]" }
    }
}

# ❌ WRONG - Re-binding creates memory leak
vbox = {
    block "portrait_vanilla" {
        datacontext = "[Character.GetPortrait(...)]"  # RE-BIND! BAD
        image = { ... }
    }
}
```

---

## Pattern 4: Conditional Blockoverride (NO if/else)
**When**: Rendering different widgets per branch  
**Rule**: Use blockoverride + visibility guards, NEVER if/else chains

```guiscript
# ✅ CORRECT
block "progress_vanilla" {
    progressbar = { ... }  # Always defined
}

block "progress_accessibility" {
    progressbar = { visible = no }  # Hidden when vanilla active
    text_single = { raw_text = "[Power]%" }
}

# ❌ WRONG - if/else in blockoverride
block "progress" {
    if = { trigger = { NOT = { GetVariableSystem.Exists(...) } }
        progressbar = { ... }
    }
    if = { trigger = { GetVariableSystem.Exists(...) }
        text_single = { ... }
    }
}
```

---

## Pattern 5: Tooltip Preservation
**When**: Adding tooltips to either branch  
**Rule**: Define tooltips OUTSIDE blockoverride, reference from both

```guiscript
# ✅ CORRECT
widget = {
    name = "progress_container"
    
    tooltip = {
        trigger_on_event = "focused"
        text = "Power: [Power]/[MaxPower]"
    }
    
    block "progress_vanilla" {
        progressbar = { ... }
    }
    
    block "progress_accessibility" {
        text_single = { raw_text = "[Power]/[MaxPower]" }
    }
}

# ❌ WRONG - Tooltip inside blockoverride
block "progress_vanilla" {
    progressbar = {
        tooltip = { text = "..." }  # Only in vanilla? Bad!
    }
}
```

---

## Pattern 6: State Machine Animation Handler
**When**: Triggering animations on state changes  
**Rule**: Use shared state machine + blockoverride handler

```guiscript
# SHARED STATE (outside blockoverride):
state = {
    name = "_show"
    next = "_combat_phase"
}

state = {
    name = "_combat_phase"
    on_start = "[ExecuteConsoleCommand('combat_ui_show')]"
}

# ✅ CORRECT (in template override):
blockoverride "animation_handler" {
    state = {
        name = "_show"
        animation = "animation_fade_in"  # Or "animation_none" in accessibility
    }
}

# ❌ WRONG - Trying to condition animation in main file
state = {
    name = "_show"
    animation = "[IF(GetVariableSystem.Exists(...)) animation_fade_in ... ]"  # Can't do this
}
```

---

## Pattern 7: Template Type Definition
**When**: Creating accessibility variant  
**Rule**: Define in types section, use blockoverride to override sections

```guiscript
# ✅ CORRECT
types CombatWindow {
    type combat_window_accessibility = window_combat {
        blockoverride "portrait_section_vanilla" {}  # Empty
        blockoverride "portrait_section_accessibility" {
            hbox = { text_single = { raw_text = "[Name]" } }
        }
        # ... repeat for all sections
    }
}

# ❌ WRONG - Trying to redefine entire widget tree
types CombatWindow {
    type combat_window_accessibility = window_combat {
        widget = { ... }  # This overrides, doesn't blockoverride!
    }
}
```

---

## Pattern 8: Enum Mapping Consistency
**When**: Using enum values (advantage types, MAA types, etc.)  
**Rule**: Use shared mapping function, same in both branches

```guiscript
# ✅ CORRECT - Shared function defined once
function get_advantage_label(type) = {
    if = { trigger = { advantage_type = hostile } text = "Hostile Advantage" }
    if = { trigger = { advantage_type = helpful } text = "Helpful Advantage" }
}

# Use in both vanilla and accessibility:
block "advantage_vanilla" {
    text_single = { raw_text = "[get_advantage_label(...)]" }
}

block "advantage_accessibility" {
    text_single = { raw_text = "[get_advantage_label(...)]" }
}

# ❌ WRONG - Different mappings per branch
block "advantage_vanilla" {
    text_single = { raw_text = "Advantage: [... + 1]" }
}
block "advantage_accessibility" {
    text_single = { raw_text = "Advantage: [...]" }  # Different output!
}
```

---

## Pattern 9: Flatten Nesting in Accessibility
**When**: Rendering accessibility branch  
**Rule**: -40% widget depth vs vanilla (flat structure for screen readers)

```guyscript
# ✅ CORRECT - Vanilla: nested (deeper)
block "commanders_vanilla" {
    vbox = {
        hbox = {
            portrait_body = { ... }
            vbox = {
                text = { raw_text = "[Name]" }
                text = { raw_text = "[Title]" }
            }
        }
    }
}

# ✅ CORRECT - Accessibility: flat (shallower)
block "commanders_accessibility" {
    vbox = {
        text_single = { raw_text = "[Name] - [Title]" }
    }
}

# ❌ WRONG - Accessibility still nested
block "commanders_accessibility" {
    vbox = {
        hbox = {
            vbox = {
                text = { raw_text = "[Name]" }
                text = { raw_text = "[Title]" }
            }
        }
    }
}
```

---

## Pattern 10: Split Responsibility (Code Organization)
**When**: Organizing file structure  
**Rule**: Group by section, comment each blockoverride, consistent naming

```guyscript
# ✅ CORRECT - Well organized with comments
window = {
    # ============================================
    # SECTION 1: PORTRAIT
    # ============================================
    # Renders commander portraits in vanilla mode
    # Renders commander name text in accessibility mode
    
    block "portrait_section_vanilla" {
        # Vanilla: 2x portrait_body side-by-side
        hbox = { ... }
    }
    
    block "portrait_section_accessibility" {
        # Accessibility: Text labels only (no images)
        hbox = { text_single = { raw_text = "[Name]" } }
    }
    
    # ============================================
    # SECTION 2: COMBAT PROGRESS
    # ============================================
    # Renders progress bar in vanilla mode
    # Renders percentage text in accessibility mode
    
    block "combat_progress_vanilla" { ... }
    block "combat_progress_accessibility" { ... }
}

# ❌ WRONG - No organization, no comments
window = {
    block "p1" { ... }
    block "p1a" { ... }
    block "p2" { ... }
    block "p2a" { ... }
}
```

---

# NON-NEGOTIABLE CONSTRAINTS

## Constraint 1: NO VANILLA CHANGES
- Vanilla rendering must be **100% identical** to baseline
- Do NOT fix vanilla bugs
- Do NOT optimize vanilla code
- Your job: Add accessibility alongside, not improve vanilla

## Constraint 2: NO BROWSER STORAGE APIs
- NO `localStorage`
- NO `sessionStorage`
- NO `document.cookie`
- NO `IndexedDB`
- **Use instead**: `GetVariableSystem.Set()` / `GetVariableSystem.Exists()`
- **Why**: Security error in CK3 sandbox

## Constraint 3: SINGLE FILE ONLY
- ONE window_combat.gui file
- NO separate accessibility file
- Blockoverride branching ONLY
- Target file size: 70-80 KB

## Constraint 4: 10 PATTERN COMPLIANCE
- All code must follow patterns (no variations)
- Pattern violations = automatic rejection
- Check patterns before coding

## Constraint 5: INCREMENTAL COMMITS (FULL TRACEABILITY)
- 1-3 sections per commit (NOT entire file at once)
- Each commit independently testable
- Commit message fills template
- Track in provided tracker

---

# INCREMENTAL COMMIT STRATEGY

## Commit Structure

Each commit = **1-3 complete sections** + full validation

**Requirements per commit**:
1. ✅ Vanilla branch renders correctly
2. ✅ Accessibility branch scaffolding present (may be empty)
3. ✅ No console errors
4. ✅ State machine intact
5. ✅ All blockoverride pairs defined

**Tests after each commit**:
```
[ ] Vanilla branch renders without errors
[ ] Accessibility branch doesn't crash
[ ] Shift+F11 toggle doesn't error
[ ] Console clean (no undefined references)
[ ] File valid Jomini syntax
[ ] FPS impact: < 5%
```

---

# COMMIT MESSAGE TEMPLATE

**Use this EXACT format for every commit**:

```
[COMMIT N] [SECTION NAME]: Implementation

SECTION: [Portrait | Progress | Advantage | MAA | Commanders | Retreat | Framework]

CHANGES:
├─ Added block "XXX_vanilla" with vanilla rendering
├─ Added block "XXX_accessibility" with accessibility rendering
├─ Total lines added: N
└─ Blockoverride pairs: N

PATTERNS USED:
├─ Pattern 1: [✓/✗]
├─ Pattern 2: [✓/✗]
├─ Pattern 3: [✓/✗]
├─ Pattern 4: [✓/✗]
├─ Pattern 5: [✓/✗]
├─ Pattern 6: [✓/✗]
├─ Pattern 7: [✓/✗]
├─ Pattern 8: [✓/✗]
├─ Pattern 9: [✓/✗]
└─ Pattern 10: [✓/✗]

VALIDATION:
├─ Vanilla parity: [✓ 100% / ⚠ X% / ✗ Issues: ___]
├─ Accessibility completeness: [✓ Full / ⚠ Partial / ✗ Missing]
├─ Hotkey toggle: [✓ Smooth / ⚠ Lag / ✗ Error]
├─ Console errors: [✓ None / ⚠ X errors]
├─ FPS impact: [✓ <1% / ⚠ 2-5% / ✗ >5%]
└─ Performance: [✓ On target / ⚠ Watch / ✗ Issue]

BLOCKERS:
├─ None
└─ [Or list any issues]

NEXT COMMIT: [SECTION NAME]
```

**Example (COMMIT 2 - Portrait)**:
```
[COMMIT 2] Portrait Section: Implementation

SECTION: Portrait

CHANGES:
├─ Added block "portrait_section_vanilla" (2x portrait_body side-by-side)
├─ Added block "portrait_section_accessibility" (text labels with names)
├─ Total lines added: 47
└─ Blockoverride pairs: 2

PATTERNS USED:
├─ Pattern 1: [✓] Global blockoverride structure
├─ Pattern 2: [✓] Visibility-guarded blockoverride
├─ Pattern 3: [✓] Datacontext preservation
├─ Pattern 4: [✓] Conditional blockoverride
└─ Pattern 5: [✓] Tooltip preservation

VALIDATION:
├─ Vanilla parity: [✓ 100%]
├─ Accessibility completeness: [⚠ Scaffolding]
├─ Hotkey toggle: [✓ Smooth]
├─ Console errors: [✓ None]
├─ FPS impact: [✓ <1%]
└─ Performance: [✓ On target]

BLOCKERS:
├─ None

NEXT COMMIT: Combat Progress Bar
```

---

# VALIDATION CHECKLIST

**Run this immediately after each commit. If ANY check fails: FIX IMMEDIATELY, DO NOT PROCEED.**

## File Syntax Validation
- [ ] File is valid Jomini GUI syntax (no parse errors)
- [ ] All blockoverride pairs defined (vanilla + accessibility for each section)
- [ ] No undefined variables or broken references
- [ ] State machine intact (no events broken)

## Vanilla Branch Validation
- [ ] Renders without console errors
- [ ] Visual output identical to baseline (pixel comparison)
- [ ] All animations smooth
- [ ] All tooltips working
- [ ] Enum mappings correct
- [ ] No performance regression

## Accessibility Branch Validation
- [ ] Doesn't crash when enabled (Shift+F11 toggle works)
- [ ] All visual elements have text alternative
- [ ] No animation flicker
- [ ] Text readable (high contrast assumed)
- [ ] Nesting simplified (-40% depth vs vanilla)

## Hotkey Toggle Validation
- [ ] Shift+F11 toggles accessibility_mode correctly
- [ ] Switch smooth (< 200ms lag)
- [ ] No console errors on toggle
- [ ] State machine intact after toggle

## Performance Validation
- [ ] FPS delta: < 5% (both branches)
- [ ] Memory delta: < +5% (accessibility vs vanilla)
- [ ] Load time: < 50ms additional
- [ ] No frame drops on toggle

## Code Quality Validation
- [ ] Follows all 10 design patterns
- [ ] Comments on each blockoverride section
- [ ] Consistent naming (XXX_vanilla, XXX_accessibility)
- [ ] No code duplication
- [ ] DRY principle respected

---

# COMMON PITFALLS

## ❌ Pitfall 1: Using if/else in Blockoverride

```guyscript
# WRONG - Jomini doesn't support if/else in blockoverride chains properly
block "section" {
    if = { trigger = { NOT = { GetVariableSystem.Exists('accessibility_mode') } }
        # Vanilla rendering
    }
    if = { trigger = { GetVariableSystem.Exists('accessibility_mode') }
        # Accessibility rendering
    }
}

# CORRECT - Use separate blockoverride pairs
block "section_vanilla" {
    # Vanilla rendering (visible = no in accessibility template)
}

block "section_accessibility" {
    # Accessibility rendering (visible = no in vanilla)
}
```

---

## ❌ Pitfall 2: Re-binding Datacontext

```guyscript
# WRONG - Re-binding creates memory leak
widget = {
    datacontext = "[Scope1]"
    
    vbox = {
        datacontext = "[Scope2]"  # RE-BIND = memory leak
    }
}

# CORRECT - Inherit from parent
widget = {
    datacontext = "[Scope1]"
    
    vbox = {
        # Use datacontext inherited from parent
    }
}
```

---

## ❌ Pitfall 3: Large Blockoverride Chains

```guyscript
# WRONG - Too complex, hard to debug
block "section_vanilla" {
    if = { condition1 ... }
    if = { condition2 ... }
    if = { condition3 ... }
    # What's being rendered?
}

# CORRECT - Simple, clear rendering (one responsibility)
block "section_vanilla" {
    # Single, clear rendering path
}
```

---

## ❌ Pitfall 4: Accessing Browser APIs

```guyscript
# WRONG - Will crash in CK3 sandbox
script = """
    localStorage.setItem('accessibility_mode', 'true');
"""

# CORRECT - Use CK3 safe API
script = """
    GetVariableSystem.Set('accessibility_mode', 'true');
"""
```

---

## ❌ Pitfall 5: Committing Entire File at Once

```
# WRONG - All sections in one commit
[COMMIT 1] Complete Implementation
├─ All 8 sections implemented
├─ Lines added: 1234
└─ Status: [✓ Pass]

# CORRECT - Incremental sections
[COMMIT 1] Scaffolding + State Machine
[COMMIT 2] Portrait Section
[COMMIT 3] Combat Progress Bar
[COMMIT 4] Advantage Section
[COMMIT 5] MAA Section
[COMMIT 6] Commanders Section
[COMMIT 7] Retreat Window
[COMMIT 8] Final Integration
```

---

# REFERENCE: VANILLA vs OCR

## Portrait Section (Vanilla)

Expected vanilla implementation:
```guyscript
block "portrait_section_vanilla" {
    hbox = {
        portrait_body = {
            name = "commander_1"
            portrait_texture = "[Attacker.GetPortraitPath('camera', 'show_full')]"
            portrait_scale = 1.0
        }
        
        portrait_body = {
            name = "commander_2"
            portrait_texture = "[Defender.GetPortraitPath('camera', 'show_full')]"
            portrait_scale = 1.0
        }
    }
}
```

Accessibility alternative:
```guyscript
block "portrait_section_accessibility" {
    hbox = {
        text_single = {
            raw_text = "Attacker: [Attacker.GetName]"
        }
        text_single = {
            raw_text = "Defender: [Defender.GetName]"
        }
    }
}
```

---

## Progress Bar Section (Vanilla)

Expected vanilla implementation:
```guyscript
block "combat_progress_vanilla" {
    progressbar = {
        min = 0
        max = "[SideB.MaxPower]"
        value = "[SideB.Power]"
        
        state = {
            name = "_show"
            animation = "animation_fade_in"
        }
    }
}
```

Accessibility alternative:
```guyscript
block "combat_progress_accessibility" {
    hbox = {
        text_single = {
            raw_text = "Power: [SideB.Power]/[SideB.MaxPower]"
        }
    }
}
```

---

# ARCHITECTURAL DECISIONS (Q1-Q11)

## Q1: Global Toggle (Shift+F11)
**Decision**: Use `GetVariableSystem.Exists('accessibility_mode')` for toggle  
**Why**: Standard CK3 approach, reliable, no storage issues  
**Impact**: Hotkey Shift+F11 triggers toggle consistently  

## Q2: Shared State Machine
**Decision**: Both modes use same state machine, only visual rendering differs  
**Why**: Zero event desync risk, perfect synchronization  
**Impact**: Events fire in both branches simultaneously  

## Q3: Portrait visible=false
**Decision**: In accessibility mode, set portrait visible=false (always in DOM)  
**Why**: Safety-first (no crash risk), minimal GPU overhead  
**Impact**: GPU memory +1-2 MB (negligible)  

## Q4: Identical Enum Mapping
**Decision**: No vanilla corrections, preserve vanilla bugs  
**Why**: Vanilla logic preserved, OCR mod responsibility  
**Impact**: Perpetuates existing vanilla bugs (acceptable)  

## Q5: Retreat Accessibility-Only
**Decision**: Retreat UI only in accessibility mode  
**Why**: Feature parity with OCR mod  
**Impact**: Vanilla players get no retreat UI (by design)  

## Q6: Single vbox + blockoverride
**Decision**: One main vbox with named blockoverride sections  
**Why**: Maintainability, single source of truth  
**Impact**: Large blockoverride list (manageable with patterns)  

## Q7: Single Datamodel
**Decision**: One datamodel, toggle item template rendering  
**Why**: Memory efficient, no data duplication  
**Impact**: Slightly more complex template inheritance  

## Q8: Shared Animation Trigger
**Decision**: State machine triggers both branches, blockoverride disables animation  
**Why**: Perfect synchronization, no event drift  
**Impact**: Requires state blockoverride mastery  

## Q9: Flatten Accessibility Nesting
**Decision**: -40% widget depth in accessibility mode  
**Why**: Screen reader friendly (semantic structure)  
**Impact**: Different DOM structure (acceptable for accessibility)  

## Q10: Debug Tooltip on Unknown Enum
**Decision**: Unknown enum shows "DEBUG: [enum_value]"  
**Why**: Modder bug discovery  
**Impact**: Small UX jank (acceptable for development)  

## Q11: Post-Implementation Benchmark
**Decision**: FPS/memory validation required before release  
**Why**: Performance guarantee  
**Impact**: Requires benchmark infrastructure  

---

# PATTERN DETAILS & EXAMPLES

## Pattern 1: Global Blockoverride Structure

**Full Example**:
```guyscript
window = {
    name = "combat_window"
    
    widget = {
        vbox = {
            # Portrait
            block "portrait_section_vanilla" {
                hbox = {
                    portrait_body = { ... }
                }
            }
            
            block "portrait_section_accessibility" {
                hbox = {
                    text_single = { raw_text = "Commander: [Name]" }
                }
            }
            
            # Progress
            block "combat_progress_vanilla" {
                progressbar = { ... }
            }
            
            block "combat_progress_accessibility" {
                text_single = { raw_text = "[Power]%" }
            }
        }
    }
}

# Template override for accessibility
types CombatWindow {
    type combat_window_accessibility = window_combat {
        blockoverride "portrait_section_vanilla" {}
        blockoverride "portrait_section_accessibility" {
            hbox = { text_single = { raw_text = "Commander: [Name]" } }
        }
        
        blockoverride "combat_progress_vanilla" {}
        blockoverride "combat_progress_accessibility" {
            text_single = { raw_text = "[Power]%" }
        }
    }
}
```

---

## Pattern 2: Visibility-Guarded Blockoverride

**Full Example**:
```guyscript
# In accessibility template override:
blockoverride "portrait_section_vanilla" {
    visible = no  # Hidden when accessibility template active
    hbox = {
        portrait_body = { ... }
    }
}

blockoverride "portrait_section_accessibility" {
    visible = no  # Hidden in vanilla (default empty anyway)
    hbox = {
        text_single = { raw_text = "Commander: [Name]" }
    }
}
```

---

## Pattern 3: Datacontext Preservation

**Full Example**:
```guyscript
widget = {
    vbox = {
        datacontext = "[Character.GetPortrait(...)]"  # Bind ONCE here
        
        block "portrait_vanilla" {
            # Inherited datacontext from parent vbox
            image = {
                texture = "[GetRoot.GetPortraitPath(...)]"
            }
        }
        
        block "portrait_accessibility" {
            # Same inherited datacontext
            text_single = {
                raw_text = "[Name]"
            }
        }
    }
}
```

---

## Pattern 4: Conditional Blockoverride

**Full Example**:
```guyscript
block "advantage_section_vanilla" {
    hbox = {
        icon = {
            visible = "[SideA.HasAdvantage]"
            texture = "[GetAdvantageIcon]"
        }
        text_single = {
            raw_text = "[AdvantageType]"
        }
    }
}

block "advantage_section_accessibility" {
    hbox = {
        text_single = {
            raw_text = "[IF(SideA.HasAdvantage) AdvantageType ELSE 'No advantage']"
        }
    }
}
```

---

# PROGRESS TRACKING

## Track in Real-Time

Use this template (fill in after each commit):

```
OVERALL PROGRESS: X/8 commits (X%)

COMMIT 1: Scaffolding .................. [ ] 0%
COMMIT 2: Portrait ..................... [ ] 0%
COMMIT 3: Progress Bar ................. [ ] 0%
COMMIT 4: Advantage .................... [ ] 0%
COMMIT 5: MAA .......................... [ ] 0%
COMMIT 6: Commanders ................... [ ] 0%
COMMIT 7: Retreat ...................... [ ] 0%
COMMIT 8: Integration .................. [ ] 0%

QUALITY METRICS:
├─ Pattern compliance: 0%
├─ Vanilla parity: 0%
├─ Accessibility completeness: 0%
├─ Console errors: 0
└─ Performance impact: 0%
```

---

# TROUBLESHOOTING

## Problem: Console Error
**Solution**:
1. Check error message in console
2. Look up undefined reference
3. Check combat_window_analysis.md for correct structure
4. Fix and re-validate

---

## Problem: Vanilla Rendering Different from Baseline
**Solution**:
1. Screenshot both vanilla and baseline
2. Compare pixel-by-pixel
3. Check combat_window_analysis.md § VANILLA BREAKDOWN
4. Identify difference
5. Restore vanilla logic

---

## Problem: FPS Drop > 5%
**Solution**:
1. Profile the section (which block is costly?)
2. Check for excessive animation handlers
3. Verify no re-binding of datacontext
4. Check for hidden particle effects
5. Optimize and re-benchmark

---

## Problem: Hotkey Toggle Lag
**Solution**:
1. Check GetVariableSystem.Set/Exists calls
2. Verify toggle trigger is instant
3. Check for heavy state machine transitions
4. Reduce animation complexity in accessibility mode
5. Test toggle speed again

---

## Problem: Pattern Violation
**Solution**:
1. Identify which pattern violated
2. Read pattern details (§ above)
3. Compare against correct example
4. Refactor code to match pattern
5. Re-validate

---

## Problem: Stuck on Syntax
**Solution**:
1. Check combat_window_analysis.md for similar code
2. Compare line-by-line
3. Look for missing brackets, commas, quotes
4. Check Jomini GUI documentation
5. Test in CK3 with console open

---

# SUCCESS CRITERIA

## Final Deliverable (After All 8 Commits)

### Code Delivery
✅ window_combat.gui (final file, 70-80 KB)  
✅ 8 git commits (each with full message template)  
✅ Complete git history (shows incremental work)  

### Functional Delivery
✅ Vanilla parity: 100% pixel-perfect vs baseline  
✅ Accessibility completeness: 100% (all elements have text)  
✅ Hotkey toggle: Smooth (< 200ms lag on Shift+F11)  
✅ Screen reader compatible (NVDA test pass)  

### Quality Delivery
✅ Pattern compliance: 100% (all 10 patterns used correctly)  
✅ Code duplication: 0% (DRY principle)  
✅ Comments: 100% on blockoverride sections  
✅ Console errors: 0 (clean log)  

### Performance Delivery
✅ FPS delta: < 5% (both vanilla and accessibility)  
✅ Memory delta: < +5% (accessibility vs vanilla)  
✅ Load time delta: < 50ms  
✅ Performance benchmark: Complete + documented  

### Documentation Delivery
✅ COMMIT_TRACKER_TEMPLATE filled in completely  
✅ All blockers documented + resolved  
✅ Final performance report complete  
✅ Known issues (if any) documented + resolved  

---

## Success Definition
```
✅ All above criteria met
= PRODUCTION READY
= PHASE 3 COMPLETE
= Ready for Phase 4 (Review & Test)
```

---

# QUICK START CHECKLIST

Before you start implementing:

- [ ] Read this entire document (120 min)
- [ ] Memorize 10 design patterns (§ PATTERNS section)
- [ ] Understand 8-commit sequence (§ 8-COMMIT ROADMAP)
- [ ] Understand validation checklist (§ VALIDATION CHECKLIST)
- [ ] Have commit message template ready (§ COMMIT MESSAGE TEMPLATE)
- [ ] Have progress tracker ready
- [ ] Git configured for commits
- [ ] CK3 development environment ready
- [ ] Console/debugger open
- [ ] Baseline (vanilla window_combat.gui) available for comparison

Status: ✅ **READY TO START COMMIT 1**

---

# TIMELINE

```
Est. 10:00 AM START
├─ 10:30 AM - COMMIT 1 done (Scaffolding) - 30 min
├─ 11:15 AM - COMMIT 2 done (Portrait) - 45 min
├─ 11:45 AM - COMMIT 3 done (Progress) - 30 min
├─ 12:30 PM - COMMIT 4 done (Advantage) - 45 min
├─ 1:00 PM - LUNCH BREAK
├─ 1:30 PM - COMMIT 5 done (MAA) - 1 hour
├─ 2:30 PM - COMMIT 6 done (Commanders) - 1 hour
├─ 3:30 PM - COMMIT 7 done (Retreat) - 30 min
├─ 4:00 PM - COMMIT 8 done (Integration) - 1 hour
├─ 5:00 PM - Final validation + documentation
└─ 5:30 PM - COMPLETE

TOTAL: ~6 hours (2026-01-08)
```

---

# FINAL REMINDERS

1. **PATTERNS ARE LAW** - Every line follows one of 10 patterns (no exceptions)
2. **INCREMENTAL COMMITS ONLY** - 1-3 sections per commit (never all at once)
3. **VANILLA PERFECT** - 100% parity vs baseline (zero changes)
4. **FULL TRACEABILITY** - Every commit tracked + validated + documented
5. **VALIDATION FIRST** - Always validate before proceeding to next commit
6. **RED FLAGS = STOP** - Fix immediately if any validation fails
7. **REFERENCE ALWAYS** - When stuck, check documentation
8. **PERFORMANCE MATTERS** - < 5% FPS delta is non-negotiable

---

# YOU'VE GOT THIS

You have:
✅ Clear mission (no ambiguity)  
✅ Locked architecture (no guessing)  
✅ Standardized patterns (no interpretation)  
✅ Atomic commits (no monolithic changes)  
✅ Validation gates (no surprises)  
✅ Full traceability (complete audit trail)  
✅ Complete reference docs (all context)  

This is **production-ready specification**.

Follow the spec. Follow the patterns. Validate at each step. Deliver production code.

**GO BUILD IT.** 🚀

---

**Version**: 1.0  
**Date**: 2026-01-07  
**Status**: PRODUCTION READY  
**For**: GitHub Copilot Agent  
**Classification**: IMPLEMENTATION SPECIFICATION (LOCKED)

---

*End of Complete Implementation Specification*

