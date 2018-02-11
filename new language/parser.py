"""
generates an abstract syntax tree from input text

line gets parsed into tokens
some tokens auto have linages

print 4+5 /3

(print_ ~str) (4 _+_ 5) (?int _/_ 3)

(print 4+5) (?int /3) X
print (4+5)/3 Y

"""

line = 'sum 1..1000 where multiple 3|5'


class Thing:
    def __init__(self, methods):
        self.name, *self.methods = tuple(methods.split())

things = (
    'any', 'num', 'str', 'list', 'iter', 'map'
)

actions = {}
class Action:
    def __init__(self, descr):
        # where descr like (sum ?iter)
        self.name = None

        self.before = []
        self.after = []

        for part in descr.strip().split():

            if part not in things:
                assert not self.name
                self.name = part

            if not self.name: self.before.append(part)
            else: self.after.append(part)

        actions[self.name] = self

    def __str__(self):
        return 'action<{}>'.format(self.name)

Action('any + any')
Action('int / int')
Action('sum iter!int')
print(actions)




