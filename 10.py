from copy import deepcopy
from collections import deque
import numpy as np
import pulp

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

    N_buttons = len(buttons)
    N_lights = len(target_state)
    A = np.zeros((N_lights, N_buttons), dtype=np.int32)
    for i, button in enumerate(buttons):
        A[button, i] = 1
    b = np.array(target_state)

    # print(f"{A=}")
    # print(f"{b=}")

    prob = pulp.LpProblem("ILP", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", range(N_buttons), lowBound=0, cat="Integer")

    prob += pulp.lpSum([x[i] for i in range(N_buttons)])
    for j in range(N_lights):
        prob += pulp.lpSum(A[j, i] * x[i] for i in range(N_buttons)) == b[j]
    # prob.solve()
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    # print("Status:", pulp.LpStatus[prob.status])
    # for i in range(N_buttons):
    #     print(f"x[{i}] =", x[i].value())

    part2 += pulp.value(prob.objective)
print(part2)
