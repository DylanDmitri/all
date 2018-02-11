locations = {}
class Location:
    def __init__(self, name, descr, passages):
        locations[name] = self
        self.name = name
        self._flavor = descr
        self.passages = passages

    @property
    def description(self):
        return self._flavor

items = {}
class Item:
    def __init__(self, name, descr, **kwargs):
        items[name] = self
        self.name = name
        self.descr = descr

class Underbrush(Item):
    def __int__(self):
        Item.__init__(self, 'dense underbrush', 'bushes and vines impedede movement')

    def before_character_move(self, character):
        character.ap -= 1


class Passage:
    def __init__(self, name, descr, exit):
        locations[entrance].passages.append(self)
        self.exit = locations[exit]

class Character:
    def __init__(self):
        self.ap = 3
        self.moves_left = 2

    def spend_move(self):
        self.ap -= 1
        self.moves_left -= 1

    def attempt(self, action):
        backup = self.__dict__
        action(self)


class PC(Character):
    def __init__(self):
        super().__init__()
        self.location = None

    def act(self):
        print(self.location.description)



Location(name='outside', descr='You are on the trail, surrounded by trees.',

         passages = (
             Passage('A *hill* rises abruptly in front of you, with stones and big trees.',
                     action='climb', challenge=),
             Passage('')

         )

         )
Passage()



