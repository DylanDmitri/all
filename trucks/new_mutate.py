from random import randint, choice, shuffle
import string
from copy import copy



class invalidPlanError(BaseException):
    """trucker cannot do this"""

def rand_location():
    return ''.join(choice(string.ascii_uppercase) for _ in range(4))

# _locations = [rand_location() for _ in range(12)]
_locations = list('AAAA BBBB CCCC'.split())
def location():
    return choice(_locations)
def display_map():
    print('    ', ' '.join(_locations))
    for l in _locations:
        print(l, end='')
        for e in _locations:
            print(' '+str(distance(l, e)).ljust(4, ' '), end='')
        print()

def distance(start, end):
    if start==end: return 0
    return hash(frozenset((start,end))) % 999


class Plan:
    def __init__(self, trucker_list):
        self.truckers = trucker_list

    def square_time(self, task_list):
        try:
            # print('\ntasks:')
            # for task in task_list:
            #     print(task)

            self.assign_tasks(task_list)
            # print('assigned')
            fitness = self._fitness()
            print('fitness', fitness)
            return fitness
        except invalidPlanError:
            return float('inf')

    def _fitness(self):
        total = 0
        for trucker in self.truckers:
            total += trucker.planned_time()
        return total / len(self.truckers)

    def assign_tasks(self, task_list):

        """
        for each task
            if it's a pickup, give to closest trucker
            if it's a dropoff, give to trucker with that pickup

        note: orders on trucks have dropoff, but no pickup
        """

        relevant = {}

        for task in task_list:
            if task.pickup:
                trucker = min(self.truckers, key=lambda t: distance(t.potential_location(), task.location))
                trucker.potential_tasks.append(task)
                relevant[task.order] = trucker

            elif task.dropoff:
                if task.order not in relevant:
                    raise invalidPlanErrora
                relevant[task.order].potential_tasks.append(task)


    def clear_potential(self):
        for trucker in self.truckers:
            trucker.potential_tasks = []


class Trucker:
    def __init__(self):
        self.location = location()
        self.in_truck = []

        self.current_tasks = []
        self.potential_tasks = []

        # self.maxWeight = 10
        self.maxVol = 10

    def potential_location(self):
        if len(self.potential_tasks) == 0:
            return self.location

        return self.potential_tasks[-1].location

    def planned_time(self):
        total_vol = sum(item.order.vol for item in self.in_truck)
        current_things = []

        currently_at = self.location
        time_elapsed = 0
        for task in self.potential_tasks:

            time_elapsed += distance(currently_at, task.location)
            currently_at = task.location

            if task.pickup:

                current_things.append(task.order)
                total_vol += task.order.vol

                if total_vol > self.maxVol:
                    raise invalidPlanError

            elif task.dropoff:
                if task.order not in current_things:
                    raise invalidPlanError
                current_things.remove(task.order)
                total_vol -= task.order.vol

        return time_elapsed

    def __str__(self):
        return 'trucker at '+self.location + ':'+','.join(str(t) for t in self.potential_tasks)

class Order:
    def __init__(self, start, end):
        self.vol = 10
        self.weight = 10

        self.start = start
        self.end = end

class Task:
    def __init__(self, o, pickup=False, dropoff=False):
        assert (pickup or dropoff) and not(pickup and dropoff)
        self.order = o

        self.pickup = pickup
        self.dropoff = dropoff

        if self.pickup:
            self.location = self.order.start
        elif self.dropoff:
            self.location = self.order.end

    def __str__(self):
        if self.pickup:
            return 'drive to {}, get order {}->{}'.format(self.order.start, self.order.start, self.order.end)
        return 'drive to {}, drop off {}->{}'.format(self.order.end, self.order.start, self.order.end)

def generate_tasks(order_list):
    ret = []
    for o in order_list:
        ret.append(Task(o, pickup=True))
        ret.append(Task(o, dropoff=True))
    return ret


def Algorithm(trucker_list, order_list):

    task_list = generate_tasks(order_list)

    best_score = float('inf')
    best_list = task_list[::]

    plan = Plan(trucker_list)

    for _ in range(1000):

        plan.clear_potential()

        this_list = best_list[::]
        shuffle(this_list)

        score = plan.square_time(this_list)

        if score < best_score:
            best_list = this_list

    plan.clear_potential()
    plan.assign_tasks(best_list)
    return plan


# -------------------------------------

display_map()

tumpo = Trucker()
tumpo.location = 'AAAA'

chungus = Trucker()
chungus.location = 'BBBB'

order1 = Order('AAAA', 'BBBB')
order2 = Order('BBBB', 'CCCC')

plan = Algorithm(
    [tumpo, ],
    [order1, order2]
)

for trucker in plan.truckers:
    print(trucker)



