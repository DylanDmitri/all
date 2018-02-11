infile = open('data.txt', 'r')
snoff=input
def input():
    return next(infile)



def IterGen(string):
    places = {}
    cur = 0

    for c in string:
        if c not in places:
            places[c] = str(cur)
            cur += 1
        yield places[c]

# get input
n, q = map(int, input().split())
bigstr = input().strip()

# populate search tree

store = {}

for i in range(n):

    key = ''
    for i in (IterGen(bigstr[i:])):
        key += i
        if key not in store:
            store[key] = 0
        store[key] += 1


# do the searches
for _ in range(q):
    left, right = map(int, input().split())
    key = ''.join(IterGen(bigstr[left-1:right]))
    print(store[key])







