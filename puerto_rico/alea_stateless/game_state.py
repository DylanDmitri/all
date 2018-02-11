
goods = ('corn','indigo','sugar','tobacco','coffee')

# class choices:
#     random_tiles = 'random_tiles'
#     role = 'role'
#     hacienda = 'hacienda'
#     random_from_stack = 'random_from_stack'
#     plantation = 'plantation'
#     bonus_settler = 'bonus_settler'
#     jobs = 'jobs'
#     building = 'building'
#     bonus_production = 'bonus_production'
#     trade_good = 'trade_good'
#     shipment = 'shipment'
#     storage = 'storage'

class state:
    role = 'role'
    hacienda = 'hacienda'
    hacienda_flip = 'hacienda_flip'
    plantation = 'plantation'
    settler_flip = 'settler_flip'
    building = 'building'

class roles:
    settler = 'settler'
    mayor = 'mayor'
    builder = 'builder'
    craftsman = 'craftsman'
    trader = 'trader'
    captain = 'captain'
    prospector = 'prospector'

    all = ('settler','mayor','builder','craftsman','trader','captain','prospector')

class message:
    pass

class Store:
    def __init__(self, corn=0, indigo=0, sugar=0, tobacco=0, coffee=0):
        self.corn = corn
        self.indigo = indigo
        self.sugar = sugar
        self.tobacco = tobacco
        self.coffee = coffee
        self.quarry = 0

    def add(self, field, i=1):
        setattr(self, field, getattr(self, field)+i)

    def increment(self, field):
        self.add(field, i=1)

    def decrement(self, field):
        self.add(field, i=-1)

    def sum(self):
        return self.corn + self.indigo + self.sugar + self.tobacco + self.coffee

    def dictionary(self):
        return {good:getattr(self, good) for good in goods}

class Board:
    def __init__(self, start, settings):

        self.island = Store()
        self.farmers = Store()
        self.goods = Store()
        self.city = {}
        self.colonists = 0
        self.dubloons = start['dubloons']
        self.vp = 0

        self.island.increment(start['tile'])

    def has(self, building):
        return self.city.get(building, False)

class GameState:

    def __init__(self, settings, logging=False, playernames=('p1', 'p2', 'p3', 'p4', 'p5')):
        self.rules = settings.rules
        self.round = 1

        self.roles = list(settings.roles)
        self.role_money = {role:0 for role in settings.roles}

        self.farm_source = Store(**settings.farms)
        self.farm_stacks = Store()
        self.farm_heap = Store()
        self.quarries = settings.quarries

        self.buildings = {b.name:b for b in settings.buildings}

        self.colonist_supply = settings.colonist_supply
        self.colonist_ship = settings.colonist_ship_min

        self.crates = Store(**settings.crates)

        self.trading_house = []

        self.cargoships = tuple([0, size, None] for size in settings.cargoships)
        self.vps = 0

        self.players = tuple(Board(start, settings) for start in settings.player_starts)
        self._active = 0
        self._role_user = 0

        self.state = state.settler_flip
        self.options = tuple(self.farm_heap.dictionary().keys())
        self.replay = []

        self._log = []
        self.logging = logging
        self.playernames = playernames

        self.log_start()
        self._cont()

    # =================== logging =====================
    def log(self, *args):
        if self.logging:
            message = ' '.join(map(str, args))
            self._log.append(message)
            print(message)

    def log_start(self):
        self.log('game initialized')

    def log_choice_and_options(self):
        if self.state not in (state.hacienda_flip,state.settler_flip):
            self.log(self.playernames[self._active], 'must now choose', self.state)
        else:
            self.log('a tile needs to be drawn randomly')

        if len(self.options)==1:
            self.log('only option is', self.options[0])
            self.step(self.options[0])
        else:
            self.log('choices are:', self.options)

    def log_round_end(self):
        for card in self.roles:
            self.log('added a bonus dubloon to', card, 'card')
        self.log('===== ROUND', self.round, '=====')

    def log_phase(self, choice):
        self.log('\n~~', choice, 'phase ~~')

    def log_tile_flip(self, tile):
        self.log('flipped over a', tile, 'tile')

    def log_hacienda_use(self, choice):
        if choice is True:
            self.log(self.playernames[self._active], 'uses their hacienda to draw a random tile')

    def log_role_money(self, amount):
        if amount > 0:
            self.log(self.playernames[self._active], 'receives', amount, 'dubloons from role card')

    def log_farm_discard(self):
        self.log('remaining', self.farm_stacks.sum(), 'farm tiles discarded. Drawing',self.rules.farm_stacks,'new ones...')

    def log_ready_plantation(self):
        if self.roleBonus:
            self.log('settler enables', self.playernames[self._active], 'to build quarries')
        if self.activePlayer.island.sum() == 12:
            self.log(self.playernames[self._active], 'has a full island, may not build more')

    def log_building(self, name):
        self.log('built', name, 'for', self.buildings[name].pricewith(self.activePlayer)-self.roleBonus, 'dubloons')

    # ============= playerstate controls ==============
    def incrementPlayer(self):
        self._active += 1
        self._active %= len(self.players)

    @property
    def phaseOver(self):
        return self._active == self._role_user

    @property
    def activePlayer(self):
        return self.players[self._active]

    @property
    def roleBonus(self):
        return self._active == self._role_user

    # ============= helper functions ==============
    def tile_transfer(self, source, dest):

        for good in goods:
            amount = getattr(source, good)
            source.add(good, -amount)
            dest.add(good, amount)

    # ================ game logic =================
    def step(self, result):
        assert result in self.options
        self.replay.append(result)

        getattr(self, 'update_'+self.state)(result)
        self.log()
        getattr(self, 'ready_' +self.state)()

        self._cont()

    def _cont(self):
        assert self.options

        self.log_choice_and_options()

        if len(self.options)==1:
            self.step(self.options[0])


    # name          start           each            end
    # role          reset_role      choose_role
    # settler                       choose_tiles    reset_plantations
    # mayor         dist_settler    choose_work     reset_colonists
    # builder                       choose_building
    # craftsman                     produce_goods
    # trader                        choose_trade    clear_house
    # captain                       choose_ship     clear_ship
    # prospector    mine_gold

    def ready_role(self):

        self.incrementPlayer()

        if len(self.roles) == self.rules.role_cards_unused:

            self.log_round_end()

            for role in self.role_money:

                if role in self.roles:
                    self.role_money[role] += 1
                else:
                    self.roles.append(role)

            self.round += 1

        self.options = tuple(sorted(self.roles))

    # ------------------------------- settler code -------------------------------
    def update_role(self, choice):

        self.log_phase(choice)

        self._role_user = self._active
        self.roles.remove(choice)

        money = self.role_money[choice]
        self.role_money[choice] = 0
        if choice == roles.prospector and self.roleBonus:
            money += 1
        self.log_role_money(money)
        self.activePlayer.dubloons += money

        self.state = {
            roles.settler:state.hacienda,
            roles.prospector:state.role,
            roles.builder:state.building,
        }[choice]

    def ready_hacienda(self):
        if self.activePlayer.has('hacienda') and self.activePlayer.island.sum() == 12:
            if self.activePlayer.has('construction_hut') and self.quarries:
                self.options = ('no tile', 'random tile', 'quarry')
            else:
                self.options = ('no tile', 'random tile')
        else:
            self.state = state.plantation
            self.ready_plantation()

    def update_hacienda(self, choice):
        self.log_hacienda_use(choice)
        if choice == 'no tile':
            self.state = state.plantation
        elif choice == 'random tile':
            self.state = state.hacienda_flip
        elif choice == 'quarry':
            self.quarries -= 1
            self.activePlayer.island.quarry += 1
            self.state = state.plantation

    def ready_hacienda_flip(self):
        if self.farm_source.sum() == 0:
            self.tile_transfer(self.farm_heap, self.farm_source)

        self.options = self.farm_source.dictionary().keys()

    def update_hacienda_flip(self, chosen):
        self.farm_source.decrement(chosen)
        self.activePlayer.island.increment(chosen)
        self.state = state.plantation

    def ready_plantation(self):
        self.log_ready_plantation()

        possible = ['no plantation',]

        if self.activePlayer.island.sum() < 12:
            for key,val in self.farm_stacks.dictionary().items():
                if val:
                    possible.append(key)
            if self.activePlayer.has('construction_hut') or self.roleBonus:
                possible.append('quarry')

        self.options = tuple(possible)

    def update_plantation(self, chosen):
        if chosen == 'no plantation':
            pass
        elif chosen == 'quarry':
            self.quarries -= 1
        else:
            self.farm_stacks.decrement(chosen)

        self.activePlayer.island.increment(chosen)

        if self.activePlayer.has('hospice'):
            self.activePlayer.farmers.increment(chosen)

        self.incrementPlayer()
        if self.phaseOver:
            self.log_farm_discard()
            self.tile_transfer(self.farm_stacks, self.farm_heap)
            self.state = state.settler_flip

    def ready_settler_flip(self):
        if self.farm_source.sum() == 0:
            self.tile_transfer(self.farm_heap, self.farm_source)
        self.options = tuple(self.farm_source.dictionary().keys())

    def update_settler_flip(self, tile):
        self.log_tile_flip(tile)
        self.farm_source.decrement(tile)
        self.farm_stacks.increment(tile)

        if self.farm_stacks.sum() == self.rules.farm_stacks:
            self.state = state.role

    # ------------------------------------- builder code -------------------------------------

    def ready_building(self):
        purchasing_power = self.activePlayer.dubloons + self.roleBonus

        ret = ['no building', ]
        for b in sorted(self.buildings.values(), key = lambda o:o.cost):
            if b.supply > 0 and b.pricewith(self.activePlayer) <= purchasing_power:
                ret.append(b.name)

        self.options = tuple(ret)

    def update_building(self, name):

        if name == 'no building':
            self.log('did not build anything')

        else:
            self.log_building(name)

            b = self.buildings[name]
            price = b.pricewith(self.activePlayer) - self.roleBonus
            self.activePlayer.dubloons -= price

            b.supply -= 1
            
            starting_workers = (1 if self.activePlayer.has('university') else 0)
            self.activePlayer.city[name] = starting_workers

        self.incrementPlayer()
        if self.phaseOver:
            self.state = state.role

    # ------------------------------------- mayor code -------------------------------------








#
#
# class etc:
#     def next(self, result):
#
#         # perform action, update state
#         # choose a role
#         if self.nextChoice is choices.role:
#             money = self.role_money[result]
#             if result == roles.prospector:
#                 money += 1
#             self.activePlayer.dubloons += money
#
#             self.roles.remove(result)
#             self.activePlayer.roles.append(result)
#
#             self.nextChoice = {
#                 roles.settler:choices.plantation,
#                 roles.mayor:choices.bonus_settler,
#                 roles.builder:choices.building,
#                 roles.craftsman:choices.bonus_production,
#                 roles.trader:choices.trade_good,
#                 roles.captain:choices.shipment,
#                 roles.prospector:choices.role
#             }[result]
#
#             self._role_user = self._active
#
#         # decide to use an active hacienda
#         elif self.nextChoice is choices.hacienda:
#             self.nextChoice = (choices.random_from_stack, choices.plantation)[result is True]
#
#         # take chosen hacienda tile
#         elif self.nextChoice is choices.random_from_stack:
#             self.farm_source.decrement(result)
#             self.activePlayer.island.increment(result)
#             self.nextChoice = choices.plantation
#
#         # take chosen tile from open tiles
#         elif self.nextChoice is choices.plantation:
#             self.activePlayer.island.increment(result)
#             self.farm_stacks.decrement(result)
#
#             self.incrementPlayer()
#             if self.roundOver:
#                 self.nextChoice = choices.random_tiles
#
#         # take chosen tile from source to stack
#         elif self.nextChoice is choices.random_tiles:
#             self.farm_stacks.increment(result)
#             self.farm_source.decrement(result)
#             if self.farm_stacks.sum() == self.rules.farm_stacks:
#                 self.nextChoice = choices.role
#
#         # build chosen building
#         elif self.nextChoice is choices.building:
#             self.buildings[result] -= 1
#             self.activePlayer.city[result] = int(self.activePlayer.has('university'))
#             self.incrementPlayer()
#
#             if self.roundOver:
#                 self.nextChoice = choices.role
#
#         # possibly give mayor extra settler
#         elif self.nextChoice is choices.bonus_settler:
#             if result is True:
#                 self.activePlayer.colonists += 1
#             self.nextChoice = choices.jobs
#
#         # assign chosen jobs
#         elif self.nextChoice is choices.jobs:
#             # assign settlers among farms and city
#
#             self.incrementPlayer()
#             if self.roundOver:
#                 self.nextChoice = choices.role
#
#         # give barrels
#         elif self.nextChoice is choices.bonus_production:
#             self.activePlayer.goods.increment(result)
#
#             while not self.roundOver:
#                 self.activePlayer.goods.add('corn', self.activePlayer.farmers.corn)
#
#                 self.activePlayer.goods.add('indigo', min(
#                     self.activePlayer.has('small_indigo_plant') + self.activePlayer.has('indigo_plant'),
#                     self.activePlayer.farmers.indigo
#                 ))
#                 self.activePlayer.goods.add('sugar', min(
#                     self.activePlayer.has('small_sugar_mill') + self.activePlayer.has('sugar_mill'),
#                     self.activePlayer.farmers.sugar
#                 ))
#                 self.activePlayer.goods.add('tobacco', min(
#                     self.activePlayer.has('tobacco_storage'),
#                     self.activePlayer.farmers.tobacco
#                 ))
#                 self.activePlayer.goods.add('coffee', min(
#                     self.activePlayer.has('coffee_roaster'),
#                     self.activePlayer.farmers.coffee
#                 ))
#
#                 self.incrementPlayer()
#
#         # trade chosen good
#         elif self.nextChoice is choices.trade_good:
#             pass
#
#         # make chosen shipment
#         elif self.nextChoice is choices.shipment:
#             pass
#
#         # store chosen goods
#         elif self.nextChoice is choices.storage:
#             pass
#
#
#         # -------------------------------------------------------------
#         # prepare possibilities for new state
#         if self.nextChoice is choices.role:
#             for role in self.role_money:
#                 if role in self.roles:
#                     self.role_money[role] += 1
#                 else:
#                     self.roles.append(role)
#             self.roles.sort()
#
#             self.possible = tuple(self.roles)
#
#         # decide to use an active hacienda
#         elif self.nextChoice is choices.hacienda:
#             self.possible = (True, False)
#
#         # take chosen hacienda tile
#         elif self.nextChoice is choices.random_from_stack:
#             self.possible = tuple(key for key, val in self.farm_source.items() if val)
#
#         # take chosen tile from open tiles
#         elif self.nextChoice is choices.plantation:
#
#
#
#             self.possible = ['no plantation',]
#
#             if sum(self.activePlayer.island.values()) < 12:
#                 for key,val in self.farm_stacks.items():
#                     if val:
#                         self.possible.append(key)
#                 if self.activePlayer.has('construction_hut') or self.roleBonus:
#                     self.possible.append('quarry')
#
#             self.possible = tuple(self.possible)
#
#         # take chosen tile from source to stack
#         elif self.nextChoice is choices.random_tiles:
#             pass
#
#         # build chosen building
#         elif self.nextChoice is choices.building:
#             pass
#
#         # possibly give mayor extra settler
#         elif self.nextChoice is choices.bonus_settler:
#             pass
#
#         # assign chosen jobs
#         elif self.nextChoice is choices.jobs:
#             pass
#
#         # give barrels
#         elif self.nextChoice is choices.bonus_production:
#             pass
#
#         # trade chosen good
#         elif self.nextChoice is choices.trade_good:
#             pass
#
#         # make chosen shipment
#         elif self.nextChoice is choices.shipment:
#             pass
#
#         # store chosen goods
#         elif self.nextChoice is choices.storage:
#             pass
#
#         return self
#
#
#
#     def prep_plantation(self):
#         self.possible = ['no plantation', ]
#
#         if sum(self.activePlayer.island.values()) < 12:
#             for key, val in self.farm_stacks.items():
#                 if val:
#                     self.possible.append(key)
#             if self.activePlayer.has('construction_hut') or self.roleBonus:
#                 self.possible.append('quarry')
#
#         self.possible = tuple(self.possible)
#
#     def choose_plantation(self, tile):
#
#         self.activePlayer.something
#
#         self.incrementPlayer()
#         if not self.roleInProgress:
#             self.nextChoice = choices.role
#
#
#     def choose_random_tiles(self, tiles):
#         print('chose random tiles', tiles)
#         self.incrementPlayer()
#
#     def choose_bonus_settler(self, took):
#         if took:
#             print('chose a settler')
#         else:
#             print('did not get the extra settler')
#
#         while self.roleInProgress:
#             # give active player settlers
#             self.incrementPlayer()
#         self.nextChoice = choices.jobs
#
#     def choose_jobs(self, jobs):
#         print('assigned jobs:', jobs)
#         self.incrementPlayer()
#
#     def choose_building(self, building):
#         print('built:', building)
#         self.incrementPlayer()
#
#     def choose_bonus_production(self, kind):
#         print('chose to produce additional', kind)
#         while self.roleInProgress:
#             # give active player goods
#             self.incrementPlayer()
#         self.nextChoice = choices.role
#
#     def choose_trade_good(self, kind):
#         print('chose to trade', kind)
#
#         if self.rules.trading_house_size == len(self.trading_house):
#             self._active = self._role_user
#
#         self.incrementPlayer()
#
#     def choose_shipment(self, shipment):
#         print('chose to ship', shipment)
#         self.incrementPlayer()
#
#     def choose_storage(self, storage):
#         print('chose to store', storage)
#         self.incrementPlayer()
#
