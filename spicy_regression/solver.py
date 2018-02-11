import numpy
import sympy

excluded = '-+=*/'
alpha = 'abcdefghijklmnopqwrstuvwxyz'

n = tuple(
'''ia + 2 ix = ix + iv
2 ix + ib = iv
i0 = iv + ix
ia + ix = 6
ix - ib = 2 ia
6 = ia + ib - 2ia '''.split('\n')
)

tokens = {*'ia ix iv ib i0'.split()}

fmap = {t:a for t, a in zip(tokens, alpha)}

for e in n:
    for t,a in fmap.items():
        # print(t, a, )
        e = e.replace(t, a)
    print(e, end=', ')

input()

for k, v in fmap.items():
    print(v, '--', k)

