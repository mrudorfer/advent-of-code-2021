import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='aoc02_input_train.txt', help='input file, one number per line')
    parser.add_argument('--with_aim', action='store_true', default=False)
    return parser.parse_args()


def part_one(filename):
    depth, horizontal_pos = 0, 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            direction, num_str = line.split()
            num = int(num_str)
            if direction == 'forward':
                horizontal_pos += num
            elif direction == 'up':
                depth -= num
            elif direction == 'down':
                depth += num
            else:
                raise ValueError('unrecognized command')
    return depth, horizontal_pos


def part_two(filename):
    depth, horizontal_pos = 0, 0
    aim = 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            direction, num_str = line.split()
            num = int(num_str)
            if direction == 'forward':
                horizontal_pos += num
                depth += aim * num
            elif direction == 'up':
                aim -= num
            elif direction == 'down':
                aim += num
            else:
                raise ValueError('unrecognized command')
    return depth, horizontal_pos


if __name__ == '__main__':
    args = parse_args()
    print(f'arguments:\n{vars(args)}')

    if args.with_aim:
        d, h = part_two(args.file)
    else:
        d, h = part_one(args.file)

    print(f'final depth: {d}, horizontal position: {h}')
    print(f'multiplied: {d * h}')
