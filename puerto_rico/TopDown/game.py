from puerto_rico.TopDown.boards import *
from random import choice

class Game:
    def __init__(self, players, settings=None, buildings=None):

        self.settings = settings
        self.board = MainBoard(buildings)
        self.playerBoards = [PlayerBoard(player, buildings) for player in players]

        # add stuff
        for bname in buildings:
            setattr(self.board.buildings, bname, buildings[bname].count)

        for name in (*tokens, *barrels):
            setattr(self.board.supply, name, settings[name])

        for name in (plantations):
            setattr(self.board.tileStack, name, settings[name])

        for card in settings['roles']:
            setattr(self.board.roleCards, card, 1)

        self.board.cargoShips = [CargoShip(size) for size in settings['ships']]


        # give players starting plantations and money

        for l, player in zip(self.settings['start_plantations'], self.playerBoards):
            tile = {'i':'tile_indigo', 'c':'tile_corn'}[l]
            self.board.tileStack.send(1, tile, player.island)

            money = self.settings['start_money']
            if self.settings.get('corn_player_dubloon_penalty', False) and tile=='tile_corn':
                money -= 1

            self.board.supply.send(money, 'dubloons', player.store)

        # flip some plantations over to start
        self.flipTiles()

    def play(self):
        round = 0
        for governor in self.loopPlayers(0, repeats=float('inf')):
            round += 1

            for id in self.loopPlayers(governor, repeats=self.settings['roles_per_round']):

                # choose role

                role = 'settler'

                self.board.roleCards.send(1, role, self.playerBoards[id].currentRole)

                for id2 in self.loopPlayers(id, repeats=len(self.playerBoards)):
                    {
                        'settler' : self.chooseTile,
                        'mayor' : self.placeColonists,
                        'builder' : self.build
                    }





                self.playerBoards[id].currentRole.send(1, role, self.playerBoards[id].oldRoles)



    def loopPlayers(self, startid, repeats=None):
        for offset in range(repeats):
            yield (startid + offset) % len(self.playerBoards)


    def flipTiles(self):
        dist = []
        for name in plantations:
            self.board.tileActive.send('all', name, self.board.tileDiscard)
            dist += [name] * getattr(self.board.tileStack, name)

        placed = 0
        target = self.settings['plantation_stacks']

        while placed < target:

            tile = choice(dist)
            self.board.tileStack.send(1, tile, self.board.tileActive)
            dist.remove(tile)

            if not dist:
                dist = []
                for name in plantations:
                    self.board.tileDiscard.send('all', name, self.board.tileStack)
                    dist += [name] * getattr(self.board.tileStack,name)

                if not dist:
                    break

            placed += 1

    def chooseTile(self, board):
        possible = [tile for tile in plantations if getattr(self.board.tileActive, tile)]

        tile = board.player.chooseTile(possible)

        self.board.tileActive.send(1, tile, board.island)








