from copy import deepcopy


def datastruct(**fields):
    class temp:
        def __init__(self, **const):
            for k, v in fields.items():
                setattr(self, k, const.get(k, v))
    return temp

class Container(list):
    def __init__(self, *args):
        list.__init__(self, args)
        for a in self:
            setattr(self, a.name, a)

role = datastruct(name='', start=None, each=None, end=None)
resource = datastruct(name='', cost=0, supply=0, farmPer=1, processingPer=1, captainValue=1)
tile = datastruct(name='', supply=0, jobs=1, output=(0, 1))

class building:
    def __init__(self, tier=None, cost=None, supply=None, exp=0, name='', production=False, jobs=1, big=None, vp=None):
        self.name = name
        self.tier = tier
        self.cost = cost
        self.production = production
        self.jobs = jobs

        if vp is None:
            vp = tier
        self.vp = vp

        if big is None:
            big = tier==4
        self.big = big

        if supply is None:
            supply = 2
            if production: supply += 1
            if production and tier==1: supply += 1
            if big: supply -= 1

default_settings = object()


# ====== change stuff here ======


default_settings.vps = NotImplemented
default_settings.colonists = NotImplemented
default_settings.money = float('inf')

default_settings.resources = Container(
    resource(name='corn', supply=10, cost=0, processingPer=0),
    resource(name='indigo', supply=11, cost=1),
    resource(name='sugar', supply=11, cost=2),
    resource(name='tobacco', supply=9,  cost=3),
    resource(name='coffee', supply=9,  cost=4),
)

default_settings.plantations = Container(
    tile(name='corn',   supply=10),
    tile(name='indigo', supply=12),
    tile(name='sugar',  supply=11),
    tile(name='tobacco',supply=9),
    tile(name='coffee', supply=8),
)
default_settings.quarry = tile(name="quarry", supply=8)

default_settings.roles = Container(
    role(name='settler', each='choose_tiles', end='reset_plantations'),
    role(name='mayor', start='distribute_colonists', each='choose_work', end='reset_colonists'),
    role(name='builder', each='choose_building'),
    role(name='craftsman', each='produce_goods'),
    role(name='trader', each='choose_trade', end='clear_house'),
    role(name='captain', each='choose_ship', end='clear_ship'),
    role(name='prospector', start='mine_gold'),
    role(name='politician', start='choose_role', each='politic_each', end='politic_end'),
    role(name='pirate', start='plunder')
)

buildings = Container(
    building(tier=1, cost=1,  name='small_indigo_plant',   production=True),
    building(tier=1, cost=2,  name='small_sugar_mill',     production=True),
    building(tier=2, cost=3,  name='indigo_plant',         production=True, jobs=3),
    building(tier=2, cost=4,  name='sugar_mill',           production=True, jobs=3),
    building(tier=3, cost=5,  name='tobacco_storage',      production=True, jobs=3),
    building(tier=3, cost=6,  name='coffee_roaster',       production=True, jobs=2),
    building(tier=1, cost=1,  name='small_market'),     # money from trader
    building(tier=1, cost=2,  name='hacienda'),         # s
    building(tier=1, cost=2,  name='construction_hut'), # s
    building(tier=1, cost=3,  name='small_warehouse'),  # storage
    building(tier=2, cost=4,  name='hospice'),
    building(tier=2, cost=5,  name='office'),
    building(tier=2, cost=5,  name='large_market'),
    building(tier=2, cost=6,  name='large_warehouse'),
    building(tier=3, cost=8,  name='university'),
    building(tier=3, cost=7,  name='factory'),
    building(tier=3, cost=8,  name='harbor'),
    building(tier=3, cost=9,  name='wharf'),
    building(tier=4, cost=10, name='guild_hall'),
    building(tier=4, cost=10, name='fortress'),
    building(tier=4, cost=10, name='city_hall'),
    building(tier=4, cost=10, name='customs_house'),
    building(tier=4, cost=10, name='residence'),

    building(tier=1, cost=1,  exp=1, name='aqueduct'),
    building(tier=1, cost=2,  exp=1, name='forest_house'),
    building(tier=1, cost=2,  exp=1, name='black_market'),
    building(tier=1, cost=3,  exp=1, name='storehouse'),
    building(tier=2, cost=4,  exp=1, name='guest_house'),
    building(tier=2, cost=5,  exp=1, name='trading_post'),
    building(tier=2, cost=5,  exp=1, name='church'),
    building(tier=2, cost=6,  exp=1, name='small_wharf'),
    building(tier=3, cost=7,  exp=1, name='lighthouse'),
    building(tier=3, cost=8,  exp=1, name='specialty_factory'),
    building(tier=3, cost=8,  exp=1, name='library'),   # should fire once per turn at most
    building(tier=3, cost=9,  exp=1, name='union_hall'),
    building(tier=4, cost=10, exp=1, vp=8, name='statue'),
    building(tier=4, cost=10, exp=1, name='cloister'),

    building(tier=1, cost=2,  exp=2, name='land_office'),
    building(tier=1, cost=3,  exp=2, name='chapel'),
    building(tier=2, cost=4,  exp=2, name='hunting_lodge'),
    building(tier=2, cost=5,  exp=2, name='zoning_office'),
    building(tier=2, cost=6,  exp=2, name='royal_supplier'),
    building(tier=3, cost=7,  exp=2, name='villa'),
    building(tier=3, cost=8,  exp=2, name='jeweler', production=True),
    building(tier=4, cost=10, exp=2, name='royal_garden'),
)

default_settings.buildings = Container(*(b for b in buildings if b.exp==0))


def generate_settings(
        numPlayers = None,
        corn_player_balance = True,
        university_factory_swap = True,
        nobles_on_ships = False,
        additional_role_cards = None,
    ):
    settings = deepcopy(default_settings)


    # draft buildings here


    settings.vp = (65, 75, 100, 122)[numPlayers-2]
    settings.colonists = 15 + numPlayers * 2
    settings.ship_min = numPlayers
    settings.ship_start = numPlayers

    settings.start_money = numPlayers - 1
    if numPlayers==2: settings.start_money = 3
    settings.start_indigo = ((0,), (0, 1), (0, 1), (0, 1, 2), (0, 1, 2))
    settings.plantation_stacks = numPlayers + 1


    # strip buildings for alea variant
    if numPlayers == 2:
        for b in settings.buildings:
            if b.production and b.exp==0: b.supply = 2
            else: b.supply = 1

        for r in settings.resources:
            r.supply -= 2

        for p in settings.plantations:
            p.supply -= 3
        settings.quarry.supply -= 3


    settings.role_cards = [role.name for role in default_settings.roles if role.name != 'prospector']
    if additional_role_cards is None:
        additional_role_cards = []
        if numPlayers == 2:
            additional_role_cards.append('prospector')
        if numPlayers == 4:
            additional_role_cards.append('prospector')
        if numPlayers >= 5:
            additional_role_cards.append('prospector')
            additional_role_cards.append('prospector')
    if type(additional_role_cards) is str:
        additional_role_cards = [additional_role_cards, ]
    elif type(additional_role_cards) is tuple:
        additional_role_cards = list(additional_role_cards)
    settings.role_cards += additional_role_cards

    if university_factory_swap:
        if 'university' in settings.buildings:
            settings.buildings.university.cost = 7
        if 'factory' in settings.buildings:
            settings.buildings.factory.cost = 8

    settings.rules = object()
    settings.rules.corn_player_balance = corn_player_balance
    settings.rules.nobles_on_ships = nobles_on_ships

    return settings







