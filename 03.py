import itertools
import tqdm

input = [line.strip() for line in open('inputs/03', 'r').readlines()]
# input = [line.strip() for line in open('inputs/03_example', 'r').readlines()]

part1 = 0
part2 = 0
for line in tqdm.tqdm(input):
    max = 0
    for i in range(len(line)):
        for j in range(i + 1, len(line)):
            num = int(line[i] + line[j])
            if num > max:
                max = num
    part1 += max

    int_line = [int(x) for x in line]
    prev = [int(x) for x in line]
    for start in range(12-1):
        max_prev = 0
        curr = []
        for i in range(len(prev)):
            if i < start:
                curr.append(0)
            else:
                curr.append(10 * max_prev + int_line[i])
            if prev[i] > max_prev:
                max_prev = prev[i]
        # print(' '.join(f'{x:05d}' for x in curr))
        prev = curr
    max2 = 0
    for x in curr:
        if x > max2:
            max2 = x
            
    part2 += max2
print(part1)
print(part2)
