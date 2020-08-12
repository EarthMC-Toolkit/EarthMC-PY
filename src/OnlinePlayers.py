from .Functions import functions

functions = functions()

class OnlinePlayer:
    def __init__(self, name="", world="", x=0, y=0, z=0):
        self.name = name
        self.world = world
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return "Name: %s \nWorld: %s \nX: %s \nY: %s \nZ: %s" % (self.name, self.world, self.x, self.y, self.z)

def createOnlinePlayer(name, world, x, y, z):
    return OnlinePlayer(name, world, x, y, z)

class onlinePlayers:
    def all(self):
        players = functions.getPlayerData()["players"]

        playerArray = []

        for player in players:
            currentPlayer = createOnlinePlayer(player["account"], player["world"], player["x"], player["y"], player["z"])
            playerArray.append(currentPlayer)
        
        return playerArray
    def get(self, playerName):
        foundPlayer = functions.find(lambda player: player.name == playerName, self.all())
    
        if foundPlayer is None: return "Could not find player '" + playerName + "'" 
        else: return foundPlayer