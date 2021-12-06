fn = 'aoc06_input_test.txt'
days = 256

with open(fn) as f:
    lines = f.readlines()

assert len(lines) == 1, f'found {len(lines)} lines'
line = lines[0]
if line.endswith('\n'):
    line = line[:-1]

counts_by_day = [0]*9
for val in line.split(','):
    counts_by_day[int(val)] += 1

for day in range(days):
    n_giving_birth = counts_by_day.pop(0)
    counts_by_day.append(n_giving_birth)  # newborns
    counts_by_day[6] += n_giving_birth  # recovering from giving birth

print('total number of fish:', sum(counts_by_day))
