import argparse
from time import time

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='aoc04_input_train.txt')
    return parser.parse_args()


def read_file(filename):
    print('parsing input...')
    with open(filename) as f:
        lines = f.readlines()

    number_line = lines.pop(0)[:-1]
    numbers = np.array([int(num) for num in number_line.split(',')])

    boards = []
    current_board = None
    i = 0
    for line in lines:
        if line == '\n':
            current_board = np.empty((5, 5), dtype=int)
            boards.append(current_board)
            i = 0
            continue

        current_board[i] = [int(num) for num in line[:-1].split()]
        i += 1

    boards = np.array(boards)
    print(f'read {len(numbers)} numbers')
    print(f'shape of bingo boards: {boards.shape}')
    return numbers, boards


def print_score(number, board, hits):
    unmarked_number_sum = np.sum(board * (1 - hits))
    print(f'sum: {unmarked_number_sum} * num: {number} = score: {unmarked_number_sum * number}')


def part_one_and_two(numbers, boards):
    # find out which board wins, also find out which board wins last
    # compute some score for those boards
    hits = np.full(boards.shape, fill_value=False, dtype=bool)
    boards_that_won = np.full(len(boards), fill_value=False, dtype=bool)
    for number in numbers:
        # mark hits
        hits |= boards == number

        # check if some board wins
        winners_rows = hits.all(axis=2).any(axis=-1)
        winners_cols = hits.all(axis=1).any(axis=-1)
        winners = winners_rows | winners_cols

        n_winners = winners.sum()
        if n_winners > boards_that_won.sum():  # we have a new winning board!
            winning_board = np.nonzero(np.bitwise_xor(winners, boards_that_won))
            boards_that_won = winners

            # print only first and last
            if n_winners == 1 or n_winners == 100:
                for board_idx in winning_board[0]:
                    print_score(number, boards[board_idx], hits[board_idx])


if __name__ == '__main__':
    args = parse_args()
    print(f'arguments:\n{vars(args)}')

    start_time = time()
    bingo_numbers, bingo_boards = read_file(args.file)
    read_time = time() - start_time
    part_one_and_two(bingo_numbers, bingo_boards)
    compute_time = time() - start_time - read_time

    print(f'it took {read_time*1000:.4f}ms to load & read the data')
    print(f'it took {compute_time*1000:.4f}ms to determine the scores')
    print(f'total time: {(read_time+compute_time)*1000:.4f}ms')
