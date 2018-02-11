class damagetype:
    stab = 'stab'
    slice = 'slice'
    crush = 'crush'

class reach:
    tiny = 1
    short = 2
    medium = 3
    long = 4
    reach = 5
    reach2 = 6

class Weapon:
    def __init__(self, kind, reach, weight, skill, block=0):
        self.kind = kind
        self.reach = reach
        self.skill = skill
        self.weight = weight
        self.block = block
        self.user = None

    @property
    def attack_skill(self):
        skill = self.skill
        bonus = self.user.strength - self.weight
        return min(self.user.dexterity,skill + bonus)

    @property
    def attack_power(self):
        return min(self.weight, self.user.strength)

    def showstats(self):
        print('{} reach, +{} to hit, {} {}'.format(self.reach, self.attack_skill, self.attack_power, self.kind))


fist = Weapon(damagetype.crush, reach.tiny, 1, -2)

class Wound:
    def __init__(self, severity, kind):
        self.severity = severity
        self.kind = kind

class Creature:
    def __init__(self, name):
        self.name = name
        self.base_strength = 3
        self.base_dexterity = 3
        self.base_will = 3
        self.base_toughness = 3
        self._weaponA, self._weaponB = None, None
        self.equip()

        self.wounds = []

    def equip(self, a=None, b=None):
        self._weaponA = a
        self._weaponB = b
        for var in ('_weaponA', '_weaponB'):
            if getattr(self, var) is None:
                setattr(self, var, fist)
            getattr(self, var).user = self

    @property
    def weapons(self):
        return (self._weaponA, self._weaponB)

    @property
    def strength(self):
        return self.base_strength + (self._weaponA==fist or self._weaponB==fist)

    @property
    def dexterity(self):
        return self.base_dexterity

    @property
    def maxHP(self):
        return self.base_will + self.base_toughness

    @property
    def currentHP(self):
        return self.maxHP - sum(wound.severity for wound in self.wounds)

    @property
    def cover(self):
        return self._weaponA.block + self._weaponB.block

    @property
    def defense_skill(self):
        return sum(w.attack_skill for w in self.weapons) + self.cover

    @property
    def resistance(self):
        return {
            damagetype.slice : 1,
            damagetype.crush : 1,
            damagetype.stab  : 0,
        }

    def showstats(self):
        for stat in ('strength', 'dexterity', 'defense_skill', 'cover'):
            print(stat, ':', eval('self.'+stat))

        for weapon in self.weapons:
            weapon and weapon.showstats()

    def _addWound(self, wound):
        print('{} takes {} {} damage'.format(self.name, wound.severity, wound.kind))
        self.wounds.append(wound)
        critdiff = wound.severity - self.maxHP/2
        if critdiff >= 0:
            print('crit of severity', critdiff)

        if self.currentHP < 0:
            print('passes out')

        return ""

    def addWound(self, wound):
        wound.severity -= self.resistance[wound.kind]
        self._addWound(wound)



shield = Weapon(damagetype.crush, reach.short, weight=2, skill=0, block=4)
scimitar = Weapon(damagetype.slice, reach.short, weight=2, skill=2, block=1)

test = Creature()
test.equip(scimitar)
test.showstats()

