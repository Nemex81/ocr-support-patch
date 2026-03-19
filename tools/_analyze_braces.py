import sys
fname = sys.argv[1]
lines = open(fname, encoding='utf-8').readlines()
depth = 0
for i, line in enumerate(lines, 1):
    depth += line.count('{') - line.count('}')
print(f"Profondita finale: {depth}")
print("--- Ultime 15 righe con profondita ---")
depth2 = 0
for i, line in enumerate(lines, 1):
    depth2 += line.count('{') - line.count('}')
    if i >= len(lines) - 14:
        print(f"L{i:3d} [d={depth2:2d}]: {line}", end='')
