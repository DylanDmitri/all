from copy import copy

class gamestate:
    def __init__(self):
        self.a1 = ' '
        self.a2 = ' '
        self.a3 = ' '
        self.b1 = ' '
        self.b2 = ' '
        self.b3 = ' '
        self.c1 = ' '
        self.c2 = ' '
        self.c3 = ' '

        self.active = 1

        self.game_over = False

class Node:
    def __init__(self, game):
        choices = {
            choice :
        }