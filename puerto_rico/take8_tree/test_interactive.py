from puerto_rico.take8_tree.game import Game
from puerto_rico.take8_tree.data import *
from random import choice

g = Game()


seq = iter((0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6, 6, 2, True, 0, 1, 6, 0, 3, None, 6, 4, None, None))
out = print


while True:

    if g.state == State.role_choice:
        out('CHOOSING ROLE...')
        out('availible:',', '.join(map(role_lookup.__getitem__,g.possible)))

    elif g.state == State.tile_flip:
        out('choosing tile...')
        out('possible',', '.join(map(lambda a:tile_lookup[a] if a is not None else 'none',tuple(g.possible))))
        # decision = choice(tuple(g.possible))
        # print(tile_lookup[decision])

    elif g.state == State.planter:
        out('planter phase')
        out('p1' if g.active is g.p1 else 'p2','choosing which farm')
        out('possible',', '.join(map(lambda a: tile_lookup[a] if a is not None else 'none', tuple(g.possible))))

    elif g.state == State.build:
        out('builder phase')
        out('p1' if g.active is g.p1 else 'p2','building something')
        out('possible',', '.join(map(lambda a:building_lookup[a] if a is not None else 'none',tuple(g.possible))))

    elif g.state == State.assign_work_up:
        out('where to assign workers?')
        out('already staffed:', ', '.join(island_lookup[i] for (i, e) in enumerate(g.active.jobs) if e))
        out('possible:', ', '.join(map(island_lookup.__getitem__,tuple(g.possible))))

    elif g.state == State.assign_work_down:
        out('where to leave unstaffed?')

    else:
        out(State.lookup[g.state])
        out(','.join(tuple(map(str,g.possible))))


    while True:
        try:
            try:
                i = next(seq)
                out(i)
            except StopIteration:
                i = int(input('::'))
            break
        except ValueError:
            out('should be a number')

    decision = tuple(g.possible)[i]

    g.step(decision)

    out(g.disp)

    # if g.state == State.tile_flip:
    #     out('open:',', '.join(str(amount) + ' ' + tile_lookup[kind] for kind,amount in enumerate(g.farm_open)))

    out()
