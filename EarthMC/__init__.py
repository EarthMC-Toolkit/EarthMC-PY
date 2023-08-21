from .Classes.Nations import nations
from .Classes.Players import players

from .Classes.OAPI.Town import OAPI_Town
from .Classes.OAPI.Nation import OAPI_Nation
from .Classes.OAPI.Player import OAPI_Player

from .DataHandler import OAPI
from .Utils import utils, FetchError

class Map(nations):
    def __init__(self, mapName=''):
        self.name = mapName.lower()

        print('Initialising map -> ' + self.name)
        super().__init__(self.name)

        self.players = players(self.name, self.towns)

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
        return self.api.fetch_single('nations', name)

    def player(self, name: str):
        return self.api.fetch_single('players', name)

    class Players:
         def __init__(self, api: OAPI):
            self.api = api

         def all(self):
             playerArr = []
             playerList = self.api.fetch_all('residents')

             for player in playerList['allResidents']:
                 playerArr.append(self.api.fetch_single('residents', player))

             return playerArr

    class Nations:
        class NationsPlayers:
            def __init__(self, api: OAPI):
                self.api = api

            def all(self):
                nationArr = []
                nationList = self.api.fetch_all('nations')

                for nation in nationList['allNations']:  
                    nation_data = self.api.fetch_single('nations', nation)
                    nationObj = OAPI_Nation(nation_data)
                    nationArr.append(nationObj)

                return nationArr


OfficialAPI = _OfficialAPI()
