class Container:
    def __init__(self, **kwargs):
        self.names = kwargs.keys()
        for name, val in kwargs.items():
            setattr(self, name, val)

    def __iter__(self):
        return self.names.__iter__()

    def __getitem__(self, item):
        return getattr(self, item)


allowed = (2, 3, 5)
def debug(*text, end='\n', sep=' ', c=5):
    if c in allowed:
        print(*text, end=end, sep=sep)