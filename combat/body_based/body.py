from random import random

from combat.body_based.enums import *


class BodyPart:
    def __init__(self, *children):
        self.name = 'snoobet'

        self.children = list(children)
        for child in self.children:
            child.parent = self
        self.parent = NotImplemented

        self.hitpoints = 10
        self.bleeding = 0

        self.armor = None

        self.init()

    def init(self):
        NotImplemented

    def take_damage(self,severity,damage_type):

        if damage_type == dmgType.slice:
            self.bleeding += severity
            self.hitpoints -= severity
            self.slice(severity)

        elif damage_type == dmgType.crush:
            self.hitpoints -= severity
            self.crush(severity)

        elif damage_type == dmgType.stab:
            self.bleeding += 1
            self.hitpoints -= severity
            self.stab(severity)

        else:
            try:
                getattr(self, damage_type)(self, severity)
            except AttributeError:
                print('unknown damage type', damage_type)
                exit()

    def update(self):
        pass


class Limb(BodyPart):
    def init(self):
        self.tendons = internals.tendons
        self.bone = internals.bone
        self.internals = [self.tendons, self.bone]

    def slice(self, severity):
        if severity > 3:
            self.parent.bleeding = severity
            self.parent.children.remove(self)
            self.parent = None
            self.tendons.functional = False
            add_condition(self, conditions.detatched)

        if random() < .1 * severity:
            self.tendons.functional = False

    def crush(self, severity):
        if severity > 3:
            self.bone.functional = False

    def stab(self, severity):

        if severity > 2:
            add_condition(self, conditions.impaled)

        if random() < .05 * severity:
            self.tendons.functional = False

    @property
    def strength(self):
        if self.hitpoints > 0 and self.tendons.functional and self.bone.functional:
            return self.hitpoints
        return 0



class Creature:
    def __init__(self, base_part):
        self.base_part = base_part
        self.blood = 100
        self.update()

    def __iter__(self):
        return self._traverse(self.base_part)

    def _traverse(self, part):
        yield part
        for p in part.children:
            self._traverse(p)

    def update(self):

        self.stats = StatBlock()

        for part in self:
            part.update()
            self.blood -= part.bleeding

            for piece in dir(part):
                piece = getattr(part, piece)
                if type(piece) == Internal:
                    for stat, amount in piece.stats.items():
                        setattr(self.stats, stat, getattr(self.stats, stat) + amount)




