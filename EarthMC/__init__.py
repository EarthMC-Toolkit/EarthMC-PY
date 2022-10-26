from .Classes import Nations

from .Utils import utilFuncs
utils = utilFuncs()

from .Classes import Players

class Map(Nations.nations):
    def __init__(self, mapName=''):
        self.name = mapName.lower()

        print('Initialising map -> ' + self.name)
        super().__init__(self.name) # Initializes self.nations & self.towns

        self.mapData = utils.fetchData('map', self.name)
        self.playerData = utils.fetchData('players', self.name)

        self.players = Players.players(self.name, self.towns)

        self.totalChunks = Map.townAreas(self.towns.all())
        self.totalPlayers = Map.addAmounts(self.players.residents.all(), self.players.townless.all())

    @staticmethod
    def townAreas(towns): return int(sum(t['area'] for t in towns))
    def addAmounts(a1, a2): return int((len(a1) + len(a2)))

class Maps():
    @staticmethod
    def Aurora(): return Map('aurora')
    def Nova(): return Map('nova')