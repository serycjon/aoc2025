from collections import deque
import networkx as nx

input = {line.split(':')[0]: line.split(':')[1].strip().split() for line in open('inputs/11', 'r').readlines()}
# input = {line.split(':')[0]: line.split(':')[1].strip().split() for line in open('inputs/11_example', 'r').readlines()}

tmp = []
for src, dsts in input.items():
    for dst in dsts:
        tmp.append(f'{src} -> {dst};')
dot = 'digraph {\n'
for node in ['you', 'svr', 'dac', 'fft', 'out']:
    dot = dot + f'{node}[color=red];\n'
dot = dot + "\n".join(tmp)
dot = dot + "\n}\n"
with open('11.dot', 'w') as f:
    f.write(dot)

cur = "you"
visited = set()

q = deque()
q.append((cur, tuple([])))

part1 = 0
while len(q) > 0:
    cur, path = q.popleft()
    visited.add(path)

    if cur == "out":
        part1 += 1
        continue

    for neigh in input[cur]:
        new_path = list(path)
        new_path.append(neigh)
        new_path = tuple(new_path)
        if new_path not in visited:
            q.append((neigh, new_path))
print(part1)

# input = {line.split(':')[0]: line.split(':')[1].strip().split() for line in open('inputs/11_example_2', 'r').readlines()}
G = nx.DiGraph()
for src, dsts in input.items():
    G.add_edges_from([(src, dst) for dst in dsts])

order = list(nx.topological_sort(G))
topo = {node: i for i, node in enumerate(order)}

def find_paths(graph, src, dst, topo):
    count = 0
    
    cur = src
    visited = set()
    q = deque()
    q.append((cur, tuple([])))

    while len(q) > 0:
        cur, path = q.popleft()
        visited.add(path)

        if cur == dst:
            count += 1
            continue

        if topo[cur] > topo[dst]:
            continue

        for neigh in input[cur]:
            new_path = list(path)
            new_path.append(neigh)
            new_path = tuple(new_path)
            if new_path not in visited:
                q.append((neigh, new_path))
    return count

def find_paths_2(graph, src, dst, topo):
    # DP
    nodes = sorted(list(graph.keys()), key=lambda x: topo[x])
    dp = {node: 1 if node == src else 0
          for node in nodes + ['out']}
    for parent in nodes:
        for child in graph.get(parent, []):
            dp[child] += dp[parent]
    return dp[dst]

targets = ['svr', 'dac', 'fft', 'out']
targets = sorted(targets, key=lambda x: topo[x])

part2 = 1
for i in range(len(targets) - 1):
    src = targets[i]
    dst = targets[i + 1]
    count = find_paths_2(input, src, dst, topo)
    part2 *= count

print(part2)
