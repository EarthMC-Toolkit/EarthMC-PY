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

class OfficialAPI:
    def __init__(self, category, item_id):
        self.category = category

        # Determine the correct URL based on the chosen category and item ID
        if category == "town":
            self.url = f"https://api.earthmc.net/v2/aurora/town/{item_id}"
        elif category == "nation":
            self.url = f"https://api.earthmc.net/v2/aurora/nation/{item_id}"
        elif category == "resident":
            self.url = f"https://api.earthmc.net/v2/aurora/resident/{item_id}"
        else:
            raise ValueError("Invalid category")

    def get_info(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    @classmethod
    def town(cls, item_id):
        return cls("town", item_id)

    @classmethod
    def nation(cls, item_id):
        return cls("nation", item_id)

    @classmethod
    def resident(cls, item_id):
        return cls("resident", item_id)



