from puerto_rico.alea_stateless.variants import AleaBalanced
from puerto_rico.alea_stateless.game_state import GameState, goods
from random import choice


def displayStore(store):
    r = ''

    rev = {}
    for good in goods:
        rev.setdefault(getattr(store, good), []).append(good)

    for key, vals in rev.items():
        r += str(key) + ' of ' + str(tuple(vals)) + '; '
    return r




def displayBoard(player):

    print('city:',player.city)
    print('farms:', displayStore(player.island))
    print('goods:', displayStore(player.goods))
    print(player.dubloons, 'dubloons')


def display(gamestate, pnum):

    for i, player in enumerate(gamestate.players):
        print(gamestate.playernames[i])
        displayBoard(player)
        print()




game = GameState(AleaBalanced, logging=True)

while True:

    while game.state.endswith('flip'):
        game.step(choice(game.options))

    c = input()
    if c == '':
        display(game,game.activePlayer)
    else:
        game.step(c)


