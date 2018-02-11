import puerto_rico.constants as constants
from random import shuffle

game_end_flag = False


class Brain:
    def __init__(self):
        pass

    def choose_role(self):
        return NotImplemented

    def choose_plantation(self, choices):
        return NotImplemented

    def choose_employment(self):
        return NotImplemented

    def choose_building(self):
        return NotImplemented



class HumanPlayer(Brain):
    def choose_role(self):
        pass



class Player_Game_Entity:
    def __init__(self, game, brain):
        self.game = game
        self.brain = brain

        self.total_colonists = 0
        self.dubloons = constants.starting_dubloons
        self.city = []
        self.island = []

    def choose_role(self):
        self.role = self.brain.choose_role()

        # get inactivity dubloons
        self.dubloons += self.game.roles[self.role]
        self.game.roles[self.role] = 0

    def execute(self, role):
        getattr(self, role+'_phase')(self)

    def active(self, building):
        return (building, 1) in self.city

    def settler_phase(self):

        # try to hacienda
        if len(self.island) < constants.plantation_spaces:
            if self.active('hacienda') and self.game.plantation_stack:
                self.island.append((self.game.plantation_stack.pop(), 0))

        # if you have free spaces
        if len(self.island) < constants.plantation_spaces:

            choices = self.game.active_plantations
            if (self.role == 'settler' or self.active('hut')) and self.game.quarries_remaining:
                choices.append('quarry')

            choice = self.brain.choose_plantation(choices)
            assert choice in choices

            # add to island, remove from game
            self.island.append((choice, int(self.active('hospice'))))
            if choice == 'quarry':
                self.game.quarries_remaining -= 1
            else:
                self.game.active_plantations.remove(choice)

    def mayor_phase(self):
        pass

    def 





class Game:
    def __init__(self, *players, variant=None):

        num_players = len(players)
        if num_players not in range(2, 6):
            raise Exception('Invalid number of players {}, must be int 2-6'.format(num_players))

        constants.colonist_ship_minimum = num_players
        constants.plantation_stacks = num_players + 1
        constants.roles_per_turn = 1

        self.players = []
        for i , brain in zip(range(num_players), players):
            self.players.append(Player_Game_Entity(self, brain()))

            # give initial plantations
            if variant is None:
                if i > num_players//2:
                    self.players[i].island.append(('indigo', 0))
                else:
                    self.players[i].island.append(('corn', 0))

        if num_players == 2 and variant is None:
            # remove 1 of each building
            for name in constants.buildings:
                if constants.buildings[name]['tier'] == 4: continue
                constants.buildings[name]['count'] -= 1

            # remove 3 of each plantation
            for resource in constants.resources.values():
                resource.plantations -= 3
                resource.barrels -= 2
            constants.total_quarries = 5

            constants.victory_points = 65
            constants.colonist_reserve = 40
            constants.starting_dubloons = 3
            constants.ships = 4, 6
            constants.prospectors = 1
            constants.roles_per_turn = 3

        elif num_players == 3 and variant is None:
            constants.victory_points = 75
            constants.colonist_reserve = 58
            constants.starting_dubloons = 2
            constants.ships = 4,5,6
            constants.prospectors = 0

        elif num_players == 4 and variant is None:
            constants.victory_points = 100
            constants.colonist_reserve = 79
            constants.starting_dubloons = 3
            constants.ships = 5,6,7
            constants.prospectors = 1

        elif num_players == 5 and variant is None:
            constants.victory_points = 122
            constants.colonist_reserve = 100
            constants.starting_dubloons = 4
            constants.ships = 6,7,8
            constants.prospectors = 2

        self.plantation_stack = []
        self.plantation_discard = []
        for name in constants.resources:
            for _ in range(constants.resources[name].plantations):
                self.plantation_stack.append(name)
        shuffle(self.plantation_stack)
        self.active_plantations = []
        self.settler_cleanup()  # places plantation tiles out

        self.colonist_ship_current = constants.colonist_ship_minimum
        self.quarries_remaining = constants.total_quarries

        self.roles = {r:0 for r in ('settler', 'mayor', 'builder', 'craftsman', 'trader', 'captain')}
        if constants.prospectors == 1: self.roles['prospector1'] = 0
        if constants.prospectors == 2: self.roles['prospector2'] = 0

    def play(self):

        # roles happen
        roles_remaining = list(self.roles.keys())
        for i, player in enumerate(self.players):
            # each player picks a roll
            role = player.choose_role(roles_remaining)

            # prospector you just get money
            if role == 'prospector':
                player.dubloons += 1
                continue

            # run the phase
            getattr(self, role + '_init')(self)
            for j in range(len(self.players)):
                spot = (i + j) % len(self.players)
                self.players[spot].execute(role)    # each player acts during the phase
            getattr(self,role + '_cleanup')(self)
            roles_remaining.remove(role)   # phase is over

        # rotate governor
        self.players = self.players[1:] + self.players[0:1]

        for role in roles_remaining:
            self.roles[role] += 1

        if game_end_flag is True:
            self.finish()
        else:
            self.play()


    def settler_init(self):
        pass

    def settler_cleanup(self):

        # discard the unpicked plantations
        self.plantation_discard.extend(self.active_plantations)
        self.active_plantations = []

        for i in range(constants.plantation_stacks):
            # refresh the stack from discard if needed
            if len(self.plantation_stack) == 0:
                self.plantation_stack = self.plantation_discard
                shuffle(self.plantation_stack)
            # place new plantations
            if len(self.plantation_stack) > 0:
                self.active_plantations.append(self.plantation_stack.pop())

    def mayor_init(self):
        for i in range(len(self.players)):
            if self.players[i].role == 'mayor': break

        # mayor privelege
        self.players[i].total_colonists += 1

        # pass out colonists
        for j in range(self.colonist_ship_current):
            spot = (i+j) % len(self.players)
            self.players[spot].total_colonists += 1

    def mayor_cleanup(self):
        total = 0
        for player in self.players:
            total += sum(constants.buildings[t[0]].max_workers - t[1] for t in player.city)
        for_ship = max(total, constants.colonist_ship_minimum)

        if for_ship > constants.colonist_reserve:
            globals()['game_end_flag'] = True
        else:
            self.colonist_ship_current = for_ship
            constants.colonist_reserve -= for_ship

    def builder_init(self): pass
    def builder_cleanup(self): pass



    def finish(self):
        pass



Game(HumanPlayer, HumanPlayer).play()