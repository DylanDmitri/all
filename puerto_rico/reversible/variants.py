from puerto_rico.reversible.enum import *

def game():
    return bytearray([0 for _ in range(190)])

def twoPlayer():
    self = game()

    self[card_planter_open] = 1
    self[card_mayor_open] = 1
    self[card_trader_open] = 1
    self[card_builder_open] = 1
    self[card_producer_open] = 1
    self[card_shipper_open] = 1
    self[card_investor_open] = 1
    self[tile_deck_corn] = 7
    self[tile_deck_indigo] = 9
    self[tile_deck_sugar] = 8
    self[tile_deck_tobacco] = 6
    self[tile_deck_coffee] = 5
    self[tile_quarry] = 5
    self[crate_corn] = 8
    self[crate_indigo] = 9
    self[crate_sugar] = 9
    self[crate_tobacco] = 7
    self[crate_coffee] = 7
    self[vps] = 65
    self[active] = 0
    self[settler_ship] = 2
    self[settler_store] = 40
    self[role_user] = 1
    self[supply_small_indigo_plant] = 2
    self[supply_small_sugar_mill] = 2
    self[supply_indigo_plant] = 2
    self[supply_sugar_mill] = 2
    self[supply_tobacco_storage] = 2
    self[supply_coffee_roaster] = 2
    self[supply_small_market] = 1
    self[supply_hacienda] = 1
    self[supply_construction_hut] = 1
    self[supply_small_warehouse] = 1
    self[supply_hospice] = 1
    self[supply_office] = 1
    self[supply_large_market] = 1
    self[supply_large_warehouse] = 1
    self[supply_university] = 1
    self[supply_factory] = 1
    self[supply_harbor] = 1
    self[supply_wharf] = 1
    self[supply_guild_hall] = 1
    self[supply_fortress] = 1
    self[supply_city_hall] = 1
    self[supply_customs_house] = 1
    self[supply_residence] = 1
    self[p1_farm_indigo] = 1
    self[p1_cash] = 3
    self[p2_farm_corn] = 1
    self[p2_cash] = 2

    return bytes(self)








