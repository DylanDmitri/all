
from random import randint, random, choice
from trucks.simpleAlgo import make_assignments

class World:
    def __init__(self, size):
        self.size = size
        self.distances = {}
        for start in range(size):
            for end in range(size):
                self.distances[frozenset((start, end))] = randint(1, 30)

        self.truckers = []
        self.orders = []

    def distance(self, start, end):
        return self.distances[frozenset((start, end))]

    def randLocation(self):
        return randint(0, self.size-1)

    def update(self, timedelay):
        for order in self.orders:
            truck = self.truckers[order.truckerId]
            truck.time_to_dest -= timedelay
            if truck.time_to_dest == 0:
                truck.location = order.end
                order.markCompletion()


class Trucker:
    def __init__(self, loc):
        self.time_to_dest = None
        self.loc = loc
        self.status = 'free'

_orderid = 0
class Order:
    def __init__(self, pickupTime, start, end):
        self.remove = False

        self.pickupTime = pickupTime
        self.start = start
        self.end = end

        self.trucker = None
        self.complete = False
        self.id = _orderid
        globals()['_orderid'] += 1

    def markCompletion(self):
        self.complete = True

    @property
    def needsPickup(self):
        return self.trucker is None and not self.complete


def test():

    worldsize = 20
    truckNum = 5
    orderChance = 1
    timeLimit = 300

    w = World(worldsize)

    for i in range(truckNum):
        w.truckers.append(Trucker(w.rand()))

    for time in range(timeLimit):

        if random() < orderChance:
            # w.orders.append(Order(time+choice(timeDelay), w.rand(), w.rand()))
            w.orders.append(Order(20, 1, 2))

        if w.orders:
            pass

        make_assignments(w, time)
        w.update(1)


test()







