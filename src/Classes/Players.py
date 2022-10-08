from ..Utils import utils
utils = utils()

from .Towns import towns

class OnlinePlayer:
    def __init__(self, name="", world="", x=0, y=0, z=0):
        self.name = name
        self.world = world
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return "Name: %s \nWorld: %s \nX: %s \nY: %s \nZ: %s" % (self.name, self.world, self.x, self.y, self.z)

class players:
    def all(self): return self.townless.all() + self.residents.all()
    def __init__(self, map): 
        self.online = self.online(map)
        self.residents = self.residents(map)
        self.townless = self.townless(map)

    class residents:
        def __init__(self, map): 
            self.mapName = map
            self.towns = towns(map)
        def all(self): 
            output = []

            for t in self.towns.all():
                for res in t.residents:
                    output.append(res)

            return output

    class townless:
        def __init__(self, map): 
            self.mapName = map
            self.playerData = utils.playerData(map)
        def all(self): return []

    class online:
        def __init__(self, map): 
            self.mapName = map
            self.data = utils.playerData(map)
        def all(self):
            output = []
            
            for player in self.data['players']:
                currentPlayer = OnlinePlayer(player["account"], player["world"], player["x"], player["y"], player["z"])
                output.append(currentPlayer)
            
            return output
        def find(self, playerName): return self.get(playerName)
        def get(self, playerName, players=None):
            if players is None: players = self.all()
            foundPlayer = utils.find(lambda player: player.name == playerName, players)
        
            if foundPlayer is None: return "Could not find player '" + playerName + "'" 
            return foundPlayer