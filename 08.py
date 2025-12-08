from collections import Counter
from math import prod

lines = [line.strip() for line in open('inputs/08', 'r').readlines()]
# lines = [line.strip() for line in open('inputs/08_example', 'r').readlines()]

inp = [tuple(int(x) for x in line.split(',')) for line in lines]

def dist(a, b):
    return sum((x - y)**2 for x, y in zip(a, b))

distances = [(dist(inp[i_a], inp[i_b]), (i_a, i_b))
             for i_a in range(len(inp))
             for i_b in range(i_a + 1, len(inp))]
distances = [x for x in distances if x[0] != 0]
distances = sorted(distances)

# poor-mans union-find without bothering to try to remember or to look up how it is done properly :D
circuits = [i for i in range(len(inp))]

def root(a, circuits):
    cur = a
    while circuits[cur] != cur:
        cur = circuits[cur]
    return cur

def connect(a, b, circuits):
    a_root = root(a, circuits)
    b_root = root(b, circuits)
    circuits[b_root] = a_root
    circuits[b] = a_root
    return circuits

for iter_i, (dist, (i_a, i_b)) in enumerate(distances):
    if iter_i == 1000:
        circuits = [root(x, circuits) for x in circuits]
        counts = Counter(circuits)
        part1 = prod(count for val, count in counts.most_common(3))
        print(part1)

    a = inp[i_a]
    b = inp[i_b]

    circuits = connect(i_a, i_b, circuits)
    circuits = [root(x, circuits) for x in circuits]
    if len(Counter(circuits)) == 1:
        print(a[0] * b[0])
        break
