
class role:
    planter = 0
    builder = 1
    mayor = 2
    producer = 3
    trader = 4
    shipper = 5
    banker = 6

    lookup = ('planter', 'builder', 'mayor', 'producer', 'trader', 'shipper', 'banker')

class tile:
    corn = 0
    indigo = 1
    sugar = 2
    tobacco = 3
    coffee = 4
    quarry = 5

    lookup = ('corn','indigo','sugar','tobacco','coffee')

class crate:
    corn = 0
    indigo = 1
    sugar = 2
    tobacco = 3
    coffee = 4

class building:
    small_indigo_plant = 5
    small_sugar_mill = 6
    indigo_plant = 7
    sugar_mill = 8
    tobacco_storage = 9
    coffee_roaster = 10
    small_market = 11
    hacienda = 12
    construction_hut = 13
    small_warehouse = 14
    hospice = 15
    office = 16
    large_market = 17
    large_warehouse = 18
    university = 19
    factory = 20
    harbor = 21
    wharf = 22
    guild_hall = 23
    fortress = 24
    city_hall = 25
    customs_house = 26
    residence = 27
    idle = 28
island_size = 29

class states:
    settup = 'settup'
    role_choice = 'role_choice'
    tile_flip = 'tile_flip'
    hacienda_choice = 'hacienda_choice'
    hacienda_flip = 'hacienda_flip'
    planter_main = 'planter_main'
    mayor_bonus = 'mayor_bonus'
    assign_work = 'assign_work'
    settler_ship = 'settler_ship'


    p1_victory = 'p1_victory'
    p2_victory = 'p2_victory'
    draw = 'draw'

# per player

island = 0
crates = 1
jobs = 2
cash = 3
vp = 4




