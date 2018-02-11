"""
1. Write a program that, given a directed graph G (1) checks whether G is acyclic or not and if G is acyclic
then outputs a topological sorting of G (2) if G is not acyclic output a cycle. Test your algorithm on 20
“random graphs” (explained below) with 50 nodes each: 10 generated with probability 0.25 and 10 with
probability 0.75.
"""

from itertools import combinations
from random import random

class RandomDirectedGraph:
    def __init__(self, nodes=50, probability=0.5):
        self.graph = {i:[] for i in range(nodes)}
        for u,v in combinations(range(50), 2):
            if random() < probability:
                if random() < 0.5:
                    self.graph[u].append(v)
                else:
                    self.graph[v].append(u)

    def checkCyclical(self):
        visited = []

        def search(spot):
            visited.append(spot)

            for i in self.graph[spot]:
                if i in visited:
                    return i,
                result = search(i)
                if result:
                    return (spot,) + result
            return False

        return search(0)

    def show(self):
        for i, vals in self.graph.items():
            print(i, ':', ', '.join(map(str, vals)))

for i in range(1):
    g = RandomDirectedGraph()
    g.show()
    print(g.checkCyclical())


