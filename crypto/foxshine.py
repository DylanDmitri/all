import enchant
from random import shuffle, choice
from itertools import permutations

d = enchant.Dict('en_US')
text = 'ldghecsmkpudmnvexmqjxfybxdw,lawgvrrhmpyevgoxlunxu'
#      'THE-----A---------------O--,THE----------------IT'

key = {
    'l':'t',
    'd':'h',
    'g':'e',
    'k':'a',
    'x':'o',
    'a':'h',
    'w':'e',
    'u':'t'
}

text = open('bigtext', 'r').read()
alpha = "abcdefghijklmnopqrstuvwxyz',-"

def freq_analysis(text, size=4):
    word_groups = [text[i*size:i*size+size] for i in range(0, len(text)//size-size)]
    print(word_groups)

    freqs = [(sum(char in group for group in word_groups),char)
             for char in alpha]

    for t in sorted(freqs):
        print(*t[::-1])

def repeat_analysis(text, size=2):
    freqs = {}
    for i in range(len(text)-size):
        chunk = text[i:i+size]
        freqs[chunk] = text.count(chunk)

    print(*sorted(list(c[::-1] for c in freqs.items())),sep='\n')


def double_analysis(text):
    dubs = {a:0 for a in alpha}
    for i in range(len(text)-1):
        if text[i] == text[i+1]:
            dubs[text[i]] += 1
    print(*sorted(list(c[::-1] for c in dubs.items())), sep='\n')



def translate():
    print(' '.join(key.get(c, '_') for c in text))


for i in range(29):
    s = ''
    for char in text:
        spot = alpha.index(char)
        newspot = spot + i

        i += 1
        s += alpha[newspot%len(alpha)]
    print(s)


# text = ''.join(choice(alpha) for _ in range(1113))
double_analysis(text)
# repeat_analysis(text, 3)

translate()

input()
freq_analysis(text)

repeat_analysis(text)

translate()


# common - dmx
# okay - eglw

