from random import choice

cflag = False

class stats:
    def __init__(self):
        self.str = 4
        self.tgh = 4
        self.dex = 4
        self.cha = 4
        self.wil = 4
        self.int = 4

    all = 'str', 'tgh', 'dex', 'cha', 'wil', 'int'

    def __str__(self):

        mystery = '\n      ' if cflag else '\n'
        return ''.join(var+' '+('•'*getattr(self, var)).ljust(8)+eof for var, eof in zip(stats.all, ('', '', mystery, '', '', ''))) + '\n'

def choosefrom(*d):
    globals()['cflag'] = True

    if len(d) == 1:
        d = d[0]

    for i, c in enumerate(d):
        print('({}) - {}'.format(i, c))
    while True:
        choice = input('> ')
        for i, c in enumerate(d):
            if str(i)==choice:
                globals()['cflag'] = False
                if type(d) == dict:
                    return d[c]
                return c

print('choose your race. Each will slightly affect ability scores, and will add an extra bonus based on your class.')
race = choosefrom('human', 'elf', 'dwarf')
print('you chose', race)
print('\n------\n')

def rollStats():
    block = stats()

    points = 2
    decr = set()

    if race != 'human':
        if race == 'elf':
            bonus = choice(('cha','dex','int'))
        elif race == 'dwarf':
            bonus = choice(('tgh','str','wil'))
        setattr(block, bonus, 5)


    for i in range(50):

        diff = choice((1, -1))

        if diff == -1 and len(decr) == 2:
            # print('only decrement two stats, these are currently', decr)
            continue

        if diff == 1 and points==0:
            # print('no points to spend')
            continue

        stat = choice(stats.all)

        if diff == -1 and stat in decr:
            # print('cannot decrement a stat twice')
            continue
        else:
            decr.add(stat)

        if diff == 1 and stat in decr:
            decr.remove(stat)

        points -= diff

        setattr(block,stat,getattr(block,stat) + diff)

    return block

print('choose a stat block')
stats = choosefrom(
    rollStats(),
    rollStats(),
    rollStats(),
)

print('you choose')
print(stats)

print('choose your class')
kind = choosefrom('Fighter','Cleric','Mage','Rouge','Ranger',)




