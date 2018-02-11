from random import random, randint
from statistics import stdev

consts = {
 5  : 0.00380,
 10 : 0.01475,
 12 : 0.02099,
 15 : 0.03221,
 20 : 0.05570,
 25 : 0.08475,
 30 : 0.11895,
 35 : 0.14628,
 40 : 0.18128,
 45 : 0.21867,
 50 : 0.25701,
 55 : 0.29509,
 60 : 0.33324,
 65 : 0.38109,
 70 : 0.42448,
}


class Crit:
    def __init__(self, vars, build_hits=None):
        chance, extra = vars[0], vars[1]

        self.first_crits = 'brew' in vars

        self.chance = chance/100
        self.extra = extra/100
        self.prd_const = consts[chance]
        self.chance_on_next = self.prd_const
        self.hits_since_last_crit = build_hits
        self.first = True

    def check(self):

        if self.first and self.first_crits:
            self.first = False
            return self.extra

        if random() < self.chance_on_next:
            self.chance_on_next = self.prd_const
            return self.extra

        self.chance_on_next += self.prd_const
        return 1


class data:
    jugg1 = (20,200)
    jugg2 = (25,200)
    jugg3 = (30,200)
    jugg4 = (35,200)

    brew1 = (10,200, 'brew')
    brew2 = (15,200, 'brew')
    brew3 = (20,200, 'brew')
    brew4 = (25,200, 'brew')

    ck1 = (12,125)
    ck2 = (12,175)
    ck3 = (12,225)
    ck4 = (12,275)

    wk1 = (15,150)
    wk2 = (15,200)
    wk3 = (15,250)
    wk4 = (15,300)
    wk_creep1 = (15,300)
    wk_creep2 = (15,400)
    wk_creep3 = (15,500)
    wk_creep4 = (15,600)

    pa1 = (15, 230)
    pa2 = (15, 340)
    pa3 = (15, 450)

    lycan1 = (40, 160)
    lycan2 = (40, 180)
    lycan3 = (40, 200)

    wolf = (20, 200)
    crystalys = (20, 175)
    daedylus = (30, 235)



class Unit:
    def __init__(self, *crits):
        self.crits = crits

    def dpsMult(self, hits=100):

        total = 0
        for crit in self.crits:
            if crit.hits_since_last_crit is None:
                for i in range(randint(20, 30)):
                    crit.check()
            else:
                crit.chance_on_next = crit.prd_const * (crit.hits_since_last_crit+1)
            crit.first = True

        for trial in range(hits):
            extra = [crit.check() for crit in self.crits]
            total += 100*max(extra) / hits

        return total


def get_preload_benefit(dat):

    hits = 0
    while True:
        crit = Crit(dat, build_hits=hits)


jugg = (
    Unit(Crit(data.jugg1)),
    Unit(Crit(data.jugg2)),
    Unit(Crit(data.jugg3)),
    Unit(Crit(data.jugg4)),
)

brew = (
    Unit(Crit(data.brew1)),
    Unit(Crit(data.brew2)),
    Unit(Crit(data.brew3)),
    Unit(Crit(data.brew4)),
)

ck = (
    Unit(Crit(data.ck1)),
    Unit(Crit(data.ck2)),
    Unit(Crit(data.ck3)),
    Unit(Crit(data.ck4)),
)

wk = (
    Unit(Crit(data.wk1)),
    Unit(Crit(data.wk2)),
    Unit(Crit(data.wk3)),
    Unit(Crit(data.wk4)),
)



for hero in wk:
    vals = [hero.dpsMult(hits=16) for _ in range(500000)]
    mean = sum(vals)/len(vals)
    sig = stdev(vals)
    print(mean, sig)
    print(mean - sig, mean + sig)
    print()


# each manta does .33, you do 1
manta_mult = 1.66

# 1-4 il
phantasm1 = 2.5
phantasm2 = 3.5
phantasm3 = 4.5


# bladedance: 31-36%
# daedylus:  37-44%
# both:      60-68%

# from the 40.5% increase of daedylus
# lycan3 loses 11.4%
# jugg
# pa3 loses 6.38%


"""
Analysis By Hero


Juggernaut

    base percent dps added: (20 / 25 / 30 / 33)
         with manta, up to: (33 / 42 / 50 / 55)

    build stats not raw damage to maximize manta value
    scales poorly, use a value point


Brewmaster
    first hit always crits; initial couple hits have higher average
    almost always better than jugg crit
        except when attacking constantly (usually roshan, clearing big wave/stack)

    percent dps increase of initial _x_ hits
     2 hits : (55 / 57 / 59 / 62)
     4 hits : (32 / 36 / 40 / 44)
     8 hits : (21 / 26 / 30 / 34)
    16 hits : (16 / 20 / 25 / 30)

    scales very poorly, use one value point
    also grants evasion (wow!)


Chaos Knight
    base percent dps added: (3 / 9 / 15 / 21)
         lifesteal percent: (8.0 / 8.5 / 9.0 / 9.4)

    Damage scales well with levels, but Lifesteal works better as a value point.

    Synergizes well with illusions.
        100% dps: ck alone
        500% dps: ck with 4 phantasms
        605% dps: ck with 4 phantasms and maxed crit

Wraith King
    base percent dps added: (7.5 / 15 / 22.5 / 30)

    Damage scales well.
    Added dps





Desolator (3500 gold)

50 damage
first hit reduce eph by 42% of maxhp

Crystalas (


"""











