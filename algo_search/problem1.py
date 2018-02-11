from random import random
from itertools import combinations


def generateRandomGraph(numNodes=50, probability=50, directed=True):

    nodes = list(range(numNodes))
    graph = {i:[] for i in range(numNodes)}

    for a, b in combinations(nodes, 2):
        if random() < probability:
            if random() < 0.5:
                graph[a].append(b)
            else:
                graph[b].append(a)

    return graph


def displayGraph(graph):
    for key, val in graph.items():
        print(key, ':', ', '.join(map(str, val)))



def cyclic(node, depth=0):
    if depth > N:
        return True

    return any(cyclic(other, depth+1) for other in graph[node])

print(cyclic(0))





