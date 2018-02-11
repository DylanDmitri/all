class Building:
    def __init__(self,tier=None,cost=None,name='',production=False,jobs=1):

        self.name = name
        self.tier = tier
        self.cost = cost
        self.production = production
        self.jobs = jobs

        self.vp = tier
        self.big = tier==4
        self.supply = (1, 2)[production]

    def pricewith(self, player):
        return self.cost - min(player.island.quarry, player.farmers.quarry, self.tier)

    def __str__(self):
        return ' '.join(word.capitalize() for word in self.name.split('_'))

class AleaBalanced:
    rules = lambda:None
    rules.role_cards_unused = 1
    rules.trading_house_size = 4

    roles = ('settler', 'mayor', 'builder', 'craftsman', 'trader', 'captain', 'prospector')

    farms = dict(coffee=8, tobacco=9, corn=10, sugar=11, indigo=12)
    rules.farm_stacks = 3
    quarries = 5

    buildings = [
        Building(tier=1, cost=1,  name='small_indigo_plant',   production=True),
        Building(tier=1, cost=2,  name='small_sugar_mill',     production=True),
        Building(tier=2, cost=3,  name='indigo_plant',         production=True, jobs=3),
        Building(tier=2, cost=4,  name='sugar_mill',           production=True, jobs=3),
        Building(tier=3, cost=5,  name='tobacco_storage',      production=True, jobs=3),
        Building(tier=3, cost=6,  name='coffee_roaster',       production=True, jobs=2),
        Building(tier=1, cost=1,  name='small_market'),
        Building(tier=1, cost=2,  name='hacienda'),
        Building(tier=1, cost=2,  name='construction_hut'),
        Building(tier=1, cost=3,  name='small_warehouse'),
        Building(tier=2, cost=4,  name='hospice'),
        Building(tier=2, cost=5,  name='office'),
        Building(tier=2, cost=5,  name='large_market'),
        Building(tier=2, cost=6,  name='large_warehouse'),
        Building(tier=3, cost=7,  name='university'),
        Building(tier=3, cost=8,  name='factory'),
        Building(tier=3, cost=8,  name='harbor'),
        Building(tier=3, cost=9,  name='wharf'),
        Building(tier=4, cost=10, name='guild_hall'),
        Building(tier=4, cost=10, name='fortress'),
        Building(tier=4, cost=10, name='city_hall'),
        Building(tier=4, cost=10, name='customs_house'),
        Building(tier=4, cost=10, name='residence'),
    ]

    colonist_ship_min = 2
    colonist_supply = 40

    crates = dict(corn=8, indigo=9, sugar=9, tobacco=7, coffee=7)

    cargoships = 4, 6
    vps = 65

    player_starts = [
        dict(tile='indigo', dubloons=3),
        dict(tile='corn', dubloons=2),
    ]