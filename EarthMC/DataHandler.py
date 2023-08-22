import aiohttp
import asyncio
from cachetools.func import ttl_cache
from .Utils import FetchError

class Endpoint:
    def __init__(self):
        endpoints = "https://raw.githubusercontent.com/EarthMC-Toolkit/Toolkit-Website/main/endpoints.json"
        self.urls = self.reqJSON(endpoints)

    @ttl_cache(2, 300)
    async def fetch(self, type, mapName):
        async with aiohttp.ClientSession() as session:
            return await self.reqJSON(session, self.urls[type][mapName])

    @staticmethod
    async def reqJSON(session, url: str):
        async with session.get(url) as response:
            try:
                return await response.json()
            except aiohttp.ContentTypeError:
                raise FetchError("Error fetching endpoint: " + url + "\nResponse content is not valid JSON!")

class OAPI:
    def __init__(self, map="aurora"):
        self.domain = f"https://api.earthmc.net/v1/{map}"
        self.urls = {
            "towns": f"{self.domain}/towns",
            "nations": f"{self.domain}/nations",
            "residents": f"{self.domain}/residents",
        }

    async def fetch_single(self, type: str, item=''):
        async with aiohttp.ClientSession() as session:
            return await Endpoint.reqJSON(session, self.urls[type] + "/" + item)

    async def fetch_all(self, type: str):
        async with aiohttp.ClientSession() as session:
            return await Endpoint.reqJSON(session, self.urls[type])
