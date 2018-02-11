from collections import defaultdict


TAGS = set()

class Attribute(dict):
    def __init__(self, *args, **kwargs):

        tags = defaultdict(lambda: 0, **kwargs)
        for a in args:
            tags[a] += 1

        for k in tags:
            TAGS.add(k)

        super().__init__(tags)


class Race(Attribute):
    def __init__(self, str=2, int=2, luck=4):
        super().__init__(str=str, int=int, luck=luck)



class Character:
    def __init__(self, race, background, stat):
        self.physical = 2
        self.mental = 2
        self.luck = 4


