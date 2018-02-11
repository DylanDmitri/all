from random import choice, randint, random

class Accum:
    winwin = 0
    winlose = 0
    loselose = 0

    @classmethod
    def clear(cls):
        Accum.winwin = 0
        Accum.winlose = 0
        Accum.loselose = 0

class options:
    VERBOSE = False

    NODE_COUNT = 8

    GAME_LENGTH = (20,20)

    # REWARDS = (
    #     (( +1, +1),(+10,-10)),
    #     ((-10,+10),( -1, -1))
    # )

    REWARDS = (
        (( +1, +1),(+10,-10)),
        ((-10,+10),( -1, -1))
    )

    INITIAL_POP = 5

def show(*args):
    if options.VERBOSE: print(*args)

def randex(length):
    return randint(1, length)-1

def randomNode():
    return (randex(options.NODE_COUNT),
            randex(options.NODE_COUNT),
            choice((True,False)))

class Actor:

    MUTATION_RATE = 0.7

    def __init__(self, nodes=None, energy=50):

        self.energy = energy

        if nodes is None:
            nodes = [randomNode() for _ in range(options.NODE_COUNT)]
        self.nodes = nodes

    def reproduce(self):

        self.energy //= 2
        child = Actor(nodes = self.nodes[:], energy=self.energy)

        if random() < self.MUTATION_RATE:
            child.mutate()

        return child


    def mutate(self):
        self.nodes[randex(options.NODE_COUNT)] = randomNode()




def battle(actor1, actor2, game_length=options.GAME_LENGTH):

    s1,s2 = actor1.energy, actor2.energy

    nicecount, meancount = 0,0

    ticks = randint(*game_length)

    # starting node
    p1head = actor1.nodes[0]
    p2head = actor2.nodes[0]

    while ticks > 0:

        p1choice = p1head[2]
        p2choice = p2head[2]

        # show(f'p1 picks {("nice", "mean")[p1choice]}')
        # show(f'p2 picks {("nice", "mean")[p2choice]}')
        # show()
        show('wl'[p1choice] + 'wl'[p2choice])

        nicecount += (not p1choice) + (not p2choice)
        meancount += p1choice + p2choice

        # update score
        if p2choice == p1choice == False:
            Accum.winwin += 1
        elif p2choice == p1choice == True:
            Accum.loselose += 1
        else:
            Accum.winlose += 1

        p1, p2 = options.REWARDS[p2choice][p1choice]

        actor1.energy += p1
        actor2.energy += p2

        # react to each other's responses
        p1head = actor1.nodes[p1head[p2choice]]
        p2head = actor2.nodes[p2head[p1choice]]

        ticks -= 1

    show('1:', actor1.energy - s1)
    show('2:', actor2.energy - s2)
    show()
    show(actor1.nodes)
    show(actor2.nodes)

class Region:

    def __init__(self, abundance=150):

        self.people = [Actor() for _ in range(options.INITIAL_POP)]

        self.abundance = abundance


    def step(self):

        if len(self.people) < 2:
            show('extinction!')
            return

        a = self.people.pop(randex(len(self.people)))
        b = self.people.pop(randex(len(self.people)))

        battle(a, b)

        for i in a,b:
            if i.energy <= 0:
                show('death, length now', len(self.people))
            else:
                self.people.append(i)

            if i.energy > 100:
                show('birth, length now',len(self.people))
                self.people.append(i.reproduce())


        amount = self.abundance // len(self.people)**2 - len(self.people)//100

        for p in self.people:
            p.energy += amount











