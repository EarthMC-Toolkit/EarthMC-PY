import re
from io import StringIO
from html.parser import HTMLParser

class AutoRepr(object):
    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}={!r}'.format(k, v) for k, v in self.__dict__.items())
        )

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()
    def handle_data(self, d): self.text.write(d)
    def get_data(self): return self.text.getvalue()

class FetchError(Exception):
    """Raised when there was an error fetching data from Dynmap."""
    pass

class utils:
    @staticmethod
    def striptags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    @staticmethod
    def find(pred, iterable):
        found = None
        for element in iterable:
            if pred(element):
                found = element
                break

        return found

    # @staticmethod
    # def intersection(arr1, arr2): return list(filter(lambda x: x in arr1, arr2))
    # def difference(arr1, arr2): return filter(lambda x: x not in arr1, arr2)

    @staticmethod
    def removeStyleCharacters(string): return re.sub('/(&amp;.|&[0-9kmnola-z])/g', "", string)

    @staticmethod
    def strAsBool(string): return True if string == 'true' else False

    @staticmethod
    def parseObject(obj): return vars(obj) if type(obj) is not dict else obj
    @staticmethod
    def dictToList(dict):
        vals = dict.values()
        return [utils.parseObject(val) for val in vals]

    @staticmethod
    def listFromDictKey(key): return list(dict.fromkeys(key))

    @staticmethod
    def townArea(town): return utils.calcArea(town['x'], town['z'], len(town['x']))

    @staticmethod
    def calcArea(x, z, points, divisor=256):
        area = 0
        j = points-1

        for i in range(points):
            area += (x[j] + x[i]) * (z[j] - z[i])
            j = i

        return abs(area/2) / divisor

    @staticmethod
    def manhattan(x1, z1, x2, z2):
        return abs(x2 - x1) + abs(z2 - z1)


