from random import randint
from copy import deepcopy

NODE = 0

class Node:
    def __init__(self):
        self.adj = []
        self.name = str(globals()['NODE'])
        globals()['NODE'] += 1

    def __str__(self):
        return self.name + ': '+' '.join(n.name for n in self.adj)


def RandGraph():
    nodes = 3
    conns = 1

    globals()['NODE'] = 0

    self = [Node() for _ in range(nodes)]

    for node in self:
        for _ in range(conns):
            node.adj.append(self[randint(0, nodes-1)])

    return self

def depth(graph):

    excluded = set()

    def go(node):
        excluded.add(node)
        for neighbor in node.adj:
            if neighbor in excluded:
                return True
            if go(neighbor): return True
        return False

    while True:
        if len(graph) == len(excluded):
            return False

        for node in graph:
            if node not in excluded:
                cyclefound = go(node)
                if cyclefound:
                    return len(excluded)



def breadth(graph):
    excluded = set()

    def go(nodes):
        next_time = []

        for node in nodes:
            excluded.add(node)
            for neighbor in node.adj:
                if neighbor in excluded:
                    return True
                next_time.append(neighbor)

        if go(next_time):
            return True

        return False

    while True:
        if len(graph) == len(excluded):
            return False

        for node in graph:
            if node not in excluded:
                cyclefound = go([node])
                if cyclefound:
                    return len(excluded)

def test():
    gd = RandGraph()

    print(depth(gd))
    print(breadth(gd))

# g = RandGraph()

# g = [Node(), Node(), Node()]
# g[0].adj.append(g[1])
# g[1].adj.append(g[2])
# g[2].adj.append(g[1])

depth_totals = []
breadth_totals = []
for i in range(100):
    g = RandGraph()
    depth_totals.append(breadth(g))
    breadth_totals.append(breadth(g))

for a in (depth_totals, breadth_totals):
    print(sum(a)/len(a))








