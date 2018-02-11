from puerto_rico.alea_stateless.variants import AleaBalanced
from puerto_rico.alea_stateless.game_state import GameState, state
from copy import deepcopy

failed = {}

def testmethod(func):
    try:
        func()
    except Exception as e:
        failed[func.__name__] = e
    else:
        print(func.__name__, 'passed')


@testmethod
def nextPlayer_test():

    game = GameState(AleaBalanced)

    for playerNum in (2, 3, 4, 5, 6):
        game.players = list(range(playerNum))
        game._active = 0

        for i in range(30):
            assert (i % playerNum) == game._active
            game.incrementPlayer()

@testmethod
def construction_hut_test():

    game = GameState(AleaBalanced)

    game.players[0].city['construction_hut'] = 1
    game._active = 0
    game.state = state.plantation
    game.ready_plantation()
    assert 'quarry' in game.options

    game._active = 1
    game.state = state.plantation
    game.ready_plantation()
    assert 'quarry' not in game.options

@testmethod
def hacienda_test():
    game = GameState(AleaBalanced, logging=True)

    game.players[0].city['hacienda'] = 1
    game._active = 0
    game.state = state.role
    game.ready_role()
    game._active = 0
    game.step('settler')
    game.step(False) # don't use it
    assert game.players[0].island.sugar == 0

    game._active = 0
    game.state = state.role
    game.ready_role()
    game._active = 0
    game.step('settler')
    game.step(True)
    game.step('sugar')
    assert game.players[0].island.sugar == 1

    game._active = 1
    game.state = state.role
    game.ready_role()
    game._active = 1
    game.update_role('settler')
    game.step('no plantation')




for name in failed:
    print('FAILED:', name)

for name, error in failed.items():
    raise error