from itertools import combinations
from random import random


def generateUndirectedGraph(numNodes=50, probability=0.5):

    nodes = list(range(numNodes))
    graph = {i:[] for i in range(numNodes)}

    for a, b in combinations(nodes, 2):
        if random() < probability:
            graph[a].append(b)
            graph[b].append(a)

    return graph


def displayGraph(graph):
    for key, val in graph.items():
        print(key, ':', ', '.join(map(str, val)))


def breadthSearchForDiameter(node, graph):

    visited = set()

    queue = [node]
    newqueue = []
    depth = 0

    while True:

        #// queue is the current "layer". If it is empty, fill it with the new values and increment depth.
        if not queue:
            if not newqueue:  #// if there's nothing to fill with, then return

                if len(visited) < len(graph):  # // if not all visited, return infinity
                    return float('inf')
                else:
                    return depth

            #// swap the queues and increment
            queue = newqueue
            newqueue = []
            depth += 1

        current = queue.pop()

        if current not in visited:
            visited.add(current)

            for child in graph[current]:
                newqueue.append(child)


def diameter(graph):
    nodes_in_max_path = max(
        breadthSearchForDiameter(node, graph)
        for node in graph)

    return nodes_in_max_path -1


def main():
    for prob in (0.25, 0.75):
        for repeat in range(10):
            graph = generateUndirectedGraph(numNodes=50, probability=prob)
            displayGraph(graph)
            print('diameter =', diameter(graph))
            print()


def singleTestCase():

    print(diameter({
        1:[3,4],
        2:[],
        3:[2],
        4:[1,3],
    }))


#// singleTestCase()
main()
