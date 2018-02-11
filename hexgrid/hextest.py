def uberpad(string, length):
    string = string[:length]
    dif = length - len(string)

    string = string.rjust(length-dif//2, '_').ljust(length, '_')
    return string




class Grid:
    def __init__(self):
        self.rows = [['as', 'we', 'tt'], ['rr']]
        self.charwidth = 2

    @property
    def height(self):
        return len(self.rows)

    @property
    def width(self):
        return len(self.rows[0])

    def print(self):
        for row in self.rows:
            print(*(uberpad(s, self.charwidth) for s in row), sep=' ')


Grid().print()

