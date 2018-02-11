class Container:
    def __init__(self, **kwargs):
        self.names = kwargs.keys()
        for name, val in kwargs.items():
            setattr(self, name, val)

    def __iter__(self):
        return self.names.__iter__()

    def __getitem__(self, item):
        return getattr(self, item)


class Roles:
    all = list(range(6))
    settler = 0
    builder = 1
    craftsman = 2
    trader = 3
    captain = 4
    prospector = 5


class Tile:
    corn = 0
    indigo = 1
    sugar = 2
    tobacco = 3
    coffee = 4
    quarry = 5



def building(name=NotImplemented, kind='purple', tier=NotImplemented, cost=NotImplemented, max_workers=1):
    assert kind in ('purple', 'production')
    purple = kind=='purple'
    production = kind=='production'

    number = (3 if production else 2)
    vps = tier
    big = tier==4

    return Container(
        name=name,
        purple=purple,
        production=production,
        tier=tier,
        vps=vps,
        cost=cost,
        max_workers=max_workers,
        big=big,
        count=number,
        __str__=lambda self: self.name
    )

def default_buildings():
    return Container(
    indigo1       = building('small indigo plant', 'production', tier=1, cost=1),
    sugar1        = building('small sugar mill', 'production', tier=1, cost=2),
    indigo3       = building('indigo plant', 'production',  tier=2, cost=3, max_workers=3),
    sugar3        = building('sugar mill', 'production',  tier=2, cost=4, max_workers=3),
    tobacco3      = building('tobacco storage', 'production',  tier=3, cost=5, max_workers=3),
    coffee2       = building('coffee roaster', 'production',  tier=3, cost=6, max_workers=2),
    market1       = building('small market', tier=1, cost=1),
    hacienda      = building('hacienda', tier=1, cost=2),
    hut           = building('construction hut', tier=1, cost=2),
    warehouse1    = building('small warehouse', tier=1, cost=3),
    hospice       = building('hospice', tier=2, cost=4),
    office        = building('office', tier=2, cost=5),
    market2       = building('large market', tier=2, cost=5),
    warehouse2    = building('large warehouse', tier=2, cost=6),
    university    = building('university', tier=3, cost=7),
    factory       = building('factory', tier=3, cost=8),
    harbor        = building('harbor', tier=3, cost=8),
    wharf         = building('wharf', tier=3, cost=9),
    guild_hall    = building('guild hall', tier=4, cost=10),
    fortress      = building('fortress', tier=4, cost=10),
    city_hall     = building('city hall', tier=4, cost=10),
    customs_house = building('customs house', tier=4, cost=10),
    residence     = building('residence', tier=4, cost=10),
)


class Triggers:
    settler =


building('Hacienda', tier=1, cost=2, trigger=, action=)



building('small indigo plant)





