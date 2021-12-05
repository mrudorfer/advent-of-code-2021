import argparse

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='aoc01_input.txt', help='path to input file, one number per line')
    parser.add_argument('--window', type=int, default=1, help='number of measurements to sum up for comparison')
    return parser.parse_args()


def count_increasing_measurements(measurements, window=1):
    increased = 0
    for i in range(len(measurements) - window):
        if measurements[i:i+window].sum() < measurements[i+1:i+1+window].sum():
            increased += 1

    print(f'number of measurements: {len(measurements)}')
    print(f'data points larger than previous: {increased}')


if __name__ == '__main__':
    args = parse_args()
    print(f'arguments:\n{vars(args)}')
    with open(args.file) as f:
        lines = f.readlines()
        int_lines = [int(line) for line in lines]
        count_increasing_measurements(np.array(int_lines), args.window)
