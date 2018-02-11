
places = {}
class __Place:
    def __init__(self, name):
        places[name] = self
        self.name = name

        self.outbound = []

def Place(name):
    if name not in places:
        __Place(name)
    return places[name]


class Journey:
    def __init__(self, start, end, *costs, bothways=True):

        Place()


