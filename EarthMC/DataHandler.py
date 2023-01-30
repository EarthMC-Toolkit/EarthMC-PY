import requests

from .Utils import FetchError
from cachetools.func import ttl_cache

class Endpoint:
    def __init__(self):
       self.urls = self.reqJSON('https://raw.githubusercontent.com/EarthMC-Toolkit/Toolkit-Website/main/endpoints.json')

    @ttl_cache(2, 300)
    def fetch(self, type, mapName): 
        return self.reqJSON(self.urls[type][mapName])
    
    @staticmethod
    def reqJSON(url):
        req = requests.get(url)
        try: return req.json()
        except: return FetchError("Error fetching endpoint: " + url + "\nResponse content is not valid JSON!")