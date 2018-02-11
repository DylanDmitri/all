from collections import defaultdict

# rotational symmetry on a torus


def states(size=5):
    s = set()

    for _ in range(int(2**size)):
        b = bin(_)[2:].rjust(size, '0')

        for _ in range(size):
            b = b[-1] + b[:-1]
            if b in s:
                break
        else:
            s.add(b)

    # return [p for p in s if sum(int(i) for i in p)<=size/2]
    return sorted(list(s))


# for i in range(10):
#     print(i, len(states(i)))



h = '1'
l = '.'

rule = {
    (l+l+l):l,
    (l+l+h):h,
    (l+h+l):h,
    (l+h+h):h,
    (h+l+l):l,
    (h+l+h):h,
    (h+h+l):h,
    (h+h+h):l,
}

print(rule)

def transform(s):

    wrapped = s[-1] + s + s[0]

    r = ''
    for i in range(len(s)):
        r += rule[wrapped[i:i+3]]
    return r


# w = '#####  '
# for gen in range(50):
#     print('|'+w+'|')
#     w = transform(w)


seen = set()
parents = defaultdict(lambda:[])

for t in states(8):
    t = t.replace('0', l).replace('1', h)

    parents[transform(t)].append(t)


for k,v in parents.items():
    print(k, v)

'''

ms
00000000  11111111   (8)
00000001  11111110   (7 1)
00000011  11111100   (6 2)
00000111  11111000   (5 3)
     00001111        (4 4)

g2/6
00000101  01011111   (5 1 1 1)
00001001  01101111   (4 1 2 1)
00010001  01110111   (3 1 3 1)

g3/5
00001011  11110100  m 00001101  11110010
00010011  11101100  m 00011001  11100110
00010101  11101010
00100101  11011010

g4/4
00010111            m 00011101
00100111  11011000
00101011            m 00110101  00101101
    00110011
    01010101


'''