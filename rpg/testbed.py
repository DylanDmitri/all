
class FullBarError(Exception):
    """That bar is already full."""

class CardNotFoundError(Exception):
    """Card not found"""

cards = {}
class Card:
    def __init__(self, link, name, size, bar):
        cards[name] = self
        self.name = name
        self.size = size
        self.bar = bar
        self.linked = link

class MeleeWeapon:
    def __init__(self, name, size):
        self.card = Card(self, name, size, 'phys')
        self.skill = 2
        self.power = size
        self.reach = size
        self.armorPen = 0

        dict(
            sword = dict(skill=1),
            spear = dict(reach=1),
            axe = dict(power=1),
            club = dict(armorPen=2)
            
        )

class Bar:
    def __init__(self, size):
        self.size = size
        self._fill = 0
        self._items = []

    def __iter__(self):
        return self._items.__iter__()

    def append(self, card):
        if card.size + self._fill > self.size:
            raise FullBarError
        self._items.append(card)
        self._fill += card.size

    def remove(self, card):
        if card not in self._items:
            raise CardNotFoundError
        self._items.remove(card)

class Unit:
    def __init__(self, phys=2, ment=2, luck=4):
        self.phys = Bar(2)
        self.ment = Bar(2)
        self.luck = 4

    def equip(self, card):
        {'phys':self.phys, 'ment':self.ment}[card.bar].append(card)

    @property
    def attack(self):




