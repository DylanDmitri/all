from random import random
from statistics import stdev

def percent(crd):
    chance = crd
    yes = 0

    trials = 10000
    for _ in range(trials):
        if random() < chance:
            chance = 0
            yes += 1
        chance += crd

    return yes / trials


def calc(nominal):
    lower = 0
    upper = 1

    for _ in range(20):
        this = (lower+upper)/2
        if percent(this) < nominal:
            lower = this
        else:
            upper = this

    return (lower + upper) / 2


vals = [calc(0.12) for _ in range(500)]
mean = sum(vals) / len(vals)
sig = stdev(vals)
print(mean,sig)
print(mean - sig,mean + sig)
print()
