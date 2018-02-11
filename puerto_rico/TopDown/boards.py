

class TransferFailedError(Exception): pass


class Zone:
    """A zone is any space that can contain components."""

    def __init__(self, *kinds):
        assert kinds
        for kind in kinds:
            setattr(self, kind, 0)

    def send(self, amount, resource, other):

        if amount == 'all':
            amount = getattr(self, resource)
            if amount == 0:
                return

        try:
            self.validate_send(resource, amount)
            other.validate_get(resource, amount)
        except TransferFailedError as te:
            raise te
        else:
            self._transfer(resource, -amount)
            other._transfer(resource, amount)

    def validate_get(self, resource, amount):
        if not hasattr(self, resource):
            raise TransferFailedError("receiving zone has no <{}> field".format(resource))

    def validate_send(self, resource, amount):
        if not hasattr(self, resource):
            raise TransferFailedError("sending zone has no <{}> field".format(resource))

        if amount > getattr(self, resource):
            raise TransferFailedError("not enough <{}> to send".format(resource))

    def _transfer(self, resource, amount):
        setattr(self, resource, getattr(self,resource) + amount)


class BoundedZone(Zone):

    def __init__(self, *resources, upperbound=float('inf')):
        super().__init__(*resources)
        self.upperbound = upperbound

    def validate_get(self, resource, amount):
        super().validate_get(resource, amount)

        if amount + getattr(self,resource) > self.upperbound:
            raise TransferFailedError("no room on the receiving end for that resource")


class CargoShip(BoundedZone):

    def __init__(self, size):
        self.current = None
        BoundedZone.__init__(self, *barrels, upperbound=size)

    def validate_get(self, resource, amount):
        if self.current is None:
            self.current = resource

        if resource != self.current:
            raise TransferFailedError("Can't load that <{}> on a <{}> ship.".format(resource, self.current))

        super().validate_get(resource, amount)


class BuildingInstance(BoundedZone):
    def __init__(self, generic):
        self.generic = generic
        super().__init__('colonists', upperbound=self.generic.jobs)


goods = []
barrels = []
plantations = []

class CreateResourceType:
    def __init__(self,name,price):
        goods.append(self)
        barrels.append('barrel_' + name)
        plantations.append('tile_' + name)
        self.price = price


# ======== begin data =========

tokens = ('dubloons', 'colonists', 'vps')

CreateResourceType('corn', price=0)
CreateResourceType('indigo', price=1)
CreateResourceType('sugar', price=2)
CreateResourceType('tobacco', price=3)
CreateResourceType('coffee', price=4)

tiles = tuple(plantations) + ('quarry', )

roles = ('settler', 'mayor', 'builder', 'craftsman', 'trader', 'captain', 'prospector')

# -------- end data ----------


class MainBoard:
    def __init__(self, buildings):
        self.supply = Zone(*tokens, *barrels)

        self.tileStack = Zone( *plantations )
        self.tileDiscard = Zone( *plantations )
        self.tileActive = Zone( *tiles )

        self.buildings = Zone(*buildings.keys())
        self.colonistShip = BoundedZone('colonists')
        self.tradingHouse = Zone(*barrels)
        self.roleCards = Zone(*roles)

        self.cargoShips = NotImplemented

class PlayerBoard:
    def __init__(self, player, buildings):
        self.player = player

        self.store = Zone(*tokens, *barrels)

        self.city = Zone(*buildings)
        self.island = Zone(*tiles)

        self.currentRole = Zone(*roles)
        self.oldRoles = Zone(*roles)