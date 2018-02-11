import os

path = '/Users/dg/Desktop/archive/FreeOrion.app/Contents/Resources/default/scripting/techs'

groups = tuple('	construction	defense		growth		learning	production	ships		specials	spy	'.strip().split())


class _tech:
    def __init__(self, text):

        self.vals = {}
        for line in text:
            if '=' in line:
                name, txt = line.split('=', 1)
                self.vals[name.strip()] = txt.strip()

        self.name = eval(self.name)

    def descr(self):
        r = ['\nTECH<{}<'.format(self.filename)]
        for name, val in self.vals.items():
            r.append(name +'\t'+ val)
        return '\n'.join(r)

    def __str__(self):
        return self.name

    def __getattr__(self, item):
        if item in self.vals: return self.vals[item]
        return super().__getattribute__(item)

techs = []
def Tech(f):
    temp = _tech(open(f, 'r'))
    temp.filename = f
    temp.fulltext = open(f, 'r').read()
    techs.append(temp)

for group in groups:
    for directory,subdirectories,files in os.walk(os.path.join(path, group)):
        for file in files:
            rpath = (os.path.join(directory,file))
            if rpath.endswith('.txt'):
                Tech(rpath)



def toint(string):
    start = ''

    if not string[0].isdigit():
        return -40

    for char in string:
        start += char
        if not start.isdigit():
            return int(start[:-1])
    return int(start)

researchcost = [tech for tech in techs if hasattr(tech, 'researchcost')]
researchcost.sort(key=lambda o: toint(o.researchcost))
for tech in researchcost:
    print(str(tech).ljust(30), tech.researchcost)



print(techs)
for tech in techs:
    if tech.name == 'SHP_KRILL_SPAWN':
        print(tech.filename)