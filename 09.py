import tqdm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import shapely

coords = [tuple(int(x) for x in line.strip().split(",")) for line in open('inputs/09', 'r').readlines()]
# coords = [tuple(int(x) for x in line.strip().split(",")) for line in open('inputs/09_example', 'r').readlines()]

part1 = 0
for i_a, a in enumerate(coords):
    for b in coords[i_a + 1:]:
        area = abs(a[0] - b[0] + 1) * abs(a[1] - b[1] + 1)
        if area > part1:
            part1 = area

coords = np.array(coords)

print(part1)

# plot and see solution:
plt.plot(coords[:, 0], coords[:, 1], '.-')
# plt.axis('equal')
# plt.grid()
# plt.show()
a = (94710, 50238)
b = (4890, 67739)
plt.plot(a[0], a[1], 'r+')
plt.plot(b[0], b[1], 'r+')
part2 = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
print(part2)

def in_interval(x, a, b):
    a, b = min(a, b), max(a, b)
    return x > a and x < b

def point_inside(x, a, b):
    return in_interval(x[0], a[0], b[0]) and in_interval(x[1], a[1], b[1])

def plot_rectangle(a, b):
    ax = plt.gca()
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    width =  abs(a[0] - b[0])
    height = abs(a[1] - b[1])
    ax.add_patch(Rectangle((x, y), width, height, facecolor='r', alpha=0.5))

# pure python, with a bit of help with plot and see (for the horizontal indent)
if True:
    part2 = 0
    best = []
    for i_a, a in enumerate(tqdm.tqdm(coords)):
        for b in coords[i_a + 1:]:
            # hack from plot and see:
            if in_interval(48527, a[1], b[1]) or in_interval(50238, a[1], b[1]):
                continue
            fail = False
            for c in coords:
                if point_inside(c, a, b):
                    fail = True
                    break
            if fail:
                continue
            area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
            if area > part2:
                part2 = area
                best = [a, b]

    print(part2)
    plt.plot(best[0][0], best[0][1], 'bx')
    plt.plot(best[1][0], best[1][1], 'bx')

    plot_rectangle(best[0], best[1])

# full bruteforce with shapely
part2 = 0
best = []
poly = shapely.Polygon(coords)
for i_a, a in enumerate(tqdm.tqdm(coords)):
    for b in coords[i_a + 1:]:
        box = shapely.box(min(a[0], b[0]), min(a[1], b[1]),
                          max(a[0], b[0]), max(a[1], b[1]))
        if poly.contains(box):
            area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
            if area > part2:
                part2 = area
                best = [a, b]

print(part2)

plot_rectangle(best[0], best[1])
plt.axis('equal')
plt.grid()
plt.show()
