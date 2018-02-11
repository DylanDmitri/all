from puerto_rico.take7.fields import building, island_size

price = [None for _ in range(island_size)]
price[building.small_indigo_plant] = 1
price[building.small_sugar_mill] = 2
price[building.indigo_plant] = 3
price[building.sugar_mill] = 4
price[building.tobacco_storage] = 5
price[building.coffee_roaster] = 6
price[building.small_market] = 1
price[building.hacienda] = 2
price[building.construction_hut] = 2
price[building.small_warehouse] = 3
price[building.hospice] = 4
price[building.office] = 5
price[building.large_market] = 5
price[building.large_warehouse] = 6
price[building.university] = 8
price[building.factory] = 7
price[building.harbor] = 8
price[building.wharf] = 9
price[building.guild_hall] = 10
price[building.fortress] = 10
price[building.city_hall] = 10
price[building.customs_house] = 10
price[building.residence] = 10

tier = [None for _ in range(island_size)]
tier[building.small_indigo_plant] = 1
tier[building.small_sugar_mill] = 1
tier[building.indigo_plant] = 2
tier[building.sugar_mill] = 2
tier[building.tobacco_storage] = 3
tier[building.coffee_roaster] = 3
tier[building.small_market] = 1
tier[building.hacienda] = 1
tier[building.construction_hut] = 1
tier[building.small_warehouse] = 1
tier[building.hospice] = 2
tier[building.office] = 2
tier[building.large_market] = 2
tier[building.large_warehouse] = 2
tier[building.university] = 3
tier[building.factory] = 3
tier[building.harbor] = 3
tier[building.wharf] = 3
tier[building.guild_hall] = 4
tier[building.fortress] = 4
tier[building.city_hall] = 4
tier[building.customs_house] = 4
tier[building.residence] = 4

job_spots = {
    building.indigo_plant:3,
    building.sugar_mill:3,
    building.tobacco_storage:3,
    building.coffee_roaster:2
}