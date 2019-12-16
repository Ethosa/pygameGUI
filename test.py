from random import randint
from pprint import pprint

size = 5

matrix = [tuple(randint(0, 9) for x in range(size)) for y in range(size)]
pprint(matrix)


def rotate90(matrix):
    return list(zip(*matrix[::-1]))

out = []
m = matrix[:]

for i in range(size):
    if i > 0:
        out.extend(m[-1][::-1])
    else:
        out.extend(m[0])
    m.pop(0)
    m = rotate90(m)

print(out)
