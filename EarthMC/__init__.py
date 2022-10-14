from .Classes import Towns, Nations, Players

from .Utils import utilFuncs
utils = utilFuncs()

class Map:
    @staticmethod
    def townAreas(towns): return sum(t['area'] for t in towns)
    def __init__(self, mapName=''): 
        self.name = mapName.lower()

        self.mapData = utils.fetchData('map', self.name)
        self.playerData = utils.fetchData('players', self.name)

        self.towns = Towns.towns(self.name)
        self.nations = Nations.nations(self.name)
        self.players = Players.players(self.name)

        self.totalChunks = int(Map.townAreas(self.towns.all()))
        self.totalPlayers = len(self.players.residents.all()) + len(self.players.townless.all())

Aurora = Map('aurora')
Nova = Map('nova')     