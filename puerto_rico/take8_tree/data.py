
class State:

    p1_victory, p2_victory, draw, role_choice, hacienda_choice, hacienda_flip, planter, tile_flip, build, mayor_bonus, \
    assign_work_up, assign_work_down, craft_bonus, trade, ship = range(15)

    lookup = list("p1_victory, p2_victory, draw, role_choice, hacienda_choice, hacienda_flip, planter, tile_flip, build, mayor_bonus, assign_work_up, assign_work_down, craft_bonus, trade, ship".split(','))




class role:
    planter = 0
    builder = 1
    mayor = 2
    producer = 3
    trader = 4
    shipper = 5
    banker = 6

    all = tuple(range(7))

role_lookup = 'planter', 'builder', 'mayor', 'producer', 'trader', 'shipper', 'banker'

class crate:
    corn = 0
    indigo = 1
    sugar = 2
    tobacco = 3
    coffee = 4

    all = tuple(range(5))

class tile:
    corn = 0
    indigo = 1
    sugar = 2
    tobacco = 3
    coffee = 4
    quarry = 5

    farms = tuple(range(5))
    all = tuple(range(6))

tile_lookup = 'corn','indigo','sugar','tobacco','coffee','quarry'
building_lookup = 'corn','indigo','sugar','tobacco','coffee','quarry','small_indigo_plant','small_sugar_mill','indigo_plant','sugar_mill','tobacco_storage',\
                  'coffee_roaster','small_market','hacienda','construction_hut','small_warehouse','hospice',\
                  'office','large_market','large_warehouse','university','factory','harbor','wharf','guild_hall',\
                  'fortress','city_hall','customs_house','residence'
island_lookup = tile_lookup + building_lookup

class building:

    small_indigo_plant = 6
    small_sugar_mill = 7
    indigo_plant = 8
    sugar_mill = 9
    tobacco_storage =  10
    coffee_roaster = 11
    small_market = 12
    hacienda = 13
    construction_hut =  14
    small_warehouse = 15
    hospice =  16
    office = 17
    large_market = 18
    large_warehouse = 19
    university = 20
    factory =  21
    harbor =  22
    wharf = 23
    guild_hall = 24
    fortress = 25
    city_hall = 26
    customs_house = 27
    residence = 28

    all = tuple(range(6, 29))
    tiers = (0,0,0,0,0,0,1,1,2,2,3,3,1,1,1,1,2,2,2,2,3,3,3,3, 4, 4, 4, 4, 4)
    costs = (0,0,0,0,0,0,1,2,3,4,5,6,1,2,2,3,4,5,5,6,8,7,8,9,10,10,10,10,10)

class island:
    corn,indigo,sugar,tobacco,coffee,quarry, \
    small_indigo_plant, small_sugar_mill, indigo_plant, sugar_mill, tobacco_storage, coffee_roaster, small_market, \
    hacienda, construction_hut, small_warehouse, hospice, office, large_market, large_warehouse, university, \
    factory, harbor, wharf, guild_hall, fortress, city_hall, customs_house, residence, \
     = range(29)

    all = tuple(range(29))

    workers = (1,1,1,1,1,1,1,1,3,3,3,2,1,1,1,1,1,1,1,1,1,1,1,1, 1, 1, 1, 1, 1)



def TileStore():
    return [0 for _ in tile.all]

def CrateStore():
    return [0 for _ in crate.all]

def RoleStore():
    return [0 for _ in role.all]

def IslandStore():
    return [0 for _ in island.all]
