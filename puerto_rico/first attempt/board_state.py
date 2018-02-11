from random import shuffle

from puerto_rico.utils import *


class Ship:
    def __init__(self,size):
        self.total_spots = size
        self.empty_spots = size
        self.kind = None

class RoleCard:
    def __init__(self, name):
        self.name = name
        self.availible = True
        self.dubloons = 0

    def reset(self):
        if self.availible:
            self.dubloons += 1
        else:
            self.dubloons = 0
        self.availible = True

    def __str__(self):
        return self.name + ('(+{})'.format(self.dubloons) if self.dubloons else '')

def building(name=NotImplemented, kind='purple', tier=NotImplemented, cost=NotImplemented, max_workers=1):
    assert kind in ('purple', 'production')
    purple = kind=='purple'
    production = kind=='production'

    number = (3 if production else 2)
    vps = tier
    big = tier==4

    return Container(
        name=name,
        purple=purple,
        production=production,
        tier=tier,
        vps=vps,
        cost=cost,
        max_workers=max_workers,
        big=big,
        count=number,
        __str__=lambda self: self.name
    )



buildings = Container(
    indigo1       = building('small indigo plant', 'production', tier=1, cost=1),
    sugar1        = building('small sugar mill', 'production', tier=1, cost=2),
    indigo3       = building('indigo plant', 'production',  tier=2, cost=3, max_workers=3),
    sugar3        = building('sugar mill', 'production',  tier=2, cost=4, max_workers=3),
    tobacco3      = building('tobacco storage', 'production',  tier=3, cost=5, max_workers=3),
    coffee2       = building('coffee roaster', 'production',  tier=3, cost=6, max_workers=2),
    market1       = building('small market', tier=1, cost=1),
    hacienda      = building('hacienda', tier=1, cost=2),
    hut           = building('construction hut', tier=1, cost=2),
    warehouse1    = building('small warehouse', tier=1, cost=3),
    hospice       = building('hospice', tier=2, cost=4),
    office        = building('office', tier=2, cost=5),
    market2       = building('large market', tier=2, cost=5),
    warehouse2    = building('large warehouse', tier=2, cost=6),
    university    = building('university', tier=3, cost=7),
    factory       = building('factory', tier=3, cost=8),
    harbor        = building('harbor', tier=3, cost=8),
    wharf         = building('wharf', tier=3, cost=9),
    guild_hall    = building('guild hall', tier=4, cost=10),
    fortress      = building('fortress', tier=4, cost=10),
    city_hall     = building('city hall', tier=4, cost=10),
    customs_house = building('customs house', tier=4, cost=10),
    residence     = building('residence', tier=4, cost=10),
)

resources = dict(
    corn = Container(plantations=10,barrels=10,price=0,captain_value=1,natural=True),
    indigo = Container(plantations=12,barrels=11,price=1,captain_value=1,natural=False),
    sugar = Container(plantations=11,barrels=11,price=2,captain_value=1,natural=False),
    tobacco = Container(plantations=9,barrels=9,price=3,captain_value=1,natural=False),
    coffee = Container(plantations=8,barrels=9,price=4,captain_value=1,natural=False)
)

total_quarries = 8
victory_point_reserve = NotImplemented
colonist_reserve = NotImplemented       # 79
ships = NotImplemented                  # (4, 5, 6)
plantation_stacks = NotImplemented
roles = 'settler', 'mayor', 'builder', 'craftsman', 'trader', 'captain'

class BoardState:
    """
    this holds what resources are present
    """
    def __init__(self):

        self.roleCards = tuple(RoleCard(name) for name in roles)

        self.quarry_stack = total_quarries
        self.victory_point_reserve = victory_point_reserve
        self.colonist_reserve = colonist_reserve
        self.colonist_ship = 0
        self.new_colonists = 0

        self.building_counts = {name:buildings[name].count for name in buildings}
        self.barrel_counts = {name:resources[name].barrels for name in resources}

        self.trading_house = []

        self.ships = tuple(Ship(num) for num in ships)

        self.plantation_deck = []
        for resource_name in ('corn','indigo','sugar','tobacco','coffee'):
            self.plantation_deck.extend([resource_name] * resources[resource_name].plantations)
        self.plantation_discard = []
        self.active_plantations = []
        self.plantation_stacks = plantation_stacks

        self.game_ending = False

    def take_plantation(self, name):
        if name == 'quarry':
            assert self.quarry_stack
            self.quarry_stack -= 1
        else:
            assert name in self.active_plantations
            self.active_plantations.remove(name)

    def settler_reset(self):
        self.plantation_discard.extend(self.active_plantations)   # clear the unpicked ones

        for _ in range(self.plantation_stacks):    # refill the active row
            if not self.plantation_deck:
                self.plantation_deck = self.plantation_discard
                shuffle(self.plantation_deck)
            self.active_plantations.append(self.plantation_deck.pop())

        debug('plantations reset', c=3)

    def mayor_reset(self):
        # there is no assert here.
        # if number is 'too big' colonist reserve goes negative triggering game end

        self.colonist_ship += self.new_colonists
        self.colonist_reserve -= self.new_colonists

        debug(self.new_colonists, 'colonists loaded onto ship', c=3)
        debug(self.colonist_reserve, 'colonists remaining in reserve', c=3)

    def build(self, name):
        assert self.building_counts[name]
        self.building_counts[name] -= 1

    def builder_reset(self):
        pass

    def barrel_production(self, **kwargs):
        for name, amount in kwargs.items():
            assert name in self.barrel_counts
            assert self.barrel_counts[name] >= amount
            self.barrel_counts[name] -= amount

    def trade(self, item):
        assert len(self.trading_house) < 4
        self.trading_house.append(item)

    def trader_reset(self):
        if len(self.trading_house) == 4:
            for b in self.trading_house:
                self.barrel_counts[b] += 1
            self.trading_house = []

            debug('trading house cleared', c=3)

    def load(self, kind, number, ship):
        ship = (s for s in self.ships if s.total_spots==ship)[0]

        assert number <= ship.empty_spots
        assert ship.kind is None or kind == ship.kind

        ship.kind = kind
        ship.empty_spots -= number

    def captain_reset(self):
        for ship in self.ships:
            if ship.empty_spots == 0:
                self.barrel_counts[ship.kind] += ship.total_spots
                ship.empty_spots = ship.total_spots
                ship.kind = None

                debug('ship', ship.total_spots, 'has sailed', c=3)







