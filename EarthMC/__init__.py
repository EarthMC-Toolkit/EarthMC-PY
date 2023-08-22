from .Utils import utils, FetchError

from .Classes import Nations
from .Classes import Players

from .Classes.OAPI import OAPI_Town, OAPI_Nation, OAPI_Player
from .DataHandler import OAPI

class Map(Nations):
    def __init__(self, mapName=''):
        self.name = mapName.lower()

        print('Initialising map -> ' + self.name)
        super().__init__(self.name)

        self.players = Players(self.name, self.towns)

        self.totalChunks = Map.townAreas(self.towns.all())
        self.totalPlayers = Map.addAmounts(self.players.residents.all(), self.players.townless.all())

    @staticmethod
    def townAreas(towns): return int(sum(t['area'] for t in towns))

    @staticmethod
    def addAmounts(a1, a2): return int((len(a1) + len(a2)))

class Maps:
    @staticmethod
    def Aurora(): return Map('aurora')
    @staticmethod
    def Nova(): return Map('nova')

class _OfficialAPI:
    def __init__(self, map = "aurora"):
        self.api = OAPI(map)

    def town(self, name: str):
         return OAPI_Town(self.api.fetch_single('towns', name))

    def nation(self, name: str):
        return OAPI_Nation(self.api.fetch_single('nations', name))

    def player(self, name: str):
        return OAPI_Player(self.api.fetch_single('players', name))

    # class Players:
    #     def __init__(self, api: OAPI):
    #         self.api = api
    #
    #     def all(self):
    #         playerArr = []
    #         playerList = self.api.fetch_all('residents')
    #
    #         for player in playerList['allResidents']:
    #             playerArr.append(self.api.fetch_single('residents', player))
    #
    #         return playerArr

OfficialAPI = _OfficialAPI()