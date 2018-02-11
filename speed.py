from time import time


def check(func):
    start = time()
    for k in range(20):
        for _ in range(1000):
            func()
        end = time()
        if end-start > 5:
            print((k * 1000) / (end-start), 'runs per second')
            return None


class fakegame:

    def __init__(self):
        self.farm_stacks = dict(coffee=0, tobacco=1, corn=1, sugar=0, indigo=0)

        self.activePlayer = lambda:None
        self.activePlayer.has = lambda x:True
        self.activePlayer.has_role = lambda x:True

    def inplace(self):
        return ('no plantation',
         *(key for key, val in self.farm_stacks.items() if val),
         *((('quarry',),tuple())[
               self.activePlayer.has('construction_hut') or self.activePlayer.has_role('settler')]))

    def concat(self):
        ret = ['no plantation', ]
        ret.extend([key for key, val in self.farm_stacks.items() if val])
        if self.activePlayer.has('construction_hut') or self.activePlayer.has_role('settler'):
            ret.append('quarry')
        return ret


check(lambda : 1+1)





