import requests
from cachetools.func import ttl_cache

class Endpoint:
    def __init__(self):
       self.urls = self.reqJSON('https://raw.githubusercontent.com/EarthMC-Toolkit/Toolkit-Website/main/endpoints.json')

    @staticmethod
    def reqJSON(url):
        req = requests.get(url)
        try: return req.json()
        except: raise ValueError("Response content is not valid JSON")

    @ttl_cache(2, 300)
    def fetch(self, type, mapName): return self.reqJSON(self.urls[type][mapName])
    