import requests

from io import StringIO
from html.parser import HTMLParser

jsonUrls = {
    "map": {
        "nova": "https://earthmc.net/map/nova/tiles/_markers_/marker_earth.json",
        "aurora": "https://earthmc.net/map/aurora/tiles/_markers_/marker_earth.json"
    },
    "player": {
        "nova": "https://earthmc.net/map/nova/up/world/earth/",
        "aurora": "https://earthmc.net/map/aurora/standalone/dynmap_earth.json"
    }
}

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
    @staticmethod
    def intersection(arr1, arr2): return list(filter(lambda x: x in arr1, arr2))
    @staticmethod
    def asJSON(req):
        try: return req.json()
        except: raise ValueError("Response content is not valid JSON")
    @staticmethod
    def playerData(map): return utils.asJSON(requests.get(jsonUrls["player"][map]))
    @staticmethod
    def mapData(map): return utils.asJSON(requests.get(jsonUrls["map"][map]))
    @staticmethod
    def townArea(town): return utils.calcArea(town.x, town.z, len(town.x))
    @staticmethod
    def calcArea(x, z, points, divisor=256):
        area = 0
        j = points-1

        for i in range(points):
            area += (x[j] + x[i]) * (z[j] - z[i])
            j = i

        return abs(area/2) / divisor    
