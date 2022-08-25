from .Nations import nations
from .Towns import towns
from .Players import players

class Map:
    @staticmethod
    def townAreas(towns): return sum(t.area for t in towns)
    def __init__(self, name=''): 
        if name.lower() != 'aurora' and name.lower() != 'nova': return None
        self.name = name

        self.nations = nations(name)
        self.towns = towns(name)
        self.players = players(name)

        self.totalChunks = Map.townAreas(self.towns.all())
        #self.totalPlayers = len(self.players.residents.all()) + len(self.players.townless.all())

Aurora = Map('aurora')
Nova = Map('nova')