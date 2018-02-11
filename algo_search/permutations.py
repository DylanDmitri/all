
class Element:
    def __init__(self, vals):
        self.off,self.val,self.on = vals

    def mobile(self):
        return self.val > self.on

    def __str__(self):
        return ' '.join(map(str, (self.off, self.val, self.on)))


def permute(size):
    a = [-8, *range(size, 0, -1), -8]
    elems = [Element(a[i:i+3]) for i in range(size)]

    while True:

        print(*elems,sep='\n')
        input()

        for e in elems:
            if e.mobile():
                break
        else:
            break

        target = elems[-e.on]
        print(e, '|', target)

        if target.on == e.val:
            e.off, e.on, target.off, target.on = target.val, target.off, e.val, e.off

        else:
            e.off, e.on, target.off, target.on = target.val, target.on, e.off, e.val

        for larger in elems[:-e.val]:
            print('swapping')
            larger.off, larger.cur = larger.cur, larger.off


permute(3)



