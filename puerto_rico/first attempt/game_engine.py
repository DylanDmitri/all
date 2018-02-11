from random import shuffle

import puerto_rico.board_state as constants
from puerto_rico.player_shell import PlayerShell
from puerto_rico.utils import *


class Game:
    def __init__(self, *players):
        numPlayers = len(players)
        assert numPlayers in (3,4,5)
        debug('starting',numPlayers,'player game',c=2)
        self._players = tuple(PlayerShell(self, 'p{}'.format(i+1), brain) for i, brain in enumerate(players))
        self.settup(numPlayers)

        self.governorPos = 0
        while not self.board.game_ending:
            self.play_round()
            self.governorPos = (self.governorPos+1) % numPlayers

        self.score()

    def settup(self, numPlayers):

        self.colonist_ship_minimum = numPlayers
        constants.plantation_stacks = numPlayers + 1

        if numPlayers == 3:
            constants.ships = 4,5,6
            constants.victory_point_reserve = 75
            constants.colonist_reserve = 58

        elif numPlayers == 4:
            constants.ships = 5,6,7
            constants.victory_point_reserve = 100
            constants.colonist_reserve = 79
            constants.roles += 'prospector',

        elif numPlayers == 5:
            constants.ships = 6,7,8
            constants.victory_point_reserve = 122
            constants.colonist_reserve = 100
            constants.roles += 'prospector','prospector'

        self.board = constants.BoardState()
        self.board.colonist_ship = self.colonist_ship_minimum

        for i, player in enumerate(self._players):
            if i+1 <= int(0.5+numPlayers/2):
                player.addFarmTile('indigo')
                self.board.plantation_deck.remove('indigo')
            else:
                player.addFarmTile('corn')
                self.board.plantation_deck.remove('corn')
            player.dubloons += numPlayers-1
        shuffle(self.board.plantation_deck)
        self.board.settler_reset()

    def players(self, start):

        if type(start) is not int: start = self._players.index(start)
        return iter(self._players[start:] + self._players[:start])

    def play_round(self):

        for roleChooser in self.players(self.governorPos):
            debug('\n')
            roleChooser.log('chooses a role')
            card = roleChooser.decision(tuple(card for card in self.board.roleCards if card.availible))

            card.availible = False
            roleChooser.get_dubloons(card.dubloons)
            role = card.name

            if role=='mayor':
                print(self.board.colonist_ship)
                dif = self.board.colonist_ship % len(self._players)
                ideal = self.board.colonist_ship // len(self._players)
                for player, amount in zip(self.players(roleChooser), [ideal+1]*dif+[ideal]*len(self._players)) :
                    player.get_colonists(amount)

            roleChooser.role = True
            for player in self.players(roleChooser):
                getattr(player, role+'_phase')()
            roleChooser.role = False

            if role=='mayor':
                self.board.new_colonists = max(
                    self.colonist_ship_minimum,
                    sum(sum(b.vacant for b in p.city) for p in self._players))

            getattr(self.board, role+'_reset')()

    def score(self):
        pass



