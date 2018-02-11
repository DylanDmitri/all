'''
1 blood loss becomes serious in 80 minutes
2 in 40 minutes
3 in 27 minutes
4 in 20 minutes
5 in 18 minutes
10 in 8 minutes
'''



class dmgType:
    stab = 'stab'
    crush = 'crush'
    slice = 'slice'



class conditions:
    fine = 'fine'
    detatched = 'detatched'
    impaled = 'impaled'

def add_condition(object, condition):
    if not hasattr(object, 'conditions'):
        object.conditions = []
    object.conditions.append(object)


class stat:
    strength = 'strength'
    toughness = 'toughness'
    dexterity = 'dexterity'
    intelligence = 'intelligence'
    wisdom = 'wisdom'
    vision = 'vision'
    hearing = 'hearing'

stat_list = [s for s in dir(stat) if s[0]!='_']

print()

class StatBlock:
    def __init__(self):
        for s in stat_list:
            setattr(self, s, 0)



class Internal:
    def __init__(self, name, **stats):
        self.name = name
        self.functional = True
        self.hp = 10
        self.stats = stats
        for key in self.stats:
            assert key in stat_list

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.functional = False

class _internals:
    @property
    def tendons(self): return Internal('tendons')

    @property
    def bone(self): return Internal('bone')

    @property
    def heart(self): return Internal('heart')

    @property
    def lungs(self): return Internal('lungs')

    @property
    def eye(self): return Internal('eye', vision=2)


internals = _internals()




