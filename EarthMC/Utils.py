import requests

from io import StringIO
from html.parser import HTMLParser

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

class utilFuncs:
    def __init__(self):
       self.endpoints = self.reqJSON('https://raw.githubusercontent.com/EarthMC-Toolkit/Toolkit-Website/main/endpoints.json')

    @staticmethod
    def reqJSON(url):
        req = requests.get(url)
        try: return req.json()
        except: raise ValueError("Response content is not valid JSON")

    def fetchData(self, type, mapName): return self.reqJSON(self.endpoints[type][mapName])
    
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

    @staticmethod
    #def intersection(arr1, arr2): return list(filter(lambda x: x in arr1, arr2))
    #def difference(arr1, arr2): return filter(lambda x: x not in arr1, arr2)

    @staticmethod
    def townArea(town): return utilFuncs.calcArea(town.x, town.z, len(town.x))
    
    @staticmethod
    def calcArea(x, z, points, divisor=256):
        area = 0
        j = points-1

        for i in range(points):
            area += (x[j] + x[i]) * (z[j] - z[i])
            j = i

        return abs(area/2) / divisor    