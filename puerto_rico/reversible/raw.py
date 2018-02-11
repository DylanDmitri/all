
class resource:
    cash = 'cash'
    dudes = 'dudes'
    vps = 'vps'

    all = ('cash', 'dudes', 'vps')

class crates:
    corn = 'crate_corn'
    indigo = 'crate_indigo'
    sugar = 'crate_sugar'
    tobacco = 'crate_tobacco'
    coffee = 'crate_coffee'

    all = ('crate_corn', 'crate_indigo', 'crate_sugar', 'crate_tobacco', 'crate_coffee')

class tiles:
    corn = 'tile_corn'
    indigo = 'tile_indigo'
    sugar = 'tile_sugar'
    tobacco = 'tile_tobacco'
    coffee = 'tile_coffee'
    quarry = 'tile_quarry'

    plantations = ('tile_corn', 'tile_indigo', 'tile_sugar', 'tile_tobacco', 'tile_coffee')
    all = ('tile_corn', 'tile_indigo', 'tile_sugar', 'tile_tobacco', 'tile_coffee', 'tile_quarry')

class buildings:
    small_indigo_plant = 'small_indigo_plant'
    small_sugar_mill = 'small_sugar_mill'
    indigo_plant = 'indigo_plant'
    sugar_mill = 'sugar_mill'
    tobacco_storage = 'tobacco_storage'
    coffee_roaster = 'coffee_roaster'
    small_market = 'small_market'
    hacienda = 'hacienda'
    construction_hut = 'construction_hut'
    small_warehouse = 'small_warehouse'
    hospice = 'hospice'
    office = 'office'
    large_market = 'large_market'
    large_warehouse = 'large_warehouse'
    university = 'university'
    factory = 'factory'
    harbor = 'harbor'
    wharf = 'wharf'
    guild_hall = 'guild_hall'
    fortress = 'fortress'
    city_hall = 'city_hall'
    customs_house = 'customs_house'
    residence = 'residence'

    all = ('small_indigo_plant','small_sugar_mill','indigo_plant','sugar_mill','tobacco_storage','coffee_roaster',
             'small_market','hacienda','construction_hut','small_warehouse','hospice','office','large_market',
             'large_warehouse','university','factory','harbor','wharf','guild_hall','fortress','city_hall',
             'customs_house','residence',)

class roles:
    planter = 'planter'
    mayor = 'mayor'
    trader = 'trader'
    builder = 'builder'
    producer = 'producer'
    shipper = 'shipper'
    investor = 'investor'

    all = ('planter','mayor','trader','builder','producer','shipper','investor')
