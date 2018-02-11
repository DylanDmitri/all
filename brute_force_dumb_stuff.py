from math import e
from random import randint, choice

points = (
    (0, 0),
    (0.01511, 0.30979),
    (0.17319, 0.73769),
    (0.10007, 0.88269),
    (0.31383, 0.32418),
    (0.40694, 0.16674)
)


def fitness(c1, c2, c3):
    i = lambda t:-c1 * e ** (-c2 * t) + c1 * e ** (-c3 * t)

    return sum(
        abs(i(point[0]) - point[1]) for point in points
    )

def disp(c1, c2, c3):
    i = lambda t:-c1 * e ** (-c2 * t) + c1 * e ** (-c3 * t)

    for point in points:
        print(point[0], i(point[0]), 'supposed to be', point[1])

best = [1.9, 19.25616487510638, 4.9452077359810565]
best = [21.781856161399542, 10.579663347826669, 9.475618669486666]
disp(*best)
top = fitness(*best)

dist = (0, 1, 2)

while True:
    new = best[::]
    for _ in range(randint(1, 3)):
        new[choice(dist)] *= 1 + randint(-400,400) / 40000

    if fitness(*new) < top:
        top = fitness(*new)
        best = new
        print(best)
        print('fitness',fitness(*best))
        # disp(*best)
        print()


