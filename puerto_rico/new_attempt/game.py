from puerto_rico.new_attempt.utils import *

# zone : area that has stuff
#        resources transferred between zones


# run game (players)
# each player is given choices
#   choice = player.choose_building()
# the player then decides


'''
settler
mayor
builder
craftsman
trader
captain
prospector
'''


def GlobalMessage(string):
    print(string)

class Game:
    def __init__(self, *players, settings=None, buildings=None):
        assert len(players) in (2,3,4,5,6)
        self.players = [Board(game=self, player=p) for p in players]

        self.supply = settings
        self.roles_per_round = settings.roles_per_round
        self.role_availibility = {role:True for role in self.supply.roles}

        self.tile_stack = []
        for good in ('corn indigo sugar tobacco coffee'.split()):
            name = 'tile_' + good
            self.tile_stack.append([name] * getattr(self,name))
        self.tiles_shown = []
        self.tile_discard = []

        for plantation,player in zip(self.supply.start_plantations,self.players):
            player.add_plantation(dict(i=Tile.indigo,c=Tile.corn)[plantation])

            player.dubloons += self.supply.start_money
            if plantation == 'c' and settings.corn_player_dubloon_penalty:
                player.dubloons -= 1


    def loopPlayers(self, start, steps=None):
        if steps is None: steps = len(self.players)

        for offset in range(steps):
            yield (start+offset)%len(self.players)


    def run(self):

        governor = 0

        while True:
            # each round
            self.active_roles = self.supply.roles

            for id in self.loopPlayers(governor, self.roles_per_round):
                role = self.players[id].choose_role()

                getattr(self, role+'_turn')(self, id)


    def settler_turn(self, start_player_id):

        for id in self.loopPlayers(start_player_id):
            self.players[id].choose_plantation()












def buildings_trigger(func):
    name = func.func_name


class Board:
    def __int__(self, game, player):
        self.game = game
        self.player = player
        self.role = None

        self.dubloons = 0
        self.plantations = [0,0,0,0,0,0]
        self.buildings = []

        self.corn = 0
        self.indigo = 0
        self.sugar = 0
        self.tobacco = 0
        self.coffee = 0

        self.colonists = 0
        self.vps = 0


    def choose_role(self):
        possible = [role for role, v in self.game.role_availibility.items if v]

        choice = self.player.choose_role(possible)
        assert choice in possible

        self.game.role_availibility[choice] = False
        self.role = choice


    def active(self, building_name):
        return True

    def choose_plantation(self):
        possible = self.game.tiles_shown

        if self.active('construction hut') or self.role == ''


    def add_plantation(self,tile):
        if sum(self.plantations) == 12:
            raise Exception("no room for a plantation, user should not have been able to get one")

        self.plantations[tile] += 1










