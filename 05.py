lines = [line.strip() for line in open('inputs/05', 'r').readlines()]
# lines = [line.strip() for line in open('inputs/05_example', 'r').readlines()]

ranges = []
ids = []
first_part = True
for line in lines:
    if len(line) == 0:
        first_part = False
        continue

    if first_part:
        lb, ub = [int(x) for x in line.split('-')]
        ranges.append((lb, ub))
    else:
        ids.append(int(line))

part1 = 0
part2 = 0

def in_range(x, lb, ub):
    return x >= lb and x <= ub

for id in ids:
    for lb, ub in ranges:
        if in_range(id, lb, ub):
            part1 += 1
            break

def union_intervals(intervals):
    intervals = sorted(intervals)

    union = []
    cur_lb, cur_ub = intervals[0]
    for lb, ub in intervals:
        if lb <= cur_ub:
            cur_ub = max(cur_ub, ub)
        else:
            union.append((cur_lb, cur_ub))
            cur_lb, cur_ub = lb, ub
        
    if union[-1] != (cur_lb, cur_ub):
        union.append((cur_lb, cur_ub))
    return union

for lb, ub in union_intervals(ranges):
    part2 += ub - lb + 1
                
print(part1)
print(part2)
