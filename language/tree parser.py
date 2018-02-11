"""

a -> sum 1..100
a -> sum ( 1 .. 100 )

element
an element has a type



"""

class Type:
    none = 'none'
    numeric = 'numeric'
    iterable = 'iterable'
    text = 'text'
    boolean = 'boolean'


class element:
    def __init__(self, value, rtypes=tuple()):
        self.value = value

        if not rtypes.__iter__:
            rtypes = (rtypes, )
        self.rtypes = rtypes

    def istype(self, name):
        return name in self.rtypes


class function(element):
    def __init__(self, value, pbefore=tuple(), rtypes=tuple(), pafter=tuple()):
        super().__init__(value, rtypes)
        self.pbefore = pbefore
        self.pafter = pafter

    def call(self):
        raise self.value(self.pbefore + self.pafter)







