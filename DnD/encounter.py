# An encounter is like
"""

narration:
You've been on the Triboar Trail for about half a day. As you come around a bend, you spot two dead horses sprawled about
fifty feet ahead of you, blocking the path. Each has several black-feathered arrows sticking out of it.
 The woods press close to the trail here, with a steep embankment and dense thickets on either side.

dense thicket (difficult terrain, heavy cover)
triboar trail (road, dirt, 10 wide, 300 long)
2 horse corpses
4 goblins

goblins ambush players

"""



class Terrain:
    def __init__(self, dimensions=(None, None), kind=None):
        self.dimensions = Location(*dimensions)

        self.kind = kind
        self.cover = 0
        self.difficulty = 0

        if kind=='flat':
            pass

        elif kind=='underbrush':
            self.cover = 5
            self.difficulty = 5

        self.items = set()

    def add(self, ns, ew, thing):
        assert 0 < thing.loc.ns < self.dimensions.ns
        assert 0 < thing.loc.ew < self.dimensions.ew
        thing.loc.ns = ns
        thing.loc.ew = ew

        self.items.add(thing)
        thing.terrain = self

class Location:
    def __init__(self,ns,ew):
        self.ns = ns
        self.ew = ew

class Object:
    def __init__(self, name, *properties):
        '''
        size =
        1 (enveloped by one hand) ring or coin
        2 (fits in hand) tennis ball, small flask
        3 (not enclosed by fingers) dagger, scroll
        4 (carried with two hands)
        5 (up to knees)
        6 (waist-high) barrel
        7 (about person sized)
        8 (big as two people)
        9 (wider than several people)
        '''

        self.loc = Location(None, None)
        self.name = name

        for k, val in properties:
            setattr(self, k, val)



road = Terrain(dimensions=(10, 300), kind='flat')
thicket = Terrain(dimensions=(50, 300), kind='underbrush')

road.north = thicket
road.south = thicket

class Creature:
    def __init__(self):
        self.loc = Location(5, 50)
        self.sight = None
        self.smell = None

    @property
    def perceptions(self):
        pass
        '''
        for each item around
         if you can notice something about the item add it
        '''

class Goblin(Creature):
    def __init__(self):
        pass

    def action(self):
        pass

    def goals(self):
        cowardice = 50
        








