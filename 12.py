import tqdm
from collections import deque
import numpy as np
from scipy.ndimage import label

lines = [line.strip() for line in open('inputs/12', 'r').readlines()]
# lines = [line.strip() for line in open('inputs/12_example', 'r').readlines()]

def repr_shape(shape):
    result = []
    for row in shape:
        row_res = []
        for x in row:
            row_res.append('#' if x else '.')
        result.append(''.join(row_res))
    return '\n'.join(result)

def all_transforms(shape):
    for k in range(4):
        rot = np.rot90(shape, k)
        yield rot
        yield np.fliplr(rot)

def place(shape, board, r_min, c_min):
    # if (r_min + shape.shape[0] - 1 >= board.shape[0]) or \
    #    (c_min + shape.shape[1] - 1 >= board.shape[1]):
    #     # 
    #     return None
    new_board = board.copy()
    target_view = new_board[r_min:r_min+shape.shape[0],
                            c_min:c_min+shape.shape[1]]
    if np.any(target_view[shape]):
        # something already placed there
        return None

    target_view[shape] = True
    return new_board

def component_sizes(binary):
    labeled, n = label(binary)
    # bincount: sizes of labels 1..n (ignore index 0)
    sizes = np.bincount(labeled.ravel())[1:]
    return sizes

def feasible(board, min_size, total_to_be_placed):
    empty_component_sizes = component_sizes(~board)
    usable_empty = sum(size for size in empty_component_sizes if size >= min_size)
    already_placed = np.sum(board)
    return usable_empty >= (total_to_be_placed - already_placed)

shapes = []
parsing_shapes = True
regions = []

shape = []
for line in lines:
    if len(line) == 0:
        shape = (np.array([list(row) for row in shape]) == '#')
        shapes.append(shape)
        shape = []
        continue
    if 'x' in line:
        parsing_shapes = False

    if parsing_shapes:
        if ':' in line:
            continue
        shape.append(line)
    else:
        size, quantities = line.split(':')
        size = tuple(int(x) for x in size.split('x'))
        quantities = np.array([int(x) for x in quantities.strip().split()])
        regions.append((size, quantities))

# print(shapes)
# print(regions)

min_size = min(np.sum(shape) for shape in shapes)

# diffs = []
# for size, quantities in regions:
#     total_to_be_placed = sum(count * np.sum(shape) for shape, count in zip(shapes, quantities))
#     board_size = size[0] * size[1]
#     diffs.append(board_size - total_to_be_placed)

# diffs = sorted(diffs)
# import matplotlib.pyplot as plt
# plt.plot(diffs)
# plt.grid()
# plt.show()

part1 = 0
for size, quantities in tqdm.tqdm(regions):
    board = np.zeros((size[0], size[1])) > 0

    total_to_be_placed = sum(count * np.sum(shape) for shape, count in zip(shapes, quantities))

    if total_to_be_placed > np.prod(board.shape):
        # definitely wont fit
        continue

    total_each_in_own_cell = sum(count * np.prod(shape.shape) for shape, count in zip(shapes, quantities))
    if np.prod(board.shape) >= total_each_in_own_cell:
        # definitely will fit
        part1 += 1
        continue

    q = deque([(board, quantities)])

    iter = 0
    while len(q) > 0:
        iter += 1
        cur_board, cur_quantities = q.pop()

        # if iter % 100 == 0:
        #     print(repr_shape(cur_board))
        #     print(cur_quantities)
        #     print()
        #     print()

        if np.all(cur_quantities == 0):
            part1 += 1
            break

        for i, orig_shape in enumerate(shapes):
            if cur_quantities[i] > 0:
                next_quantities = cur_quantities.copy()
                next_quantities[i] -= 1

                for shape in all_transforms(orig_shape):
                    for row in range(board.shape[0] - shape.shape[0] + 1):
                        for col in range(board.shape[1] - shape.shape[1] + 1):
                            next_board = place(shape, cur_board, row, col)
                            if next_board is not None and feasible(next_board, min_size, total_to_be_placed):
                                q.append((next_board, next_quantities))
print(part1)
                




