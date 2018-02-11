from random import randint, random

class Crystalys:
    def __init__(self):
        self.name = 'crystalas'
        self.damage = 30
        self.prd_const = 0.05570

        self.chance_on_next = self.prd_const
        for _ in range(randint(1,30)):
            self.check()

    def check(self):

        if random() < self.chance_on_next:
            self.chance_on_next = self.prd_const
            return 1.75

        self.chance_on_next += self.prd_const
        return 1

crystalys = Crystalys()

class deso: pass
desolator = deso()
desolator.damage = 50

def hits(damagemin, damagemax, targethp, targetarmor, weapon):

    if weapon is desolator:
        targetarmor -= 7

    hits = [0 for _ in range(10)]

    for trial in range(10000):

        if hasattr(weapon, 'preload'):
            weapon.chance_on_next = weapon.prd_const * (1+weapon.preload)

        eph = targethp * (1 + .06 * targetarmor)

        for hit in range(20):
            damage = randint(damagemin, damagemax) + weapon.damage

            if weapon is crystalys:
                damage *= weapon.check()

            # ally
            # damage += randint(damagemin, damagemax)

            eph -= damage
            if eph <= 0: break

        hits[hit] += 1

    for i, num in enumerate(hits):
        print(str(i).rjust(2), num)


hits(290, 310, 2000, 10, crystalys)


# 6-7 hits with deso





