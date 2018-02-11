from puerto_rico.utils import *

CITY_SPACES = 12
MAX_BIG_BUILDINGS = 4
FARM_SPACES = 12

class Tile:
    def __init__(self, name, spaces):
        self.name = name
        self.spaces = spaces
        self.vacant = self.spaces


class PlayerShell:
    def __init__(self, game, name, brain):
        self.game = game
        self.name = name
        self.brain = brain
        self.role = False
        self.colonists = 0
        self.dubloons = 0

        self.farm = []
        self.city = []

        self.hospice_procced = False

    def log(self, *items, ret=0, **kwargs):
        debug('\n'*ret+self.name, *items, **kwargs)

    def decision(self, options):
        res = options[self.brain(str(o) for o in options)]
        self.log('chooses', res)
        return res

    def settler_phase(self):
        self.log('settler phase', ret=1)
        self.hospice_procced = False

        if len(self.farm) == FARM_SPACES:
            self.log('no room for new farm tile')
            return

        if self.active('hacienda'):
            name = self.game.board.plantation_deck.pop()
            self.addFarmTile(name)

        choices = 'no tile',

        if len(self.farm) <= FARM_SPACES:
            choices += tuple(self.game.board.active_plantations)
        if (self.roleBonus or self.active('construction hut')) and self.game.board.quarry_stack:
            choices += 'quarry',

        choice = self.decision(choices)
        if choice == 'no tile':
            return
        self.game.board.take_plantation(choice)
        self.addFarmTile(choice)

    def addFarmTile(self, name):
        tile = Tile(name, 1)
        if not self.hospice_procced and self.active('hospice'):
            tile.vacant = 0
            self.colonists += 1
            self.hospice_procced = True

        self.log('builds new', tile.name)
        self.farm.append(tile)

    def get_dubloons(self, amoount):
        self.dubloons += amoount
        self.log('gains', amoount, 'dubloons')


    def mayor_phase(self):
        if self.roleBonus:
            self.get_colonists(1)

    def get_colonists(self, amount):
        self.log('gains', amount, 'colonists')
        self.colonists += 1

    @property
    def roleBonus(self):
        if self.role:
            self.log('role bonus activated')
            return True
        return False

    def active(self, name):
        for b in self.city:
            if b.name == name and not b.vacant:
                self.log('activates', name, '-')
                return True
        return False



