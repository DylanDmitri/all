
class Bank:
    def __init__(self):
        self.vps = 65
        self.colonists = 40
        self.colonist_ship = 2

        self.corn = 8
        self.

class Game:
    def __init__(self, players):
        self.bank = Bank()
        self.boards = [Board(player) for player in players]

