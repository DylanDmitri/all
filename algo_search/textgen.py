from random import choice

text = '''Contests you can sink your teeth into!
Toilet paper mummy wrapping contest.

Spoooooky cusotmer contest!

Bobbing for apples.

Sick jamz from Lanister's very own DJ Ricky Romba.

Halloween treats including caramel apples, candy, and more!
'''

for line in range(30):
    try:
        raise Exception()
        t = text.split('\n')[line]
    except:
        t =''
    print(''.join(t[i] if 0<=i<len(t)-1 else choice('01') for i in range(-10, 80)))
