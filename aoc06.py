import argparse
from time import time

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='aoc06_input_train.txt')
    parser.add_argument('--days', type=int, default=80)
    return parser.parse_args()


def read_file(filename):
    print('parsing input...')
    with open(filename) as f:
        lines = f.readlines()

    assert len(lines) == 1, f'found {len(lines)} lines'
    line = lines[0]
    if line.endswith('\n'):
        line = line[:-1]
    fish = np.array([int(val) for val in line.split(',')], dtype=np.uint8)

    print('initial state:', fish)
    print(f'found {len(fish)} fish on day 1, with initial states between {np.min(fish)} and {np.max(fish)}')
    return fish


def update_step(list_of_fish_arrays):
    spawn_fish = 0
    for fish_array in list_of_fish_arrays:
        reproducing = fish_array == 0
        spawn_fish += np.count_nonzero(reproducing)
        fish_array -= 1
        fish_array[reproducing] = 6  # time to recover from reproducing

    # add new array for spawned fish
    if spawn_fish > 0:
        list_of_fish_arrays.append(np.full(spawn_fish, fill_value=8, dtype=np.uint8))


def part_one(initial_fish, days=80):
    # keep track of every single fish
    # have list of arrays to avoid overhead of concatenating arrays, looping through lists should be cheap as have
    # at most `days` lists
    # still works reasonably only up until around 150 days, due to exponential growth of fish, resulting in
    # exponential growth of arrays
    list_of_fish_arrays = [initial_fish]
    for day in range(days):
        update_step(list_of_fish_arrays)

    total_num = 0
    for fish_array in list_of_fish_arrays:
        total_num += len(fish_array)

    print('total number of fish:', total_num)


def part_two(initial_fish, days=80):
    # fish only distinguish themselves by day, so aggregate them by days
    counts_by_day = [0]*9  # use list to be more flexible with shifting around elements
    vals, counts = np.unique(initial_fish, return_counts=True)
    for val, count in zip(vals, counts):
        counts_by_day[val] = count

    for day in range(days):
        n_giving_birth = counts_by_day.pop(0)
        counts_by_day.append(n_giving_birth)  # newborns
        counts_by_day[6] += n_giving_birth  # recovering from giving birth

    print('total number of fish:', sum(counts_by_day))


if __name__ == '__main__':
    args = parse_args()
    print(f'arguments:\n{vars(args)}')

    start_time = time()
    data = read_file(args.file)
    read_time = time() - start_time
    if args.days < 150:  # takes a lot of time otherwise
        part_one(data.copy(), args.days)
    compute_time = time() - start_time - read_time
    part_two(data, args.days)
    compute_time2 = time() - start_time - read_time - compute_time

    print(f'it took {read_time*1000:.4f}ms to load & read the data')
    print(f'it took {compute_time*1000:.4f}ms to compute')
    print(f'it took {compute_time2*1000:.4f}ms to compute with variant 2')
    print(f'total time: {(read_time+compute_time2)*1000:.4f}ms')
