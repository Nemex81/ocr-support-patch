#!/usr/bin/env python3
"""Verifica integrità strutturale dei file vanilla type-separated."""
import os, re

vanilla_dir = os.path.join('ocr_support_compatibility_pach', 'gui', 'vanilla')
files = sorted(os.listdir(vanilla_dir))

print(f'Files found: {len(files)}')
print('=' * 120)

summary_rows = []

for fname in files:
    fpath = os.path.join(vanilla_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    size_bytes = os.path.getsize(fpath)
    size_kb = size_bytes / 1024

    # 1. Brace count
    open_braces = content.count('{')
    close_braces = content.count('}')
    braces_ok = open_braces == close_braces

    # 2. Starts with types OCR_PATCH_VANILLA
    first_nonblank = ''
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            first_nonblank = stripped
            break
    starts_ok = 'types OCR_PATCH_VANILLA' in first_nonblank

    # 3. visible guard
    guard_pattern = re.findall(
        r"visible\s*=\s*\"\[GetVariableSystem\.Exists\(\s*'ocr'\s*\)\]\"",
        content
    )

    # 4. Forbidden properties inside type
    forbidden = {}
    forbidden_keys = ['state = {', 'widgetid =', 'layer =', 'attachto =', 'movable =']
    for prop in forbidden_keys:
        matches = []
        for i, line in enumerate(lines, 1):
            if prop in line:
                matches.append(i)
        if matches:
            forbidden[prop] = matches

    # 5. Unmatched quotes check
    unmatched_quotes = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        q_count = stripped.count('"')
        if q_count % 2 != 0:
            unmatched_quotes.append(i)

    # 6. Check brace nesting never goes negative
    depth = 0
    negative_depth_line = None
    for i, line in enumerate(lines, 1):
        for ch in line:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth < 0 and negative_depth_line is None:
                    negative_depth_line = i

    print(f'FILE: {fname}')
    print(f'  Size: {size_kb:.1f} KB ({size_bytes} bytes), Lines: {len(lines)}')
    print(f'  Braces: open={open_braces}, close={close_braces} -> {"OK" if braces_ok else "MISMATCH!"}')
    print(f'  Final depth: {depth}')
    if negative_depth_line:
        print(f'  WARNING: Negative brace depth first at line {negative_depth_line}')
    print(f'  Starts with types OCR_PATCH_VANILLA: {"YES" if starts_ok else "NO!"}')
    print(f'  First significant line: {first_nonblank[:80]}')
    print(f'  Visible guard count: {len(guard_pattern)}')
    if not guard_pattern:
        print(f'  WARNING: No visible guard found!')
    if forbidden:
        print(f'  FORBIDDEN properties found:')
        for prop, lns in forbidden.items():
            shown = lns[:10]
            extra = f'... (+{len(lns)-10} more)' if len(lns) > 10 else ''
            print(f'    "{prop}" at lines: {shown}{extra}')
    else:
        print(f'  Forbidden properties: NONE (OK)')
    if unmatched_quotes:
        shown = unmatched_quotes[:20]
        extra = f'... (+{len(unmatched_quotes)-20} more)' if len(unmatched_quotes) > 20 else ''
        print(f'  Unmatched quotes at lines: {shown}{extra}')
    else:
        print(f'  Unmatched quotes: NONE (OK)')

    # Summary status
    issues = []
    if not braces_ok:
        issues.append(f'BRACE MISMATCH ({open_braces} vs {close_braces})')
    if depth != 0:
        issues.append(f'FINAL DEPTH={depth}')
    if negative_depth_line:
        issues.append(f'NEG DEPTH@L{negative_depth_line}')
    if not starts_ok:
        issues.append('NO HEADER')
    if not guard_pattern:
        issues.append('NO GUARD')
    if forbidden:
        total_forbidden = sum(len(v) for v in forbidden.values())
        issues.append(f'FORBIDDEN({total_forbidden})')
    if unmatched_quotes:
        issues.append(f'QUOTES({len(unmatched_quotes)})')

    status = 'OK' if not issues else 'PROBLEMI'
    summary_rows.append((fname, f'{size_kb:.1f}KB', len(lines),
                         f'{open_braces}/{close_braces}', depth,
                         'Y' if starts_ok else 'N',
                         len(guard_pattern),
                         sum(len(v) for v in forbidden.values()),
                         len(unmatched_quotes),
                         status,
                         '; '.join(issues) if issues else ''))

    print(f'  STATUS: {status}' + (f' -> {"; ".join(issues)}' if issues else ''))
    print('-' * 120)

# Final summary table
print('\n\n===== TABELLA RIEPILOGATIVA =====\n')
header = f'{"File":<55} {"Size":>7} {"Lines":>6} {"{}":>7} {"Dep":>4} {"Hdr":>4} {"Grd":>4} {"Forb":>5} {"Quot":>5} {"Status":>10} Issues'
print(header)
print('-' * len(header) + '-' * 30)
for row in summary_rows:
    print(f'{row[0]:<55} {row[1]:>7} {row[2]:>6} {row[3]:>7} {row[4]:>4} {row[5]:>4} {row[6]:>4} {row[7]:>5} {row[8]:>5} {row[9]:>10} {row[10]}')

ok_count = sum(1 for r in summary_rows if r[9] == 'OK')
print(f'\nTotale: {ok_count}/{len(summary_rows)} file OK')
