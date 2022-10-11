from .Classes.Players import players
from .Classes.Towns import towns
from .Classes.Nations import nations

from .Utils import utilFuncs
utils = utilFuncs()

class Map:
    @staticmethod
    def townAreas(towns): return sum(t['area'] for t in towns)
    def __init__(self, mapName=''): 
        self.name = mapName.lower()

        self.mapData = utils.fetchData('map', self.name)
        self.playerData = utils.fetchData('players', self.name)

        self.towns = towns(self.name)
        self.nations = nations(self.name)
        self.players = players(self.name)

        self.totalChunks = int(Map.townAreas(self.towns.all()))
        #self.totalPlayers = len(self.players.residents.all()) + len(self.players.townless.all())

Aurora = Map('aurora')
Nova = Map('nova')     