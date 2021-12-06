import argparse
from time import time

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='aoc05_input_train.txt')
    parser.add_argument('-s', '--straight_lines_only', action='store_true', default=False)
    return parser.parse_args()


def read_file(filename):
    print('parsing input...')
    with open(filename) as f:
        lines = f.readlines()

    line_segments = []
    for line in lines:
        line_elems = line.split()
        points = []
        for elem in [line_elems[0], line_elems[2]]:
            point = [int(val) for val in elem.split(',')]
            points.append(point)
        line_segments.append(points)

    line_segments = np.array(line_segments)
    print('line_segments:', line_segments.shape)
    print(f'1st: {line_segments[0, 0]} -> {line_segments[0, 1]}')

    return line_segments


def part_one_and_two(line_segments, straight_only):
    # size: find out size of area to consider, assume min_val = 0, only need to find max vals
    max_x = np.max(line_segments[:, :, 0])
    max_y = np.max(line_segments[:, :, 1])
    occurrences = np.zeros((max_x+1, max_y+1), dtype=int)
    print('determined shape:', occurrences.shape)

    if straight_only:
        # filter: horizontal/vertical lines
        straight = np.bitwise_or(line_segments[:, 0, 0] == line_segments[:, 1, 0],
                                 line_segments[:, 0, 1] == line_segments[:, 1, 1])
        print(f'only considering {np.count_nonzero(straight)} lines which are either horizontal or vertical')
        line_segments = line_segments[straight]

    for seg in line_segments:
        x1, x2 = seg[0, 0], seg[1, 0]
        y1, y2 = seg[0, 1], seg[1, 1]

        if x1 == x2:
            x_indices = x1
        else:
            sign_x = (x2-x1) // abs(x2-x1)
            x_indices = np.arange(x1, x2 + sign_x, sign_x)

        if y1 == y2:
            y_indices = y1
        else:
            sign_y = (y2 - y1) // abs(y2 - y1)
            y_indices = np.arange(y1, y2 + sign_y, sign_y)

        occurrences[x_indices, y_indices] += 1

    print(occurrences.T)
    print('places with more than two occurrences:', np.count_nonzero(occurrences >= 2))


if __name__ == '__main__':
    args = parse_args()
    print(f'arguments:\n{vars(args)}')

    start_time = time()
    segments = read_file(args.file)
    read_time = time() - start_time
    part_one_and_two(segments, args.straight_lines_only)
    compute_time = time() - start_time - read_time

    print(f'it took {read_time*1000:.4f}ms to load & read the data')
    print(f'it took {compute_time*1000:.4f}ms to compute')
    print(f'total time: {(read_time+compute_time)*1000:.4f}ms')
