input = open('inputs/01', 'r').readlines()

x = 50
x_total = 50
N = 100

total = 0
total2 = 0

for line in input:
    if line[0] == '#':
        continue
    direction = dict(L=-1, R=+1)[line[0]]
    distance = int(line[1:])

    step = distance * direction
    x_old = x
    x = (x + step) % N

        
    if x == 0:
        total += 1

    N_cross = abs(step) // N
    step -= direction * N * N_cross
    if x_old > 0:
        N_cross += abs((x_old + step) // 100)
        if x_old + step == 0:
            N_cross += 1
    total2 += N_cross

    print(f"{line=} {total=} {total2=} {x=}")

print(total)
print(total2)
