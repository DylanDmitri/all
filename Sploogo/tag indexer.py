infile = open('data.txt', 'r')
snoff=input
def input():
    return next(infile)


Error

from collections import defaultdict
digits = '1234567890'
def _patternize(string):
    places = {}
    cur = 0

    for c in string:
        if c not in places:
            places[c] = digits[cur]
            cur += 1
        yield places[c]

def patternize(string):
    return ''.join(_patternize(string))

# get input
n, q = map(int, input().split())
bigstr = input().strip()

# populate search tree

WINDOW = 10

starts = defaultdict(lambda:[])
for i in range(len(bigstr)-WINDOW):
    segment = patternize(bigstr[i:i+WINDOW])
    starts[segment].append(i)

print(starts)

for _ in range(q):
    left, right = map(int, input().split())
    segment = bigstr[left-1:right]

    if len(segment) < WINDOW:
        print('?? INSIDE WINDOW DEPTH')
    else:
        for poss in starts[patternize(segment[:10])]:
            print(poss, end=';')
        print()



