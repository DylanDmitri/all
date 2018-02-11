from itertools import combinations
from random import random


def generateDirectedRandomGraph(numNodes=50, probability=0.5):

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


def checkGraph(graph):

    #// this is a helper function. It trims the path down to get just the cycle.
    def displayTrueCycle(node, path):
        cycle = []
        flag = False

        for step in path:
            if step == node:
                flag = True
            if flag:
                cycle.append(step)

        cycle.append(node)

        print('cycle found:',' -> '.join(map(str,cycle)))
    #// end helper function

    topoList = []
    visited = set()

    #// start recursive search function
    def depthFirstSearch(node, path):

        if node in path:  #// cycle found!
            displayTrueCycle(node,path)
            return True

        if node not in visited:
            visited.add(node)

            for child in graph[node]:
                if depthFirstSearch(child, path+[node]):
                    return True

            topoList.append(node)
    #// end recursive search function


    while len(visited) < len(graph):
        #// while there are nodes left to vist
        #// find an empty node and search from it

        for node in graph:
            cycleFound = depthFirstSearch(node, path=[])
            if cycleFound:
                return True

    topoList.reverse()  #// because it adds to the 'wrong' end

    print("topological sorting:", ' -> '.join(map(str, topoList)))



def main():
    for prob in (0.25, 0.75):
        for repeat in range(10):
            graph = generateDirectedRandomGraph(numNodes=50, probability=prob)
            displayGraph(graph)
            checkGraph(graph)


def singleTestCase():

    checkGraph({
        1:[3,4],
        2:[],
        3:[2],
        4:[1,3],
    })

#// singleTestCase()
main()

print('hello world!')