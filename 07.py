from collections import defaultdict

lines = [line.strip() for line in open('inputs/07', 'r').readlines()]
# lines = [line.strip() for line in open('inputs/07_example', 'r').readlines()]

part1 = 0
part2 = 0

# start = lines[0].index('S')
beams = {lines[0].index('S'): 1}

for line in lines[1:]:
    new_beams = defaultdict(int)
    for position, count in beams.items():
        if line[position] == '^':
            new_beams[position - 1] += count
            new_beams[position + 1] += count
            part1 += 1
        else:
            new_beams[position] += count

    beams = new_beams

part2 = sum(count for position, count in beams.items())

print(part1)
print(part2)
