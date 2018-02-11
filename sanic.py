from time import perf_counter
from random import shuffle

def check(func, *args):
    trials = 10000
    start = perf_counter()
    for k in range(trials):
        func(*args)
    end = perf_counter()

    return trials / (end-start)


foo = lambda :None
foo.amount = 0

bar = lambda:None
bar.amount = 0

class fakegame:

    def __init__(self):
        self.vals = [1, 1, 1, 0, 0, 5]

    def swap1(self, reverse):
        return sum(self.vals) - self.vals[-1]

    def swap2(self, reverse):
        return sum(self.vals[:-1])

    def swap3(self, reverse):
        return self.vals[0]+self.vals[1]+self.vals[2]+self.vals[3]+self.vals[4]






t = fakegame()
test = [t.swap2, t.swap3, t.swap1]
res = {t:[0, 0] for t in test}

for swap in test:
    for i in range(100):
        # shuffle(trie_test)
        t.amount = 5
        res[swap][0] += check(swap, True)
        t.amount = 5
        res[swap][1] += check(swap, False)

for swap in (t.swap1, t.swap2, t.swap3):
    print(res[swap][0])
    print(res[swap][1])
    print()

# 325560866.4799105   319073023.994213
# 331427567.097525    314615459.1625885
# 312792165.14658433  299371317.0998928
# 309001364.379733    303692594.89803934
# 275163965.90097487  272836424.66882354
# 276681379.31948286  270340139.49815875
#


