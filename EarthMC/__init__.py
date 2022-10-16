from .Classes import Nations

from .Utils import utilFuncs
utils = utilFuncs()

class Map(Nations.nations):
    def __init__(self, mapName=''):
        self.name = mapName.lower()

        print('Initialising map -> ' + self.name)
        super().__init__(self.name)

        self.mapData = utils.fetchData('map', self.name)
        self.playerData = utils.fetchData('players', self.name)

        #self.towns = Towns.towns(self.name)
        #self.nations = Nations.nations(self.name)
        #self.players = Players.players(self.name)

        #self.totalChunks = int(Map.townAreas(self.towns.all()))
        #self.totalPlayers = len(self.players.residents.all()) + len(self.players.townless.all())

    @staticmethod
    def townAreas(towns): return sum(t['area'] for t in towns)

class Maps():
    @staticmethod
    def Aurora(): return Map('aurora')

    @staticmethod
    def Nova(): return Map('nova')