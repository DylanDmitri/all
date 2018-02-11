from civsim.main import *
from copy import deepcopy

Actor.MUTATION_RATE = 0

nice = Actor()
nice.nodes[0] = (0,0,False)  # always redirect to self, mean=False

naughty = Actor()
naughty.nodes[0] = (0,0,True)

# niceland = Region()
# niceland.people = [nice for _ in range(5)]
#
# for i in range(100):
#     niceland.step()
#
# assert len(niceland.people) > 10
#
# print(len(niceland.people))



meanland = Region()
meanland.people = [deepcopy(naughty) for _ in range(5)]

for i in range(100):
    meanland.step()
    print(len(meanland.people))

