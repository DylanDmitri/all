import operator
import itertools
import re


class dist(dict):
    def __init__(self,items={}):
        dict.__init__(self,items)
        # assert abs(1-sum(self.keys()))<.001

    def combine(self,function,other):
        if type(other) == int:
            other = dist({other:1})

        assert type(other) == dist

        result = {}
        for num1,prob1 in self.items():
            for num2,prob2 in other.items():
                key = int(function(num1,num2))
                if key not in result:
                    result[key] = 0
                result[key] += prob1 * prob2
        return dist(result)

    def __add__(self,other): return self.combine(operator.add,other)
    def __mul__(self,other): return self.combine(operator.mul,other)
    def __sub__(self,other): return self.combine(operator.sub,other)
    def __neg__(self,other): return self.combine(operator.neg,other)
    def __lt__(self,other): return self.combine(operator.lt,other)
    def __gt__(self,other): return self.combine(operator.gt,other)
    def __eq__(self,other): return self.combine(operator.gt,other)


def newDice(size=6):
    assert size >= 1
    return dist({(i + 1):1 / size for i in range(size)})


def newRoll(number=1,size=6):
    assert number >= 1

    base = newDice(size)
    for _ in range(number - 1):
        base += newDice(size)
    return base


def minmax(func):
    def inner(*args):
        result = {}

        for poss in itertools.product(*(a.items() for a in args)):

            key = func(t[0] for t in poss)
            if key not in result:
                result[key] = 0

            p = 1
            for t in poss: p *= t[1]
            result[key] += p

        return dist(result)

    return inner

dmin = minmax(min)
dmax = minmax(max)


def advantage(roll):
    return dmax(roll, roll)

def disadvantage(roll):
    return dmin(roll, roll)

def cummulative(d):
    m = [0]
    for i in range(max(d.keys())+1):
        m.append(m[-1]+d.get(i, 0))
    return dist(dict(enumerate(m[1:])))


# parser

def run(text):
    for psub in (
        ('(\d+)d(\d+)', 'newRoll(\\1, \\2)'),
        ('d(\d+)', 'newRoll(1, \\1)'),
        ('=', '=='),):
        text = re.sub(*psub, text)
    return eval(text)


# stats
def stats(d):

    running = 0
    for k,v in sorted(d.items()):
        running += v
        if running>.5:
            median = k
            break

    return f"""
    mean: {sum(k*v for k,v in d.items())}
    median: {median}
    mode: {pmax(d.items(), key=lambda t:t[1])[0]}
    """

import matplotlib.pyplot as plt

def plot(result=None, text=None):
    # plt.plot(tuple(result.keys()), tuple(result.values()))
    if result is None: result = run(text)
    plt.bar(tuple(result.keys()), tuple(result.values()), label=text)

def show():
    plt.legend()
    plt.show()
    input()
    plt.close()

plot((run('advantage(2d6)')))
show()

# ------- sw system tests ---------


difs = {
    'trivial':5,
    'easy':6,
    'decent':7,
    'tricky':8,
    'hard':9,
    'challenging':10,
    # 'impossible':13,
}

if __name__ == '__main__':
    flat = dist({1:1})
    def percent(d):
        l = 5

        val = 100*d.get(1, 0)
        if val==100:
            return '#'*l
        if val==0:
            return ' '*l
        return f'{val:.1f}%'.rjust(l)



    for skill in range(0, 7):
        print(f'{skill} skill', {0:'(untrained)', 3:'(competent)', 6:'(legendary)'}.get(skill, ''))

        for name, diff in difs.items():

            roll = run('2d6') + skill

            fail = roll < diff-3
            setback = (roll < diff) - fail

            win = roll+1 > diff+3
            partial = (roll+1 > diff) - win

            print(percent(win), percent(partial), percent(setback), percent(fail), f'{name} problem')

        print()







