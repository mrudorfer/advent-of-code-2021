import argparse

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='aoc03_input_train.txt')
    return parser.parse_args()


def read_file(filename):
    with open(filename) as f:
        rows = []
        lines = f.readlines()

    for line in lines:
        if line.endswith('\n'):
            line = line[:-1]
        rows.append(np.array([int(val) for val in line], dtype=bool))
    data = np.array(rows)
    print(f'shape of input data: {data.shape}')
    return data


def binary_to_decimal(binary_array):
    # converts 1d-array with values of binary digits to a decimal number
    return binary_array.dot(1 << np.arange(len(binary_array))[::-1])


def part_one(data):
    # gamma rate: most common bit in each column (median)
    # epsilon rate: inverse binary number
    # power consumption is gamma rate * epsilon rate

    gamma = np.median(data, axis=0)
    epsilon = 1 - gamma

    print(f'gamma rate is {gamma} = {binary_to_decimal(gamma)}')
    print(f'epsilon rate is {epsilon} = {binary_to_decimal(epsilon)}')
    print(f'product is {binary_to_decimal(gamma)*binary_to_decimal(epsilon)}')


def part_two(data):
    # parse bitwise, follow pattern and discard numbers
    # oxygen generator rating: most common bit (or 1), discard numbers that deviate until only one left
    # CO2 scrubber rating: least common bit (or 0), discard numbers that deviate...

    oxygen_mask = np.full(len(data), fill_value=True, dtype=bool)
    oxygen_rating = None
    for i in range(data.shape[1]):
        oxygen_mask &= data[:, i] == np.ceil(np.median(data[oxygen_mask][:, i]))
        if np.count_nonzero(oxygen_mask) == 1:
            oxygen_rating = data[oxygen_mask].flatten()
            break

    co2_mask = np.full(len(data), fill_value=True, dtype=bool)
    co2_rating = None
    for i in range(data.shape[1]):
        co2_mask &= data[:, i] == 1 - np.ceil(np.median(data[co2_mask][:, i]))
        if np.count_nonzero(co2_mask) == 1:
            co2_rating = data[co2_mask].flatten()
            break

    print(f'oxygen rating: {oxygen_rating} = {binary_to_decimal(oxygen_rating)}')
    print(f'co2_rating: {co2_rating} = {binary_to_decimal(co2_rating)}')
    print(f'multiplied: {binary_to_decimal(oxygen_rating) * binary_to_decimal(co2_rating)}')


if __name__ == '__main__':
    args = parse_args()
    print(f'arguments:\n{vars(args)}')

    input_data = read_file(args.file)
    part_one(input_data)
    part_two(input_data)
