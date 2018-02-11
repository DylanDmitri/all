class damage:
    stab = 'stab'
    impact = 'impact'
    slash = 'slash'

class weaponType:
    melee = 'melee'
    ranged = 'ranged'
    magic = 'magic'


class status:
    eye_marked = 'eye marked'


class Attack:
    def __init__(self, kind, damagetype, range, skill, power):
        self.range = range
        self.skill = skill
        self.power = power
        self.damagetype = damagetype


class Unit:
    strength = NotImplemented
    toughness = NotImplemented
    dexterity = NotImplemented
    charisma = NotImplemented
    will = NotImplemented
    intelligence = NotImplemented

    block = NotImplemented
    cover = NotImplemented

    resist = {}
    melee = NotImplemented
    actions = []

    watching_eye_modifier = False

    def __init__(self):
        self.wounds = []
        self.status = []
        self.combat = False

    def update(self):
        if self.combat and any(unit.watching_eye_modifier for unit in self.combat_enemies):
            self.status.append(status.eye_marked)

    def attackroll(self):
        pass

    def choose(self):
        pass

class Combat:
    def __init__(self, good, bad):
        self.good = good
        self.bad = bad

        for unit in self:
            unit.combat = self
            unit.combat_enemies = self.bad if unit in self.good else self.good

    def __iter__(self):
        for u in self.good:
            yield u
        for u in self.bad:
            yield u

    def resolve(self):
        for unit in self:
            unit.attackroll()


class Warden:
    strength = 7
    toughness = 6
    dexterity = 4
    charisma = 3
    will = 5
    intelligence = 2
    block = 2
    cover = 0
    resist = {damage.slash:2, damage.impact:1, damage.stab:2}
    melee = Attack(weaponType.melee, (damage.slash, damage.impact), range=2, skill=4, power=5)
    actions = []

    watching_eye_modifier = True






