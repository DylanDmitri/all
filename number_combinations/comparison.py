from number_combinations.reddit_script import process
from number_combinations.sacred_geometry import getints, qprimes
from random import randint
from time import time





dice = 6
skillranks = 5
spell_level = 5

while True:
    rolls = tuple(randint(1,dice) for i in range(skillranks))

    start = time()
    theirs = process(spell_level, rolls, False, False)
    print()
    print(time()-start)

    start = time()
    mine = any((p in getints(rolls)) for p in qprimes[spell_level])
    print(time()-start)

    print(rolls)

    if mine != theirs:
        print('mine', mine)
        print('theirs', theirs)
        print('YIKES')

        input()

# 3 2 3 3 2
