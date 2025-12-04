input = [line.strip() for line in open('inputs/04', 'r').readlines()]
# input = [line.strip() for line in open('inputs/04_example', 'r').readlines()]

map = {}
for r, line in enumerate(input):
    for c, x in enumerate(line):
        if x == '@':
            map[(r, c)] = 1

H = len(input)
W = len(input[0])

# directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
directions = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if not (dr == dc == 0)]

part1 = 0

for r in range(H):
    for c in range(W):
        if map.get((r, c)):
            N_rolls = sum(map.get((r + dr, c + dc), 0) for dr, dc in directions)
            if N_rolls < 4:
                part1 += 1

part2 = 0
changed = True
while changed:
    changed = False
    for r in range(H):
        for c in range(W):
            if map.get((r, c)):
                N_rolls = sum(map.get((r + dr, c + dc), 0) for dr, dc in directions)
                if N_rolls < 4:
                    part2 += 1
                    changed = True
                    map[r, c] = 0
                
print(part1)
print(part2)
