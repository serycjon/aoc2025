from itertools import batched
import tqdm
input = [[int(x) for x in range.split('-')] for range in open('inputs/02', 'r').read().split(',')]
# input = [[int(x) for x in range.split('-')] for range in open('inputs/02_example', 'r').read().split(',')]

def has_digits_twice(x):
    for mult in range(1, 20):
        div = 10**mult
        left_part = x // div
        right_part = x % div
        if left_part < right_part:
            break
        if left_part == right_part and right_part >= div/10:
            return True
    return False

def has_digits_at_least_twice(x):
    sx = str(x)
    for period in range(1, (len(sx) // 2) + 1):
        parts = tuple(batched(sx, period))
        if all(x == parts[0] for x in parts):
            return True
    return False

# print(input)
part1 = 0
part2 = 0
for lb, ub in tqdm.tqdm(input):
    for x in range(lb, ub + 1):
        if has_digits_twice(x):
            part1 += x
        if has_digits_at_least_twice(x):
            part2 += x

print(part1)
print(part2)
