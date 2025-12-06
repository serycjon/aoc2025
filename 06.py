import numpy as np
lines = [line.rstrip('\n') for line in open('inputs/06', 'r').readlines()]
# lines = [line.rstrip('\n') for line in open('inputs/06_example', 'r').readlines()]

split = [line.split() for line in lines]

N_lines = len(lines)
N_cols = len(split[0])

fn = {'*': np.prod, '+': np.sum}

part1 = 0
for c in range(N_cols):
    nums = []
    for r in range(N_lines):
        x = split[r][c]
        try:
            nums.append(int(x))
        except ValueError:
            part1 += fn[x](nums)

print(part1)

operand_line = lines[-1]
pos_op = [(i, c) for i, c in enumerate(operand_line) if c!=" "] + [(len(operand_line) + 1 ,None)]

def extract_column(lines, col):
    column = ''.join(line[col] for line in lines[:-1])
    return int(column)

part2 = 0
for op_i, (start_i, op) in enumerate(pos_op):
    if op is None:
        break
    end_i = pos_op[op_i + 1][0] - 2
    # print(start_i, end_i, op)

    nums = [extract_column(lines, col) for col in range(start_i, end_i + 1)]
    part2 += fn[op](nums)

print(part2)
