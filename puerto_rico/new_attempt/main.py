from puerto_rico.new_attempt.utils import *
from puerto_rico.new_attempt.game import *


all_roles = ('settler', 'mayor', 'builder', 'craftsman', 'trader', 'captain', )
prospector = ('prospector', )

default = dict(
    colonists = (42, 58, 79, 100, 121),
    dubloons = [float('inf')]*5,
    vps = (65, 75, 100, 122, 150),

    tile_quarry = (5, 8, 8, 8, 10),
    tile_corn = (7, 10, 10, 10, 12),
    tile_indigo = (9, 12, 12, 12, 15),
    tile_sugar = (8, 11, 11, 11, 14),
    tile_tobacco = (6, 9, 9, 9, 11),
    tile_coffee = (5, 8, 8, 8, 10),

    barrels_corn = (8, 10, 10, 10, 12),
    barrels_indigo = (9, 11, 11, 11, 14),
    barrels_sugar = (9, 11, 11, 11, 14),
    barrels_tobacco = (7, 9, 9, 9, 11),
    barrels_coffee = (7, 9, 9, 9, 11),

    roles_per_round = (6, 3, 4, 5),
    roles = (all_roles+prospector, all_roles, all_roles+prospector, all_roles+prospector+prospector),
    ships = ((4,6), (4, 5, 6), (5, 6, 7), (6, 7, 8), (7, 8, 9)),
    start_money = (3, 2, 3, 4, 5),
    start_plantations = ('ic', 'iic', 'iicc', 'iiicc', 'iiiccc'),
    plantation_stacks = (3, 4, 5, 6, 7),
)


# ----- general game settings ------
# change the numPlayers here
numPlayers = 2

# this line looks up the defaults based on the number of players
settings = Container(**{k:v[numPlayers-2] for k,v in default.items()})

# then, you can change individual settings here
# settings.barrels_corn = 4
# settings.colonists = 10


# ----- building settings ------
buildings = default_buildings()



game = Game(numPlayers=2, settings=settings, buildings=buildings)




