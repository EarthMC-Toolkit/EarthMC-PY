from .Utils import utils
utils = utils()

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
    def __init__(self, map): 
        self.online = self.online(map)
    class residents:
        def __init__(self): raise NotImplementedError
    class townless:
        def __init__(self): raise NotImplementedError
    class online:
        def __init__(self, map): self.mapName = map
        def all(self):
            data = utils.playerData(self.mapName)
            output = []
            
            for player in data['players']:
                currentPlayer = OnlinePlayer(player["account"], player["world"], player["x"], player["y"], player["z"])
                output.append(currentPlayer)
            
            return output
        def find(self, playerName): return self.get(self, playerName)
        def get(self, playerName, players=None):
            if players is None: players = self.all()
            foundPlayer = utils.find(lambda player: player.name == playerName, players)
        
            if foundPlayer is None: return "Could not find player '" + playerName + "'" 
            return foundPlayer