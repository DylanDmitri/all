"""


weight, best_child,


take fringe with highest weight


state : {
    parents = (a, b, c)
    children = (d, e, f)
    choices = (3, 2, 5)

    weight = .5
    score = 1
}


"""


class Node:
    __slots__ = ['parents', 'children', 'choices', 'weight', 'score']

    def __init__(self):
        self.parents = []

        self.weight = 0


class SearchTree(dict):

    def __init__(self, get_next, get_possible, evaluate, active_index):
        """
        assumes a two-player game

        state is an tuple representing the board

        get_next(state, choice) -> gamestate
        get_possible(state) -> {choice: weight}

        'evaluate' scores the game and returns the advantage for the first player

        state[active_index] gives the player making the decision
        state[active_index] should return 0 for a random decider
        state[active_index] should return 1 for p1, where if they're winning evaluate is positive
        state[active_index] should return 2 for p2, where if they're winning evaluate is negative

        """

        self.get_next = get_next
        self.get_possible = get_possible
        self.evaluate = evaluate
        self.p1 = active_index

        super().__init__()

    def explode(self, state):

        self[state].choices = tuple(self.get_possible(state))
        self[state].children = tuple(self.get_next(state, choice) for choice in self[state].choices)

        for child in self[state].children:
            self[child] = Node()
            self[child].score = self.evaluate(child)


        if state[self.p1]:
            self[state].score = max(child.score for child in self[state].children)
        else:
            self[state].score = min(child.score for child in self[state].children)




