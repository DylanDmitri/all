from civsim.main import *
from copy import deepcopy

nice = Actor()
nice.nodes[0] = (0, 0, False)  # always redirect to self, mean=False

naughty = Actor()
naughty.nodes[0] = (0, 0, True)

def testbattle(a, b):

    a = deepcopy(a)
    b = deepcopy(b)

    battle(a, b, (10, 10))
    return a.energy, b.energy

assert sum(testbattle(nice, nice)) > sum(testbattle(naughty, naughty))

assert testbattle(naughty, nice) == testbattle(nice, naughty)[::-1]

slam = testbattle(naughty, nice)
assert slam[0] > slam[1]

# -------
# now mutate stuff

assert nice.energy == 50

child = nice.reproduce()

assert nice.energy == 25
assert child.energy == 25

child.mutate()

assert child.nodes != nice.nodes


