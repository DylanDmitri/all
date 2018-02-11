

# rps
# p1wins p2wins prev_choice

new_game = (0, 0, 0, 0, 0, 0, 0, 0, 0, 'x', None)

top_left = 0
top_mid = 1
top_right = 2
mid_left = 3
mid_mid = 4
mid_right = 5
bot_left = 6
bot_mid = 7
bot_right = 8
active = 9
winner = 10

def get_possible(gamestate):

    return (i for i in range(9) if gamestate[i] is None)

def get_next(gamestate, choice):

    delta = {}

    delta[choice] = 'xy'[gamestate[active]]

    for line in (
            (top_left, top_mid, top_right),
            (mid_left, mid_mid, mid_right),
            (bot_left, bot_mid, bot_right),
            (top_left, mid_left, bot_left),
            (top_mid, mid_mid, bot_mid),
            (top_right, mid_right, bot_right),
            (top_left, mid_mid, bot_right),
            (bot_left, mid_mid, top_right)):

        for p in 'xy':
            if all(gamestate[i]==p for i in line):
                delta[winner] = p

    return (delta.get(*vals) for vals in enumerate(gamestate))





