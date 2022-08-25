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

class utils:
    def striptags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()
    def find(self, pred, iterable):
        for element in iterable:
            if pred(element):
                return element

        return None
    def intersection(self, arr1, arr2): return list(filter(lambda x: x in arr1, arr2))
    def getPlayerData(self, map): return requests.get("https://earthmc.net/map/up/world/earth/").json()
    def getMapData(self, map): 
        req = requests.get("https://earthmc.net/map/aurora/tiles/_markers_/marker_earth.json")

        try: return req.json()
        except: return ValueError("Response content is not valid JSON")
