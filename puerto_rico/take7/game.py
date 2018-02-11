from puerto_rico.take7.fields import *
from puerto_rico.take7.buildings import *


class InvalidChoiceError(Exception):
    """A problem was encountered."""

class Settings:
    VP_LIMIT = 75
    SETTLER_LIMIT = 42

    TILES = (7, 9, 8, 6, 5)

class Game(list):
    def __init__(self):
        list.__init__(self, [None for _ in range(game_size)])

        self[0+island] = [0 for _ in range(island_size)]
        self[0+crates] = [0 for _ in range(5)]
        self[0+jobs] = [0 for _ in range(island_size)]
        self[0+vp] = 0

        self[5+island] = [0 for _ in range(island_size)]
        self[5+crates] = [0 for _ in range(5)]
        self[5+jobs] = [0 for _ in range(island_size)]
        self[5+vp] = 0

        self[wharf_used] = False
        self[farm_open] = [0 for _ in range(6)]
        self[farm_deck] = [None for _ in range(5)]

        self[settler_ship] = 2

        self[ship4_fill] = 0
        self[ship4_kind] = None
        self[ship6_fill] = 0
        self[ship5_kind] = None

        self[trade_crates] = [0 for _ in range(5)]

        self[roles] = [True for _ in range(7)]
        self[which_role_has_bonus] = None
        self[role_bonus] = 0

        self[state] = states.settup
        self[active] = 0
        self[role_user] = 5  # gets settup working correctly

        self[0+island][building.idle] = 40
        self[0+island][building.idle]

        # settup
        self[0+cash] = 3
        self[0+island][tile.indigo] = 1

        self[5+cash] = 2
        self[5+island][tile.corn] = 2

        self[farm_open][tile.quarry] = 5
        self[farm_deck][tile.corn] = 6
        self[farm_deck][tile.indigo] = 8
        self[farm_deck][tile.sugar] = 8
        self[farm_deck][tile.tobacco] = 6
        self[farm_deck][tile.coffee] = 5

    def swap_players(self):
        self[active] = 0 if self[active] else 5

    def has(self, number):
        return min(self[self[active]+island][number], self[self[active]+jobs][number])

    #  ------------------ state machine ------------------
    def step(self, choice):

        if self[state] == states.settup:
            if self.flip_tile(choice):
                self.proceed()

        elif self[state] == states.role_choice:
            self.pick_role(choice)  # this sets state internally

        elif self[state] == states.tile_flip:
            if self.flip_tile(choice):  # flipped all three tiles
                self.possibly_check_hacienda()

        elif self[state] == states.hacienda_choice:
            assert type(choice) is bool
            self[state] = states.hacienda_flip if choice else states.planter_main

        elif self[state] == states.hacienda_flip:
            self.take_from_farm_deck(choice)
            self[self[active]+island][choice] += 1
            self[state] = states.planter_main

        elif self[state] == states.planter_main:
            self.give_tile(choice)

            if self[active] == self[role_user]:
                self.swap_players()
                self.possibly_check_hacienda()
            else:
                self[state] = states.settup

        elif self[state] == states.mayor_bonus:
            assert type(choice) is bool
            self[self[active]+jobs][building.idle] += int(choice)
            self.give_settlers()

        elif self[state] == states.assign_work:
            self.assign_work(choice)
            if self[active] == self[role_user]:
                self.swap_players()
                self.give_settlers()
            else:
                self.refill_settlers()
                self.proceed()

        elif self[state] in (states.p1_victory, states.p2_victory, states.draw):
            raise Exception('game is over')

    def proceed(self):
        if self[active] == self[role_user]:
            self.swap_players()

        else:
            if self[game_end]:
                scores = self.score()
                if scores[0] > scores[1]:
                    self[state] = states.p2_victory
                elif scores[0] < scores[1]:
                    self[state] = states.p1_victory
                else:
                    self[state] = states.draw

            self[state] = states.role_choice
            if sum(self[roles]) == 1:
                self[which_role_has_bonus] = self[roles].index(1)
                self[role_bonus] += 1
                self[roles] = [True for _ in range(7)]

    def pick_role(self, choice):

        assert self[roles][choice]

        # take card and money
        self[roles][choice] = False
        if self[which_role_has_bonus] == choice:
            self[self[active]+cash] += self[role_bonus]
            self[role_bonus] = 0

        self[role_user] = self[active]  # you have the role privilige

        if choice == role.planter:
            self.possibly_check_hacienda()

        elif choice == role.mayor:
            self[state] = states.mayor_bonus

    def score(self):

        # actually calculate points
        scores = [0, 0]

        for player in (0, 5):

            scores[bool(player)] += self[player+vp]

            for b in range(building.small_indigo_plant, building.idle):
                if self[player+island][b]:
                    scores[bool(player)] += tier[b]

            self[active] = player
            if self.has(building.guild_hall):
                for small_production in (building.small_indigo_plant, building.small_sugar_mill):
                    if self[self[active] + island][small_production]:
                        scores[bool(player)] += 1
                for big_production in (building.sugar_mill, building.indigo_plant,
                                       building.coffee_roaster, building.tobacco_storage):
                    if self[self[active]+island][big_production]:
                        scores[bool(player)] += 2

            if self.has(building.residence):
                plantations = sum(self[self[active]+island][:6])
                scores[bool(player)] += max(4, plantations-5)

            if self.has(building.fortress):
                scores[bool(player)] += sum(self[self[active]+jobs])//3

            if self.has(building.customs_house):
                scores[bool(player)] += self[self[active]+vp] // 4

            if self.has(building.city_hall):
                for pink_building in range(building.small_market, building.idle):
                    scores[bool(player)] += 1

        return scores

    # ------------------ planter phase ------------------
    def possibly_check_hacienda(self):
        self[state] = states.hacienda_choice if self.has(building.hacienda) else states.planter_main

    def take_from_farm_deck(self, choice):
        assert self[farm_deck][choice]
        self[farm_deck][choice] -= 1
        if sum(self[farm_deck]) == 0:
            self[farm_deck] = [t-p1-p2 for (t, p1, p2) in zip(Settings.TILES, self[island], self[5+island])]

    def give_tile(self, choice):
        assert self[farm_open][choice]
        assert choice!=tile.quarry or self[active]==self[role_user] or self.has(building.construction_hut)

        self[farm_open][choice] -= 1
        self[self[active]+island][choice] += 1

        if self.has(building.hospice):
            self[self[active]+jobs][choice] = 1

    def flip_tile(self, choice):
        assert self[farm_deck][choice]

        self.take_from_farm_deck(choice)
        self[farm_open][choice] += 1
        return sum(self[farm_open])-self[farm_open][-1] == 3

    # --------------- mayor phase ------------------
    def give_settlers(self):
        amount = self[settler_ship] // 2
        amount += self[settler_ship]%2 if self[active]==self[role_user] else 0

        self[self[active]+jobs][building.idle] += amount
        self[state] = states.assign_work

    def assign_work(self, choice):
        assert sum(choice)==sum(self[self[active]+jobs])
        for i in range(island_size):
            assert self[self[active] + island][i] >= choice[i]

        self[self[active]+jobs] = choice[::]

    def refill_settlers(self):
        total = 0
        for player in (0, 5):
            for i in range(island_size):
                total += self[player+island][i] - self[player+jobs][i]

        amount = max(2, total)
        if amount + sum(self[0+jobs]) + sum(self[5+jobs]) > Settings.SETTLER_LIMIT:
            amount = sum(self[0+jobs]) + sum(self[5+jobs])
            self[game_end] = True

        self[settler_ship] = amount

    # --------------- builder phase ------------------
    def build(self, choice):

        cost = max(0, price[choice] - min(self[self[active]+island][tile.quarry], tier[choice]) - self[active]==self[role_user])

        assert self[self[active]+cash] >= cost

        self[self[active]+cash] -= cost
        self[self[active]+island][choice] = job_spots.get(choice, default=1)










