from random import choice, randint
from copy import deepcopy

def totalTime(func, orders):
    total = 0
    for order in orders:
        total += func(order.potential_trucker.loc, order.start)
    return total

def smonch(world):

    availible_truckers = [t for t in world.truckers if t.status=='free']
    orders = [order for order in world.orders if order.needsPickup]

    for order in orders:
        trucker = choice(availible_truckers)
        order.potential_trucker = trucker
        trucker.status = 'busy'

    current_best = orders
    best_time = totalTime(world.distance, current_best)

    for _ in range(3000):
        flips = randint(1, 3)
        this = deepcopy(current_best)



        for __ in range(flips):
            a, b = randint(0, len(orders)-1)
            this[a].potential_trucker = None

        this_time = totalTime(world.distance, this)
        if this_time < best_time:
            best_time = this_time
            current_best = this

    return current_best


def make_assignments(world, time):

    to_assign = [order for order in world.orders if order.needsPickup]

    # matrix :: all trucker locs -> all order pickup locs

    matches = smonch(world)

    for order in matches:

        # the trucks that need to leave now LEAVE
        # the other trucks don't do anything

        time_to_pickup = time - order.pickupTime
        drive_time = world.distance(order.potential_trucker.loc, order.start)
        time_to_departure = time_to_pickup - drive_time

        if time_to_departure < 1:
            world.orders[order.id].trucker = order.potential_trucker
