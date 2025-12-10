from copy import deepcopy
from collections import deque
import heapq

import tqdm

lines = [line.strip() for line in open('inputs/10', 'r').readlines()]
# lines = [line.strip() for line in open('inputs/10_example', 'r').readlines()]

def press(button, state):
    new_state = list(state)
    for i in button:
        new_state[i] = not new_state[i]
    return tuple(new_state)

def state_repr(state):
    return ''.join('#' if x else '.' for x in state)

part1 = 0
for line in lines:
    target_state, *buttons, joltage_requirements = line.split()
    target_state = tuple({'.': False, '#': True}[x] for x in target_state[1:-1])
    buttons = [tuple(int(x) for x in button.strip('()').split(','))
               for button in buttons]

    start = tuple(False for _ in target_state)
    visited = set()

    q = deque([(start, 0)])

    while len(q) > 0:
        cur_state, presses = q.popleft()
        # print(f'{state_repr(cur_state)} -- {state_repr(target_state)}')
        if cur_state == target_state:
            part1 += presses
            break
            
        if cur_state in visited:
            continue
        visited.add(cur_state)

        for button in buttons:
            q.append((press(button, cur_state), presses + 1))

print(part1)

def press2(button, state):
    new_state = list(state)
    for i in button:
        new_state[i] += 1
    return tuple(new_state)

def diff(a, target):
    return sum(tgt - x if tgt >= x else float('inf') for x, tgt in zip(a, target))

part2 = 0
for line in tqdm.tqdm(lines):
    target_state, *buttons, joltage_requirements = line.split()
    target_state = tuple(int(x) for x in joltage_requirements[1:-1].split(','))
    buttons = [tuple(int(x) for x in button.strip('()').split(','))
               for button in buttons]

    start = tuple(0 for _ in target_state)
    visited = {start: 0}
    # came_from = {}

    q = []
    heapq.heappush(q, (diff(start, target_state), start, 0))

    # iteration = 0
    while len(q) > 0:
        # iteration += 1
        # if iteration > 20:
        #     break
        score, cur_state, presses = heapq.heappop(q)
        # print(score, cur_state, presses)
        # print(f'{state_repr(cur_state)} -- {state_repr(target_state)}')
        if cur_state == target_state:
            part2 += presses
            break

        for button in buttons:
            new_state = press2(button, cur_state)
            new_cost = presses + 1
            if new_state not in visited or visited[new_state] > new_cost:
                visited[new_state] = new_cost
                new_score = new_cost + diff(new_state, target_state)
                heapq.heappush(q, (new_score, new_state, new_cost))
                # came_from[new_state] = (cur_state, button)
    
print(part2)
