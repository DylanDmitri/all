
import math

# assumptions
# one player gets at least 2 vps
# less than 15 settlers on ship
# less than 8 dubloons on a card

fields = [
    ('role_planter', 2),
    ('role_builder', 2),
    ('role_mayor', 2),
    ('role_farmer', 2),
    ('role_trader', 2),
    ('role_captain', 2),
    ('role_investor', 2),
    ('role_money_which', 7),
    ('role_money_amount', 8),
    ('tiles_corn', 8),
    ('tiles_indigo', 10),
    ('tiles_sugar', 9),
    ('tiles_tobacco', 7),
    ('tiles_coffee', 6),
    ('tiles_slot1', 5),
    ('tiles_slot2', 5),
    ('tiles_slot3', 5),
    ('settler_ship', 16),
    ('cargo4_kind', 5),
    ('cargo4_fill', 5),
    ('cargo6_kind', 5),
    ('cargo6_fill', 7),
    ('trade_corn', 5),
    ('trade_indigo', 5),
    ('trade_sugar', 5),
    ('trade_tobacco', 5),
    ('trade_coffee', 5),

    ('p1_vps', 64),
    ('p1_men', 40),
    ('p1_cash', 20),
    ('p1_tiles_corn', 8),
    ('p1_tiles_indigo', 10),
    ('p1_tiles_sugar', 9),
    ('p1_tiles_tobacco', 7),
    ('p1_tiles_coffee', 6),
    ('p1_tiles_quarry', 6),
    ('p1_small_indigo_plant', 3),
    ('p1_small_sugar_mill', 3),
    ('p1_indigo_plant', 5),
    ('p1_sugar_mill', 5),
    ('p1_tobacco_storage', 5),
    ('p1_coffee_roaster', 4),
    ('p1_small_market', 2),
    ('p1_hacienda', 2),
    ('p1_construction_hut', 2),
    ('p1_small_warehouse', 2),
    ('p1_hospice', 2),
    ('p1_office', 2),
    ('p1_large_market', 2),
    ('p1_large_warehouse', 2),
    ('p1_university', 2),
    ('p1_factory', 2),
    ('p1_harbor', 2),
    ('p1_wharf', 2),
    ('p1_guild_hall', 2),
    ('p1_fortress', 2),
    ('p1_city_hall', 2),
    ('p1_customs_house', 2),
    ('p1_hut_used', 2),
    ('p1_wharf_used', 2),

    ('p2_vps',64),
    ('p2_men',40),
    ('p2_cash',20),
    ('p2_tiles_corn',8),
    ('p2_tiles_indigo',10),
    ('p2_tiles_sugar',9),
    ('p2_tiles_tobacco',7),
    ('p2_tiles_coffee',6),
    ('p2_tiles_quarry',6),
    ('p2_small_indigo_plant',3),
    ('p2_small_sugar_mill',3),
    ('p2_indigo_plant',5),
    ('p2_sugar_mill',5),
    ('p2_tobacco_storage',5),
    ('p2_coffee_roaster',4),
    ('p2_small_market',2),
    ('p2_hacienda',2),
    ('p2_construction_hut',2),
    ('p2_small_warehouse',2),
    ('p2_hospice',2),
    ('p2_office',2),
    ('p2_large_market',2),
    ('p2_large_warehouse',2),
    ('p2_university',2),
    ('p2_factory',2),
    ('p2_harbor',2),
    ('p2_wharf',2),
    ('p2_guild_hall',2),
    ('p2_fortress',2),
    ('p2_city_hall',2),
    ('p2_customs_house',2),
    ('p1_hut_used',2),
    ('p1_wharf_used',2),
]


class Game:
    def __init__(self):
        for name, val in fields:
            setattr(self, name, 0)



a = Game()

from sys import getsizeof

print(getsizeof(a))
print(a.p2_office)




