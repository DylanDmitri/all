import operator
import itertools
from fractions import Fraction
from collections import defaultdict

class op:
    def __init__(self, num_function, fstring):
        self.function = num_function
        self.display = lambda a, b : fstring.format(a, b)

def div(a, b):
    if b == 0:
        return None
    return a / b

def rdiv(a, b):
    if a == 0:
        return None
    return b / a

operations = (
    op(operator.add, "({})+({})"),
    op(operator.sub, "({})-({})"),
    op(lambda a,b:b-a, "({1})-({0})"),
    op(operator.mul, "({})*({})"),
    op(div, "({})/({})"),
    op(rdiv, "({1})/({0})")
)

links = [{(i,):{Fraction(i):str(i)} for i in range(1, 9)}]


def solve(dice):




    for layer in range(2, len(dice)+1):
        # print('building layer', layer)
        new = defaultdict(lambda: {})

        for a,b in zip(links[len(links)//2:][::-1], links):

            for set_a, set_b in itertools.product(a, b):

                set_new = tuple(sorted(set_a + set_b))

                # assert dice aren't used twice
                # ideally, wouldn't even consider these optimizations
                if any(dicecheck[d] < set_new.count(d) for d in set_new):
                    continue

                for f in operations:

                    for items_a, items_b in itertools.product(a[set_a].items(), b[set_b].items()):
                        new_int = f.function(items_a[0], items_b[0])
                        new_str = f.display(items_a[1], items_b[1])

                        if new_int is not None:
                            new[set_new][new_int] = new_str

        links.append(new)

    return new


def showints(dice):
    l = solve(dice)
    integer_results = sorted((i,v) for i,v in l[tuple(sorted(dice))].items() if i.denominator == 1)
    print(*(f'{i}={v}' for i,v in integer_results),sep='\n')

def getints(dice):
    l = solve(dice)
    # integer_results = sorted((i,v) for i,v in l[dice].items() if i.denominator == 1)
    # print(*(f'{i}={v}' for i,v in integer_results),sep='\n')
    return [int(i) for i in l[tuple(sorted(dice))] if i.denominator == 1]


# --------------

qprimes = [[NotImplemented], [3, 5, 7], [11, 13, 17], [19, 23, 29], [31, 37, 41],
	[43, 47, 53], [59, 61, 67], [71, 73, 79], [83, 89, 97], [101, 103, 107]]


from random import randint

def test(trials, spell_level, skillranks, dice):

    yes = 0
    for t in range(trials):
        rolls = tuple(randint(1,dice) for i in range(skillranks))
        if any((p in getints(rolls)) for p in qprimes[spell_level]):
            yes += 1
            print('yes')
        else:
            print('no')

    print(yes / trials)


# showints((6,5,4,3,2))



