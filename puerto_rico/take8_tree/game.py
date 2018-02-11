from puerto_rico.take8_tree.data import *


class Settings:
    deck_tiles = [7, 9, 8, 6, 5]
    crate_count = [8, 9, 9, 7, 7]

def smunch(poss):
    if type(poss) is list:
        return tuple(poss)
    if type(poss) is Board:
        return poss.to_seq()
    return poss

class Board:
    __slots__ = ['island', 'jobs', 'settlers', 'crates', 'cash', 'vps']

    def __init__(self):
        self.island = IslandStore()
        self.jobs = IslandStore()

        self.settlers = 0

        self.crates = CrateStore()
        self.cash = 0
        self.vps = 0

    @property
    def disp(self):
        return '\n'.join([
            '${}  {} vp'.format(self.cash*100, self.vps),

            'farms: ' + ', '.join('*'*self.jobs[i]+island_lookup[i] for (i, e) in enumerate(self.island[:6]) if e),

            'city: ' + ', '.join('*'*self.jobs[i]+island_lookup[i] for (i, e) in enumerate(self.island[6:]) if e),

        ])

    def to_seq(self):
        return tuple(smunch(getattr(self,field)) for field in self.__slots__)


class Game:
    __slots__ = ['p1', 'p2', 'roles', 'which_role_has_bonus', 'bonus_amount', 'farm_deck', 'farm_open',
                 'settler_ship', 'trade_crates', 'ship4_fill', 'ship4_kind', 'ship6_fill', 'ship6_kind',
                 'wharf_used', 'crate_reserve', 'active', 'role_user', 'state', 'game_end', 'possible']

    @property
    def disp(self):
        return '\n'.join((
            self.p1.disp,
            '',
            self.p2.disp,
            '',
        ))

    def to_seq(self):
        return tuple(smunch(getattr(self, field)) for field in self.__slots__)

    # ============= MEAT ============

    def __init__(self):
        self.p1 = Board()
        self.p2 = Board()

        self.roles = [1, 1, 1, 1, 1, 1, 1]
        self.which_role_has_bonus = None
        self.bonus_amount = 0

        self.farm_deck = [6, 8, 8, 6, 5]
        self.farm_open = [0, 0, 0, 0, 0, 5]

        self.settler_ship = 2

        self.crate_reserve = CrateStore()
        self.trade_crates = CrateStore()

        self.ship4_fill = 0
        self.ship4_kind = None
        self.ship6_fill = 0
        self.ship6_kind = None
        self.wharf_used = False

        self.active = self.p1
        self.game_end = False
        self.role_user = None
        self.state = None
        self.possible = None

        self.p1.cash = 3
        self.p1.island[tile.indigo] += 1
        self.p2.cash = 2
        self.p2.island[tile.corn] += 1

        self.transition_to_tile_flip()

    def swap_players(self):
        self.active = self.p1 if self.active is self.p2 else self.p2

    def working(self, b):
        return self.active.island[b] and self.active.island[b]

    def step(self, choice):

        assert choice in self.possible

        if self.state == State.role_choice:
            self.role_user = self.active
            self.roles[choice] = 0
            if choice == self.which_role_has_bonus:
                self.active.cash += self.bonus_amount
                self.bonus_amount = 0

            if choice == role.planter:
                self.transition_to_possibly_hacienda()
            elif choice == role.builder:
                self.transition_to_builder()
            elif choice == role.mayor:
                self.transition_to_mayor()
            elif choice == role.producer:
                self.transition_to_producer()
            elif choice == role.trader:
                self.transition_to_trader()
            elif choice == role.shipper:
                self.transition_to_shipper_potentially_cleanup()
            elif choice == role.banker:
                self.active.cash += 1
                self.transition_to_role_choice()

        elif self.state == State.hacienda_choice:
            self.transition_to_hacienda_flip() if choice else self.transition_to_planter()

        elif self.state == State.hacienda_flip:
            self.take_from_deck(choice)
            self.active.island[choice] += 1
            self.transition_to_planter()

        elif self.state == State.planter:

            if choice is not None:
                self.farm_open[choice] -= 1
                self.active.island[choice] += 1

            if self.active==self.role_user:
                self.swap_players()
                self.transition_to_planter()
            else:
                self.farm_open = [0, 0, 0, 0, 0, self.farm_open[-1]]
                self.transition_to_tile_flip()

        elif self.state == State.tile_flip:
            self.take_from_deck(choice)
            self.farm_open[choice] += 1

            if sum(self.farm_open[:-1]) == 3:
                self.transition_to_role_choice()
            else:
                self.transition_to_tile_flip()

        elif self.state == State.build:
            if choice is not None:
                self.active.island[choice] += island.workers[choice]

            if self.active==self.role_user:
                self.swap_players()
                self.transition_to_builder()
            else:
                self.transition_to_role_choice()

        elif self.state == State.mayor_bonus:
            self.active.settlers += choice
            self.active.settlers += self.settler_ship//2 + self.settler_ship%2
            self.swap_players()
            self.active.settlers += self.settler_ship//2
            self.swap_players()

            self.transition_to_assign_work()

        elif self.state == State.assign_work_up:
            self.active.jobs[choice] += 1
            self.transition_to_assign_work_up()

        elif self.state == State.assign_work_down:
            self.active.jobs[choice] -= 1
            self.transition_to_assign_work_down()

        elif self.state == State.craft_bonus:
            for kind, amount in enumerate(self.production()):
                self.active.crates[kind] += min(amount, self.crate_reserve[kind]) + kind==choice

            self.swap_players()
            for kind,amount in enumerate(self.production()):
                self.active.crates[kind] += min(amount,self.crate_reserve[kind])

            self.transition_to_role_choice()

        elif self.state == State.trade:
            if choice is not None:
                self.active.crates[choice] -= 1
                self.trade_crates[choice] += 1
                self.active.cash += (choice +
                                     (self.active==self.role_user) +
                                     self.working(building.small_market) +
                                     3*self.working(building.large_market))

            if self.active==self.role_user:
                self.swap_players()
                self.transition_to_trader()

            else:
                if sum(self.trade_crates)==4:
                    for i in crate.all:
                        self.crate_reserve[i] += self.trade_crates[i]
                        self.trade_crates[i] = 0
                self.transition_to_role_choice()

        elif self.state == State.ship:
            if choice=='finished shipping':
                self.wharf_used = True

            else:
                if choice[1]=='ship4':
                    self.ship4_kind = choice[0]
                    amount = min(4-self.ship4_fill, self.active.crates[choice[0]])
                    self.ship4_fill += amount

                elif choice[1]=='ship6':
                    self.ship6_kind = choice[0]
                    amount = min(6-self.ship6_fill, self.active.crates[choice[0]])
                    self.ship6_fill += amount

                elif choice[1]=='wharf':
                    self.wharf_used = True
                    amount = self.active.crates[choice[0]]

                self.active.crates[choice[0]] -= amount

            self.transition_to_shipper_potentially_cleanup()

        else:
            raise Exception('Invalid State')

    # ================ helper funcs ================
    def take_from_deck(self, choice):
        self.farm_deck[choice] -= 1
        if sum(self.farm_deck) == 0:
            self.farm_deck = [total-p1-p2-o for total, p1, p2, o in
                              zip(Settings.deck_tiles, self.p1.island, self.p2.island, self.farm_open)]

    def production(self):
        return [
            min(self.active.island[tile.corn], self.active.jobs[tile.corn]),

            min(self.active.island[tile.indigo], self.active.jobs[tile.indigo],
                self.working(building.small_indigo_plant) + self.working(building.indigo_plant)),

            min(self.active.island[tile.sugar], self.active.jobs[tile.sugar],
                self.working(building.small_sugar_mill) + self.working(building.sugar_mill)),

            min(self.active.island[tile.tobacco], self.active.jobs[tile.tobacco],
                self.working(building.tobacco_storage)),

            min(self.active.island[tile.coffee], self.active.jobs[tile.coffee],
                self.working(building.coffee_roaster))
            ]

    def shipping_options(self):
        options = list()
        for cargo in crate.all:
            if not self.active.crates[cargo]: continue

            if self.ship4_kind == cargo and self.ship4_fill < 4:
                options.append((cargo,'ship4'))

            if self.ship6_kind == cargo and self.ship6_fill < 6:
                options.append((cargo,'ship6'))

            if self.ship4_kind is None and self.ship6_kind != cargo:
                options.append((cargo,'ship4'))

            if self.ship6_kind is None and self.ship4_kind != cargo:
                options.append((cargo,'ship6'))

            if self.working(building.wharf) and not self.wharf_used:
                options.append((cargo,'wharf'))

        if self.working(building.wharf) and not self.wharf_used:
            options.append('no wharf usage')

        return tuple(options)

    # ============== transition funcs ==============
    def transition_to_role_choice(self):
        if sum(self.roles) == 1:
            self.which_role_has_bonus = self.roles.index(1)
            self.bonus_amount += 1
            self.roles = [1 for _ in range(7)]

            if self.game_end:
                # TODO: SCORING
                self.state = State.draw
                return

        self.possible = tuple(i for i in role.all if self.roles[i])
        self.state = State.role_choice


    def transition_to_possibly_hacienda(self):
        if self.working(building.hacienda) and sum(self.active.island[:island.small_indigo_plant])<12:
            self.possible = (True, False)
            self.state = State.hacienda_choice
        else:
            self.transition_to_planter()

    def transition_to_planter(self):
        # return 'None' for no plantation
        # return a number to pick that tile enum (eg 2->indigo)

        self.possible = frozenset(
            (None,
               *((i for i in tile.all if
                  (self.farm_open[i] and (i != tile.quarry or (
                      self.active is self.role_user or self.working(building.construction_hut)))))
                 if sum(self.active.island[:island.small_indigo_plant])<12 else tuple())))

        self.state = State.planter

    def transition_to_hacienda_flip(self):
        self.possible = frozenset(i for i in tile.farms if (self.farm_deck[i]))
        self.state = State.hacienda_flip

    def transition_to_tile_flip(self):
        self.possible = frozenset(i for i in tile.farms if (self.farm_deck[i]))
        self.state = State.tile_flip

    def transition_to_builder(self):
        # same as planter

        if sum(bool(b) for b in self.active.island[building.small_indigo_plant:])==12:
            self.possible = (None, )

        else:
            room_for_big = sum(bool(b) for b in self.active.island[island.small_indigo_plant:])<11 and sum(self.active.island[island.guild_hall:])<4
            money = self.active.cash + (self.active is self.role_user)

            self.possible = frozenset((None, *(
                b for b in building.all if
                    money >= building.costs[b]-min(self.active.island[tile.quarry], building.tiers[b])
                    and (b<building.guild_hall or room_for_big)
                    and ((not self.active.island[b] and (b<=building.coffee_roaster))               # and is either a production building
                         or not (self.p1.island[b] or self.p2.island[b]))     #               or not built already
            )))

        self.state = State.build

    def transition_to_mayor(self):
        self.possible = (True, False)
        self.state = State.mayor_bonus

    def transition_to_assign_work(self):
        jobs = sum(self.active.island)
        if self.active.settlers > jobs // 2:
            self.active.jobs = self.active.island[::]
            self.transition_to_assign_work_down()
        else:
            self.active.jobs = IslandStore()
            self.transition_to_assign_work_up()

    def transition_to_assign_work_down(self):

        self.possible = tuple(
            i for i in island.all if
            self.active.jobs[i]
        )

        self.state = State.assign_work_down

        if not self.possible or (sum(self.active.island) <= self.active.settlers):
            if self.active == self.role_user:
                self.swap_players()
                self.transition_to_assign_work()
            else:
                self.transition_to_role_choice()

    def transition_to_assign_work_up(self):

        self.possible = tuple(
            i for i in island.all if
            self.active.jobs[i] < self.active.island[i]
        )

        self.state = State.assign_work_up

        if not self.possible or (sum(self.active.jobs) >= self.active.settlers):
            if self.active == self.role_user:
                self.swap_players()
                self.transition_to_assign_work()
            else:
                self.transition_to_role_choice()

    def transition_to_producer(self):
        self.possible = (None, *(i for i in crate.all if self.production()[i]))
        self.state = State.craft_bonus

    def transition_to_trader(self):
        self.possible = frozenset(
            (None, *((i for i in crate.all if
                      (self.active.crates[i] and (self.working(building.office) or not self.trade_crates[i])))
                     if sum(self.trade_crates)<4 else tuple())))

        self.state = State.trade

    def transition_to_shipper_potentially_cleanup(self):

        options = self.shipping_options()
        if options:
            self.possible = options
            self.state = State.ship
        else:
            self.swap_players()
            options = self.shipping_options()
            if options:
                self.possible = options
                self.state = State.ship
            else:
                self.wharf_used = False

                if self.ship4_fill == 4:
                    self.crate_reserve[self.ship4_kind] += 4
                    self.ship4_fill = 0
                    self.ship4_kind = None
                if self.ship4_fill == 6:
                    self.crate_reserve[self.ship4_kind] += 6
                    self.ship6_fill = 0
                    self.ship6_kind = None

                self.transition_to_role_choice()







