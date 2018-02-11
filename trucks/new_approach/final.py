from random import randint, choice, shuffle
import string
from copy import copy



class invalidPlanError(BaseException):
    """trucker cannot do this"""

def rand_location():
    return ''.join(choice(string.ascii_uppercase) for _ in range(4))
# _locations = [rand_location() for _ in range(12)]
_locations = list('AAAA BBBB CCCC DDDD'.split())
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


class Trucker:
    def __init__(self):
        self.orders_in_truck = []
        self.potential_tasks = []

class Task:
    def __init__(self, o, pickup=False, dropoff=False, current_truck=None):
        assert (pickup or dropoff) and not(pickup and dropoff)
        self.order = o

        self.current_truck = current_truck
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


def generate_tasks(trucker_list, order_list):
    ret = []

    for trucker in trucker_list:
        for order in trucker.orders_in_truck:
            ret.append(Task(order, dropoff=True, current_truck=trucker))

    for order in order_list:
        ret.append(Task(order, pickup=True))
        ret.append(Task(order, dropoff=True))

    return ret


class Plan:
    def __init__(self, trucker_list):
        self.truckers = trucker_list

    def square_time(self, task_list):
        try:
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
                if task.current_truck is not None:
                    task.current_truck.potential_tasks.append(task)
                elif task.order in relevant:
                    relevant[task.order].potential_tasks.append(task)
                else:
                    raise invalidPlanError



    def clear_potential(self):
        for trucker in self.truckers:
            trucker.potential_tasks = []

class Order:
    def __init__(self,start,end):
        self.vol = 10
        self.weight = 10

        self.start = start
        self.end = end



"""
generate task list

repeat
    shuffle task list
    score task list
    check conditions and save

output

"""


def Algorithm(trucker_list, order_list):

    # generate tasks
    #   pickups/dropoffs from order_list
    #   dropoffs already on the truck
    #   create the initial mapping of orders->truckers

    task_list = generate_tasks(trucker_list, order_list)

    # initialize to get min and max
    best_score = float('inf')
    best_list = task_list[::]
    tries_since_last_improvement = 0

    # plan knows about truckers
    plan = Plan(trucker_list)

    for _ in range(1000):
        # make a copy
        this_list = best_list[::]

        # swap stuff around
        #   for every log(x)/log(10) swap an extra thing
        #   base on time_since_last_improvement
        shuffle(this_list)

        # check the fitness value: total squared time
        #   the clearing should happen in the fitness function
        plan.clear_potential()
        score = plan.square_time(this_list)

        if score < best_score:
            best_list = this_list
            time_since_last_improvement = 0

        tries_since_last_improvement += 1

    plan.clear_potential()
    plan.assign_tasks(best_list)
    return plan

def generate_task_list(trucker_list, order_list):
    ret = []
    for trucker in trucker_list:



# -------------------------------------

display_map()
#
# tumpo = Trucker()
# tumpo.location = 'AAAA'
#
# chungus = Trucker()
# chungus.location = 'BBBB'
#
# # order1 = Order('AAAA', 'BBBB')
# order2 = Order('CCCC', 'AAAA')

print()
orders = [Order(), Order(), Order()]
for order in orders:
    print(order.start, '->', order.end)
print()

truckers = [Trucker(), Trucker(), Trucker()]

tasks = generate_tasks(orders)

plan = Plan(truckers)
original = plan.square_time(tasks)
print('original\n', plan)

for i in range(len(tasks)):
    for j in range(len(tasks)):
        for k in range(len(tasks)):
            for l in range(len(tasks)):

                new = tasks[::]
                temp = new[i]
                new[i] = new[j]
                new[j] = temp

                temp = new[k]
                new[k] = new[l]
                new[l] = temp

                score = plan.square_time(new)
                if score < original:
                    print()
                    print(score)
                    print('new plan\n', plan)
                    tasks = new
                    original = score




