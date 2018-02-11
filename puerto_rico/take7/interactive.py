from puerto_rico.take7.game import Game
from puerto_rico.take7.fields import *
from random import randint

g = None
def reset():
    global g
    g = Game()
    while g[state] != states.role_choice:
        g.step(randint(0, 4))
reset()