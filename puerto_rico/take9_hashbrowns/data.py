
state_lookup = list("p1_victory, p2_victory, draw, role_choice, hacienda_choice, hacienda_flip, planter, tile_flip, build, mayor_bonus, assign_work_up, assign_work_down, craft_bonus, trade, ship".split(','))
role_lookup = 'planter', 'builder', 'mayor', 'producer', 'trader', 'shipper', 'banker'

tile_lookup = 'corn','indigo','sugar','tobacco','coffee','quarry'
building_lookup = 'corn','indigo','sugar','tobacco','coffee','quarry','small_indigo_plant','small_sugar_mill','indigo_plant','sugar_mill','tobacco_storage',\
                  'coffee_roaster','small_market','hacienda','construction_hut','small_warehouse','hospice',\
                  'office','large_market','large_warehouse','university','factory','harbor','wharf','guild_hall',\
                  'fortress','city_hall','customs_house','residence'
island_lookup = tile_lookup + building_lookup


class State:

    p1_victory, p2_victory, draw, role_choice, hacienda_choice, hacienda_flip, planter, tile_flip, build, mayor_bonus, \
    assign_work_up, assign_work_down, craft_bonus, trade, ship = range(15)

class Role:
    planter = 0
    builder = 1
    mayor = 2
    producer = 3
    trader = 4
    shipper = 5
    banker = 6

    all = tuple(range(7))

class Data:
    corn,indigo,sugar,tobacco,coffee,quarry, \
    small_indigo_plant, small_sugar_mill, indigo_plant, sugar_mill, tobacco_storage, coffee_roaster, small_market, \
    hacienda, construction_hut, small_warehouse, hospice, office, large_market, large_warehouse, university, \
    factory, harbor, wharf, guild_hall, fortress, city_hall, customs_house, residence, \
     = range(29)

    all = tuple(range(29))
    buildings = tuple(range(6, 29))
    crates = tuple(range(5))
    farms = tuple(range(5))
    tiles = tuple(range(6))

    tiers = (0,0,0,0,0,0,1,1,2,2,3,3,1,1,1,1,2,2,2,2,3,3,3,3, 4, 4, 4, 4, 4)
    costs = (0,0,0,0,0,0,1,2,3,4,5,6,1,2,2,3,4,5,5,6,8,7,8,9,10,10,10,10,10)
    workers = (1,1,1,1,1,1,1,1,3,3,3,2,1,1,1,1,1,1,1,1,1,1,1,1, 1, 1, 1, 1, 1)



def TileStore():
    return [0 for _ in Data.tiles]

def CrateStore():
    return [0 for _ in Data.crates]

def RoleStore():
    return [0 for _ in Role.all]

def IslandStore():
    return [0 for _ in Data.all]
