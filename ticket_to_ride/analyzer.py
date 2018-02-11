from collections import namedtuple
Route = namedtuple('Route', ('length', 'color1', 'color2', 'tunnel'))
null_route = Route(float('inf'), None, None)

source = 'Europe'
tickets = source + '_Tickets'

def get_color_distribution():
    colors = {
        '1f':[],
        '2f':[],
        'black':[],
        'blue':[],
        'green':[],
        'grey':[],
        'orange':[],
        'pink':[],
        'red':[],
        'white':[],
        'yellow':[],
    }
    for line in open(source, 'r'):
        color = line.split()[2]

        length = int(line.split()[1])
        # length = 1

        for each in colors:
            if each in color:
                colors[each].append(length)
            if color == each+'/'+each:
                colors[each].append(length)

    for each in colors:
        colors[each].sort()

    for c, rs in (colors.items()):
        print(c.ljust(10), rs)






cities = {}
class city:
    def __init__(self, name):
        self.name = name
        cities[self.name] = self
        self.routes = {}

    @property
    def total_routes(self):
        total = 0
        for route in self.routes.values():
            total += bool(route.color1)
            total += bool(route.color2)
        return total

    @property
    def destination_count(self):
        return destination_counts[self.name]

    def add_route(self, other, length, color):
        if '/' not in color:
            color1 = color
            color2 = None
        else:
            color1, color2 = color.split('/')

        self.routes[other] = Route(int(length), color1, color2, )

    def __str__(self):
        r = self.name.upper()
        for other, route in self.routes.items():
            r += '\n  {} {}'.format(other, route.length)
        return r

city_names = set()
for line in open(source, 'r'):
    start, end = line.split()[0].split('-')
    city_names.add(start)
    city_names.add(end)

for name in city_names:
    city(name)

for route in open(source, 'r'):
    start, end = route.split()[0].split('-')
    length = route.split()[1]
    colors = route.split()[2]
    tunnel = route.split()[3].startswith('t')

    cities[start].add_route(end, length, colors, tunnel)
    cities[end].add_route(start, length, colors, tunnel)

destination_counts = {name:0 for name in city_names}

for line in open(tickets, 'r'):
    points, start, end = line.split()
    destination_counts[start.lower()] += 1
    destination_counts[end.lower()] += 1

def effective_effort(route):
    return 2 + route.length + int(route.tunnel) + (int(route.color[0]) if len(route.color)==2)


def floydify():
    n = len(cities)

    names = sorted(city_names)
    D = {}
    for start in names:
        for end in names:

            D[start, end] = cities[start].routes.get(end, null_route).length

    for k in names:
        for i in names:
            for j in names:
                D[i,j] = min(D[i,j], D[i,k] + D[k,j])

    return D


# ============== start ================


distances = floydify()
while True:
    print(distances.get((input(), input()), 'no result found'))

print(*sorted(item[::-1] for item in tuple(destination_counts.items())), sep='\n')

data = []
for city in cities.values():
    data.append((city.total_routes, city.destination_count, city.name))

for tup in sorted(data):
    print(*tup, sep='\t')
