from collections import defaultdict
from string import ascii_lowercase

class alph:
    __slots__ = 'count', *ascii_lowercase

    def __init__(self):
        self.count = 0

    def __getitem__(self, item):
        if not hasattr(self, item):
            setattr(self, item, alph())

        return getattr(self, item)

def dylan():

    root = alph()

    def traverse(string,inc=0):
        current = root
        for c in string:
            current = current[c]
            current.count += inc
        return current.count

    for line in open('trie_test'):
        action, word = line.split()
        if action=='add':
            traverse(word, inc=1)
        else:
            traverse(word)


def dylan2():

    def node():
        return defaultdict(node, count=0)

    root = node()

    def traverse(string,inc=0):
        current = root
        for c in string:
            current = current[c]
            current['count'] += inc
        return current['count']

    for line in open('trie_test'):
        action, word = line.split()
        if action=='add':
            traverse(word, inc=1)
        else:
            traverse(word)


def james():
    root = dict(Count=0)

    def add(x):
        current = root
        for ch in x:
            if ch in current:
                current = current[ch]
                current['Count'] += 1
            else:
                current[ch] = dict(Count=1)
                current = current[ch]


    def find(x):
        current = root
        for ch in x:
            if ch in current:
                current = current[ch]
            else:
                return 0

        return current['Count']


    for line in open('trie_test'):
        action,word = line.split()
        if action == 'add':
            add(word)
        else:
            find(word)


from timeit import timeit

print(timeit("dylan()", setup="from __main__ import dylan", number=2))
print(timeit("dylan2()", setup="from __main__ import dylan2", number=2))





