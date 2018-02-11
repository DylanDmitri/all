from puerto_rico.TopDown.game import Game
from puerto_rico.TopDown.human_player import HumanPlayer


class GenericBuilding:
    def __init__(self, tier, cost, count, production=False, jobs=1):
        self.production = production
        self.tier = tier
        self.cost = cost
        self.count = count
        self.jobs = jobs

        if tier==4: self.count=1
        elif production: self.count = 3
        else: self.count = 2

all_roles = ('settler', 'mayor', 'builder', 'craftsman', 'trader', 'captain', )
prospector = ('prospector', )

vanilla_buildings = dict(
    #                                         tier cost count
    small_indigo_plant      = GenericBuilding(1,   1,   3, production=True),
    small_sugar_mill        = GenericBuilding(1,   2,   3, production=True),
    indigo_plant            = GenericBuilding(2,   3,   3, production=True, jobs=3),
    sugar_mill              = GenericBuilding(2,   4,   3, production=True, jobs=3),
    tobacco_storage         = GenericBuilding(3,   5,   3, production=True, jobs=3),
    coffee_roaster          = GenericBuilding(3,   6,   3, production=True, jobs=2),

    small_market            = GenericBuilding(1,   1,   2),
    hacienda                = GenericBuilding(1,   2,   2),
    construction_hut        = GenericBuilding(1,   2,   2),
    small_wharehouse        = GenericBuilding(1,   3,   2),
    hospice                 = GenericBuilding(2,   4,   2),
    office                  = GenericBuilding(2,   5,   2),
    large_market            = GenericBuilding(2,   5,   2),
    large_wharehouse        = GenericBuilding(2,   6,   2),
    university              = GenericBuilding(3,   7,   2),
    factory                 = GenericBuilding(3,   8,   2),
    harbor                  = GenericBuilding(3,   8,   2),
    wharf                   = GenericBuilding(3,   9,   2),
    guild_hall              = GenericBuilding(4,   0,   1),
    fortress                = GenericBuilding(4,   0,   1),
    city_hall               = GenericBuilding(4,   0,   1),
    customs_house           = GenericBuilding(4,   0,   1),
    residence               = GenericBuilding(4,   0,   1),
)

default = dict(
    dubloons = (60, 60, 60, 60, 60),
    colonists = (42, 58, 79, 100, 121),
    vps = (65, 75, 100, 122, 150),

    tile_quarry = (5, 8, 8, 8, 10),
    tile_corn = (7, 10, 10, 10, 12),
    tile_indigo = (9, 12, 12, 12, 15),
    tile_sugar = (8, 11, 11, 11, 14),
    tile_tobacco = (6, 9, 9, 9, 11),
    tile_coffee = (5, 8, 8, 8, 10),

    barrel_corn = (8, 10, 10, 10, 12),
    barrel_indigo = (9, 11, 11, 11, 14),
    barrel_sugar = (9, 11, 11, 11, 14),
    barrel_tobacco = (7, 9, 9, 9, 11),
    barrel_coffee = (7, 9, 9, 9, 11),

    roles_per_round = (6, 3, 4, 5),
    roles = (all_roles+prospector, all_roles, all_roles+prospector, all_roles+prospector+prospector),
    ships = ((4,6), (4, 5, 6), (5, 6, 7), (6, 7, 8), (7, 8, 9)),
    start_money = (3, 2, 3, 4, 5),
    start_plantations = ('ic', 'iic', 'iicc', 'iiicc', 'iiiccc'),
    plantation_stacks = (3, 4, 5, 6, 7),
)


# ======= BEGIN CHANGEABLE DATA =========

# ----- general game settings ------
# change the numPlayers here
players = (HumanPlayer, HumanPlayer)

# ----- more advanced options ------
# (leave this line alone)
settings = {k:v[len(players)-2] for k,v in default.items()}

# then, you can change individual settings here

settings['corn_player_dubloon_penalty'] = True


# settings['barrels_corn'] = 4
# settings['colonists'] = 10

# ----- building settings ------

buildings = vanilla_buildings


# take out buildings on the two-player version
if len(players)==2:
    for name, building in buildings.items():
        if building.production:
            building.count = 2
        else:
            building.count = 1

# ======= END CHANGEABLE DATA =========

g = Game(players, settings, buildings)

while True:
    g.flipTiles()
