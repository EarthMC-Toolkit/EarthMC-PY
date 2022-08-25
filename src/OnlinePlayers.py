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

class onlinePlayers:
    def all(self):
        players = utils.getPlayerData()["players"]
        pArr = []

        for player in players:
            currentPlayer = OnlinePlayer(player["account"], player["world"], player["x"], player["y"], player["z"])
            pArr.append(currentPlayer)
        
        return pArr
    def get(self, playerName):
        foundPlayer = utils.find(lambda player: player.name == playerName, self.all())
    
        if foundPlayer is None: return "Could not find player '" + playerName + "'" 
        return foundPlayer