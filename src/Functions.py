import json, requests

class functions:
    def find(self, pred, iterable):
        for element in iterable:
            if pred(element):
                return element
        return None
    def getPlayerData(self): return requests.get("https://earthmc.net/map/up/world/earth/").json() 
    def getMapData(self): return requests.get("https://earthmc.net/map/tiles/_markers_/marker_earth.json").json()