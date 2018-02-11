from puerto_rico.tic_tac_toe.game_logic import *


def evaluate(state, player):

    if not get_possible(state):
        return 0

    if state[winner] is None:
        return 0

    elif state[winner] == player:
        return 1

    elif state[winner] != player:
        return -1


class Tree:




def search(state):

    for decision in get_possible(state):



        search(get_next(state, decision))


search(new_game)



