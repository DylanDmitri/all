from random import shuffle


def scramble(word):
    mid = list(word[1:-1])
    shuffle(mid)
    return word[0] + ''.join(mid) + word[-1]

text = """Your answer depends on the environment, this looks like C# and the input is an int, so any int divided by 2 will return an int, and the result would always be true."""


out = []
w = ''
for c in text:
    if c in ' \\\'".,/':
        if w:
            out.append(scramble(w))
            w = ''
        out.append(c)
    else:
        w += c

print(''.join(out))


