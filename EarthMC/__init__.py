from .Classes.Nations import nations
from .Classes.Players import players

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
    def addAmounts(a1, a2): return int((len(a1) + len(a2)))

class Maps():
    @staticmethod
    def Aurora(): return Map('aurora')
    def Nova(): return Map('nova')