from copy import deepcopy
from puerto_rico.take8_tree.game import Game
from puerto_rico.take8_tree.data import *

end = set()
stack = []

best_p1_cash = 0
best_path = []

def search():

    g = Game()

    for decision in stack:
        g.step(decision)

    if g.bonus_amount:
        if g.p1.cash > best_p1_cash:
            print('new best', g.p1.cash)
            print(', '.join(map(str, stack)))
            globals()['best_p1_cash'] = g.p1.cash
            globals()['best_path'] = stack[::]

    else:
        for p in g.possible:
            stack.append(p)
            search()
            stack.pop()

search()

print(best_path)
print('done')

