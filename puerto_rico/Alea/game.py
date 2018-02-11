from puerto_rico.Alea.data import *
from itertools import combinations

"""

board: current state

game: players & board

choice: list<options>, which player

choice = self.offerChoice(options, player)

def makeChoice(self, choice):


"""


class Game:

    def __init__(self, p1, p2):

        self.bank = Bank()

        self.tileChooser = None

        self.p1 = PlayerBoard(brain=p1, indigo=True)
        self.p2 = PlayerBoard(brain=p2, indigo=False)

        self.activePlayer = self.p1

    def nextPlayer(self):
        self.activePlayer = (self.p1, self.p2)[self.activePlayer==self.p2]

    def game(self):
        while self.bank.rungame:

            while len(self.bank.roles) > 1:
                role = self.getChoice(choice.role)


    def getChoice(self):
        pass

    def settler(self):
        pass


    def log(self, message, priority=5):
        print(message)


class Bank:
    def __init__(self):

        self.roles = list(roles.all)
        self.dubloons = {role:0 for role in roles.all}

        self.farm_availible = []
        self.farm_stack = []
        self.farm_discard = []

        self.rungame = False


class Player:
    def __init__(self, brain=None, corn=False, indigo=False):

        self.brain = brain

        assert corn+indigo == 1

        self.city = []
        self.farm = [farm.corn, farm.indigo][indigo]

        self.dubloons = (2, 3)[indigo]
        self.vps = 0

        self.goods = []

    def choose(self):







