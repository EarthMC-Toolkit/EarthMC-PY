import requests
from cachetools.func import ttl_cache

from .Utils import FetchError

class Endpoint:
    def __init__(self):
        endpoints = "https://raw.githubusercontent.com/EarthMC-Toolkit/Toolkit-Website/main/endpoints.json"
        self.urls = self.reqJSON(endpoints)

    @ttl_cache(2, 300)
    def fetch(self, type, mapName):
        return self.reqJSON(self.urls[type][mapName])

    @staticmethod
    def reqJSON(url: str):
        req = requests.get(url)
        try: return req.json()
        except: return FetchError("Error fetching endpoint: " + url + "\nResponse content is not valid JSON!")

class OAPI:
    def __init__(self, map = "aurora"):
        self.domain = f"https://api.earthmc.net/v1/{map}"
        self.urls = {
            "towns": f"{self.domain}/towns",
            "nations": f"{self.domain}/nations",
            "residents": f"{self.domain}/residents",
        }

    @ttl_cache(2, 5) # Cache it for 5 seconds to avoid spamming API.
    def fetch_single(self, type: str, item = ''):
        return Endpoint.reqJSON(self.urls[type] + "/" + item)

    def fetch_all(self, type: str):
        return Endpoint.reqJSON(self.urls[type])