from puerto_rico.Take4.assumptions import settings



class Plantation:
    jobs = 1

    corn = 'tile_corn'
    indigo = 'tile_indigo'
    sugar = 'tile_sugar'
    tobacco = 'tile_tobacco'
    coffee = 'tile_coffee'
    quarry = 'tile_quarry'

class Job:
    def __init__(self, base):
        self.base = base
        self.workers = 0

    def addWorker(self):
        assert self.workers + 1 <= self.base.jobs
        self.workers += 1


class CargoShip:
    def __init__(self, size):
        self.size = size
        self.filled = 0
        self.kind = None

    def take(self, kind, amount):

        assert self.filled + amount <= self.size

        if self.kind is None:
            self.kind = kind
        assert self.kind == kind

        self.filled += amount


class RoleCard:
    def __init__(self,name):
        bank.roles.name = self
        self.name = name
        self.availible = True
        self.dubloons = 0

class bank:

    roles = []

    def __init__(self, settings):

        self.roleCards = tuple(RoleCard(role) for role in settings.roles)
        self.buildings = [Job(building) for building in settings.buildings]


class board:

    def __init__(self):

        self.dubloons = 0
        self.island = []
        self.city = []

        self.goods =






