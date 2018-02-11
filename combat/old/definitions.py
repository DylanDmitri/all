from collections import defaultdict
from itertools import groupby

sizes = ('tiny', 'small', 'medium', 'large')

class _Slot:
    def __init__(self, name, default='empty_slot'):
        self.name = name
        self.default = default
        self.item = default

    def add(self, item):
        temp = self.item
        self.item = item
        return  temp

    def clear(self):
        temp = self.item
        self.item = self.default
        return temp

    def __str__(self):
        return 'slot<{}> {}'.format(self.name, self.item)

    @property
    def empty(self):
        return self.item == self.default

class Slot:
    helmet = lambda : _Slot("helmet")
    mask = lambda : _Slot("mask")
    glove = lambda : _Slot("gloves")
    ring = lambda : _Slot("ring")
    shoe = lambda : _Slot("shoes")
    arm = lambda : _Slot("arm")
    leg = lambda : _Slot("leg")
    chest = lambda : _Slot("chest")
    belt = lambda : _Slot("belt")
    amulet = lambda : _Slot("amulet")
    hand = lambda : _Slot("hand")


class damage_type:
    slash = 'slash'
    stab = 'stab'
    smash = 'smash'

class attack_type:
    melee = 'melee'
    ranged = 'ranged'

class reach:
    tiny, short, medium, long, reach1, reach2 = range(6)


# ----------------------------------------------------------------------------
class Statable(dict):
    def __add__(self, other):
        new = dict(self)
        for key in other:
            if key in new:
                new[key] += other[key]
            else:
                new[key] = other[key]
        return Statable(new)

class Bodypart:
    def __init__(self, abstract_part, connected):
        self.name = abstract_part.name
        self.slots = abstract_part.slots
        self.connected = set(connected)

class BodypartConstructor:
    def __init__(self, name, *slots, **attributes):
        self.name = name
        self.slots = slots

    def __call__(self, *args):
        return Bodypart(self, args)

# ----------------------------------------------------------------------------
class Attack:
    def __init__(self, type, range, damage_kind, skill_bonus=0):

        self.melee = type == 'melee'
        self.ranged = type == 'ranged'

        if self.melee:
            self.reach = range
        elif self.ranged:
            self.range = range

        self.damage_kind = damage_kind
        self.skill_bonus = skill_bonus

equipment = {}
placeholders = {}
class Equipment:
    def __init__(self, name, *slots, **attributes):
        if name in equipment:
            raise Exception('Duplicate item', name)
        equipment[name] = self
        self.name = name

        self.slots = tuple(s().name for s in slots)

        self.weight = NotImplemented
        self.base_cost = NotImplemented
        self.stats = Statable(attributes)
        self.weaponable = []

        for key, val in attributes.items():
            if key in ('weight', 'base_cost', 'stats', 'weaponable'):
                setattr(self, key, val)
            if key == 'bonus':
                self.stats[val[0]] = val[1]
            if key == 'attack':
                self.weaponable.append(val)

    def __str__(self):
        return self.name


#-----------------------------------------------------------------------------------------
def transverse(base, r=NotImplemented):
    r.append(base)
    for el in base.connected:
        transverse(el, r)
    return r

class Body:
    def __init__(self, base):

        self.inventory = []
        self.current = []

        self.parts = list(transverse(base, []))

        self.slots = defaultdict(lambda:[])
        for part in self.parts:
            for slot in part.slots:
                slot = slot()
                self.slots[slot.name].append(slot)

    def getEmptySlot(self, name):
        for s in self.slots[name]:
            if s.empty: return s
        raise Exception('no empty slots')


    def equip(self, item):
        assert type(item) == Equipment

        empty = {key:[s for s in slots if s.empty] for key,slots in self.slots.items()}

        for slot in item.slots:
            if len(empty[slot]) < item.slots.count(slot):
                print('already {} there'.format(item))
                return False

        for slot in item.slots:
            self.getEmptySlot(slot).add(item)
        self.inventory.remove(item)
        self.current.append(item)
        return True

    def remove(self, item):
        for slotname in self.slots:
            for slot in self.slots[slotname]:
                if slot.item == item:
                    slot.clear()
        self.current.remove(item)
        self.inventory.append(item)

    def display(self):
        for name, slot in self.slots.items():
            print(name.ljust(20), ''.join(str(s.item).ljust(30) for s in slot))


# -----------------------------------------------------------------------------------------
head = BodypartConstructor('head',   Slot.mask, Slot.helmet, vital=True)
torso = BodypartConstructor('torso', Slot.chest,Slot.amulet, vital=True)
arm = BodypartConstructor('arm',     Slot.arm)
hand = BodypartConstructor('hand',   Slot.hand, Slot.glove, Slot.ring)
leg = BodypartConstructor('leg',     Slot.leg)
foot = BodypartConstructor('foot',   Slot.shoe)

humanoid = Body(torso(head(), arm(hand()), arm(hand()), leg(foot()), leg(foot())))


class Race(Body):
    def __init__(self, body_trunk, **stats):
        self.racial_stats = Statable(stats)

    @property
    def stat(self):
        return self.base_stats + sum(item.stats for item in self.current) + sum(part.stats for part in self.parts)

    def new(self):


class Individual(Body):

    def __init__(self, **stats):
'''
Android's key advantage over iOS is the openness of the platform, which makes it difficult to monetize.

'''



