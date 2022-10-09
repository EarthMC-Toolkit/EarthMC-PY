from .Classes.Nations import nations
from .Classes.Towns import towns
from .Classes.Players import players

class Map:
    @staticmethod
    def townAreas(towns): return sum(t.area for t in towns)
    def __init__(self, name=''): 
        map = name.lower()
        if map != 'aurora' and map != 'nova': return None

        self.nations = nations(map)
        self.towns = towns(map)
        self.players = players(map)

        self.totalChunks = int(Map.townAreas(self.towns.all()))
        #self.totalPlayers = len(self.players.residents.all()) + len(self.players.townless.all())

Aurora = Map('aurora')
Nova = Map('nova')