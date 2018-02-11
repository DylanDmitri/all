from textwrap import wrap


class Container:
    def __init__(self, **kwargs):
        for

def para(text):
    for line in wrap(''.join(c for c in text if c!='\n')):
        print(line)


def choose(options):
    options = tuple(options)
    for i, o in enumerate(options):
        print(i, '-', o)



class Race:
    human = 'human'
    elf = 'elf'
    dwarf = 'dwarf'
    orc = 'orc'
    half_orc = 'half_orc'
    half_elf = 'half_elf'
    halfing = 'halfing'

