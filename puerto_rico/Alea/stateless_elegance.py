from puerto_rico.Alea.data import *
from collections import namedtuple


container = lambda fields: namedtuple(p+str(hash(fields)), list(fields.split()))

Choice = container('kind options playerNum')
FarmSupply = container('stack heap open decider')
GameState = container('round vps colonist_supply farms roles role_money players choice governor')
Player = container('brain city farms dubloons vps goods')

class Game(GameState):

    roles_left = 1

    def __init__(self):
        self.round = 0
        self.vps = 65
        self.colonist_supply = 40
        self.colonist_ship = 2
        self.buildings = {

        }

    def step(self):
        eval(self.choice.kind)(self)
    
    def random_tiles(self):
        pass
    
    def role(self):
        pass
    
    def plantation(self):
        pass
    
    def bonus_settler(self):
        pass
    
    def jobs(self):
        pass
    
    def building(self):
        pass
    
    def bonus_production(self):
        pass
    
    def trade_good(self):
        pass
    
    def shipment(self):
        pass
    
    def storage(self):
        pass
    
    def cleanup(self):
        self.governor += 1
        self.governor %= len(self.players)
        for leftover in self.roles:
            self.role_money[leftover] += 1
        self.roles = roles.all



Enginer.step()
