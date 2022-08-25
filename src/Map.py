from .Utils import utils

from .Nations import nations
from .Towns import towns
from .Players import players

class EMCMap:
    def townAreas(self, towns): 
        chunks = 0
        for i in range(len(towns)):
            chunks += utils.townArea(towns[i])

        return chunks
    def __init__(self, name=''): 
        if name.lower() != 'aurora' and name.lower() != 'nova': return None

        self.name = name
        self.nations = nations(name)
        self.towns = towns(name)
        self.players = players(name)

        #self.totalChunks = self.townAreas(self.towns.all())
        #self.totalPlayers = len(players.residents) + len(players.townless)